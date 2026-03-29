"""HTML templates for Fieldwork blog build system."""

import json
import os
from nav_config import (
    SITE_NAME, SITE_URL, SITE_TAGLINE,
    NAV_ITEMS, NAV_CTA, FOOTER_LINKS, FOOTER_COPY,
)


def get_html_head(title, description, canonical_url, og_type="article", og_image=None, extra_head=""):
    """Generate <head> block with meta tags, fonts, CSS."""
    if og_image is None:
        og_image = f"{SITE_URL}/assets/logos/og-image.png"

    return f"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">

    <!-- Favicon -->
    <link rel="icon" href="/assets/favicons/favicon.svg" type="image/svg+xml">
    <link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">
    <link rel="icon" href="/assets/favicons/favicon-32.png" sizes="32x32" type="image/png">
    <link rel="icon" href="/assets/favicons/favicon-16.png" sizes="16x16" type="image/png">
    <link rel="apple-touch-icon" href="/assets/favicons/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">
    <meta name="theme-color" content="#14171C" media="(prefers-color-scheme: dark)">
    <meta name="theme-color" content="#F0EDE8" media="(prefers-color-scheme: light)">

    <!-- Open Graph -->
    <meta property="og:type" content="{og_type}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="en_US">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{og_image}">

    <!-- Fonts (non-blocking) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&display=swap" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&display=swap"></noscript>

    <!-- Brand CSS -->
    <link rel="stylesheet" href="/css/fieldwork.css?v=1">
{extra_head}
</head>"""


def get_blog_css():
    """Inline CSS for blog pages."""
    return """<style>
        /* ─── LAYOUT ─── */
        .container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
        a { color: var(--fw-primary); text-decoration: none; transition: color var(--fw-transition-fast); }
        a:hover { color: var(--fw-primary-hover); }
        .fw-btn.fw-btn--primary, .fw-btn.fw-btn--primary:hover { color: #fff; }
        html { scroll-behavior: smooth; }

        /* ─── HEADER ─── */
        .site-header {
            background: rgba(20, 23, 28, 0.95);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--fw-border);
            padding: 14px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo-link { text-decoration: none; color: var(--fw-text); }
        .nav-links { display: flex; gap: 28px; align-items: center; list-style: none; margin: 0; padding: 0; }
        .nav-links a {
            color: var(--fw-text-muted);
            font-size: var(--fw-text-sm);
            font-weight: 500;
            transition: color var(--fw-transition-fast);
        }
        .nav-links a:hover { color: var(--fw-text); }
        .mobile-toggle { display: none; background: none; border: none; color: var(--fw-text); font-size: 1.5rem; cursor: pointer; padding: 4px; }

        @media (max-width: 768px) {
            .nav-links { display: none; flex-direction: column; position: absolute; top: 100%; left: 0; right: 0; background: var(--fw-bg); border-bottom: 1px solid var(--fw-border); padding: 16px 24px; gap: 16px; }
            .nav-links.open { display: flex; }
            .mobile-toggle { display: block; }
        }

        /* ─── FOOTER ─── */
        .site-footer { border-top: 1px solid var(--fw-border); padding: 32px 0; }
        .footer-inner {
            display: flex; justify-content: space-between; align-items: center;
            font-size: var(--fw-text-sm); color: var(--fw-text-muted);
        }
        .footer-links { display: flex; gap: 24px; }
        .footer-links a { color: var(--fw-text-muted); font-size: var(--fw-text-sm); }
        .footer-links a:hover { color: var(--fw-text); }
        @media (max-width: 768px) { .footer-inner { flex-direction: column; gap: 16px; } }

        /* ─── BREADCRUMBS ─── */
        .breadcrumbs {
            padding: 16px 0;
            font-size: var(--fw-text-sm);
            color: var(--fw-text-muted);
        }
        .breadcrumbs a { color: var(--fw-text-muted); }
        .breadcrumbs a:hover { color: var(--fw-primary); }
        .breadcrumbs .sep { margin: 0 8px; opacity: 0.4; }

        /* ─── ARTICLE ─── */
        .article-header {
            padding: 48px 0 32px;
            border-bottom: 1px solid var(--fw-border);
            margin-bottom: 40px;
        }
        .article-meta {
            display: flex;
            gap: 16px;
            align-items: center;
            margin-bottom: 20px;
        }
        .article-content {
            max-width: 720px;
            margin: 0 auto;
            padding-bottom: 64px;
        }
        .article-content h2 {
            font-family: var(--fw-font-display);
            font-size: var(--fw-text-2xl);
            font-weight: 600;
            color: var(--fw-text-strong);
            letter-spacing: -0.5px;
            margin: 48px 0 16px;
            line-height: var(--fw-leading-snug);
        }
        .article-content h3 {
            font-family: var(--fw-font-display);
            font-size: var(--fw-text-xl);
            font-weight: 600;
            color: var(--fw-text-strong);
            margin: 36px 0 12px;
            line-height: var(--fw-leading-snug);
        }
        .article-content p {
            margin: 0 0 20px;
            line-height: var(--fw-leading-loose);
            color: var(--fw-text);
        }
        .article-content ul, .article-content ol {
            margin: 0 0 20px;
            padding-left: 24px;
            color: var(--fw-text);
        }
        .article-content li {
            margin-bottom: 8px;
            line-height: var(--fw-leading-normal);
        }
        .article-content blockquote {
            border-left: 3px solid var(--fw-primary);
            margin: 24px 0;
            padding: 16px 24px;
            background: var(--fw-primary-alpha-06);
            border-radius: 0 var(--fw-radius-md) var(--fw-radius-md) 0;
            color: var(--fw-text);
        }
        .article-content blockquote p { margin: 0; }
        .article-content strong { color: var(--fw-text-strong); }
        .article-content a { color: var(--fw-primary); text-decoration: underline; text-underline-offset: 2px; }
        .article-content a:hover { color: var(--fw-primary-hover); }

        /* ─── FAQ ─── */
        .faq-section {
            margin: 48px 0 32px;
            padding-top: 32px;
            border-top: 1px solid var(--fw-border);
        }
        .faq-item {
            margin-bottom: 24px;
        }
        .faq-item h3 {
            font-family: var(--fw-font-display);
            font-size: var(--fw-text-lg);
            font-weight: 600;
            color: var(--fw-text-strong);
            margin: 0 0 8px;
        }
        .faq-item p {
            margin: 0;
            color: var(--fw-text);
            line-height: var(--fw-leading-normal);
        }

        /* ─── CTA BANNER ─── */
        .cta-banner {
            background: var(--fw-surface);
            border: 1px solid var(--fw-border-accent);
            border-radius: var(--fw-radius-xl);
            padding: 40px;
            text-align: center;
            margin: 48px 0;
        }
        .cta-banner h3 {
            font-family: var(--fw-font-display);
            font-size: var(--fw-text-2xl);
            font-weight: 600;
            color: var(--fw-text-strong);
            margin: 0 0 12px;
        }
        .cta-banner p {
            color: var(--fw-text-muted);
            margin: 0 0 20px;
        }

        /* ─── BLOG INDEX ─── */
        .blog-hero {
            padding: 64px 0 40px;
            text-align: center;
            border-bottom: 1px solid var(--fw-border);
        }
        .blog-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 24px;
            padding: 48px 0;
        }
        .blog-card {
            background: var(--fw-surface);
            border: 1px solid var(--fw-border);
            border-radius: var(--fw-radius-xl);
            padding: 28px;
            transition: border-color var(--fw-transition-normal), box-shadow var(--fw-transition-normal);
            display: flex;
            flex-direction: column;
        }
        .blog-card:hover {
            border-color: var(--fw-border-accent);
            box-shadow: var(--fw-shadow-glow);
        }
        .blog-card a { text-decoration: none; }
        .blog-card .card-category {
            font-family: var(--fw-font-mono);
            font-size: 10px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--fw-primary);
            margin-bottom: 12px;
        }
        .blog-card h3 {
            font-family: var(--fw-font-display);
            font-size: var(--fw-text-xl);
            font-weight: 600;
            color: var(--fw-text-strong);
            margin: 0 0 10px;
            line-height: var(--fw-leading-snug);
        }
        .blog-card h3 a { color: var(--fw-text-strong); }
        .blog-card h3 a:hover { color: var(--fw-primary); }
        .blog-card .card-excerpt {
            color: var(--fw-text-muted);
            font-size: var(--fw-text-sm);
            line-height: var(--fw-leading-normal);
            margin-bottom: 16px;
            flex-grow: 1;
        }
        .blog-card .card-meta {
            font-family: var(--fw-font-mono);
            font-size: 11px;
            color: var(--fw-text-dim);
        }
    </style>"""


def get_nav_html():
    """Generate site header/nav matching existing Fieldwork nav."""
    links = ""
    for item in NAV_ITEMS:
        links += f'            <a href="{item["href"]}">{item["label"]}</a>\n'
    links += f'            <a href="{NAV_CTA["href"]}" class="{NAV_CTA["class"]}">{NAV_CTA["label"]}</a>'

    return f"""<header class="site-header">
    <div class="container header-inner">
        <a href="/" class="logo-link">
            <span class="fw-wordmark fw-wordmark--sm">fieldwork<span class="fw-dot"></span></span>
        </a>
        <nav class="nav-links" id="main-nav">
{links}
        </nav>
        <button class="mobile-toggle" id="mobile-toggle" aria-label="Toggle navigation">&#9776;</button>
    </div>
</header>"""


def get_footer_html():
    """Generate site footer matching existing Fieldwork footer."""
    links = ""
    for item in FOOTER_LINKS:
        ext = ' target="_blank" rel="noopener"' if item.get("external") else ""
        links += f'            <a href="{item["href"]}"{ext}>{item["label"]}</a>\n'

    return f"""<footer class="site-footer">
    <div class="container footer-inner">
        <span>{FOOTER_COPY}</span>
        <div class="footer-links">
{links}        </div>
    </div>
</footer>"""


def get_mobile_js():
    """Inline JS for mobile nav toggle."""
    return """<script>
    document.getElementById('mobile-toggle').addEventListener('click', function() {
        document.getElementById('main-nav').classList.toggle('open');
    });
    </script>"""


def breadcrumb_html(crumbs):
    """Generate breadcrumb nav HTML. crumbs = [{"label": ..., "url": ...}, ...]"""
    parts = []
    for i, crumb in enumerate(crumbs):
        if i < len(crumbs) - 1:
            parts.append(f'<a href="{crumb["url"]}">{crumb["label"]}</a>')
        else:
            parts.append(f'<span>{crumb["label"]}</span>')
    sep = '<span class="sep">/</span>'
    return f'<div class="breadcrumbs"><div class="container">{sep.join(parts)}</div></div>'


def breadcrumb_schema(crumbs):
    """Generate BreadcrumbList JSON-LD. crumbs = [{"label": ..., "url": ...}, ...]"""
    items = []
    for i, crumb in enumerate(crumbs):
        items.append({
            "@type": "ListItem",
            "position": i + 1,
            "name": crumb["label"],
            "item": crumb["url"],
        })
    return {
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def article_schema(title, description, url, date_published, date_modified=None, author="Fieldwork Team"):
    """Generate Article JSON-LD."""
    schema = {
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": url,
        "datePublished": date_published,
        "dateModified": date_modified or date_published,
        "author": {
            "@type": "Organization",
            "name": author,
            "url": SITE_URL,
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": SITE_URL,
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url,
        },
    }
    return schema


def faq_schema_and_html(faqs):
    """Generate FAQPage JSON-LD and FAQ HTML. faqs = [{"q": ..., "a": ...}, ...]"""
    # Schema
    schema = {
        "@type": "FAQPage",
        "mainEntity": [],
    }
    for faq in faqs:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"],
            },
        })

    # HTML
    html = '<div class="faq-section">\n<h2>Frequently Asked Questions</h2>\n'
    for faq in faqs:
        html += f'<div class="faq-item">\n<h3>{faq["q"]}</h3>\n<p>{faq["a"]}</p>\n</div>\n'
    html += '</div>'

    return schema, html


def get_page_wrapper(head_content, body_content, schemas=None):
    """Assemble full HTML page."""
    schema_block = ""
    if schemas:
        graph = {"@context": "https://schema.org", "@graph": schemas}
        schema_block = f'\n    <script type="application/ld+json">\n{json.dumps(graph, indent=4)}\n    </script>'

    return f"""<!DOCTYPE html>
<html lang="en">
{head_content}
<body>
{body_content}
</body>
</html>"""


def write_page(filepath, content):
    """Write HTML content to file, creating directories as needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote: {filepath}")
