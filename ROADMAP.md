# Fieldwork — Roadmap

## Current (Feb 2026)

### Landing Site (runfieldwork.com)
- [x] Live on GitHub Pages with custom domain
- [x] 12 companies with real data from jobs.db
- [x] Interactive search/dropdown, sample cards, CTA form

### Greenhouse ATS Importer (`scripts/greenhouse_import.py`)
- [x] Fetches full job data from any Greenhouse board
- [x] Classifies function, seniority, AI mentions
- [x] Extracts hiring signals (growth, team structure, comp, segment, motion, geo)
- [x] Extracts tech stack (80+ tools across 12 categories)
- [x] Parses multi-location, international cities, remote detection
- [x] Writes to jobs, job_signals, job_tools tables
- [x] `--reimport` and `--dry-run` flags for safe re-runs

### Report Generator
- [x] Fieldwork branding
- [x] Multi-source attribution (Indeed + Greenhouse ATS)
- [x] Signal analysis, tech stack comparison, geographic footprint

---

## Next Up

### Historical Job Data
- Wayback Machine scraping for cached Greenhouse boards
- Serper searches for archived job listings
- Goal: trend analysis (headcount growth/decline over 6-12 months)

### Additional ATS Integrations
- **Ashby** (`jobs.ashbyhq.com`) — Pulley also uses this
- **Lever** (`jobs.lever.co`)
- **Workday** — complex but covers large enterprises
- Each importer follows same pattern as greenhouse_import.py

### Report Enhancements
- Narrative summary section (AI-generated competitive analysis)
- Trend charts (hiring velocity over time, once historical data exists)
- Department-level deep dives (e.g., "Sales org analysis")

---

## Future Initiative: Fieldwork Viewer UI

A user-facing web interface for browsing the competitive hiring database.

### Core Features
- Company search and browse
- Real-time data cards showing open roles, signals, comp data
- Buttons to pull/import data from ATS platforms (Greenhouse, Lever, Ashby)
- Side-by-side company comparisons
- Export reports as PDF/markdown

### Technical Direction
- Could be Streamlit (fast to build), or a proper React app
- Reads from the same jobs.db
- ATS import buttons call the same scripts (greenhouse_import.py, etc.)
- Auth layer for client access

### Why This Matters
- Clients can self-serve instead of waiting for custom reports
- Real-time data freshness (pull on demand)
- Scales the product beyond manual report generation
