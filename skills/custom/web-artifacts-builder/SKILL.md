---
name: web-artifacts-builder
description: Suite of tools for creating elaborate, multi-component HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.
---

# Web Artifacts Builder

To build powerful frontend artifacts, follow these steps:
1. Initialize the frontend repo using `scripts/init-artifact.sh`
2. Develop your artifact by editing the generated code
3. Bundle all code into a single HTML file using `scripts/bundle-artifact.sh`
4. Display artifact to user

**Stack**: React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui

## Design & Style Guidelines

VERY IMPORTANT: To avoid "AI slop", avoid excessive centered layouts, purple gradients, uniform rounded corners, and Inter font. Prefer distinctive, intentional design choices.

## Quick Start

### Step 1: Initialize Project

Run the initialization script from this skill's scripts/ directory:
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

This creates a fully configured project with:
- React + TypeScript (via Vite)
- Tailwind CSS 3.4.1 with shadcn/ui theming system
- Path aliases (`@/`) configured
- `components.json` ready for shadcn CLI

### Step 2: Add shadcn/ui Components

After init, add components as needed:
```bash
pnpm dlx shadcn@latest add button card dialog input label select table tabs toast
```

Reference: https://ui.shadcn.com/docs/components

### Step 3: Develop Your Artifact

Edit the generated files. Common tasks:
- `src/App.tsx` — Main component
- `src/components/` — Your components
- `src/index.css` — Global styles & CSS variables

### Step 4: Bundle to Single HTML

From the project root:
```bash
bash bundle-artifact.sh
```

This creates `bundle.html` — a self-contained file with all JS, CSS, and dependencies inlined.

### Step 5: Share the Artifact

The bundled HTML file works in any browser. Save it or serve it as needed.

## Script Locations

- `scripts/init-artifact.sh` — Project initialization
- `scripts/bundle-artifact.sh` — Bundle to single HTML

## Reference

- shadcn/ui components: https://ui.shadcn.com/docs/components
- Vite: https://vitejs.dev
- Tailwind CSS: https://tailwindcss.com
