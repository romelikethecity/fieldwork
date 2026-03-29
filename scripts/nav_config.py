"""Navigation and site configuration for Fieldwork blog build system."""

SITE_NAME = "Fieldwork"
SITE_URL = "https://runfieldwork.com"
SITE_TAGLINE = "Competitive Hiring Intelligence"
SITE_DESCRIPTION = "Track what your competitors are hiring, how much they're paying, and what it signals about their strategy."

NAV_ITEMS = [
    {"label": "Demo", "href": "/#demo"},
    {"label": "Reports", "href": "/#reports"},
    {"label": "Pricing", "href": "/#pricing"},
    {"label": "Blog", "href": "/blog/"},
]

NAV_CTA = {
    "label": "Get Free Sample",
    "href": "/#sample-report",
    "class": "fw-btn fw-btn--primary fw-btn--sm",
}

FOOTER_LINKS = [
    {"label": "Contact", "href": "mailto:hello@runfieldwork.com"},
    {"label": "Blog", "href": "/blog/"},
    {"label": "The CRO Report", "href": "https://thecroreport.com", "external": True},
    {"label": "AI Market Pulse", "href": "https://theaimarketpulse.com", "external": True},
]

FOOTER_COPY = "&copy; 2026 Fieldwork. A product of Pariter Media Inc."
