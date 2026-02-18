#!/usr/bin/env python3
"""
Fieldwork — Wayback Machine Greenhouse History Scraper
Fetches archived snapshots of a company's Greenhouse job board from the Wayback Machine
and extracts job counts over time to build a hiring trend timeline.

Usage:
    python wayback_greenhouse.py --board carta --output reports/carta_history.json
    python wayback_greenhouse.py --board carta --output reports/carta_history.json --frequency monthly
    python wayback_greenhouse.py --board pulley --output reports/pulley_history.json

Flags:
    --board       Greenhouse board slug (e.g., "carta")
    --output      Output JSON file path
    --frequency   Sampling frequency: "monthly" or "quarterly" (default: monthly)
    --start       Start date YYYY-MM-DD (default: 2020-01-01)
    --end         End date YYYY-MM-DD (default: today)
"""

import argparse
import json
import re
import ssl
import sys
import time
import urllib.request
from datetime import datetime, timezone

SSL_CTX = ssl.create_default_context()
try:
    import certifi
    SSL_CTX.load_verify_locations(certifi.where())
except ImportError:
    SSL_CTX.check_hostname = False
    SSL_CTX.verify_mode = ssl.CERT_NONE

WAYBACK_CDX = "https://web.archive.org/cdx/search/cdx"
WAYBACK_RAW = "https://web.archive.org/web"

# Greenhouse board URLs (old and new format)
BOARD_URLS = [
    "boards.greenhouse.io/{board}",
    "job-boards.greenhouse.io/{board}",
]


def fetch_cdx_index(board_slug, url_template):
    """Fetch the CDX index of all Wayback snapshots for a board URL."""
    target_url = url_template.format(board=board_slug)
    cdx_url = (
        f"{WAYBACK_CDX}?url={target_url}&output=json"
        f"&fl=timestamp,statuscode,length&matchType=exact&limit=5000"
    )
    print(f"  Fetching CDX index for {target_url}")
    req = urllib.request.Request(cdx_url, headers={"User-Agent": "Fieldwork/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"  CDX error: {e}")
        return []

    if not data or len(data) < 2:
        return []

    # First row is header
    header = data[0]
    rows = data[1:]
    snapshots = []
    for row in rows:
        entry = dict(zip(header, row))
        if entry.get("statuscode") == "200":
            ts = entry["timestamp"]
            try:
                dt = datetime.strptime(ts, "%Y%m%d%H%M%S")
                snapshots.append({
                    "timestamp": ts,
                    "date": dt.strftime("%Y-%m-%d"),
                    "year_month": dt.strftime("%Y-%m"),
                    "length": int(entry.get("length", 0)),
                    "url_template": url_template,
                })
            except ValueError:
                pass

    print(f"    Found {len(snapshots)} usable snapshots")
    return snapshots


def select_snapshots(snapshots, frequency="monthly"):
    """Select one snapshot per time period (monthly or quarterly)."""
    if not snapshots:
        return []

    # Sort by date
    snapshots.sort(key=lambda s: s["timestamp"])

    selected = {}
    for snap in snapshots:
        if frequency == "quarterly":
            dt = datetime.strptime(snap["date"], "%Y-%m-%d")
            quarter = (dt.month - 1) // 3 + 1
            key = f"{dt.year}-Q{quarter}"
        else:
            key = snap["year_month"]

        # Take the latest snapshot in each period (most representative)
        selected[key] = snap

    result = sorted(selected.values(), key=lambda s: s["timestamp"])
    print(f"  Selected {len(result)} snapshots ({frequency})")
    return result


def count_openings_old_format(html):
    """Count job openings from old Greenhouse board format (server-rendered HTML)."""
    # Old format: each job is in a <div class="opening"> element
    count = len(re.findall(r'class="opening"', html))
    if count == 0:
        # Alternative: count job links in the listing
        count = len(re.findall(r'<a[^>]+data-mapped="true"', html))
    if count == 0:
        # Try counting job title links
        count = len(re.findall(r'gh-job-listing', html, re.IGNORECASE))
    return count


def count_openings_new_format(html):
    """Count job openings from new Greenhouse board format (React SPA with initial data)."""
    # New format embeds job data in a __NEXT_DATA__ or similar JSON blob
    # Look for job IDs in the initial payload
    job_ids = re.findall(r'"id"\s*:\s*(\d{7,})', html)
    unique_ids = set(job_ids)
    if unique_ids:
        return len(unique_ids)

    # Fallback: count job card elements
    count = len(re.findall(r'data-job-id', html))
    return count


def extract_departments(html):
    """Try to extract department/function breakdown from the board page."""
    # Old format: departments are in <h2> or section headers
    depts = {}
    # Look for department sections with job counts
    dept_sections = re.findall(
        r'<h[23][^>]*>([^<]+)</h[23]>\s*(?:<[^>]+>\s*)*'
        r'((?:<div[^>]*class="opening"[^>]*>.*?</div>\s*)+)',
        html, re.DOTALL
    )
    for dept_name, openings_html in dept_sections:
        dept_name = dept_name.strip()
        count = len(re.findall(r'class="opening"', openings_html))
        if count > 0:
            depts[dept_name] = count
    return depts if depts else None


def fetch_snapshot(snap, board_slug):
    """Fetch a single Wayback snapshot and extract job count."""
    target_url = snap["url_template"].format(board=board_slug)
    wayback_url = f"{WAYBACK_RAW}/{snap['timestamp']}id_/{target_url}"

    try:
        req = urllib.request.Request(wayback_url, headers={"User-Agent": "Fieldwork/1.0"})
        with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"    Error fetching {snap['date']}: {e}")
        return None

    # Try old format first, then new
    count = count_openings_old_format(html)
    format_type = "old"
    if count == 0:
        count = count_openings_new_format(html)
        format_type = "new"

    departments = extract_departments(html) if format_type == "old" else None

    return {
        "date": snap["date"],
        "timestamp": snap["timestamp"],
        "open_roles": count,
        "format": format_type,
        "page_size": snap["length"],
        "departments": departments,
    }


def run(board_slug, output_path, frequency="monthly", start_date=None, end_date=None):
    """Main pipeline: fetch CDX index, select snapshots, extract counts."""
    print(f"\nFieldwork — Wayback Machine History")
    print(f"  Board: {board_slug}")
    print(f"  Frequency: {frequency}")
    print()

    # Fetch CDX index from both old and new URL formats
    all_snapshots = []
    for url_template in BOARD_URLS:
        snapshots = fetch_cdx_index(board_slug, url_template)
        all_snapshots.extend(snapshots)

    if not all_snapshots:
        print("  No snapshots found in Wayback Machine.")
        sys.exit(1)

    # Filter by date range
    if start_date:
        all_snapshots = [s for s in all_snapshots if s["date"] >= start_date]
    if end_date:
        all_snapshots = [s for s in all_snapshots if s["date"] <= end_date]

    print(f"  Total usable snapshots: {len(all_snapshots)}")
    print(f"  Date range: {all_snapshots[0]['date']} to {all_snapshots[-1]['date']}")

    # Select one per period
    selected = select_snapshots(all_snapshots, frequency)

    # Fetch each snapshot and extract data
    timeline = []
    for i, snap in enumerate(selected):
        print(f"  [{i+1}/{len(selected)}] Fetching {snap['date']}...", end=" ", flush=True)
        result = fetch_snapshot(snap, board_slug)
        if result and result["open_roles"] > 0:
            print(f"{result['open_roles']} roles ({result['format']} format)")
            timeline.append(result)
        elif result:
            print(f"0 roles (may be error)")
        else:
            print("failed")

        # Rate limit: be nice to Wayback Machine
        time.sleep(1.5)

    # Add current live count
    print(f"\n  Fetching live count from Greenhouse API...")
    try:
        live_url = f"https://boards-api.greenhouse.io/v1/boards/{board_slug}/jobs?per_page=1"
        req = urllib.request.Request(live_url, headers={"User-Agent": "Fieldwork/1.0"})
        with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
            live_data = json.loads(resp.read())
        live_count = live_data.get("meta", {}).get("total", 0)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        timeline.append({
            "date": today,
            "timestamp": "live",
            "open_roles": live_count,
            "format": "api",
            "page_size": 0,
            "departments": None,
        })
        print(f"  Live: {live_count} roles")
    except Exception as e:
        print(f"  Live fetch error: {e}")

    # Output
    output = {
        "board": board_slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "frequency": frequency,
        "data_points": len(timeline),
        "timeline": timeline,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n  Saved {len(timeline)} data points to {output_path}")

    # Print summary
    print(f"\n  {'Date':<14} {'Roles':>6}  {'Format':<6}")
    print(f"  {'-'*30}")
    for point in timeline:
        print(f"  {point['date']:<14} {point['open_roles']:>6}  {point['format']:<6}")

    if timeline:
        peak = max(timeline, key=lambda t: t["open_roles"])
        trough = min(timeline, key=lambda t: t["open_roles"])
        current = timeline[-1]
        print(f"\n  Peak: {peak['open_roles']} roles ({peak['date']})")
        print(f"  Trough: {trough['open_roles']} roles ({trough['date']})")
        print(f"  Current: {current['open_roles']} roles ({current['date']})")
        if peak["open_roles"] > 0:
            pct_of_peak = current["open_roles"] / peak["open_roles"] * 100
            print(f"  Current vs peak: {pct_of_peak:.0f}%")

    print("\n  Done.\n")


def main():
    parser = argparse.ArgumentParser(description="Fieldwork — Wayback Machine Greenhouse History")
    parser.add_argument("--board", required=True, help="Greenhouse board slug")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--frequency", default="monthly", choices=["monthly", "quarterly"])
    parser.add_argument("--start", default="2020-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", default=None, help="End date YYYY-MM-DD")
    args = parser.parse_args()

    run(args.board, args.output, args.frequency, args.start, args.end)


if __name__ == "__main__":
    main()
