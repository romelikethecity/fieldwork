# Fieldwork — Tools & Scripts Reference

All tools built for competitive hiring intelligence reports. Each script is standalone (no external dependencies beyond Python 3 stdlib) and reads from or writes to the shared `jobs.db` SQLite database.

---

## 1. Greenhouse ATS Importer

**File:** `scripts/greenhouse_import.py` (~870 lines)
**Purpose:** Fetches all active jobs from a company's public Greenhouse board and imports them into jobs.db with full enrichment.

### What it does
1. Hits the Greenhouse public API (`boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true&per_page=500`)
2. Classifies each job by **function** (Sales, Engineering, Marketing, etc.) and **seniority** (Entry through C-Suite)
3. Detects **AI/ML mentions** in job descriptions
4. Extracts **hiring signals** across 6 categories:
   - `hiring_signal` — growth hire, turnaround, immediate fill
   - `team_structure` — build team, first hire, reports to CRO/VP/CEO
   - `comp_signal` — above market, equity heavy, performance bonus
   - `segment` — enterprise, mid-market, SMB
   - `motion` — PLG, ABM, channel, outbound
   - `geo_focus` — North America, EMEA, APAC, LATAM, global
5. Extracts **tech stack** (80+ tools across 12 categories: CRM, Languages, Frameworks, Cloud, Databases, AI/ML, etc.)
6. Parses **multi-location** postings (San Francisco, New York, London, etc.) and detects remote/hybrid
7. Writes to three tables: `jobs`, `job_signals`, `job_tools`

### Usage
```bash
# Basic import
python greenhouse_import.py --board carta --company "Carta" --url "https://carta.com" --db data/jobs.db

# Preview without writing to DB
python greenhouse_import.py --board carta --company "Carta" --url "https://carta.com" --db data/jobs.db --dry-run

# Re-import (deletes existing data for this company first)
python greenhouse_import.py --board carta --company "Carta" --url "https://carta.com" --db data/jobs.db --reimport

# With industry label
python greenhouse_import.py --board pulley --company "Pulley" --url "https://pulley.com" --db data/jobs.db --industry "Equity Management"
```

### Flags
| Flag | Required | Description |
|------|----------|-------------|
| `--board` | Yes | Greenhouse board slug (from the URL) |
| `--company` | Yes | Display name |
| `--url` | Yes | Company website URL |
| `--db` | Yes | Path to jobs.db |
| `--dry-run` | No | Print enrichment results without writing |
| `--reimport` | No | Delete existing company data before importing |
| `--industry` | No | Industry label (e.g., "Equity Management") |

### Output
- Writes directly to SQLite: `jobs` (main), `job_signals` (signal_type + signal_value per job), `job_tools` (tool_name + tool_category per job)
- Sentinel records: Jobs with no signals/tools get `_none` entries so they're marked as processed
- Console summary: total jobs, signals, tools extracted

### Tested results
- Carta: 88 jobs, 438 signals, 129 tools
- Pulley: 6 jobs, 23 signals, 25 tools

---

## 2. Wayback Machine History Scraper

**File:** `scripts/wayback_greenhouse.py` (~305 lines)
**Purpose:** Fetches archived snapshots of a company's Greenhouse job board from the Wayback Machine and extracts job counts over time to build a hiring trend timeline.

### What it does
1. Queries the Wayback Machine CDX API for all archived snapshots of the company's Greenhouse board
2. Checks both old (`boards.greenhouse.io/{board}`) and new (`job-boards.greenhouse.io/{board}`) URL formats
3. Selects one snapshot per time period (monthly or quarterly)
4. Fetches each archived page and counts open roles using:
   - **Old format:** Counts `class="opening"` elements in server-rendered HTML
   - **New format:** Extracts unique job IDs from React SPA initial data payload
5. Appends a **live count** from the current Greenhouse API as the final data point
6. Outputs a JSON timeline with date, role count, format type, and page size

### Usage
```bash
# Monthly snapshots (default)
python wayback_greenhouse.py --board carta --output reports/carta_history.json

# Quarterly snapshots
python wayback_greenhouse.py --board carta --output reports/carta_history.json --frequency quarterly

# Custom date range
python wayback_greenhouse.py --board carta --output reports/carta_history.json --start 2021-01-01 --end 2025-12-31
```

### Flags
| Flag | Required | Description |
|------|----------|-------------|
| `--board` | Yes | Greenhouse board slug |
| `--output` | Yes | Output JSON file path |
| `--frequency` | No | `monthly` (default) or `quarterly` |
| `--start` | No | Start date YYYY-MM-DD (default: 2020-01-01) |
| `--end` | No | End date YYYY-MM-DD (default: today) |

### Output
JSON file with this structure:
```json
{
  "board": "carta",
  "generated_at": "2026-02-17T...",
  "frequency": "quarterly",
  "data_points": 16,
  "timeline": [
    {"date": "2021-03-22", "open_roles": 187, "format": "old", "page_size": 142857, "departments": null},
    {"date": "2021-06-28", "open_roles": 269, "format": "old", ...},
    ...
    {"date": "2026-02-17", "open_roles": 88, "format": "api", ...}
  ]
}
```

### Known limitations
- Wayback Machine rate limit: script sleeps 1.5s between fetches (be patient)
- New Greenhouse format (post-Aug 2024) uses client-side React rendering with paginated payloads. Snapshots may undercount if only the initial 50 job IDs are in the HTML.
- Some snapshots return 0 roles due to rendering issues — these are filtered out
- Coverage varies by company. Carta has 500+ snapshots; smaller companies may have <20.

### Tested results
- Carta quarterly: 16 clean data points from Q1 2021 to present
  - Peak: 427 roles (Q3 2021)
  - Trough: 32 roles (Q4 2023)
  - Current: 88 roles (21% of peak)

---

## 3. Competitive Report Generator

**File:** `products/competitive-hiring-tracker/generate_competitor_report.py` (~860 lines)
**Also deployed:** Server at `~/scrapers/master/generate_competitor_report.py`
**Purpose:** Generates competitive hiring analysis reports comparing multiple companies from jobs.db.

### What it does
1. Queries jobs.db for all active postings matching the specified companies
2. Computes per-company breakdowns: function mix, seniority, compensation, signals, tools, geography
3. Builds cross-company comparison tables: hiring volume, comp benchmarking, team building vs backfilling, remote adoption
4. Generates key takeaways based on the data
5. Outputs markdown report, JSON data, and CSV export

### Usage
```bash
# Compare specific companies
python generate_competitor_report.py --companies "Carta,Pulley" --db data/jobs.db --report-name "pulley-vs-carta"

# Filter by function
python generate_competitor_report.py --companies "Carta,Pulley" --function sales --db data/jobs.db

# Top N companies by volume
python generate_competitor_report.py --top 10 --db data/jobs.db
```

### Output files
For `--report-name "pulley-vs-carta"`:
- `reports/pulley-vs-carta_competitor_report.md` — Full markdown report
- `reports/pulley-vs-carta_competitor_report.json` — Structured data
- `reports/pulley-vs-carta_competitor_data.csv` — Flat CSV for spreadsheets

---

## 4. Visual HTML Report (Manual/Custom)

**File:** `reports/pulley-vs-carta.html`
**Purpose:** Presentation-quality visual report built for a specific prospect. Standalone HTML with inline CSS, Google Fonts, zero JS dependencies.

### Sections
- Executive Summary (stat cards + key insights)
- Hiring Trend Chart (SVG polyline with layoff event markers)
- Layoff Timeline (event cards with dates and context)
- Company Comparison Cards (side-by-side with seniority distribution bars)
- Function Comparison (horizontal bar charts)
- Compensation Table (with company-vs-company deltas)
- Hiring Signals (tagged badges by category)
- Tech Stack Grid (tool mentions by company)
- Geographic Footprint (location lists + remote % cards)
- People Team Deep Dive (function-specific role breakdown with comp)
- Key Takeaways (prospect-focused insights)
- Methodology & Appendix

### Brand system
Uses Fieldwork "Slate Ember" palette:
- Primary: `#E07850` (warm ember)
- Secondary: `#5B9EA6` (teal)
- Background: `#14171C` (dark slate)
- Fonts: Sora (headings), DM Sans (body), IBM Plex Mono (data)

---

## Report Outputs (Current)

All in `reports/`:

| File | Description |
|------|-------------|
| `pulley-vs-carta.html` | Visual HTML report (presentation-quality) |
| `pulley-vs-carta_competitor_report.md` | Full markdown report |
| `pulley-vs-carta_competitor_report.json` | Structured JSON data |
| `pulley-vs-carta_competitor_data.csv` | Flat CSV export |
| `carta_history.json` | Historical hiring trend data (16 quarterly points) |

---

## How These Tools Connect

```
                    Greenhouse API
                         |
                         v
              greenhouse_import.py
              (fetch + enrich + classify)
                         |
                         v
                      jobs.db
                   (jobs, job_signals, job_tools)
                         |
            +------------+------------+
            |                         |
            v                         v
  generate_competitor_report.py   wayback_greenhouse.py
  (cross-company analysis)        (historical trend data)
            |                         |
            v                         v
     .md / .json / .csv         carta_history.json
            |                         |
            +------------+------------+
                         |
                         v
              pulley-vs-carta.html
              (hand-assembled visual report
               combining current + historical data)
```

### Current workflow (manual)
1. Run `greenhouse_import.py` for each company to populate jobs.db
2. Run `generate_competitor_report.py` for the markdown/JSON/CSV reports
3. Run `wayback_greenhouse.py` for historical trend data
4. The visual HTML report is currently hand-built, pulling from all of the above

### Future integration
- Single CLI command: `fieldwork report --companies "Carta,Pulley"` that runs the full pipeline
- Auto-generate the visual HTML report from the JSON data + history
- Add Ashby, Lever, Workday importers (same pattern as greenhouse_import.py)
- Viewer UI for browsing and generating reports on demand (see ROADMAP.md)

---

## Server Deployment

Scripts are deployed to `rome@100.91.208.46:~/scrapers/master/`:
- `greenhouse_import.py`
- `generate_competitor_report.py`
- Database: `~/scrapers/master/data/jobs.db`

Deploy with:
```bash
scp scripts/greenhouse_import.py rome@100.91.208.46:~/scrapers/master/greenhouse_import.py
scp ../products/competitive-hiring-tracker/generate_competitor_report.py rome@100.91.208.46:~/scrapers/master/generate_competitor_report.py
```

---

## Dependencies

All scripts use Python 3 stdlib only. No pip installs required.
- `urllib.request` for HTTP
- `sqlite3` for database
- `json`, `re`, `html` for parsing
- `ssl` + optional `certifi` for HTTPS (falls back to unverified if certifi not installed)
