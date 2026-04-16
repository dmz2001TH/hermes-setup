---
name: algorithmic-art
description: Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work.
---

# Algorithmic Art

Algorithmic philosophies are computational aesthetic movements expressed through code. Output .md files (philosophy), .html files (interactive viewer), and .js files (generative algorithms).

## Process

1. **Algorithmic Philosophy Creation** (.md file) — Write a generative art manifesto
2. **Implementation** — Create p5.js generative art (.html with embedded algorithm)

## Algorithmic Philosophy

First, create an ALGORITHMIC PHILOSOPHY — a computational worldview to be expressed through code:

- **Name the movement** (1-2 words): "Organic Turbulence" / "Quantum Harmonics" / "Emergent Stillness"
- **Articulate the philosophy** (4-6 paragraphs)
- Focus on: computational processes, noise functions, particle behaviors, temporal evolution, parametric variation
- Emphasize craftsmanship — the algorithm should feel meticulously crafted
- Leave creative space for implementation choices

### Philosophy Examples

**"Organic Turbulence"** — Chaos constrained by natural law, order from disorder. Flow fields driven by layered Perlin noise, particles following vector forces.

**"Quantum Harmonics"** — Discrete entities exhibiting wave-like interference. Phase values evolve through sine waves, constructive/destructive interference creates patterns.

**"Recursive Whispers"** — Self-similarity across scales. Branching structures subdividing recursively, constrained by golden ratios.

**"Stochastic Crystallization"** — Random processes crystallizing into ordered structures. Circle packing, Voronoi tessellation, relaxation algorithms.

## P5.JS Implementation

### STEP 0: Read the template
**Read** `templates/viewer.html` as the starting point. Keep the sidebar structure, seed controls, and action buttons. Replace only the algorithm, parameters, and parameter UI controls.

### Technical Requirements

**Seeded Randomness (always):**
```javascript
let seed = 12345;
randomSeed(seed);
noiseSeed(seed);
```

**Parameter Structure:**
```javascript
let params = {
    seed: 12345,
    // Quantities, scales, probabilities, ratios, angles, thresholds
    // that emerge from YOUR algorithmic philosophy
};
```

**Canvas Setup:**
```javascript
function setup() {
    createCanvas(1200, 1200);
    // Initialize your system
}
function draw() {
    // Your generative algorithm
    // Can be static (noLoop) or animated
}
```

### Output Format
1. **Algorithmic Philosophy** — .md file explaining the generative aesthetic
2. **Single HTML Artifact** — Self-contained interactive generative art (start from templates/viewer.html)

The HTML artifact must be self-contained: p5.js from CDN, algorithm inline, parameter controls, seed navigation, download button — everything in one file.

### Interactive Features (Required)
- **Seed navigation**: Prev/Next/Random/Jump buttons
- **Parameter controls**: Sliders for numeric params, color pickers if needed
- **Actions**: Regenerate, Reset, Download PNG

## Creative Process
User request → Algorithmic philosophy → Implementation → Interactive artifact

## Resources
- `templates/viewer.html` — Starting point for all HTML artifacts (dark theme, sidebar controls)
- `templates/generator_template.js` — Reference for p5.js best practices
