#!/usr/bin/env python3
"""
Fieldwork Blog Build System
Generates blog articles, index page, and updates sitemap.xml.
Usage: python3 scripts/build.py (from repo root)
"""

import json
import os
import sys
from datetime import datetime

# Add scripts dir to path so we can import siblings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nav_config import SITE_URL, SITE_NAME
from templates import (
    get_html_head, get_blog_css, get_nav_html, get_footer_html,
    get_mobile_js, get_page_wrapper, write_page,
    breadcrumb_html, breadcrumb_schema, article_schema,
    faq_schema_and_html,
)

# ── Project root (one level up from scripts/) ──
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT, "blog")

# ═══════════════════════════════════════════════════════════════
# ARTICLE DATA
# ═══════════════════════════════════════════════════════════════

ARTICLES = [
    # ── Article 1 ──
    {
        "slug": "read-competitor-job-postings-strategic-intelligence",
        "title": "How to Read Competitor Job Postings for Strategic Intelligence",
        "meta_title": "Read Competitor Job Postings for Strategy | Fieldwork",
        "meta_description": "Learn what competitor job titles, locations, and salary ranges reveal about their strategic direction. A practical guide to hiring signal analysis.",
        "date": "2026-03-29",
        "category": "Competitive Intelligence",
        "excerpt": "Job postings are public filings of intent. Here's how to decode what your competitors are telling you without meaning to.",
        "faqs": [
            {"q": "What can competitor job postings tell you about strategy?", "a": "Job postings reveal expansion plans (new office locations), technology bets (required skills), compensation positioning, and organizational priorities. A sudden surge in data engineering hires, for example, often precedes a product pivot."},
            {"q": "How often should I review competitor job postings?", "a": "Weekly scans catch fast-moving changes. Monthly analysis is enough to spot trends. Fieldwork delivers structured monthly reports covering hiring volume, comp, signals, and geography for up to 25 competitors."},
            {"q": "Are job postings reliable indicators of company strategy?", "a": "They're one of the most reliable public signals available. Companies can bluff in press releases, but they don't spend money hiring for roles they don't need. The budget commitment makes postings high-signal."},
            {"q": "What tools can I use to track competitor hiring?", "a": "You can manually check career pages and LinkedIn, use job board aggregators, or subscribe to a competitive hiring intelligence platform like Fieldwork that normalizes and analyzes the data for you."},
        ],
        "content": """
<h2>Job Postings Are Public Filings of Intent</h2>

<p>Every company with a careers page is publishing a detailed map of where they're headed. Not where they say they're headed in earnings calls or press releases. Where they're actually spending money.</p>

<p>Most competitive intelligence teams overlook this. They're busy monitoring product launches, pricing changes, and executive quotes. All of which can be staged. But nobody hires 15 machine learning engineers as a bluff.</p>

<p>The signal-to-noise ratio in job postings is unusually high. A company has to pay recruiters, allocate headcount budget, and commit manager time to every open role. That makes each posting a small but real bet on the future. Your job is to read those bets and figure out what game they're playing.</p>

<h2>What Job Titles Tell You About Organizational Priorities</h2>

<p>Start with the titles themselves. Not the seniority level (everyone has "Senior" in their title now), but the function and specialization.</p>

<p>A company hiring its first "Head of Developer Relations" is signaling a platform play. Three "Solutions Engineer" postings in a quarter means they're pushing upmarket. A "Chief AI Officer" listing tells you they're either serious about AI or serious about appearing serious about AI. Context matters.</p>

<p>Track title velocity, not just title existence. One product manager posting is maintenance hiring. Seven product manager postings in 60 days is a new product line. The pattern matters more than any individual data point.</p>

<h3>Titles That Signal Expansion</h3>

<ul>
<li><strong>Regional Sales Manager (APAC/EMEA/LATAM):</strong> Geographic expansion. If they've never had boots on the ground in a region, this is the tip of the spear.</li>
<li><strong>Enterprise Account Executive:</strong> Moving upmarket. Especially telling if they've historically been SMB-focused.</li>
<li><strong>Developer Advocate / DevRel:</strong> Platform or API strategy. They want an ecosystem.</li>
<li><strong>Compliance / Regulatory roles:</strong> Entering a regulated vertical or preparing for international expansion.</li>
</ul>

<h3>Titles That Signal Contraction or Pivot</h3>

<ul>
<li><strong>Sudden pause in engineering hiring:</strong> Budget freeze or strategic uncertainty. Compare to prior quarter volume.</li>
<li><strong>"Restructuring" or "Transformation" in job descriptions:</strong> Reorg in progress. Read between the lines of what they're building next.</li>
<li><strong>Replacing senior roles that were recently filled:</strong> Internal churn. The first hire didn't work out, which suggests unclear strategy.</li>
</ul>

<h2>Location Data: Where They're Planting Flags</h2>

<p>Office location tells you as much as the role itself. A company opening an office in Austin is making a different bet than one opening in Singapore. Both are growth signals, but the markets they're chasing are entirely different.</p>

<p>Remote-first companies make this harder to parse, but not impossible. When a "remote" posting specifies a timezone requirement or lists specific metro areas, that's a constraint that tells you something about their customer base or talent strategy.</p>

<p>Watch for clusters. Three hires in the same city over two months is a satellite office forming, even if they haven't announced it. This is often visible in job posting data 3-6 months before the official press release. <a href="https://www.bls.gov/ooh/" target="_blank" rel="noopener">Bureau of Labor Statistics data</a> can help you contextualize local market dynamics.</p>

<h2>Salary Ranges: The Comp Intelligence Most Teams Ignore</h2>

<p>Thanks to pay transparency laws in states like Colorado, New York, California, and Washington, more job postings now include salary ranges. This is a goldmine for competitive intelligence that goes beyond HR.</p>

<p>Comp data tells you three things:</p>

<ol>
<li><strong>How aggressively they're competing for talent.</strong> Above-market ranges mean they're in acquisition mode and willing to pay for speed.</li>
<li><strong>How they value specific functions.</strong> When a company pays ML engineers 40% more than their backend engineers, that tells you where the strategic weight is.</li>
<li><strong>Their overall cost structure.</strong> A company hiring 50 people in San Francisco at top-of-market rates has very different unit economics than one hiring 50 people in Nashville at median.</li>
</ol>

<p>Fieldwork's <a href="/#reports">monthly reports</a> include comp benchmarking across your competitor set, broken down by function and geography. You can see exactly where rivals are spending more (and less) than you.</p>

<h2>Tech Stack Requirements: Reading the Engineering Roadmap</h2>

<p>The required and preferred technologies listed in engineering job postings are an unfiltered view of a company's technical direction.</p>

<p>When a company that built everything on AWS starts listing GCP or Azure requirements, they're either multi-cloud or migrating. Both are expensive decisions that reveal strategic priorities.</p>

<p>Similarly, a pivot from monolithic frameworks to microservices (Kubernetes, service mesh mentions) signals a scaling push. New data infrastructure requirements (Snowflake, Databricks, dbt) suggest they're investing in analytics capabilities.</p>

<p>You don't need to be an engineer to read these signals. Look for pattern changes. The same stack listed for two years is business as usual. A sudden shift in required technologies is a leading indicator of product evolution.</p>

<h2>Putting It Together: From Data Points to Strategic Narrative</h2>

<p>Individual job postings are data points. The value comes from connecting them into a narrative. Here's a framework:</p>

<ol>
<li><strong>Volume trend:</strong> Are they hiring more or fewer people than last quarter? This is the baseline growth/contraction signal.</li>
<li><strong>Function mix:</strong> What percentage goes to engineering vs. sales vs. operations? Shifts here reveal changing priorities.</li>
<li><strong>Seniority distribution:</strong> Heavy senior hiring means new initiatives. Heavy junior hiring means scaling existing ones.</li>
<li><strong>Geographic spread:</strong> New markets, new offices, or consolidation.</li>
<li><strong>Comp positioning:</strong> Aggressive, market, or below-market. And for which roles.</li>
</ol>

<p>Track these five dimensions for each competitor monthly. Over a quarter, patterns become clear. Over two quarters, you can start making predictions. <a href="https://hbr.org/2024/01/competitive-intelligence-that-actually-works" target="_blank" rel="noopener">Harvard Business Review</a> has noted that hiring data is among the most underused inputs in competitive strategy.</p>

<p>If doing this manually sounds like a lot of work, that's because it is. <a href="/#demo">Fieldwork automates the collection and normalization</a>. You focus on the analysis.</p>

<h2>What to Do With What You Find</h2>

<p>Intelligence without action is trivia. Once you've identified a hiring signal, route it to the right team:</p>

<ul>
<li><strong>Sales:</strong> "Competitor X just posted 8 enterprise AE roles in the northeast. Expect them to get aggressive on your accounts in that region. Here's their likely pitch based on the role requirements."</li>
<li><strong>Product:</strong> "Competitor Y is hiring Rust and WebAssembly engineers for the first time. They may be rebuilding their core product for performance. Watch for a re-architecture announcement in 6-9 months."</li>
<li><strong>Executive team:</strong> "Competitor Z's hiring velocity dropped 40% this quarter while ours grew 15%. We have a window to capture market share before they recover."</li>
<li><strong>Talent acquisition:</strong> "Competitor X is offering 20% above market for senior SREs. Either match the comp or accelerate your offer timelines to close candidates before they see competing offers."</li>
</ul>

<p>The companies that win aren't the ones with the most data. They're the ones that move fastest from signal to decision. And right now, most of your competitors aren't reading your job postings for intel.</p>

<p>Are you reading theirs? <a href="/#pricing">See Fieldwork pricing</a> to get started.</p>
""",
    },

    # ── Article 2 ──
    {
        "slug": "compensation-benchmarking-without-expensive-tools",
        "title": "Compensation Benchmarking Without Expensive Tools",
        "meta_title": "Comp Benchmarking Without Expensive Tools | Fieldwork",
        "meta_description": "Compare DIY compensation benchmarking methods against platforms like Fieldwork. Get comp intelligence without a six-figure contract.",
        "date": "2026-03-29",
        "category": "Compensation Intelligence",
        "excerpt": "You don't need a $100K Radford subscription to know what competitors pay. But you do need a system.",
        "faqs": [
            {"q": "How can I benchmark compensation without expensive tools?", "a": "Use public job posting salary data (from states with pay transparency laws), Glassdoor/Levels.fyi/H1B data, and aggregated job board data. The key is building a consistent tracking system rather than doing ad hoc lookups."},
            {"q": "How accurate are salary ranges in job postings?", "a": "Ranges in states with mandatory disclosure (CO, NY, CA, WA) are generally accurate because companies face legal risk for misleading ranges. Voluntary disclosures elsewhere can be wider or less precise."},
            {"q": "What's the difference between Fieldwork and a comp survey?", "a": "Traditional comp surveys (Radford, Mercer) collect self-reported data from participating companies, often with a 6-12 month lag. Fieldwork pulls real-time salary data from active job postings, giving you current market rates for the roles competitors are actually filling."},
            {"q": "How often does compensation data change?", "a": "Market rates shift quarterly in fast-moving sectors like tech. Monthly tracking catches significant movements before they compound. Annual surveys miss too much in a dynamic market."},
            {"q": "Can I benchmark comp without revealing my own data?", "a": "Yes. Job posting data is public. You can analyze competitor pay without participating in any data exchange. Traditional surveys require you to share your own compensation data to access the dataset."},
        ],
        "content": """
<h2>The Comp Data Problem</h2>

<p>If you've priced a Radford or Mercer subscription lately, you know the number starts with a comma. Enterprise comp surveys run $50K-$150K per year, and they're designed for companies with dedicated compensation teams and the budget to match.</p>

<p>For everyone else, compensation benchmarking has been a game of guessing. Glassdoor averages that feel stale. LinkedIn salary "insights" based on self-reported data of questionable accuracy. The occasional H1B disclosure that gives you one data point for one role at one company.</p>

<p>There's a better way. It doesn't require six figures or a comp team. But it does require a system.</p>

<h2>Free and Low-Cost Comp Data Sources (Ranked by Reliability)</h2>

<h3>1. Job Postings With Mandatory Salary Disclosure</h3>

<p>This is your best free source. Period. Colorado, New York, California, and Washington now require salary ranges in job postings. Several other states have similar laws taking effect. When a company posts a range because the law requires it, that range has legal weight. It's not a wish or an aspiration. It's a commitment.</p>

<p>The challenge: you need to find, track, and normalize this data across dozens or hundreds of competitor postings. Manually, this is 4-6 hours per week of tedious work. Fieldwork does it automatically across 27,000+ postings, but if you're bootstrapping, start with your top 5 competitors and track their postings in a spreadsheet.</p>

<h3>2. Levels.fyi (Tech Roles)</h3>

<p>For software engineering, product management, and data science roles at tech companies, <a href="https://www.levels.fyi/" target="_blank" rel="noopener">Levels.fyi</a> is surprisingly accurate. The data is crowdsourced but verified against offer letters. It skews toward large tech companies, so coverage for mid-market or non-tech is thin.</p>

<h3>3. H1B Salary Disclosures</h3>

<p>The Department of Labor publishes H1B visa salary data. This gives you exact base salaries (not ranges) for specific roles at specific companies. The catch: it only covers H1B workers, which skews the data toward certain engineering and data roles, and there's a 6-12 month lag.</p>

<h3>4. Glassdoor and Indeed</h3>

<p>Self-reported data with no verification. Useful for broad directional signals ("are they paying above or below market?") but not reliable enough for precise benchmarking. The averages often lag the market by a year or more.</p>

<h3>5. State and Federal Salary Databases</h3>

<p>Public sector organizations publish employee salaries. If you're competing with government or quasi-government entities for talent (common in healthcare, education, defense), this is free and accurate data.</p>

<h2>Building a DIY Comp Tracking System</h2>

<p>Here's a system that takes about 2 hours per week and produces useful comp intelligence:</p>

<h3>Step 1: Define Your Benchmark Roles</h3>

<p>Pick 8-12 roles that matter most to your business. Don't try to track everything. Focus on roles where you're losing candidates or where you suspect competitors are outbidding you. Typical priority roles: Senior Software Engineer, Product Manager, Account Executive, Data Scientist, Engineering Manager.</p>

<h3>Step 2: Identify Your Competitor Set</h3>

<p>Choose 5-10 companies you compete with for talent. These aren't always your product competitors. A fintech startup in Austin competes for engineering talent with Dell, Indeed, and Oracle, not just other fintechs. Think about who your candidates are choosing between you and.</p>

<h3>Step 3: Weekly Collection</h3>

<p>Every Monday, check each competitor's careers page and note new postings for your benchmark roles. Record: company, title, location, salary range (if disclosed), and any notable requirements. A simple Google Sheet works fine.</p>

<h3>Step 4: Monthly Analysis</h3>

<p>At month's end, compute ranges for each benchmark role across your competitor set. Where do you fall? Are competitors moving ranges up faster than you? Which roles show the biggest gap?</p>

<p>This is where most people run out of discipline. The first month is interesting. By month three, it's a chore. That's the moment when a tool like <a href="/#pricing">Fieldwork</a> pays for itself. The data collection is the boring part. The analysis is where the value lives.</p>

<h2>What Good Comp Intelligence Actually Looks Like</h2>

<p>Raw salary data isn't intelligence. Intelligence is the answer to "what should we do differently?" Here's what matters:</p>

<ul>
<li><strong>Range positioning:</strong> Where does your range sit relative to the market? 25th, 50th, 75th percentile? And is that where you want to be?</li>
<li><strong>Comp velocity:</strong> How fast are ranges moving? If your top competitor raised their SWE range by 12% this quarter, you need to know before your next comp cycle.</li>
<li><strong>Total comp structure:</strong> Some companies lead with base salary. Others use equity or bonuses. Job postings increasingly disclose total comp structure. A competitor offering $180K base + $50K equity competes differently than one offering $210K base + $20K bonus.</li>
<li><strong>Geographic arbitrage:</strong> Who's paying SF rates for Denver roles? Who's adjusting by location? This tells you about their remote work strategy and their talent competition map.</li>
</ul>

<h2>The Real Cost of Bad Comp Data</h2>

<p>Here's math that most companies haven't done. If you're offering below-market comp because your data is stale, every failed hire costs you:</p>

<ul>
<li>Recruiter time: 15-20 hours per search</li>
<li>Hiring manager time: 8-10 hours of interviews</li>
<li>Pipeline delay: 30-60 days per restart</li>
<li>Opportunity cost: whatever that unfilled seat costs in lost revenue</li>
</ul>

<p>For a $150K role, a failed search easily costs $30K-$50K when you account for all the time and pipeline delays. Do that three times because your ranges are wrong, and you've spent more than a year of <a href="/#pricing">Fieldwork's Professional plan</a>.</p>

<p>The <a href="https://www.shrm.org/topics-tools/news/talent-acquisition/average-cost-per-hire-rises-to-4700-shrm-survey-finds" target="_blank" rel="noopener">SHRM cost-per-hire benchmark</a> pegs average hiring costs at $4,700. But that's the average across all roles. For the competitive technical and go-to-market roles where comp data matters most, the real number is 5-10x that.</p>

<h2>When to Invest in a Platform vs. DIY</h2>

<p>DIY comp tracking works when:</p>
<ul>
<li>You have fewer than 5 competitors to track</li>
<li>You're benchmarking fewer than 10 roles</li>
<li>You have someone willing to dedicate 2+ hours per week consistently</li>
<li>You only need directional data, not precise benchmarks</li>
</ul>

<p>A platform makes sense when:</p>
<ul>
<li>You're tracking 10+ competitors</li>
<li>You need historical trend data, not just current snapshots</li>
<li>Multiple teams (TA, comp, CI, sales) need the data</li>
<li>You can't afford the 6-month ramp-up to build a useful dataset from scratch</li>
</ul>

<p>Fieldwork sits in the gap between "manually check careers pages" and "sign a $100K Lightcast contract." It's <a href="/#pricing">structured comp and hiring intelligence</a> at a price point that doesn't require VP-level budget approval.</p>

<p>What's the cost of not knowing what your competitors pay? If you can't answer that question, you're probably already behind.</p>
""",
    },

    # ── Article 3 ──
    {
        "slug": "hiring-signals-predict-competitor-next-move",
        "title": "5 Hiring Signals That Predict a Competitor's Next Move",
        "meta_title": "5 Hiring Signals That Predict Competitors | Fieldwork",
        "meta_description": "These five patterns in competitor job postings predict strategic moves months before they're announced. Learn to spot them.",
        "date": "2026-03-29",
        "category": "Hiring Signals",
        "excerpt": "Companies lie in press releases. They don't lie in headcount budgets. Here are the five patterns that predict what's coming next.",
        "faqs": [
            {"q": "What are hiring signals in competitive intelligence?", "a": "Hiring signals are patterns in job postings that indicate a company's strategic direction. These include changes in hiring volume, new role types, geographic expansion, compensation shifts, and technology stack requirements."},
            {"q": "How far in advance can hiring data predict strategy?", "a": "Hiring data typically leads public announcements by 3-9 months. A company must hire the team before launching a product, entering a market, or executing a pivot. The hiring precedes the announcement."},
            {"q": "How do I distinguish noise from real hiring signals?", "a": "Look for sustained patterns, not one-off postings. A single job posting is noise. Five postings in the same function over 60 days is signal. Compare against the company's historical hiring baseline to spot meaningful deviations."},
            {"q": "Can hiring signals help sales teams win deals?", "a": "Yes. If a competitor is ramping their sales team in your territory, that's an early warning to defend accounts. If they're cutting sales headcount, it may signal an opening to poach their customers. Fieldwork routes these insights to sales teams monthly."},
        ],
        "content": """
<h2>Why Hiring Data Is the Best Leading Indicator</h2>

<p>Companies can say anything they want in a press release. They can spin narrative on earnings calls. They can position themselves however they'd like at industry conferences.</p>

<p>But when they spend money on headcount, they're telling the truth. Hiring is one of the few strategic signals that comes with a price tag attached. Every open role represents approved budget, manager conviction, and organizational priority. That's hard to fake.</p>

<p>After analyzing tens of thousands of job postings across hundreds of companies, five patterns consistently predict strategic moves before they're announced. Here's what to watch for.</p>

<h2>Signal 1: The Function Shift</h2>

<p>A company's hiring mix by function is a real-time view of where they're investing. When that mix changes, something strategic is happening.</p>

<p>Example: a SaaS company that historically hired 60% engineering and 30% sales suddenly flips to 40% engineering and 50% sales. That's a company that's done building and is now in distribution mode. Their product roadmap is probably frozen while they push for revenue.</p>

<p>The reverse is equally telling. A company pulling back on sales hiring while ramping engineering is likely preparing a major product overhaul. They're betting that the current product won't win in the market, so they're rebuilding before scaling again.</p>

<p>Track the ratio of go-to-market (sales, marketing, customer success) to R&D (engineering, product, design, data) hires. Shifts of 15%+ in a quarter are meaningful.</p>

<h2>Signal 2: The Geographic Cluster</h2>

<p>When multiple job postings appear in a new city within a 60-day window, that's a new office forming. Companies rarely announce satellite offices until they have 10+ people seated. The postings show up months earlier.</p>

<p>In 2024, several AI startups posted clusters of roles in DC and Northern Virginia before announcing government or defense-focused product lines. The location told the story before the product announcement.</p>

<p>International clusters are even more telling. A US-based company hiring 5+ roles in London or Singapore is expanding into that market. Period. You don't build a local team to serve US customers from overseas timezones.</p>

<p>What to track: new cities where a competitor has never posted before. Any city with 3+ postings in a quarter that had zero in the prior year deserves attention.</p>

<h2>Signal 3: The Executive Hire</h2>

<p>When a company posts for a new VP or C-level role in a function they didn't previously have at that level, they're building a new organizational capability.</p>

<p>A first-ever VP of Data posting means they're getting serious about data products, analytics, or data monetization. A new VP of Partnerships means they're shifting from direct sales to ecosystem distribution. A Chief Revenue Officer posting at a company that previously had a VP of Sales means they're scaling go-to-market and probably raising their next round.</p>

<p>The specificity of executive role descriptions matters too. A VP of Sales posting that mentions "enterprise" or "upmarket" tells you their strategic direction. One that emphasizes "PLG" or "self-serve" tells you the opposite.</p>

<p>The <a href="https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-organization-blog" target="_blank" rel="noopener">McKinsey org performance blog</a> has documented how executive hiring patterns correlate with strategic pivots.</p>

<h2>Signal 4: The Tech Stack Shift</h2>

<p>This signal requires some technical literacy, but it's one of the highest-confidence predictors available.</p>

<p>When a company's engineering job postings start requiring a technology they've never mentioned before, they're making a significant technical bet. Examples that have predicted real moves:</p>

<ul>
<li><strong>Rust or Go appearing for the first time:</strong> Performance-critical systems rebuild. They're replacing something slow with something fast.</li>
<li><strong>Kubernetes, Terraform, or cloud-native infrastructure:</strong> Scaling push. They expect significantly more traffic or complexity.</li>
<li><strong>ML/AI frameworks (PyTorch, MLflow, vector databases):</strong> AI product features incoming. Probably 6-12 months out.</li>
<li><strong>Compliance or security tools (SOC2, FedRAMP, HIPAA):</strong> Entering a regulated market segment. Government or healthcare push likely.</li>
</ul>

<p>The inverse matters too. When a company stops mentioning a technology they've used for years, they're migrating off it. That migration consumes engineering resources and usually means fewer new features during the transition.</p>

<p>Fieldwork's <a href="/#reports">monthly competitive reports</a> track tech stack mentions across your competitor set so you don't need to parse individual job descriptions.</p>

<h2>Signal 5: The Hiring Velocity Change</h2>

<p>This is the simplest signal and often the most powerful. Hiring velocity, the number of open roles at any point in time, is a proxy for a company's confidence in their trajectory.</p>

<p>A 50% increase in open roles quarter-over-quarter usually means: they've closed funding, hit a growth milestone, or are executing on a strategic initiative. A 50% decrease means: budget cuts, strategic uncertainty, or a failed initiative being wound down.</p>

<p>Watch for asymmetric velocity. If a competitor's engineering hiring stays flat while their sales hiring doubles, that's signal 1 (function shift) combining with signal 5. The combination of multiple signals in the same direction creates high-confidence predictions.</p>

<h3>How to Calculate Hiring Velocity</h3>

<p>Count active open roles for each competitor at the same point each month. Plot the trend. You're looking for inflection points: months where the count jumps or drops by more than 20% versus the prior month.</p>

<p>If you have historical data, calculate the 3-month rolling average. Compare each month's count to the rolling average. A count more than 30% above the rolling average is a surge. More than 30% below is a pullback.</p>

<h2>Combining Signals Into Predictions</h2>

<p>No single signal is conclusive on its own. The confidence level rises when multiple signals align:</p>

<ul>
<li><strong>Function shift toward sales + geographic cluster in new region + executive hire (VP Sales, region):</strong> Market expansion into that geography. High confidence.</li>
<li><strong>Tech stack shift to AI/ML + velocity increase in engineering + new ML executive hire:</strong> AI product launch coming. Very high confidence.</li>
<li><strong>Velocity decrease across all functions + no executive hires + geographic contraction:</strong> Company in trouble. Budget cuts or strategic reset.</li>
<li><strong>Comp increases in specific roles + velocity stable + function mix unchanged:</strong> Retention fight. They're losing people to competitors (possibly you) and raising pay to stem the bleeding.</li>
</ul>

<p>The companies doing this well track 5+ signals across 10+ competitors and review monthly. It sounds like a lot, but with the right system, the data collection is automated and the analysis takes 30 minutes per month. <a href="/#demo">See how Fieldwork structures this for you.</a></p>

<p>The question isn't whether your competitors are sending these signals. They are. The question is whether anyone at your company is reading them. What signals have you been missing?</p>
""",
    },

    # ── Article 4 ──
    {
        "slug": "build-competitive-hiring-dashboard",
        "title": "How to Build a Competitive Hiring Dashboard",
        "meta_title": "Build a Competitive Hiring Dashboard | Fieldwork",
        "meta_description": "Step-by-step guide to building a competitive hiring dashboard for talent acquisition and CI teams. Data sources, metrics, and visualization.",
        "date": "2026-03-29",
        "category": "Talent Acquisition",
        "excerpt": "A practical guide to building the dashboard your TA and CI teams wish they had. Data sources, metrics, and the build-vs-buy decision.",
        "faqs": [
            {"q": "What should a competitive hiring dashboard track?", "a": "Core metrics include: hiring velocity by competitor, function mix, geographic distribution, compensation ranges by role, tech stack mentions, and seniority distribution. The best dashboards also show trend lines and anomaly detection."},
            {"q": "What data sources feed a hiring dashboard?", "a": "Primary sources: competitor career pages, job board APIs (Indeed, LinkedIn), pay transparency disclosures. Secondary sources: Glassdoor reviews, H1B filings, SEC filings for headcount data. Fieldwork aggregates these into a single structured feed."},
            {"q": "How long does it take to build a hiring dashboard from scratch?", "a": "A basic version with manual data collection takes 2-3 weeks to set up and 4-6 hours per week to maintain. An automated version with API integrations takes 2-3 months of engineering time and ongoing maintenance for scraper reliability."},
            {"q": "Who should own the competitive hiring dashboard?", "a": "Joint ownership between Talent Acquisition and Competitive Intelligence works best. TA owns the comp and talent pipeline data. CI owns the strategic analysis layer. Both teams benefit from the same underlying data."},
            {"q": "Should I build or buy a competitive hiring dashboard?", "a": "Build if you have engineering resources, unique data requirements, and 3+ months of patience. Buy if you need insights within 30 days or if your engineering team is better deployed on product work. Fieldwork is purpose-built for this use case."},
        ],
        "content": """
<h2>Why Most CI Teams Don't Have a Hiring Dashboard (and Should)</h2>

<p>Competitive intelligence teams track product launches, pricing changes, executive moves, and funding rounds. Most have some form of dashboard or tracking system for these signals. Very few have anything comparable for hiring data.</p>

<p>This is strange, because hiring data is arguably the most reliable strategic signal available. It's public, it's frequent, and it comes with a budget commitment attached. Yet most CI and TA teams still approach hiring intelligence with ad hoc LinkedIn searches and occasional manual career page checks.</p>

<p>The reason is simple: the data is messy. Job titles aren't standardized. Companies use different terminology for the same roles. Postings appear and disappear without warning. Building a clean, comparable dataset requires significant effort.</p>

<p>Here's how to do it anyway.</p>

<h2>Step 1: Define Your Competitor Set</h2>

<p>Start with 10-15 companies. Not your entire competitive landscape. The companies that matter most for two reasons:</p>

<ol>
<li><strong>Product competitors:</strong> Companies your sales team encounters in deals. Their hiring tells you about product direction, market focus, and sales strategy.</li>
<li><strong>Talent competitors:</strong> Companies your candidates choose instead of you. These aren't always the same as product competitors. A B2B SaaS startup in Denver might compete for talent with Datadog and Splunk, not just direct product competitors.</li>
</ol>

<p>The overlap between these two lists is your priority set. If a company appears on both lists, track them first.</p>

<h2>Step 2: Choose Your Data Sources</h2>

<h3>Tier 1: Career Pages (Most Reliable)</h3>

<p>Direct career page monitoring is the gold standard. The data is first-party, current, and complete. The challenge is that every company has a different ATS (Greenhouse, Lever, Workday, custom), and each presents data differently.</p>

<p>If you're building this yourself, you'll need scrapers for each ATS format. Greenhouse and Lever have public API endpoints that make this easier. Workday and custom career pages require web scraping, which is more brittle.</p>

<h3>Tier 2: Job Board Aggregators</h3>

<p>Indeed, LinkedIn, Glassdoor, and ZipRecruiter aggregate postings from multiple sources. They're useful for breadth but have a lag (postings may appear 1-3 days after the career page) and sometimes miss postings that aren't syndicated.</p>

<h3>Tier 3: Government Filings</h3>

<p>SEC filings include headcount data for public companies (usually quarterly). <a href="https://www.dol.gov/agencies/eta/foreign-labor/performance" target="_blank" rel="noopener">H1B disclosures from the Department of Labor</a> give you exact salaries for visa-sponsored roles. Both are lagging indicators but useful for validation.</p>

<h2>Step 3: Normalize the Data</h2>

<p>This is where most DIY efforts die. Raw job posting data is inconsistent. One company calls the role "Software Engineer II," another calls it "Senior Backend Developer," and a third calls it "Platform Engineer." They might all be the same role.</p>

<p>You need a normalization layer that maps raw titles to a standard taxonomy. Start simple: Engineering, Product, Design, Data, Sales, Marketing, Customer Success, Operations, Executive, Other. Within each, add seniority levels: IC Junior, IC Mid, IC Senior, IC Staff+, Manager, Director, VP+.</p>

<p>This normalization is what makes the data comparable across companies. Without it, you're comparing apples to job-posting-shaped oranges.</p>

<h2>Step 4: Design Your Dashboard Metrics</h2>

<p>The metrics that matter, in priority order:</p>

<h3>Primary Metrics (Check Weekly)</h3>
<ul>
<li><strong>Open role count by competitor:</strong> The basic pulse. Is each competitor growing or shrinking?</li>
<li><strong>30-day change in open roles:</strong> The velocity signal. A +40% jump demands attention.</li>
<li><strong>Function mix breakdown:</strong> Pie chart or stacked bar showing engineering vs. GTM vs. other for each competitor.</li>
</ul>

<h3>Secondary Metrics (Check Monthly)</h3>
<ul>
<li><strong>Compensation ranges by benchmark role:</strong> Where each competitor falls for your priority roles.</li>
<li><strong>Geographic distribution:</strong> Map view of where competitors are hiring. New pins = new markets.</li>
<li><strong>Tech stack heatmap:</strong> Technologies mentioned in engineering postings, tracked over time.</li>
<li><strong>Time-to-fill estimate:</strong> How long postings stay active. Longer = harder to fill or less urgent.</li>
</ul>

<h3>Strategic Metrics (Check Quarterly)</h3>
<ul>
<li><strong>Function mix trend:</strong> How the engineering-to-sales ratio has shifted over 12 months.</li>
<li><strong>Comp velocity:</strong> Rate of change in salary ranges quarter-over-quarter.</li>
<li><strong>Net hiring momentum:</strong> Postings added minus postings removed. Captures the real growth rate.</li>
</ul>

<h2>Step 5: Visualization and Distribution</h2>

<p>The dashboard is useless if nobody looks at it. Design for your audience:</p>

<ul>
<li><strong>TA teams</strong> want comp data and role-level detail. They need to answer "what's market rate for this role?" in real time.</li>
<li><strong>CI teams</strong> want strategic signals and trend analysis. They need to answer "what is competitor X about to do?"</li>
<li><strong>Sales leadership</strong> wants competitive positioning data. They need to answer "where is competitor X investing, and how do we counter?"</li>
<li><strong>Executives</strong> want the 3-bullet summary. Top 3 signals from the past month, with recommended actions.</li>
</ul>

<p>Build the full dashboard for CI and TA. Create derivative views (email digests, slide decks) for sales and executives. Fieldwork's <a href="/#reports">monthly reports</a> are designed for this distribution pattern.</p>

<h2>Build vs. Buy: The Honest Math</h2>

<p>Building this yourself requires:</p>

<ul>
<li><strong>Scrapers:</strong> 2-3 weeks of engineering time to build. Ongoing maintenance as career pages change formats. Budget 4-8 hours per month for scraper fixes.</li>
<li><strong>Data pipeline:</strong> Storage, normalization, deduplication. Another 2-3 weeks to build properly.</li>
<li><strong>Dashboard:</strong> 1-2 weeks for the visualization layer (Looker, Metabase, custom).</li>
<li><strong>Maintenance:</strong> A conservative 10-15 hours per month once everything is running.</li>
</ul>

<p>Total: 6-8 weeks of engineering time upfront, plus 10-15 hours per month ongoing. At a blended engineering rate of $150/hour, that's $15K-$20K to build and $1,500-$2,250 per month to maintain.</p>

<p>Compare that to a purpose-built solution. <a href="/#pricing">Fieldwork's plans</a> start at a fraction of the DIY engineering cost and include the data collection, normalization, and reporting layer. The math favors buying for most teams, unless you have very specific data requirements that no platform covers.</p>

<p>The companies that build their own hiring dashboards and maintain them long-term tend to be the ones that also build their own CRM and their own analytics platform. If that's your culture, build. If you'd rather spend engineering cycles on your product, buy.</p>

<p>Either way, the competitive hiring dashboard is the missing piece in most CI stacks. When are you going to fill the gap?</p>
""",
    },

    # ── Article 5 ──
    {
        "slug": "job-posting-data-vs-linkedin-competitor-intelligence",
        "title": "Job Posting Data vs LinkedIn for Competitor Intel",
        "meta_title": "Job Posting Data vs LinkedIn for CI | Fieldwork",
        "meta_description": "Job posting data and LinkedIn each reveal different things about competitors. Here's when to use which, and why most teams get the mix wrong.",
        "date": "2026-03-29",
        "category": "Competitive Intelligence",
        "excerpt": "LinkedIn tells you who works somewhere. Job postings tell you what they're building next. The difference matters more than most CI teams realize.",
        "faqs": [
            {"q": "Is LinkedIn or job posting data better for competitive intelligence?", "a": "They answer different questions. LinkedIn shows current headcount, employee backgrounds, and turnover patterns. Job posting data shows future plans: what roles they're filling, what they're paying, and what technology they're adopting. The best CI programs use both."},
            {"q": "Can I track competitor hiring through LinkedIn alone?", "a": "Partially. LinkedIn shows some job postings and employee counts, but its data is incomplete. Not all jobs are posted on LinkedIn, headcount numbers lag by weeks, and salary data is limited. Direct career page monitoring catches what LinkedIn misses."},
            {"q": "What does LinkedIn tell you that job postings don't?", "a": "LinkedIn reveals employee tenure, departure patterns (who's leaving and where they're going), team composition, and individual employee backgrounds. This is backward-looking intelligence that job postings can't provide."},
            {"q": "How do I combine LinkedIn and job posting data effectively?", "a": "Use job posting data for forward-looking signals (what they're building, where they're expanding, what they'll pay). Use LinkedIn for backward-looking signals (who left, team size changes, skill composition). Review both monthly and look for patterns that confirm or contradict each other."},
        ],
        "content": """
<h2>Two Data Sources, Two Different Questions</h2>

<p>Most competitive intelligence teams default to LinkedIn when they want to understand a competitor's talent strategy. It makes sense. LinkedIn is the largest professional network, it's searchable, and it shows you who works where.</p>

<p>But LinkedIn answers a fundamentally different question than job posting data. LinkedIn tells you what already happened. Job postings tell you what's about to happen. And in competitive intelligence, the future is worth a lot more than the past.</p>

<p>Here's a detailed breakdown of what each source gives you, where they overlap, and when to use which.</p>

<h2>What LinkedIn Tells You</h2>

<h3>Current Headcount and Team Structure</h3>

<p>LinkedIn's company pages show employee counts, broken down by function and location. This gives you a snapshot of how a competitor's team is structured right now. You can see that Company X has 200 engineers and 80 salespeople, weighted toward San Francisco and New York.</p>

<p>Limitation: these numbers are self-reported and lag reality by weeks or months. People don't always update their profiles when they change jobs. The counts are directionally useful but not precise.</p>

<h3>Employee Backgrounds and Skill Composition</h3>

<p>LinkedIn profiles include work history, education, and skills. You can analyze what backgrounds a competitor hires from. If their last 10 engineering hires all came from fintech companies, that tells you something about their product direction.</p>

<h3>Departure Patterns</h3>

<p>This is LinkedIn's killer feature for CI. When employees leave a competitor, their profile updates (eventually). You can track: who's leaving, what level, which function, and where they're going. A wave of senior engineering departures to the same company suggests something specific pulled them. A broad exodus across levels suggests internal problems.</p>

<h3>Network Analysis</h3>

<p>LinkedIn lets you see connections between employees at different companies. This is useful for tracking advisor relationships, board connections, and potential partnerships or acquisitions. If a competitor's CEO and a PE firm partner suddenly connect, that might signal something.</p>

<h2>What Job Posting Data Tells You</h2>

<h3>Future Hiring Plans</h3>

<p>Job postings are forward-looking by definition. They represent roles that don't yet exist at the company. This is the single biggest advantage over LinkedIn: you see what the company will look like in 3-6 months, not what it looks like today.</p>

<h3>Compensation Strategy</h3>

<p>With pay transparency laws expanding, job postings increasingly include salary ranges. LinkedIn has some salary data, but it's self-reported and unverified. Job posting salary data from states with mandatory disclosure is as close to official comp data as you can get without access to the company's HRIS.</p>

<h3>Technology Direction</h3>

<p>Engineering job postings list required and preferred technologies. This is a direct readout of the company's technical architecture and future direction. LinkedIn skills endorsements are noisy and outdated. Job requirements represent what the company needs right now.</p>

<h3>Urgency and Priority</h3>

<p>The specificity and seniority of job postings reveal urgency. A posting that's been up for 90 days is either a nice-to-have or impossible to fill. A posting with aggressive comp and a "start immediately" note is a priority hire. LinkedIn can't show you this urgency signal.</p>

<h2>Head-to-Head Comparison</h2>

<p>Let's compare specific use cases:</p>

<p><strong>Understanding competitor team size:</strong> LinkedIn wins. It shows actual employees, not just open roles.</p>

<p><strong>Predicting competitor product moves:</strong> Job postings win. New role types, tech stack changes, and hiring surges appear in postings months before they manifest in LinkedIn headcount.</p>

<p><strong>Benchmarking compensation:</strong> Job postings win. Verified salary ranges in postings vs. self-reported data on LinkedIn.</p>

<p><strong>Tracking employee turnover:</strong> LinkedIn wins. You can see departures and destinations. Job postings only show incoming hires.</p>

<p><strong>Identifying geographic expansion:</strong> Tie. LinkedIn shows where employees are located. Job postings show where new hires will be. Both are useful. Job postings are earlier (leading indicator), LinkedIn is confirming (lagging indicator).</p>

<p><strong>Understanding organizational culture:</strong> LinkedIn wins (Glassdoor wins more, but that's a different article). Employee reviews, post engagement, and departure patterns paint a picture. Job descriptions sometimes reveal culture through language, but it's less reliable.</p>

<h2>The Combination Play</h2>

<p>The real intelligence advantage comes from using both sources together. Here's how:</p>

<ol>
<li><strong>Spot the signal in job postings:</strong> Competitor X just posted 8 ML engineering roles. First time they've had any ML postings.</li>
<li><strong>Validate on LinkedIn:</strong> Check if they've recently hired any ML leaders. If a VP of ML appeared on their team 2 months ago, those 8 roles are their team buildout. High confidence.</li>
<li><strong>Track the outcome:</strong> Over the next 3-6 months, watch LinkedIn for those ML engineers to appear as employees. Confirm the hiring was successful.</li>
<li><strong>Anticipate the impact:</strong> 6-12 months after the ML team assembles, expect AI-powered product features.</li>
</ol>

<p>This loop, signal (postings) to validation (LinkedIn) to tracking (LinkedIn) to prediction (analysis), is the core of a sophisticated competitive hiring intelligence program.</p>

<p>Fieldwork's <a href="/#reports">monthly reports</a> provide the job posting layer. Pair them with your own LinkedIn monitoring and you have full coverage. The <a href="https://www.crayon.co/blog/competitive-intelligence-best-practices" target="_blank" rel="noopener">Crayon competitive intelligence framework</a> recommends this multi-source approach.</p>

<h2>Where Both Sources Fall Short</h2>

<p>Neither job postings nor LinkedIn capture:</p>

<ul>
<li><strong>Internal transfers:</strong> A company reassigning 20 engineers from one product to another. No external signal for this.</li>
<li><strong>Contractor and agency hires:</strong> Often invisible in both datasets.</li>
<li><strong>Confidential searches:</strong> Executive placements through search firms bypass both channels.</li>
<li><strong>Layoffs that are backfilled:</strong> A team that lost 5 people and hired 5 replacements looks stable from the outside but is actually in turmoil.</li>
</ul>

<p>No data source is complete. The best CI programs acknowledge these blind spots and use multiple inputs to triangulate. Job postings and LinkedIn are two of the most accessible and highest-signal sources available. Using only one is leaving intelligence on the table.</p>

<p>Which source is your team relying on more heavily? And what are you missing because of that choice? <a href="/#demo">Fieldwork can fill the job posting gap</a>. LinkedIn, you've already got covered.</p>
""",
    },

    # ── Article 6 ──
    {
        "slug": "ai-hiring-trends-job-postings-enterprise-adoption",
        "title": "AI Hiring Trends: What Job Postings Reveal About Enterprise AI",
        "meta_title": "AI Hiring Trends in Enterprise Job Postings | Fieldwork",
        "meta_description": "What enterprise job postings reveal about real AI adoption in 2026. Beyond the hype, here's who's hiring, what they need, and what it signals.",
        "date": "2026-03-29",
        "category": "Market Trends",
        "excerpt": "Everyone says they're doing AI. Job postings tell you who's actually spending money on it. The gap between talk and talent investment is revealing.",
        "faqs": [
            {"q": "What AI roles are companies hiring for in 2026?", "a": "The fastest-growing categories are AI/ML Engineer, Prompt Engineer, AI Product Manager, ML Infrastructure Engineer, and AI Ethics/Safety roles. The shift from research-focused to production-focused AI hiring is the defining trend of 2026."},
            {"q": "How can I tell if a company is serious about AI from their job postings?", "a": "Look for production-oriented roles (ML Engineers, MLOps), not just research roles (Research Scientists). Check for AI leadership hires (VP/Head of AI). And look at the ratio of AI roles to total engineering roles. Above 20% signals a real commitment."},
            {"q": "Are AI engineer salaries still increasing?", "a": "Yes, but the rate of increase is slowing for generalist ML roles. Specialist roles (ML infrastructure, LLM fine-tuning, AI safety) still command significant premiums. The market is bifurcating between commodity AI skills and scarce specialist skills."},
            {"q": "What industries are hiring the most AI talent?", "a": "Financial services, healthcare, and enterprise SaaS lead in volume. The fastest growth is in manufacturing (predictive maintenance), logistics (route optimization), and legal (document analysis). Traditionally non-tech industries are now competing directly with tech companies for AI talent."},
        ],
        "content": """
<h2>The Gap Between AI Talk and AI Talent</h2>

<p>In 2026, every company's investor deck mentions AI. Every quarterly earnings call includes the phrase "AI-powered." Every product marketing page has at least one reference to machine learning.</p>

<p>Job postings tell a different story. They tell you which companies are actually committing budget to AI capabilities, and which are just borrowing the vocabulary. The gap between the two is enormous.</p>

<p>By analyzing job posting data across thousands of companies, clear patterns emerge about where enterprise AI adoption actually stands, not where press releases claim it stands.</p>

<h2>The Three Phases of Enterprise AI Hiring</h2>

<h3>Phase 1: The Exploration Hire (2022-2023)</h3>

<p>Companies hired their first "data scientist" or "ML researcher." Often a lone wolf role, reporting to engineering or product. The job descriptions were vague: "apply ML to our data" without specifying what problem to solve. Many of these hires churned within 18 months because the company didn't have the infrastructure to support them.</p>

<h3>Phase 2: The Infrastructure Build (2024-2025)</h3>

<p>The smart companies figured out that ML models are useless without ML infrastructure. Postings shifted toward "ML Platform Engineer," "MLOps Engineer," and "Data Infrastructure Engineer." This was the unsexy but necessary phase: building the pipes before turning on the water.</p>

<h3>Phase 3: The Production Push (2026-Present)</h3>

<p>Now the postings are getting specific. "LLM Fine-Tuning Engineer." "AI Product Manager, Customer-Facing Features." "ML Engineer, Recommendation Systems." These aren't exploration hires. They're production hires with defined scope and measurable outcomes.</p>

<p>Where a company falls on this phase timeline tells you how far ahead or behind they are on AI. If they're still posting generalist "Data Scientist" roles with vague descriptions, they're in Phase 1. If they're posting for AI product managers, they've reached Phase 3.</p>

<h2>What the Job Requirements Reveal</h2>

<p>The specific technologies and skills listed in AI job postings track the market's evolution in real time.</p>

<h3>Technologies Growing Fast in 2026 Postings</h3>

<ul>
<li><strong>LangChain, LlamaIndex, vector databases (Pinecone, Weaviate):</strong> RAG (retrieval-augmented generation) is the dominant architecture for enterprise LLM applications. Companies hiring for these skills are building AI features, not running experiments.</li>
<li><strong>Fine-tuning frameworks (LoRA, QLoRA, PEFT):</strong> Signals that companies are moving past generic foundation models to domain-specific ones. This is expensive and only worth doing if the use case is validated.</li>
<li><strong>ML monitoring tools (Arize, WhyLabs, Evidently):</strong> These appear when models are in production and need reliability. Seeing these in postings means the company is past experimentation.</li>
<li><strong>Edge AI frameworks (TensorRT, ONNX Runtime):</strong> On-device inference. Shows up in hardware, automotive, and IoT companies building real-time AI features.</li>
</ul>

<h3>Technologies Declining or Plateauing</h3>

<ul>
<li><strong>Generic "Python, SQL, Tableau" data science postings:</strong> These are being replaced by more specific AI engineering roles. The generalist data scientist is giving way to the specialist.</li>
<li><strong>Hadoop, Spark-only data infrastructure:</strong> Being replaced by modern stack (Snowflake/Databricks + dbt + Airflow). Companies still hiring for legacy data infra are behind.</li>
</ul>

<h2>Salary Data: The AI Premium Is Real but Narrowing</h2>

<p>Job posting salary data from pay transparency states tells a clear story about AI compensation in 2026:</p>

<ul>
<li><strong>Senior ML Engineer:</strong> $200K-$280K base at mid-to-large tech companies. Up ~8% from 2025.</li>
<li><strong>LLM/NLP Specialist:</strong> $220K-$320K base. The scarcity premium for LLM expertise remains significant.</li>
<li><strong>AI Product Manager:</strong> $180K-$250K base. A relatively new category commanding a 10-15% premium over general PM roles.</li>
<li><strong>ML Infrastructure/MLOps:</strong> $190K-$260K base. The unsung heroes of AI are finally getting paid like it.</li>
<li><strong>Junior ML Engineer / Data Scientist:</strong> $110K-$150K base. Flat or declining as the supply of entry-level AI talent grows faster than demand.</li>
</ul>

<p>The bifurcation is the story. Specialist AI roles (LLM fine-tuning, ML infrastructure, AI safety) continue to command large premiums. Generalist ML roles are becoming commoditized as bootcamps and university programs flood the market with entry-level talent. The <a href="https://www.bls.gov/ooh/computer-and-information-technology/home.htm" target="_blank" rel="noopener">Bureau of Labor Statistics</a> projects strong growth for AI-adjacent roles through 2030.</p>

<h2>Industry Breakdowns: Who's Hiring and Who's Bluffing</h2>

<h3>Financial Services: The Biggest Spender</h3>

<p>Banks and hedge funds have the largest AI hiring volumes, driven by fraud detection, algorithmic trading, and risk modeling. JPMorgan, Goldman Sachs, and Citadel consistently rank among the top AI employers. They pay the most and hire the most. If you're competing with financial services for AI talent, prepare to lose on comp.</p>

<h3>Enterprise SaaS: The Fastest Mover</h3>

<p>SaaS companies are integrating AI into their core products at a pace that exceeds every other sector. The postings are specific: "ML Engineer, Document Understanding" at a legal tech company, "AI Engineer, Revenue Forecasting" at a CRM company. These are product hires, not research hires.</p>

<h3>Healthcare: Cautious but Growing</h3>

<p>Healthcare AI hiring is constrained by regulatory requirements (HIPAA, FDA clearance for clinical AI). The postings reflect this: heavy emphasis on compliance, explainability, and validation. Slower to hire but, once committed, these companies build durable AI capabilities.</p>

<h3>Manufacturing and Logistics: The Sleeper</h3>

<p>Predictive maintenance, quality inspection, route optimization. These aren't glamorous applications, but they deliver clear ROI. Companies in these sectors are hiring AI engineers and often struggling to attract talent because candidates don't see manufacturing as a "tech" employer.</p>

<h2>What This Means for Competitive Intelligence</h2>

<p>If your competitor just posted 5 AI engineering roles and they had zero a year ago, that's a signal. Here's what to do with it:</p>

<ol>
<li><strong>Map the roles to the phase framework.</strong> Are these exploration hires, infrastructure hires, or production hires? The answer tells you their timeline to market.</li>
<li><strong>Check the comp.</strong> Are they paying above market? That signals urgency and competition for the same talent pool you're targeting.</li>
<li><strong>Note the technologies.</strong> RAG stack? Fine-tuning? Edge deployment? The tech requirements tell you what they're building.</li>
<li><strong>Track the leader.</strong> Did they hire an AI executive first, or are individual contributors coming before leadership? Bottom-up hiring (ICs first) suggests experimentation. Top-down hiring (leader first, then team) suggests committed strategy.</li>
</ol>

<p>Fieldwork tracks AI hiring signals across your competitor set in every <a href="/#reports">monthly report</a>. You get a clear picture of who's investing, what they're building, and how their AI team is evolving. <a href="/#demo">Request a demo</a> to see the data.</p>

<p>The AI hype cycle will cool eventually. The companies that survive it are the ones that hired for production, not press releases. Which kind is your competitor?</p>
""",
    },

    # ── Article 7 ──
    {
        "slug": "sales-leaders-use-hiring-data-win-deals",
        "title": "How Sales Leaders Use Hiring Data to Win Deals",
        "meta_title": "Sales Leaders Use Hiring Data to Win Deals | Fieldwork",
        "meta_description": "Sales leaders who track competitor hiring close more deals. Here's how hiring data informs territory defense, objection handling, and deal strategy.",
        "date": "2026-03-29",
        "category": "Sales Intelligence",
        "excerpt": "Your competitor just posted 12 AE roles in your best territory. What do you do? Sales leaders who track hiring data already know the answer.",
        "faqs": [
            {"q": "How can sales teams use competitor hiring data?", "a": "Sales teams use hiring data to anticipate competitor moves in specific territories, handle objections about competitor capabilities, time outreach to prospects, and identify accounts where competitors are pulling back investment."},
            {"q": "What hiring signals should sales leaders monitor?", "a": "Sales team expansion (new AE hires by region), product investment signals (engineering hires that indicate new features), customer success scaling (CS hires that indicate growing customer base), and leadership changes (new CRO or VP Sales)."},
            {"q": "How does hiring data help with deal strategy?", "a": "If a competitor is ramping their sales team in your territory, expect more aggressive pricing and outreach. If they're cutting, their existing customers are vulnerable. If they're hiring product roles in your space, prepare for feature parity arguments."},
            {"q": "Can hiring data tell you about a competitor's financial health?", "a": "Yes. Sustained hiring growth correlates with positive financial trajectory. Hiring freezes, layoffs, and unfilled senior roles often precede public announcements of financial difficulty. For private companies, hiring data is one of the few visible financial indicators."},
            {"q": "How often should sales teams review hiring intelligence?", "a": "Monthly is sufficient for strategic planning. Weekly alerts for high-priority competitors (large sales team additions, new office locations) help with tactical response. Fieldwork delivers monthly reports with the option to flag urgent changes."},
        ],
        "content": """
<h2>The Intelligence Gap in Most Sales Orgs</h2>

<p>Sales teams obsess over product comparisons. Feature matrices. Pricing sheets. Win/loss analysis. These are all backward-looking: they tell you what happened in deals that already closed.</p>

<p>What most sales orgs lack is a forward-looking competitive signal. Something that tells you what's about to happen in your market, your territory, and your deals before it happens. Hiring data is that signal.</p>

<p>When a competitor posts 12 new Account Executive roles concentrated in the Northeast, that's not HR housekeeping. That's a territory assault. You have 60-90 days before those AEs are ramped and calling on your accounts. The sales leaders who see this signal early adjust. The ones who don't get surprised.</p>

<h2>Four Ways Hiring Data Changes Sales Strategy</h2>

<h3>1. Territory Defense</h3>

<p>A competitor ramping sales headcount in your best region is the clearest competitive threat you can observe. Here's what that signal looks like in practice:</p>

<ul>
<li><strong>3-5 new AE postings in a region:</strong> They're testing the market. Increase your account coverage in that region now, before their reps are ramped.</li>
<li><strong>Regional Sales Manager or VP Sales posting in a new geo:</strong> They're committing to the market long-term. This isn't a test. Prioritize retention plays with your top accounts in the region.</li>
<li><strong>SE (Solutions Engineer) postings alongside AE postings:</strong> They're going after enterprise accounts. SMB-focused defense won't work. Elevate your enterprise selling motion.</li>
</ul>

<p>Action: share competitor hiring intelligence with regional sales leaders monthly. When a competitor ramps in their territory, they should increase touch frequency with top accounts and accelerate any stalled deals before new competition arrives.</p>

<h3>2. Objection Handling</h3>

<p>Some of the best sales objections are powered by hiring intelligence. Examples:</p>

<p><strong>Prospect says:</strong> "We're also looking at [Competitor X], they seem like they're investing heavily in [feature area]."</p>

<p><strong>With hiring data, you can respond:</strong> "I track their hiring data closely. They posted their first product manager for [feature area] three months ago and have two open engineering roles. They're about 12-18 months from shipping anything meaningful there. We've had a team on this for two years and already have [specific capability] in production. Let me show you."</p>

<p>This kind of response demonstrates market awareness that prospects rarely encounter. It positions you as someone who understands the competitive landscape at a level that earns trust.</p>

<p><strong>Another scenario. Prospect says:</strong> "We're worried about [Competitor X]'s long-term viability."</p>

<p><strong>With hiring data:</strong> "That's a fair concern. Their engineering team has grown 30% this year and they just hired a new CRO from [well-known company]. The investment signals are positive. But if you look at what they're building, it's mostly infrastructure catch-up, not new capabilities. Our roadmap is 18-24 months ahead."</p>

<p>Or conversely: "I'll be direct. They've reduced hiring by 40% this quarter and several senior engineers have left for [Company Y]. I can't tell you what that means for their financials, but I can tell you we're growing and shipping. Here's our most recent release notes."</p>

<h3>3. Deal Timing</h3>

<p>Hiring data helps you time your outreach to prospects, not just defend against competitors.</p>

<p>When a prospect company starts hiring for a function that your product supports, that's a buying signal. Examples:</p>

<ul>
<li><strong>Company posts first "Revenue Operations" role:</strong> They're building the function. They'll need RevOps tools in 3-6 months.</li>
<li><strong>Company posts multiple "Data Engineer" roles:</strong> Data infrastructure investment. They'll need data tools.</li>
<li><strong>Company posts "VP of Customer Success":</strong> They're formalizing post-sale. They'll need CS platform tooling.</li>
</ul>

<p>The hiring event tells you when to reach out. Not too early (they haven't started), not too late (they've already bought). The window between "first hire in function" and "function has a leader and a budget" is the sweet spot.</p>

<h3>4. Identifying Weakness</h3>

<p>When a competitor's hiring data shows contraction, that's an opportunity to go after their customers. Signals to watch:</p>

<ul>
<li><strong>Customer Success team shrinking:</strong> Their accounts are getting less attention. Reach out to their customers with a high-touch pitch.</li>
<li><strong>Engineering headcount declining while CS headcount grows:</strong> They're in firefighting mode. Product is stalling while they manage churn. Their customers are feeling the pain.</li>
<li><strong>Long-unfilled senior roles:</strong> A VP of Engineering posting open for 6+ months means internal dysfunction. Projects are delayed. Customers are affected.</li>
</ul>

<p>The <a href="https://www.gartner.com/en/sales" target="_blank" rel="noopener">Gartner sales research</a> increasingly emphasizes intelligence-driven selling. Hiring data is one of the most underused inputs in the sales intelligence stack.</p>

<h2>How to Operationalize Hiring Intel in Your Sales Org</h2>

<p>Intelligence that stays in a dashboard doesn't close deals. Here's how to make it actionable:</p>

<h3>Monthly Competitive Brief</h3>

<p>A one-page document for the sales team covering:</p>
<ul>
<li>Top 3 competitor hiring moves this month</li>
<li>Which territories are most affected</li>
<li>Recommended actions (defend, attack, time deals differently)</li>
</ul>

<p>This should take 15 minutes to read and directly impact next week's activity. <a href="/#reports">Fieldwork's monthly reports</a> include a sales-ready summary for exactly this purpose.</p>

<h3>Deal-Level Intelligence</h3>

<p>When a specific deal involves a competitor, pull the hiring data for that competitor. Include in your deal strategy: their current engineering investment in the product area, their sales team's size and trajectory in the region, and any leadership changes that might affect their ability to deliver.</p>

<h3>QBR Integration</h3>

<p>Add a competitive hiring data slide to your quarterly business reviews. Show the team how competitor investment has shifted. Use it to set strategic priorities for the next quarter: where to defend, where to attack, and where to differentiate.</p>

<h2>The ROI Case for Sales Hiring Intelligence</h2>

<p>Assume your average deal size is $50K ARR and you run 100 competitive deals per quarter. If hiring intelligence helps you win just 2 additional deals per quarter, that's $400K in annual incremental revenue from an intelligence investment that costs less than a single enterprise software seat.</p>

<p>Most sales leaders will invest $10K-$50K per rep in sales engagement tools, CRM seats, and training. An investment in competitive hiring intelligence costs a fraction of that and arms every rep with information their competitors' reps don't have.</p>

<p>What's your competitor's sales team doing right now? If you can't answer that question, you need to start watching. <a href="/#pricing">See Fieldwork pricing</a>.</p>
""",
    },

    # ── Article 8 ──
    {
        "slug": "talent-acquisition-analytics-metrics-that-matter",
        "title": "Talent Acquisition Analytics: Metrics That Matter",
        "meta_title": "TA Analytics: Metrics That Actually Matter | Fieldwork",
        "meta_description": "Most TA teams track the wrong metrics. Here are the talent acquisition analytics that drive hiring outcomes, with benchmarks from real job posting data.",
        "date": "2026-03-29",
        "category": "Talent Acquisition",
        "excerpt": "Time-to-fill is a vanity metric. Here are the talent acquisition analytics that predict hiring outcomes.",
        "faqs": [
            {"q": "What are the most important talent acquisition metrics?", "a": "Quality of hire (measured by performance and retention), competitive win rate (offers accepted vs. lost to competitors), source effectiveness (which channels produce the best hires), and comp competitiveness (how your offers compare to market). Time-to-fill and cost-per-hire matter less than most teams think."},
            {"q": "How do I benchmark my hiring against competitors?", "a": "Track competitor job posting volume and duration. If competitors fill similar roles faster (shorter posting duration), they may have a more efficient process or more competitive offers. Fieldwork provides competitor hiring velocity data to support this benchmarking."},
            {"q": "What does time-to-fill actually measure?", "a": "Time-to-fill measures your process speed, not your hiring effectiveness. A fast fill with a wrong hire costs more than a slow fill with the right one. Use time-to-fill as a process efficiency metric, not a success metric."},
            {"q": "How can I tell if my compensation is competitive?", "a": "Compare your offer ranges against active job postings for equivalent roles at your talent competitors. If candidates are declining offers, pull comp data for the companies they're choosing instead. Fieldwork provides this data across your competitor set."},
            {"q": "What metrics should a TA team present to the C-suite?", "a": "Focus on business impact metrics: revenue per employee, time to productivity for new hires, competitive offer win rate, and hiring pipeline velocity for revenue-critical roles. Executives care about business outcomes, not recruiting funnel metrics."},
        ],
        "content": """
<h2>The Metrics Most TA Teams Track (And Shouldn't)</h2>

<p>Open any talent acquisition dashboard and you'll find the same metrics: time-to-fill, cost-per-hire, applicants per opening, and offer acceptance rate. These are easy to measure. They look good in quarterly presentations. And most of them are a distraction from what actually matters.</p>

<p>Time-to-fill rewards speed over quality. Cost-per-hire penalizes investment in good sourcing. Applicants per opening measures your job board spend, not your hiring effectiveness. These metrics optimize for the process of hiring, not the outcome.</p>

<p>Here's what to measure instead.</p>

<h2>Tier 1: Outcome Metrics (What Leadership Cares About)</h2>

<h3>Quality of Hire</h3>

<p>This is the only metric that matters at a fundamental level, and it's the hardest to measure. Quality of hire tracks whether the people you hired perform well and stay.</p>

<p>Measurement approach: combine 90-day manager satisfaction scores, 6-month performance ratings, and 12-month retention. Weight them 20/40/40. A hire who gets great reviews but leaves in 9 months isn't a quality hire. A hire who takes 6 months to ramp but becomes a top performer at month 12 is.</p>

<p>Benchmark this by source (which channels produce the highest-quality hires?), by recruiter (who's consistently hiring top performers?), and by hiring manager (whose interviews predict performance best?).</p>

<h3>Competitive Win Rate</h3>

<p>Of the candidates who received your offer, how many accepted vs. chose a competitor? And which competitors are you losing to?</p>

<p>This metric is gold because it directly connects your hiring performance to the competitive landscape. If you're losing 40% of final-stage candidates to the same competitor, you have a specific, addressable problem. It might be comp. It might be brand. It might be interview experience. But you know exactly who you're losing to and can diagnose why.</p>

<p>Track by role, by competitor, and by region. You might win 80% of competitive offers for marketing roles but only 50% for engineering. That tells you where to invest.</p>

<h3>Revenue Impact per Hire</h3>

<p>For revenue-generating roles (sales, customer success), measure the revenue impact of each hire. What's the average ramp time to full productivity? What's the revenue per AE at month 6 vs. month 12? How does this compare to industry benchmarks?</p>

<p>For non-revenue roles, use a proxy: time to first meaningful contribution (first shipped feature, first closed project, first process improvement). This is subjective but useful when calibrated across hiring managers.</p>

<h2>Tier 2: Process Metrics (What TA Managers Need)</h2>

<h3>Pipeline Velocity by Stage</h3>

<p>Don't measure time-to-fill as a single number. Break it into stages: sourcing to screen, screen to interview, interview to offer, offer to accept, accept to start. Measure the conversion rate and cycle time at each stage.</p>

<p>This reveals where your bottlenecks are. If 80% of your time-to-fill is between "hiring manager interview" and "offer approval," the problem isn't recruiting. It's your internal approvals process. Fix the right thing.</p>

<h3>Source Effectiveness</h3>

<p>Not all channels are equal. Track by channel: employee referrals, inbound applications, recruiter sourced (LinkedIn/direct), job boards, agencies. For each, measure: volume, conversion rate through the funnel, quality of hire score, and cost.</p>

<p>The channel that produces the most applicants is almost never the channel that produces the best hires. Employee referrals consistently outperform every other source in quality and retention metrics. <a href="https://www.ere.net/articles" target="_blank" rel="noopener">ERE's recruiting research</a> has documented this pattern across industries.</p>

<h3>Comp Competitiveness Index</h3>

<p>Where do your offers sit relative to the market? Not based on last year's comp survey. Based on current job postings from your talent competitors.</p>

<p>Build a comp competitiveness index: for each benchmark role, calculate your midpoint vs. the market midpoint (derived from active job posting salary data). Express as a percentage: 100% = at market, 110% = 10% above, 90% = 10% below.</p>

<p>Track this monthly. When your index drops below 95% for a role, expect to see declining offer acceptance rates within 30-60 days. <a href="/#pricing">Fieldwork</a> provides the market comp data you need to calculate this index across your competitor set.</p>

<h2>Tier 3: Competitive Benchmarking Metrics</h2>

<h3>Competitor Hiring Velocity</h3>

<p>How fast are your talent competitors growing? If they're adding headcount at 2x your rate, you'll face increasing competition for candidates and potentially lose candidates to their momentum narrative.</p>

<p>Track monthly open roles for each talent competitor. Plot the trend. When a competitor accelerates, adjust your sourcing aggressiveness accordingly.</p>

<h3>Market Share of Talent</h3>

<p>In your key roles, what percentage of the available talent pool is flowing to you vs. competitors? This is hard to measure precisely but directionally useful. Track offer acceptance rates and candidate pipeline trends as proxies.</p>

<p>If you're seeing fewer qualified applicants per opening while competitors post more roles at higher comp, you're losing market share of talent. That's an early warning that needs executive attention.</p>

<h3>Posting Duration by Competitor</h3>

<p>How long do competitors keep postings active? A posting that disappears in 30 days was probably filled. One that stays up for 120 days is either a permanent pipeline role or an impossible-to-fill position. Track these patterns. If competitors consistently fill similar roles 20 days faster than you, they have a process or comp advantage worth investigating.</p>

<h2>Building Your TA Analytics Dashboard</h2>

<p>Start simple. Three metrics on a dashboard that you review weekly:</p>

<ol>
<li><strong>Pipeline velocity by stage:</strong> Where are things stuck right now?</li>
<li><strong>Offer acceptance rate (30-day rolling):</strong> Are we winning or losing candidates?</li>
<li><strong>Comp competitiveness index for top 5 roles:</strong> Are we paying enough?</li>
</ol>

<p>Add monthly reviews of:</p>
<ol>
<li><strong>Quality of hire scores for recent hires:</strong> Are we hiring well?</li>
<li><strong>Competitive win rate by competitor:</strong> Who's beating us and why?</li>
<li><strong>Competitor hiring velocity:</strong> What's changing in the market?</li>
</ol>

<p>Present to leadership quarterly with a focus on business impact: revenue per hire, competitive positioning, and talent market share trends. Skip the vanity metrics. Executives don't care about your applicant volume. They care about whether you're winning the talent war.</p>

<h2>The Metrics You're Missing Without Competitive Data</h2>

<p>Internal TA analytics tell you how well you're running your process. They don't tell you how you compare to the market. Without competitive data, you can't answer:</p>

<ul>
<li>Are we paying enough for this role?</li>
<li>Why did that candidate choose [Competitor X] over us?</li>
<li>Is our competitor about to flood this market with AEs?</li>
<li>How fast does the market typically fill this role?</li>
</ul>

<p>These are the questions that separate reactive TA teams from strategic ones. Internal metrics are necessary but insufficient. You need the market context to make the numbers meaningful.</p>

<p>Fieldwork's <a href="/#reports">monthly competitive reports</a> provide the external benchmarking data that most TA dashboards are missing. Pair internal analytics with competitive intelligence and you have a complete picture. <a href="/#demo">See how it works.</a></p>

<p>What's the one metric your TA team doesn't track today that would change how you operate if you did?</p>
""",
    },
]


# ═══════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def build_article_page(article):
    """Build a single article HTML page."""
    slug = article["slug"]
    url = f"{SITE_URL}/blog/{slug}/"
    out_dir = os.path.join(BLOG_DIR, slug)

    # Schemas
    crumbs = [
        {"label": "Home", "url": SITE_URL + "/"},
        {"label": "Blog", "url": SITE_URL + "/blog/"},
        {"label": article["title"], "url": url},
    ]
    bc_schema = breadcrumb_schema(crumbs)
    art_schema = article_schema(
        title=article["title"],
        description=article["meta_description"],
        url=url,
        date_published=article["date"],
    )
    faq_schema, faq_html = faq_schema_and_html(article["faqs"])

    schemas = [bc_schema, art_schema, faq_schema]

    # Head
    schema_json = json.dumps({"@context": "https://schema.org", "@graph": schemas}, indent=4)
    extra_head = f"""    <script type="application/ld+json">
{schema_json}
    </script>
{get_blog_css()}"""

    head = get_html_head(
        title=article["meta_title"],
        description=article["meta_description"],
        canonical_url=url,
        og_type="article",
        extra_head=extra_head,
    )

    # Body
    bc_html = breadcrumb_html(crumbs)
    body = f"""{get_nav_html()}

{bc_html}

<article>
    <header class="article-header">
        <div class="container" style="max-width: 720px; margin: 0 auto;">
            <div class="article-meta">
                <span class="fw-badge fw-badge--ember">{article["category"]}</span>
                <span class="fw-mono" style="color: var(--fw-text-muted); font-size: 12px;">{article["date"]}</span>
            </div>
            <h1 class="fw-h2">{article["title"]}</h1>
            <p class="fw-body-lg" style="color: var(--fw-text-muted); margin-top: 12px;">{article["excerpt"]}</p>
        </div>
    </header>

    <div class="article-content container">
{article["content"]}

{faq_html}

        <div class="cta-banner">
            <h3>Get Competitive Hiring Intelligence</h3>
            <p>Track what your competitors are hiring, paying, and signaling. Delivered monthly.</p>
            <a href="/#sample-report" class="fw-btn fw-btn--primary fw-btn--lg">Get a Free Sample Report</a>
        </div>
    </div>
</article>

{get_footer_html()}
{get_mobile_js()}"""

    page = f"""<!DOCTYPE html>
<html lang="en">
{head}
<body>
{body}
</body>
</html>"""

    write_page(os.path.join(out_dir, "index.html"), page)
    return url


def build_blog_index():
    """Build the blog index page."""
    url = f"{SITE_URL}/blog/"

    crumbs = [
        {"label": "Home", "url": SITE_URL + "/"},
        {"label": "Blog", "url": url},
    ]
    bc_schema = breadcrumb_schema(crumbs)
    schema_json = json.dumps({"@context": "https://schema.org", "@graph": [bc_schema]}, indent=4)

    extra_head = f"""    <script type="application/ld+json">
{schema_json}
    </script>
{get_blog_css()}"""

    head = get_html_head(
        title="Competitive Hiring Intelligence Blog | Fieldwork",
        description="Insights on competitive hiring intelligence, compensation benchmarking, talent acquisition analytics, and hiring signal analysis from Fieldwork.",
        canonical_url=url,
        og_type="website",
        extra_head=extra_head,
    )

    # Build article cards
    cards = ""
    for article in ARTICLES:
        article_url = f"/blog/{article['slug']}/"
        cards += f"""        <div class="blog-card">
            <div class="card-category">{article["category"]}</div>
            <h3><a href="{article_url}">{article["title"]}</a></h3>
            <p class="card-excerpt">{article["excerpt"]}</p>
            <div class="card-meta">{article["date"]}</div>
        </div>
"""

    bc_html = breadcrumb_html(crumbs)
    body = f"""{get_nav_html()}

{bc_html}

<section class="blog-hero">
    <div class="container">
        <span class="fw-label" style="margin-bottom: 16px; display: inline-block;">Fieldwork Blog</span>
        <h1 class="fw-h2">Competitive Hiring Intelligence</h1>
        <p class="fw-body-lg" style="color: var(--fw-text-muted); max-width: 600px; margin: 16px auto 0;">Insights on hiring signals, compensation benchmarking, and talent strategy from the Fieldwork team.</p>
    </div>
</section>

<section class="container">
    <div class="blog-grid">
{cards}    </div>
</section>

{get_footer_html()}
{get_mobile_js()}"""

    page = f"""<!DOCTYPE html>
<html lang="en">
{head}
<body>
{body}
</body>
</html>"""

    write_page(os.path.join(BLOG_DIR, "index.html"), page)


def update_sitemap(article_urls):
    """Update sitemap.xml with blog URLs."""
    sitemap_path = os.path.join(ROOT, "sitemap.xml")
    today = datetime.now().strftime("%Y-%m-%d")

    urls = []
    # Keep existing homepage entry
    urls.append(f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>""")

    # Blog index
    urls.append(f"""  <url>
    <loc>{SITE_URL}/blog/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    # Individual articles
    for url in article_urls:
        urls.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"  wrote: {sitemap_path}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print(f"Building Fieldwork blog ({len(ARTICLES)} articles)...")
    print()

    # Build articles
    article_urls = []
    for article in ARTICLES:
        print(f"  [{article['slug']}]")
        url = build_article_page(article)
        article_urls.append(url)

    # Build index
    print()
    print("  [blog index]")
    build_blog_index()

    # Update sitemap
    print()
    print("  [sitemap]")
    update_sitemap(article_urls)

    print()
    print(f"Done. {len(ARTICLES)} articles + index + sitemap.")


if __name__ == "__main__":
    main()
