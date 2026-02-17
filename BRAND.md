# Fieldwork Brand System

**Palette:** Slate Ember · **Logo:** Direction B (The Data Point)  
**Domain:** runfieldwork.com

---

## Quick Start

1. Copy the `css/`, `logos/`, and `favicons/` folders into your project's public/static directory
2. Paste the contents of `head.html` into your HTML `<head>`
3. Use `brand.config.json` as the structured reference for colors, fonts, and asset paths
4. If using Tailwind, merge `css/tailwind.config.js` into your config

---

## Color System

### Dark Mode (Primary)

| Token | Hex | Usage |
|-------|-----|-------|
| Background | `#14171C` | Page background |
| Surface | `#1C2028` | Cards, panels, modals |
| Surface Raised | `#222832` | Hover states on surface, dropdowns |
| Primary (Ember) | `#E07850` | CTAs, links, highlights, accent elements |
| Primary Hover | `#E8895F` | Button hover state |
| Primary Active | `#D06840` | Button pressed state |
| Secondary (Teal) | `#5B9EA6` | Chart data, secondary badges, info states |
| Text | `#DDE0E6` | Body text |
| Text Strong | `#FFFFFF` | Headings, metrics, emphasis |
| Text Muted | `#7C8290` | Captions, descriptions, secondary text |
| Text Dim | `#4A4F5A` | Disabled text, subtle borders, placeholder |

### Light Mode (Emails, OG images, light sections)

| Token | Hex | Usage |
|-------|-----|-------|
| Background | `#F0EDE8` | Page background |
| Surface | `#FFFFFF` | Cards |
| Primary | `#D0683E` | Deeper ember for contrast on white |
| Text | `#1A1D24` | Body text |
| Text Muted | `#6B7080` | Secondary text |

### Semantic Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Success | `#6DC98C` | Positive changes, growth signals |
| Warning | `#E0A850` | Caution states |
| Danger | `#E07850` | Negative changes, contraction signals (same as primary) |
| Info | `#5B9EA6` | Informational (same as secondary) |

### Border Tokens

- Default: `rgba(255, 255, 255, 0.06)` — card edges, dividers
- Accent: `rgba(224, 120, 80, 0.15)` — hover states, accent borders
- Strong: `rgba(255, 255, 255, 0.12)` — button outlines, active states

### Alpha Fills

- Primary @ 12%: `rgba(224, 120, 80, 0.12)` — badge backgrounds, subtle highlights
- Primary @ 6%: `rgba(224, 120, 80, 0.06)` — table row hover, very subtle fills
- Secondary @ 12%: `rgba(91, 158, 166, 0.12)` — teal badge backgrounds

---

## Typography

### Font Stack

| Role | Family | Weights | Usage |
|------|--------|---------|-------|
| Display | **Sora** | 300–800 | Headings, wordmark, metrics, hero text |
| Body | **DM Sans** | 300–700 + italic | Paragraphs, UI text, descriptions |
| Mono | **IBM Plex Mono** | 400–600 + italic | Labels, badges, data values, code |

### Type Scale

| Name | Size | Used For |
|------|------|----------|
| xs | 12px | Fine print, timestamps |
| sm | 13px | Body small, table cells, buttons |
| base | 15px | Default body text |
| lg | 17px | Lead paragraphs, intro text |
| xl | 20px | H5, section subheads |
| 2xl | 24px | H4 |
| 3xl | 32px | H3 |
| 4xl | 40px | H2, page titles |
| 5xl | 48px | H1, hero headlines |

### Label Pattern

The distinctive Fieldwork label style uses IBM Plex Mono:
```
font-family: 'IBM Plex Mono';
font-size: 10px;
font-weight: 500;
letter-spacing: 2px;
text-transform: uppercase;
color: #E07850;
```

---

## Wordmark

### Construction

- **Font:** Sora Medium (weight 500)
- **Tracking:** -1px (tight)
- **Case:** All lowercase — `fieldwork`
- **Period:** Replaced with a **rounded square** (the "data point")
  - Border radius: 2.5px
  - Color: `#E07850` on dark, `#D0683E` on light
  - Size: ~22% of the wordmark's cap height
  - Position: baseline-aligned, 1px left margin

### HTML Usage

```html
<span class="fw-wordmark fw-wordmark--lg">
  fieldwork<span class="fw-dot"></span>
</span>
```

Size variants: `--xl` (48px), `--lg` (36px), `--md` (24px), `--sm` (18px), `--xs` (14px)

Background variants: default (dark bg), `--light` (light bg), `--white` (colored bg)

### SVG Logos

- `logos/fieldwork-wordmark-dark.svg` — for dark backgrounds
- `logos/fieldwork-wordmark-light.svg` — for light backgrounds
- `logos/fieldwork-wordmark-white.svg` — for colored backgrounds
- `logos/fieldwork-logo-dark-bg.png` — PNG fallback, dark bg
- `logos/fieldwork-logo-light-bg.png` — PNG fallback, light bg

---

## Companion Mark: Dot Grid

A 3×3 grid of rounded squares. Center dot is ember (the signal), bottom-right is teal (secondary data), rest are dim.

- `logos/fieldwork-grid-mark.svg` — dark variant
- `logos/fieldwork-grid-mark-light.svg` — light variant
- `logos/fieldwork-grid-mark-256.png` — large PNG

---

## Favicons

### Primary Set (dark bg, ember F)

| File | Size | Purpose |
|------|------|---------|
| `favicon.svg` | Scalable | Modern browsers |
| `favicon.ico` | 16/32/48 | Legacy browsers |
| `favicon-16.png` | 16×16 | Browser tab |
| `favicon-32.png` | 32×32 | Browser tab (retina) |
| `favicon-48.png` | 48×48 | Windows taskbar |
| `icon-192.png` | 192×192 | Android manifest |
| `icon-512.png` | 512×512 | Android splash |
| `apple-touch-icon.png` | 180×180 | iOS home screen |

### Brand Set (ember bg, dark F)

Same sizes with `brand-` prefix. Use when the dark-bg version doesn't stand out (e.g., dark OS themes).

---

## OG Image

- `logos/og-image.png` — 1200×630px
- Dark background with wordmark, tagline, and dot-grid decoration
- Use for `og:image` and `twitter:image` meta tags

---

## Component Patterns

### Badges
```html
<span class="fw-badge fw-badge--ember">Hiring Volume</span>
<span class="fw-badge fw-badge--teal">Comp Benchmark</span>
<span class="fw-badge fw-badge--success">Growth</span>
<span class="fw-badge fw-badge--neutral">Steady</span>
```

### Buttons
```html
<button class="fw-btn fw-btn--primary fw-btn--lg">Get a Report</button>
<button class="fw-btn fw-btn--ghost">Log In</button>
<button class="fw-btn fw-btn--outline-primary">Compare Peers →</button>
```

### Cards
```html
<div class="fw-card">
  <span class="fw-badge fw-badge--ember">Signal</span>
  <h3 class="fw-h4">+34% engineering headcount</h3>
  <p class="fw-body-sm">Description text here...</p>
</div>
```

---

## File Structure

```
fieldwork-brand/
├── brand.config.json        ← Structured reference (colors, fonts, paths)
├── BRAND.md                 ← This file
├── head.html                ← Drop-in <head> snippet
├── site.webmanifest         ← PWA manifest
├── css/
│   ├── fieldwork.css        ← Full design system CSS
│   └── tailwind.config.js   ← Tailwind tokens (merge into your config)
├── logos/
│   ├── fieldwork-wordmark-dark.svg
│   ├── fieldwork-wordmark-light.svg
│   ├── fieldwork-wordmark-white.svg
│   ├── fieldwork-logo-dark-bg.png
│   ├── fieldwork-logo-light-bg.png
│   ├── fieldwork-grid-mark.svg
│   ├── fieldwork-grid-mark-light.svg
│   ├── fieldwork-grid-mark-256.png
│   └── og-image.png
├── favicons/
│   ├── favicon.svg
│   ├── favicon.ico
│   ├── favicon-16.png
│   ├── favicon-32.png
│   ├── favicon-48.png
│   ├── icon-192.png
│   ├── icon-512.png
│   ├── apple-touch-icon.png
│   ├── favicon-brand-16.png
│   ├── favicon-brand-32.png
│   ├── favicon-brand-48.png
│   ├── icon-brand-192.png
│   └── icon-brand-512.png
└── docs/
    └── (this directory reserved for future brand guidelines)
```
