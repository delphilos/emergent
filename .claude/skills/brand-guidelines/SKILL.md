---
name: brand-guidelines
description: "Apply Emergent brand guidelines to web development in this repo. Use this skill whenever working on any UI, page, component, or visual element for the Emergent agent-based modeling framework — including docs pages, landing pages, dashboards, React/HTML/CSS components, or any styled interface. Don't guess at colors, fonts, or layout; always consult this skill to ensure correct typography (Space Grotesk, Inter, JetBrains Mono), colors (emerald #00d4aa primary accent), logo usage, and spacing are applied consistently. Trigger on any request involving design, styling, branding, UI, or visual appearance in this repo."
---

# Emergent Brand Guidelines

Emergent is an open-source framework for agent-based modeling. The visual language reflects the core principle that **complex patterns emerge from simple rules** — minimal, geometric, technically precise.

**Bundled assets (in this skill's directory):**
- `emergent-logo.svg` — Primary logo, use for SVG contexts (scalable, recommended)
- `emergent-logo-sm.png` — Rasterized logo for contexts that don't support SVG

---

## Logo

The logo is a bold "E" shape formed from offset horizontal bars within a circular border — individual elements creating a recognizable whole, mirroring emergence itself.

**Usage rules:**
- Maintain clear space equal to the circle border width on all sides
- Use on high-contrast backgrounds only (white, light gray, or deep black)
- Scale proportionally — never distort, rotate, or skew
- Minimum size: 40px height (digital) / 0.5 inches (print)
- Black logo on light backgrounds (`#ffffff`, `#f5f5f5`)
- White logo on dark backgrounds (`#0a0a0a`, `#1a1a1a`)
- Never add effects, shadows, gradients, or change the logo colors

---

## Typography

Three-font system — use each in its designated role:

| Font | Role | Weights |
|------|------|---------|
| **Space Grotesk** | Display, headings (H1–H4), nav, hero text | 400, 500, 600, 700 |
| **Inter** | Body text, UI labels, buttons, captions | 400, 500, 600 |
| **JetBrains Mono** | Code blocks, inline code, terminal, technical specs | 400, 500, 600 |

### Font Import

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

### Type Scale

```css
:root {
  --font-display: 'Space Grotesk', sans-serif;
  --font-body:    'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono:    'JetBrains Mono', 'Courier New', monospace;
}

body {
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.6;
  color: #1a1a1a;
}

h1, h2, h3, h4 {
  font-family: var(--font-display);
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

h1 { font-size: 3.5rem; }  /* 56px */
h2 { font-size: 2.5rem; }  /* 40px */
h3 { font-size: 1.75rem; } /* 28px */
h4 { font-size: 1.25rem; } /* 20px */

code, pre { font-family: var(--font-mono); font-size: 0.875rem; }
```

---

## Color System

### Core Palette

| Name | Hex | Usage |
|------|-----|-------|
| Deep Black | `#0a0a0a` | Primary text, dark backgrounds, logo |
| Dark Gray | `#1a1a1a` | Alt dark backgrounds, softer than black |
| Charcoal | `#333333` | Secondary text, captions |
| Medium Gray | `#d4d4d4` | Borders, dividers, disabled |
| Light Gray | `#f5f5f5` | Subtle backgrounds, code surfaces |
| Pure White | `#ffffff` | Main background, cards |

### Accent Colors

| Name | Hex | Hover | Role |
|------|-----|-------|------|
| **Emerald** (primary) | `#00d4aa` | `#00bf99` | Primary buttons, links, success, highlights |
| Digital Blue | `#667eea` | `#5568d3` | Secondary buttons, info, data viz |
| Warning Orange | `#f59e0b` | `#dc8b0a` | Warnings, CTAs, important notices |
| Comp Purple | `#8b5cf6` | `#7c3aed` | Premium features, advanced tools, inline code |

### CSS Variables

```css
:root {
  /* Neutrals */
  --color-black:    #0a0a0a;
  --color-white:    #ffffff;
  --color-gray-100: #f5f5f5;
  --color-gray-200: #e5e5e5;
  --color-gray-300: #d4d4d4;
  --color-gray-400: #a3a3a3;
  --color-gray-500: #737373;
  --color-gray-600: #525252;
  --color-gray-700: #333333;
  --color-gray-800: #262626;
  --color-gray-900: #1a1a1a;

  /* Accents */
  --color-emerald:       #00d4aa;
  --color-emerald-hover: #00bf99;
  --color-emerald-light: #33ddb8;
  --color-blue:          #667eea;
  --color-blue-hover:    #5568d3;
  --color-blue-light:    #8599ee;
  --color-orange:        #f59e0b;
  --color-orange-hover:  #dc8b0a;
  --color-purple:        #8b5cf6;
  --color-purple-hover:  #7c3aed;

  /* Semantic aliases */
  --color-primary: var(--color-emerald);
  --color-secondary: var(--color-blue);
  --color-success: var(--color-emerald);
  --color-warning: var(--color-orange);
  --color-info:    var(--color-blue);

  /* Spacing scale */
  --space-xs:  0.25rem;  /*  4px */
  --space-sm:  0.5rem;   /*  8px */
  --space-md:  1rem;     /* 16px */
  --space-lg:  1.5rem;   /* 24px */
  --space-xl:  2rem;     /* 32px */
  --space-2xl: 3rem;     /* 48px */
  --space-3xl: 4rem;     /* 64px */

  /* Border radius */
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-xl:   16px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
  --shadow-xl: 0 20px 25px rgba(0,0,0,0.15);
}
```

---

## Design Principles

1. **Emergence through simplicity** — Minimal geometric elements that combine into sophisticated interfaces. Resist adding decoration; let structure do the work.
2. **Technical precision** — Sharp edges, clean layouts, monospaced fonts for technical content. Reflect the mathematical nature of ABM.
3. **Open and accessible** — High contrast, generous whitespace, clear hierarchy. WCAG AA minimum, AAA where possible.
4. **Systematic thinking** — Consistent patterns across all components. Every element serves a purpose; nothing is purely decorative.

---

## Component Patterns

For detailed HTML/CSS patterns for buttons, cards, code blocks, navigation, hero sections, React components, and Tailwind config, read:

→ `references/components.md`

---

## Implementation Checklist

When building any Emergent-branded UI:

- [ ] Import Space Grotesk, Inter, and JetBrains Mono from Google Fonts
- [ ] Set up CSS variables (neutrals + accents + spacing + radius + shadows)
- [ ] Use the bundled SVG logo in the header (min 40px height)
- [ ] Space Grotesk for all headings; Inter for body; JetBrains Mono for code
- [ ] Emerald `#00d4aa` for primary actions and interactive highlights
- [ ] Color contrast meets WCAG AA (4.5:1+) — see `references/components.md` for verified pairs
- [ ] Focus states use `outline: 2px solid var(--color-emerald); outline-offset: 2px`
- [ ] Code blocks: JetBrains Mono on dark gray `#1a1a1a` background
- [ ] Generous spacing — 16px+ between elements, use the spacing scale
- [ ] Test logo on both light and dark backgrounds