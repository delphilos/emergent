# Emergent Component Patterns

## Buttons

```html
<!-- Primary Button -->
<button class="btn-primary">Run Simulation</button>

<!-- Secondary Button -->
<button class="btn-secondary">View Documentation</button>

<!-- Outline Button -->
<button class="btn-outline">Learn More</button>
```

```css
.btn-base {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: var(--color-emerald);
  color: var(--color-white);
}
.btn-primary:hover {
  background: var(--color-emerald-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background: var(--color-blue);
  color: var(--color-white);
}
.btn-secondary:hover {
  background: var(--color-blue-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-outline {
  background: transparent;
  color: var(--color-black);
  border: 2px solid var(--color-gray-300);
}
.btn-outline:hover {
  border-color: var(--color-emerald);
  color: var(--color-emerald);
}
```

---

## Cards

```html
<div class="card">
  <h3 class="card-title">Agent Behavior</h3>
  <p class="card-description">
    Define rules and interactions for autonomous agents in your simulation.
  </p>
  <a href="#" class="card-link">Learn more →</a>
</div>
```

```css
.card {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-gray-200);
  transition: all 0.3s ease;
}
.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}

.card-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-black);
  margin-bottom: var(--space-sm);
}
.card-description {
  color: var(--color-gray-700);
  line-height: 1.6;
  margin-bottom: var(--space-md);
}
.card-link {
  color: var(--color-emerald);
  text-decoration: none;
  font-weight: 500;
}
.card-link:hover { color: var(--color-emerald-hover); }
```

---

## Code Blocks

```html
<pre class="code-block"><code class="language-python">class Agent:
    def __init__(self, x, y):
        self.position = (x, y)
        self.state = "active"
</code></pre>
```

```css
.code-block {
  background: var(--color-gray-900);
  color: var(--color-gray-100);
  font-family: var(--font-mono);
  font-size: 0.875rem;
  padding: var(--space-lg);
  border-radius: var(--radius-md);
  overflow-x: auto;
  border: 1px solid var(--color-gray-800);
}

/* Inline code */
:not(pre) > code {
  background: var(--color-gray-100);
  color: var(--color-purple);
  padding: 0.125rem 0.375rem;
  border-radius: var(--radius-sm);
  font-size: 0.875em;
  font-family: var(--font-mono);
}
```

Syntax highlighting colors:
- **Keywords**: `#8b5cf6` (purple)
- **Strings**: `#00d4aa` (emerald)
- **Functions**: `#667eea` (blue)
- **Comments**: `#737373` (gray-500)

---

## Navigation

```html
<nav class="nav-primary">
  <div class="nav-logo">
    <img src="emergent-logo.svg" alt="Emergent" class="nav-logo-img">
    <span class="nav-brand">Emergent</span>
  </div>
  <ul class="nav-links">
    <li><a href="#" class="nav-link">Documentation</a></li>
    <li><a href="#" class="nav-link">Examples</a></li>
    <li><a href="#" class="nav-link">Community</a></li>
    <li><a href="#" class="nav-link nav-link-cta">Get Started</a></li>
  </ul>
</nav>
```

```css
.nav-primary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md) var(--space-xl);
  background: var(--color-white);
  border-bottom: 1px solid var(--color-gray-200);
}
.nav-logo { display: flex; align-items: center; gap: var(--space-sm); }
.nav-logo-img { height: 40px; width: auto; }
.nav-brand {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-black);
}
.nav-links { display: flex; gap: var(--space-lg); list-style: none; margin: 0; padding: 0; }
.nav-link {
  font-family: var(--font-body);
  font-weight: 500;
  color: var(--color-gray-700);
  text-decoration: none;
  transition: color 0.2s ease;
}
.nav-link:hover { color: var(--color-emerald); }
.nav-link-cta {
  background: var(--color-emerald);
  color: var(--color-white) !important;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
}
.nav-link-cta:hover { background: var(--color-emerald-hover); }
```

---

## Hero Section

```html
<section class="hero">
  <h1 class="hero-title">Build Complex Systems from Simple Rules</h1>
  <p class="hero-subtitle">
    Emergent is an open-source framework for agent-based modeling,
    enabling researchers and developers to simulate emergent behavior.
  </p>
  <div class="hero-actions">
    <button class="btn-primary">Start Building</button>
    <button class="btn-outline">View Examples</button>
  </div>
</section>
```

```css
.hero {
  text-align: center;
  padding: var(--space-3xl) var(--space-xl);
  max-width: 1000px;
  margin: 0 auto;
}
.hero-title {
  font-family: var(--font-display);
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--color-black);
  margin-bottom: var(--space-lg);
}
.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  color: var(--color-gray-700);
  max-width: 700px;
  margin: 0 auto var(--space-2xl);
}
.hero-actions { display: flex; gap: var(--space-md); justify-content: center; }
```

---

## Accessibility

Always provide visible focus indicators:

```css
*:focus {
  outline: 2px solid var(--color-emerald);
  outline-offset: 2px;
}
```

WCAG contrast ratios:
- Deep Black on White: **20.6:1** (AAA)
- Emerald on Black: **9.2:1** (AA)
- Blue on Black: **6.8:1** (AA)
- Charcoal on White: **12.6:1** (AA)

---

## Framework Integrations

### React

```jsx
import './emergent-brand.css';

export const SimulationCard = ({ title, description, onStart }) => (
  <div className="card">
    <h3 className="card-title">{title}</h3>
    <p className="card-description">{description}</p>
    <button className="btn-primary" onClick={onStart}>Run Simulation</button>
  </div>
);
```

### Tailwind Config

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        'emerald': '#00d4aa',
        'digital-blue': '#667eea',
        'warning-orange': '#f59e0b',
        'comp-purple': '#8b5cf6',
        'deep-black': '#0a0a0a',
      },
    },
  },
}
```

### GitHub README Badges

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-00d4aa.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-667eea.svg)](https://www.python.org/)
```