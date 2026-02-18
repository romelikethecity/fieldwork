#!/usr/bin/env python3
"""
Fieldwork — Greenhouse ATS Importer
Fetches all jobs from a company's Greenhouse board and imports into jobs.db.
Extracts hiring signals, tools/tech stack, and enriches all fields.

Usage:
    python greenhouse_import.py --board carta --company "Carta" --url "https://carta.com" --db ~/scrapers/master/data/jobs.db
    python greenhouse_import.py --board pulley --company "Pulley" --url "https://pulley.com" --db ~/scrapers/master/data/jobs.db
    python greenhouse_import.py --board carta --company "Carta" --url "https://carta.com" --db data/jobs.db --reimport
    python greenhouse_import.py --board stripe --company "Stripe" --url "https://stripe.com" --db data/jobs.db --dry-run

Flags:
    --board       Greenhouse board slug (e.g., "carta")
    --company     Display name (e.g., "Carta")
    --url         Company website URL
    --db          Path to jobs.db
    --dry-run     Print what would be imported without writing to DB
    --reimport    Delete existing data for this company before importing (for re-runs)
    --industry    Optional industry label (e.g., "Equity Management")
"""

import argparse
import html
import json
import re
import sqlite3
import ssl
import sys
import urllib.request
from datetime import datetime, timezone


# SSL context for environments without updated certs (e.g., macOS Python)
SSL_CTX = ssl.create_default_context()
try:
    import certifi
    SSL_CTX.load_verify_locations(certifi.where())
except ImportError:
    SSL_CTX.check_hostname = False
    SSL_CTX.verify_mode = ssl.CERT_NONE


# ══════════════════════════════════════════════
# GREENHOUSE API
# ══════════════════════════════════════════════

def fetch_greenhouse_jobs(board_slug):
    """Fetch all jobs from a Greenhouse board with full content and department data."""
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_slug}/jobs?content=true&per_page=500"
    print(f"  Fetching from {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Fieldwork/1.0"})
    with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as resp:
        data = json.loads(resp.read())

    jobs = data.get("jobs", [])
    total = data.get("meta", {}).get("total", len(jobs))

    page = 2
    while len(jobs) < total:
        page_url = f"{url}&page={page}"
        req = urllib.request.Request(page_url, headers={"User-Agent": "Fieldwork/1.0"})
        with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as resp:
            page_data = json.loads(resp.read())
        page_jobs = page_data.get("jobs", [])
        if not page_jobs:
            break
        jobs.extend(page_jobs)
        page += 1

    print(f"  Fetched {len(jobs)} jobs (API reported {total} total)")
    return jobs


# ══════════════════════════════════════════════
# TEXT EXTRACTION
# ══════════════════════════════════════════════

def strip_html(html_str):
    """Remove HTML tags and decode entities."""
    if not html_str:
        return ""
    text = re.sub(r"<br\s*/?>", "\n", html_str, flags=re.IGNORECASE)
    text = re.sub(r"<li[^>]*>", "\n• ", text, flags=re.IGNORECASE)
    text = re.sub(r"<p[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ══════════════════════════════════════════════
# SALARY EXTRACTION
# ══════════════════════════════════════════════

SALARY_PATTERNS = [
    re.compile(r"\$\s*([\d,]+(?:\.\d+)?)\s*[-–—to]+\s*\$\s*([\d,]+(?:\.\d+)?)"),
    re.compile(r"\$\s*([\d.]+)\s*k\s*[-–—to]+\s*\$\s*([\d.]+)\s*k", re.IGNORECASE),
    re.compile(r"\$\s*([\d,]+(?:\.\d+)?)\s+OTE", re.IGNORECASE),
]


def extract_salary(description_text):
    """Extract salary min/max from job description text."""
    if not description_text:
        return None, None
    for pattern in SALARY_PATTERNS:
        match = pattern.search(description_text)
        if match:
            vals = []
            for g in match.groups():
                g = g.replace(",", "")
                v = float(g)
                if v < 1000:
                    v *= 1000
                vals.append(v)
            if len(vals) == 2:
                return min(vals), max(vals)
            elif len(vals) == 1:
                ote = vals[0]
                return round(ote * 0.6), round(ote)
    return None, None


# ══════════════════════════════════════════════
# FUNCTION CLASSIFICATION
# ══════════════════════════════════════════════

DEPARTMENT_TO_FUNCTION = {
    "account executive": "sales", "account management": "sales",
    "business development": "sales", "sales": "sales",
    "sales development": "sales", "sales operations": "sales",
    "sales enablement": "sales", "sales strategy": "sales",
    "sales strategy & operations": "sales", "cartax sales": "sales",
    "revenue": "sales",
    "engineering": "engineering", "engineering leadership": "engineering",
    "infrastructure": "engineering", "site reliability": "engineering",
    "mobile": "engineering", "information security & it": "engineering",
    "business systems": "engineering", "data & machine learning": "data",
    "product": "product", "design": "product", "r&d operations": "product",
    "marketing": "marketing", "brand marketing": "marketing",
    "demand generation": "marketing", "marketing operations": "marketing",
    "product marketing": "marketing",
    "finance": "finance", "strategic finance": "finance",
    "accounting": "finance", "treasury": "finance",
    "procurement": "finance", "tax": "finance", "valuations": "finance",
    "people": "people", "human resources": "people",
    "recruiting": "people", "total rewards": "people",
    "learning & development": "people",
    "legal": "legal", "compliance": "legal",
    "policy": "legal", "policy & strategy": "legal",
    "customer success": "operations", "customer support": "operations",
    "customer implementations": "operations", "delivery operations": "operations",
    "operations & underwriting": "operations",
    "strategy & business operations": "operations",
    "fund administration": "operations", "broker & market operations": "operations",
    "portfolio insights": "operations", "administrative": "operations",
    "real estate and workplace services": "operations", "liquidity": "operations",
    "executive": "other", "executive assistant": "operations",
    "confidential": "other",
}

TITLE_TO_FUNCTION = [
    (r"\b(engineer|developer|sre|devops|architect|infrastructure)\b", "engineering"),
    (r"\b(data scientist|data engineer|machine learning|ml engineer|analytics)\b", "data"),
    (r"\b(product manager|product lead|product director)\b", "product"),
    (r"\b(designer|ux|ui)\b", "product"),
    (r"\b(account executive|ae|sales|sdr|bdr|business development)\b", "sales"),
    (r"\b(marketing|demand gen|content|brand|growth)\b", "marketing"),
    (r"\b(finance|accounting|controller|tax|treasury)\b", "finance"),
    (r"\b(recruiter|talent|people|hr|human resources|hrbp)\b", "people"),
    (r"\b(legal|counsel|compliance|paralegal)\b", "legal"),
    (r"\b(operations|support|success|implementation|onboarding)\b", "operations"),
]


def classify_function(department_name, title):
    if department_name:
        dept_lower = department_name.lower().strip()
        if dept_lower in DEPARTMENT_TO_FUNCTION:
            return DEPARTMENT_TO_FUNCTION[dept_lower]
    title_lower = title.lower()
    for pattern, func in TITLE_TO_FUNCTION:
        if re.search(pattern, title_lower):
            return func
    return "other"


# ══════════════════════════════════════════════
# SENIORITY CLASSIFICATION
# ══════════════════════════════════════════════

SENIORITY_RULES = [
    (r"\b(chief|ceo|cto|cfo|coo|cpo|cro|cmo)\b", "c_level"),
    (r"\bevp\b|executive vice president", "evp"),
    (r"\bsvp\b|senior vice president", "svp"),
    (r"\bvice president\b|\bvp\b", "vp"),
    (r"\bsenior director\b", "senior_director"),
    (r"\bdirector\b", "director"),
    (r"\bhead of\b|\bhead,", "head"),
    (r"\bsenior manager\b", "senior_manager"),
    (r"\bmanager\b", "manager"),
    (r"\bstaff\b", "senior"),
    (r"\bprincipal\b", "senior"),
    (r"\blead\b", "senior"),
    (r"\bsenior\b|\bsr\.?\b", "senior"),
    (r"\bassociate\b", "associate"),
    (r"\bjunior\b|\bjr\.?\b", "entry"),
    (r"\bintern\b", "entry"),
]


def classify_seniority(title):
    title_lower = title.lower()
    for pattern, tier in SENIORITY_RULES:
        if re.search(pattern, title_lower):
            return tier
    return "mid"


# ══════════════════════════════════════════════
# AI DETECTION
# ══════════════════════════════════════════════

AI_TERMS = re.compile(
    r"\b(artificial intelligence|machine learning|deep learning|neural network|"
    r"nlp|natural language processing|computer vision|llm|large language model|"
    r"generative ai|gpt|transformer model|reinforcement learning|"
    r"ai[ -]native|ai[ -]first|ai[ -]powered|ai/ml)\b|\bAI\b",
    re.IGNORECASE,
)

AI_NATIVE_PATTERNS = re.compile(
    r"\b(machine learning engineer|ml engineer|ai engineer|"
    r"data scientist|deep learning|nlp engineer|computer vision engineer|"
    r"ai researcher|llm|prompt engineer)\b",
    re.IGNORECASE,
)


def detect_ai(title, description):
    text = f"{title} {description}"
    mentions = AI_TERMS.findall(text)
    has_ai = len(mentions) > 0
    terms_found = ", ".join(set(m if isinstance(m, str) else m[0] for m in mentions)) if has_ai else None
    is_native = bool(AI_NATIVE_PATTERNS.search(title))
    return has_ai, terms_found, is_native


# ══════════════════════════════════════════════
# HIRING SIGNAL EXTRACTION
# Compatible with job_signals table format from unified scraper
# ══════════════════════════════════════════════

SIGNAL_PATTERNS = {
    "hiring_signals": {
        "immediate": r"immediate|asap|urgent",
        "growth_hire": r"growth|expansion|adding\s*to\s*team",
        "turnaround": r"turnaround|transform|rebuild|restructur",
    },
    "team_structure": {
        "first_hire": r"first\s*(sales)?\s*hire|founding|build\s*from\s*scratch|ground\s*up",
        "player_coach": r"player.?coach|selling\s*manager|carry.*quota.*manage",
        "build_team": r"build.*team|hire.*team|recruit.*team|grow.*team",
        "reports_cro": r"report.*cro|report.*chief\s*revenue",
        "reports_ceo": r"report.*ceo|report.*founder",
        "reports_vp": r"report.*vp\s*sales|report.*vice\s*president",
    },
    "comp_signals": {
        "equity": r"equity|stock|rsu|option|ownership",
        "uncapped": r"uncapped|no\s*cap|unlimited\s*commission",
        "ote_mentioned": r"\bote\b|on.?target",
    },
    "segment": {
        "smb": r"\bsmb\b|small\s*business|small.*medium",
        "mid_market": r"mid.?market|middle\s*market",
        "enterprise": r"\benterprise\b",
    },
    "motion": {
        "channel": r"\bchannel\b|partner\s*sales|reseller",
        "plg": r"product.?led|\bplg\b|self.?serve|freemium",
        "abm": r"account.?based|\babm\b",
    },
    "geo_focus": {
        "north_america": r"north\s*america|\busa\b|united\s*states|\bus\s*market",
        "emea": r"\bemea\b|europe|\buk\b|european",
        "apac": r"\bapac\b|asia|pacific|japan|china|india|australia",
        "latam": r"\blatam\b|latin\s*america|brazil|mexico",
        "global": r"\bglobal\b|worldwide|international",
    },
}


def extract_signals(title, description):
    """Extract hiring signals from title + description. Returns list of dicts."""
    text = f"{title} {description}".lower()
    found = []
    seen = set()

    for signal_type, signals in SIGNAL_PATTERNS.items():
        for signal_id, pattern in signals.items():
            key = f"{signal_type}:{signal_id}"
            if key in seen:
                continue
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    found.append({
                        "signal_type": signal_type,
                        "signal_id": signal_id,
                        "signal_value": signal_id.replace("_", " ").title(),
                    })
                    seen.add(key)
            except re.error:
                if pattern.lower() in text:
                    found.append({
                        "signal_type": signal_type,
                        "signal_id": signal_id,
                        "signal_value": signal_id.replace("_", " ").title(),
                    })
                    seen.add(key)

    return found


# ══════════════════════════════════════════════
# TOOL/TECH STACK EXTRACTION
# Compatible with job_tools table format from unified scraper
# Focused set: covers major tools across all functions
# ══════════════════════════════════════════════

TOOL_PATTERNS = {
    # CRM & Sales
    "CRM": {
        "salesforce": r"\bsalesforce\b",
        "hubspot": r"\bhubspot\b",
        "dynamics_365": r"dynamics\s*365|microsoft\s*dynamics",
    },
    "Sales_Engagement": {
        "outreach": r"outreach\.io|outreach\s*(platform|sales\s*engagement)",
        "salesloft": r"\bsalesloft\b",
        "apollo": r"\bapollo\.io\b|\bapollo\b",
        "gong": r"\bgong\b",
    },
    # Engineering
    "Languages": {
        "python": r"\bpython\b",
        "javascript": r"\bjavascript\b|\bnode\.?js\b|\btypescript\b",
        "java": r"\bjava\b(?!script)",
        "golang": r"\bgo\b(?:lang)?|\bgolang\b",
        "ruby": r"\bruby\b(?!\s*on\s*rails)?",
        "ruby_on_rails": r"ruby\s*on\s*rails|\brails\b",
        "rust": r"\brust\b",
        "scala": r"\bscala\b",
        "kotlin": r"\bkotlin\b",
        "swift": r"\bswift\b",
        "cpp": r"\bc\+\+\b|\bcpp\b",
        "csharp": r"\bc#\b|\.net\b",
        "sql": r"\bsql\b",
        "graphql": r"\bgraphql\b",
    },
    "Cloud_Infrastructure": {
        "aws": r"\baws\b|amazon\s*web\s*services",
        "gcp": r"\bgcp\b|google\s*cloud",
        "azure": r"\bazure\b",
        "kubernetes": r"\bkubernetes\b|\bk8s\b",
        "docker": r"\bdocker\b",
        "terraform": r"\bterraform\b",
    },
    "Databases": {
        "postgresql": r"\bpostgres(?:ql)?\b",
        "mysql": r"\bmysql\b",
        "mongodb": r"\bmongodb\b|\bmongo\b",
        "redis": r"\bredis\b",
        "elasticsearch": r"\belasticsearch\b|\belastic\b",
        "snowflake": r"\bsnowflake\b",
        "bigquery": r"\bbigquery\b|big\s*query",
        "redshift": r"\bredshift\b",
    },
    "Frameworks": {
        "react": r"\breact\b(?![\s-]*native)",
        "react_native": r"react[\s-]*native",
        "angular": r"\bangular\b",
        "vue": r"\bvue\.?js\b|\bvue\b",
        "django": r"\bdjango\b",
        "flask": r"\bflask\b",
        "spring": r"\bspring\s*boot\b|\bspring\b",
        "nextjs": r"\bnext\.?js\b",
    },
    # Data & Analytics
    "Data_Tools": {
        "spark": r"\bspark\b|pyspark",
        "airflow": r"\bairflow\b",
        "dbt": r"\bdbt\b",
        "tableau": r"\btableau\b",
        "looker": r"\blooker\b",
        "power_bi": r"power\s*bi",
        "fivetran": r"\bfivetran\b",
    },
    # AI/ML
    "AI_ML": {
        "pytorch": r"\bpytorch\b",
        "tensorflow": r"\btensorflow\b",
        "langchain": r"\blangchain\b",
        "openai_api": r"\bopenai\b",
        "huggingface": r"hugging\s*face|\bhuggingface\b",
        "rag": r"\brag\b|retrieval\s*augmented",
        "fine_tuning": r"fine[\s-]*tuning",
    },
    # Marketing
    "Marketing_Tools": {
        "marketo": r"\bmarketo\b",
        "pardot": r"\bpardot\b",
        "google_analytics": r"google\s*analytics|\bga4\b",
        "segment": r"\bsegment\b(?!ation)",
        "mixpanel": r"\bmixpanel\b",
        "amplitude": r"\bamplitude\b",
    },
    # Collaboration
    "Collaboration": {
        "jira": r"\bjira\b",
        "confluence": r"\bconfluence\b",
        "figma": r"\bfigma\b",
        "slack": r"\bslack\b",
        "notion": r"\bnotion\b",
    },
    # Finance/Ops
    "Finance_Tools": {
        "netsuite": r"\bnetsuite\b",
        "workday": r"\bworkday\b",
        "sap": r"\bsap\b",
        "quickbooks": r"\bquickbooks\b",
        "stripe_api": r"\bstripe\b",
    },
}


def extract_tools(title, description):
    """Extract tools/tech from title + description. Returns list of dicts."""
    text = f"{title} {description}"
    found = []
    seen = set()

    for tool_category, tools in TOOL_PATTERNS.items():
        for tool_id, pattern in tools.items():
            if tool_id in seen:
                continue
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    found.append({
                        "tool_name": tool_id.replace("_", " ").title(),
                        "tool_category": tool_category,
                        "tool_id": tool_id,
                    })
                    seen.add(tool_id)
            except re.error:
                pass

    return found


# ══════════════════════════════════════════════
# LOCATION PARSING (fixed for multi-location + remote)
# ══════════════════════════════════════════════

US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC",
}

METRO_MAP = {
    "san francisco": "San Francisco Bay Area",
    "santa clara": "San Francisco Bay Area",
    "palo alto": "San Francisco Bay Area",
    "mountain view": "San Francisco Bay Area",
    "sunnyvale": "San Francisco Bay Area",
    "new york": "New York Metro",
    "new york city": "New York Metro",
    "brooklyn": "New York Metro",
    "hamilton": "New York Metro",
    "new brunswick": "New York Metro",
    "seattle": "Seattle Metro",
    "boston": "Boston Metro",
    "chicago": "Chicago Metro",
    "los angeles": "Los Angeles Metro",
    "sandy": "Salt Lake City Metro",
    "salt lake city": "Salt Lake City Metro",
    "austin": "Austin Metro",
    "denver": "Denver Metro",
    "waterloo": "Waterloo, Canada",
    "toronto": "Toronto, Canada",
    "london": "London, UK",
    "singapore": "Singapore",
    "sydney": "Sydney, Australia",
    "rio de janeiro": "Rio de Janeiro, Brazil",
    "hong kong": "Hong Kong",
    "abu dhabi": "Abu Dhabi, UAE",
}


def parse_location(location_str):
    """Parse location string into components. Handles multi-location and remote."""
    if not location_str:
        return None, None, None, False

    loc_lower = location_str.lower().strip()

    # Remote detection
    is_remote = loc_lower in ("remote", "remote, us", "remote, usa", "remote - us",
                              "remote - usa", "anywhere", "work from home")

    if is_remote:
        return "remote", None, None, True

    # Multi-location: scan ALL locations for best metro match
    # Split on semicolons (Greenhouse multi-location format)
    all_locs = [s.strip() for s in location_str.split(";")]

    # Find first metro match across all locations
    metro = None
    state = None
    for loc in all_locs:
        loc_parts = [p.strip() for p in loc.split(",")]
        city = loc_parts[0].lower().strip() if loc_parts else ""

        # Check metro
        if not metro:
            for city_key, metro_name in METRO_MAP.items():
                if city_key in city:
                    metro = metro_name
                    break

        # Check state
        if not state:
            for part in loc_parts:
                upper = part.strip().upper()
                if upper in US_STATES:
                    state = upper
                    break

        if metro and state:
            break

    loc_type = "onsite"
    return loc_type, metro, state, False


# ══════════════════════════════════════════════
# DB IMPORT (with signals + tools)
# ══════════════════════════════════════════════

def delete_company_data(db_path, company_name):
    """Delete all existing data for a company (for reimport)."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    normalized = company_name.lower().strip()

    # Get job IDs
    cursor.execute("SELECT id FROM jobs WHERE company_name_normalized = ?", (normalized,))
    job_ids = [row[0] for row in cursor.fetchall()]

    if job_ids:
        placeholders = ",".join("?" * len(job_ids))
        cursor.execute(f"DELETE FROM job_signals WHERE job_id IN ({placeholders})", job_ids)
        cursor.execute(f"DELETE FROM job_tools WHERE job_id IN ({placeholders})", job_ids)
        cursor.execute(f"DELETE FROM jobs WHERE id IN ({placeholders})", job_ids)

    conn.commit()
    count = len(job_ids)
    conn.close()
    return count


def import_to_db(db_path, jobs_data, company_name, company_url, industry, dry_run=False):
    """Import parsed job data into jobs.db including signals and tools."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    company_normalized = company_name.lower().strip()

    if dry_run:
        print(f"\n  DRY RUN — would import {len(jobs_data)} jobs for {company_name}")
        sig_count = sum(len(j.get("signals", [])) for j in jobs_data)
        tool_count = sum(len(j.get("tools", [])) for j in jobs_data)
        print(f"    {sig_count} signals, {tool_count} tools detected")
        for j in jobs_data[:5]:
            print(f"    {j['title']} | {j['function_category']} | {j['seniority_tier']} | {j['location_raw']}")
        if len(jobs_data) > 5:
            print(f"    ... and {len(jobs_data) - 5} more")
        return 0, 0

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()

    inserted = 0
    updated = 0
    signals_inserted = 0
    tools_inserted = 0

    for j in jobs_data:
        # Check if already exists
        cursor.execute(
            "SELECT id FROM jobs WHERE source = ? AND source_id = ?",
            ("greenhouse", j["source_id"]),
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "UPDATE jobs SET last_seen = ?, is_active = 1 WHERE id = ?",
                (now, existing[0]),
            )
            updated += 1
            job_db_id = existing[0]
        else:
            cursor.execute(
                """INSERT INTO jobs (
                    source, source_id, source_url, title,
                    company_name, company_name_normalized, company_url,
                    location_raw, location_type, location_metro, location_state, is_remote,
                    annual_salary_min, annual_salary_max, has_salary,
                    compensation_min, compensation_max, compensation_interval,
                    function_category, seniority_tier,
                    description_raw, has_description,
                    company_industry,
                    has_ai_mention, ai_terms_found, is_ai_native_role,
                    date_posted, date_scraped, last_seen, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    "greenhouse", j["source_id"], j["source_url"], j["title"],
                    company_name, company_normalized, company_url,
                    j["location_raw"], j["location_type"], j["location_metro"],
                    j["location_state"], j["is_remote"],
                    j["salary_min"], j["salary_max"],
                    1 if j["salary_min"] else 0,
                    j["salary_min"], j["salary_max"],
                    "yearly" if j["salary_min"] else None,
                    j["function_category"], j["seniority_tier"],
                    j["description"], 1 if j["description"] else 0,
                    industry,
                    j["has_ai_mention"], j["ai_terms_found"], j["is_ai_native_role"],
                    j["date_posted"], now, now, 1,
                ),
            )
            job_db_id = cursor.lastrowid
            inserted += 1

        # Insert signals
        for sig in j.get("signals", []):
            cursor.execute(
                "INSERT INTO job_signals (job_id, signal_type, signal_id, signal_value) VALUES (?, ?, ?, ?)",
                (job_db_id, sig["signal_type"], sig["signal_id"], sig["signal_value"]),
            )
            signals_inserted += 1

        # Sentinel if no signals
        if not j.get("signals"):
            cursor.execute(
                "INSERT INTO job_signals (job_id, signal_type, signal_id, signal_value) VALUES (?, ?, ?, ?)",
                (job_db_id, "_none", "_none", "_none"),
            )

        # Insert tools
        for tool in j.get("tools", []):
            cursor.execute(
                "INSERT INTO job_tools (job_id, tool_name, tool_category, tool_id) VALUES (?, ?, ?, ?)",
                (job_db_id, tool["tool_name"], tool["tool_category"], tool["tool_id"]),
            )
            tools_inserted += 1

        # Sentinel if no tools
        if not j.get("tools"):
            cursor.execute(
                "INSERT INTO job_tools (job_id, tool_name, tool_category, tool_id) VALUES (?, ?, ?, ?)",
                (job_db_id, "_none", "_none", "_none"),
            )

    # Upsert companies table
    cursor.execute("SELECT id FROM companies WHERE name_normalized = ?", (company_normalized,))
    if not cursor.fetchone():
        cursor.execute(
            """INSERT INTO companies (name, name_normalized, industry, is_tech, total_job_postings, url, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (company_name, company_normalized, industry, 1, len(jobs_data), company_url, now),
        )
    else:
        cursor.execute(
            "UPDATE companies SET total_job_postings = ?, updated_at = ? WHERE name_normalized = ?",
            (len(jobs_data), now, company_normalized),
        )

    conn.commit()
    conn.close()

    print(f"  DB import: {inserted} inserted, {updated} updated")
    print(f"  Signals: {signals_inserted} | Tools: {tools_inserted}")
    return inserted, updated


# ══════════════════════════════════════════════
# MAIN PIPELINE
# ══════════════════════════════════════════════

def process_greenhouse_jobs(raw_jobs):
    """Parse raw Greenhouse API response into DB-ready records with full enrichment."""
    parsed = []
    for job in raw_jobs:
        job_id = str(job["id"])
        title = job.get("title", "")
        location = job.get("location", {}).get("name", "")
        updated = job.get("updated_at", "")
        abs_url = job.get("absolute_url", "")
        content_html = job.get("content", "")

        depts = job.get("departments", [])
        dept_name = depts[0]["name"] if depts else None

        description = strip_html(content_html)
        salary_min, salary_max = extract_salary(description)
        func = classify_function(dept_name, title)
        seniority = classify_seniority(title)
        has_ai, ai_terms, is_native = detect_ai(title, description)
        loc_type, metro, state, is_remote = parse_location(location)
        signals = extract_signals(title, description)
        tools = extract_tools(title, description)

        date_posted = None
        if updated:
            try:
                dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                date_posted = dt.strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                date_posted = updated[:19] if len(updated) >= 19 else updated

        parsed.append({
            "source_id": job_id,
            "source_url": abs_url,
            "title": title,
            "location_raw": location,
            "location_type": loc_type,
            "location_metro": metro,
            "location_state": state,
            "is_remote": is_remote,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "function_category": func,
            "seniority_tier": seniority,
            "department": dept_name,
            "description": description,
            "has_ai_mention": has_ai,
            "ai_terms_found": ai_terms,
            "is_ai_native_role": is_native,
            "date_posted": date_posted,
            "signals": signals,
            "tools": tools,
        })

    return parsed


def print_summary(parsed, company_name):
    """Print a summary of parsed jobs."""
    print(f"\n{'='*60}")
    print(f"  {company_name} — {len(parsed)} jobs parsed")
    print(f"{'='*60}")

    funcs = {}
    for j in parsed:
        funcs[j["function_category"]] = funcs.get(j["function_category"], 0) + 1
    print("\n  By function:")
    for f, c in sorted(funcs.items(), key=lambda x: -x[1]):
        print(f"    {f:<16} {c:>3}")

    seniorities = {}
    for j in parsed:
        seniorities[j["seniority_tier"]] = seniorities.get(j["seniority_tier"], 0) + 1
    print("\n  By seniority:")
    for s, c in sorted(seniorities.items(), key=lambda x: -x[1]):
        print(f"    {s:<16} {c:>3}")

    salaries = [j["salary_max"] for j in parsed if j["salary_max"]]
    if salaries:
        avg = sum(salaries) / len(salaries)
        print(f"\n  Salary data: {len(salaries)}/{len(parsed)} jobs ({len(salaries)/len(parsed)*100:.0f}%)")
        print(f"    Avg max: ${avg:,.0f}")
        print(f"    Range: ${min(salaries):,.0f} — ${max(salaries):,.0f}")
    else:
        print("\n  Salary data: 0 jobs with posted salary")

    ai_count = sum(1 for j in parsed if j["has_ai_mention"])
    print(f"\n  AI mentions: {ai_count}/{len(parsed)} ({ai_count/len(parsed)*100:.1f}%)")

    # Signals summary
    all_signals = {}
    for j in parsed:
        for sig in j.get("signals", []):
            key = sig["signal_value"]
            all_signals[key] = all_signals.get(key, 0) + 1
    if all_signals:
        print(f"\n  Hiring signals ({sum(all_signals.values())} total):")
        for s, c in sorted(all_signals.items(), key=lambda x: -x[1])[:10]:
            print(f"    {s:<24} {c:>3}")

    # Tools summary
    all_tools = {}
    for j in parsed:
        for tool in j.get("tools", []):
            key = tool["tool_name"]
            all_tools[key] = all_tools.get(key, 0) + 1
    if all_tools:
        print(f"\n  Tech stack ({len(all_tools)} unique tools):")
        for t, c in sorted(all_tools.items(), key=lambda x: -x[1])[:10]:
            print(f"    {t:<24} {c:>3}")

    # Locations
    locations = {}
    for j in parsed:
        loc = j["location_metro"] or j["location_raw"] or "Unknown"
        locations[loc] = locations.get(loc, 0) + 1
    remote_count = sum(1 for j in parsed if j["is_remote"])
    print(f"\n  Locations (remote: {remote_count}/{len(parsed)}):")
    for loc, c in sorted(locations.items(), key=lambda x: -x[1])[:8]:
        print(f"    {loc:<30} {c:>3}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Fieldwork — Import Greenhouse jobs into jobs.db")
    parser.add_argument("--board", required=True, help="Greenhouse board slug (e.g., 'carta')")
    parser.add_argument("--company", required=True, help="Company display name (e.g., 'Carta')")
    parser.add_argument("--url", required=True, help="Company website URL")
    parser.add_argument("--db", required=True, help="Path to jobs.db")
    parser.add_argument("--industry", default=None, help="Industry label")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing to DB")
    parser.add_argument("--reimport", action="store_true", help="Delete existing data before import")
    args = parser.parse_args()

    print(f"\nFieldwork — Greenhouse Import")
    print(f"  Board: {args.board}")
    print(f"  Company: {args.company}")
    print()

    # Reimport: delete existing data first
    if args.reimport and not args.dry_run:
        deleted = delete_company_data(args.db, args.company)
        print(f"  Reimport: deleted {deleted} existing jobs for {args.company}")
        print()

    # Fetch
    raw_jobs = fetch_greenhouse_jobs(args.board)

    # Parse, classify, extract signals + tools
    parsed = process_greenhouse_jobs(raw_jobs)

    # Summary
    print_summary(parsed, args.company)

    # Import
    if args.dry_run:
        print("  DRY RUN — no data written")
    else:
        import_to_db(args.db, parsed, args.company, args.url, args.industry)

    print("  Done.\n")


if __name__ == "__main__":
    main()
