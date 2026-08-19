# Context for future sessions

This file exists so a new Claude Code session can get oriented on this repo
quickly, without re-deriving decisions that were already made deliberately.
Read this before making structural or stylistic changes.

## What this is

`nickmobus.github.io` — a personal project hub (GitHub Pages), meant to be
linked from a resume/LinkedIn. It replaced an earlier repo that was a single
machine learning class project. The owner (Nick Mobus) has limited web dev
experience, which is why the stack is deliberately simple.

- **No build step, no framework.** Plain HTML/CSS/JS throughout, on purpose —
  chosen specifically so it stays transparent to debug and easy to edit
  directly (by hand or by Claude) without a toolchain in the way.
- **Hosting:** GitHub Pages, serving straight from `main`.

## Site structure

- `index.html` — homepage. Renders a grid of project cards by fetching
  `projects.json` client-side (see `assets/js/main.js`). This means the
  homepage **cannot be previewed by double-clicking the file** — browsers
  block `fetch()` on `file://` URLs. Preview with `python -m http.server`
  from the repo root, or VS Code's Live Server extension.
- `assets/css/style.css` — homepage-only styles (the project pages below do
  *not* use this file — see "Project pages" below).
- `assets/js/main.js` — fetches `projects.json`, renders cards, escapes
  user-controlled fields (title/description/tags) before injecting HTML.
- `assets/img/og-banner.png` — 1200×630 Open Graph preview image (generated,
  see "Open Graph" below).
- `projects.json` — single source of truth for the homepage grid. Adding a
  project never requires touching `index.html`, CSS, or JS — see
  `HOW_TO_ADD_A_PROJECT.md` for the exact field format (internal vs.
  `external: true` projects, sorting by `date`, etc.).
- `projects/<slug>/` — one folder per internally-hosted project, each with
  its own self-contained `index.html` (see below).
- `MIGRATION.md` — historical notes from the original single-project → hub
  restructure. That migration is done; this file is now stale/reference-only
  and could be deleted, but hasn't been asked for.

## Design system (the "lab notebook" aesthetic)

Deliberately chosen to avoid both the generic cream+terracotta AI-template
look and the dark+neon-AI look. Paper background, deep teal accent, serif
headers, monospace for labels/tags/captions — meant to feel like a data/code
notebook, not a marketing site.

```css
--paper: #faf9f6;
--paper-raised: #ffffff;
--ink: #1b1f23;
--ink-soft: #5b6470;
--hairline: #dedbd2;
--accent: #2b6e63;
--accent-tint: #e4efec;
--accent-ink: #163f38;

--font-display: "Source Serif 4", Georgia, serif;   /* headings */
--font-body: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace; /* labels, tags, captions, code */

--radius: 3px;
--wrap: 880px;   /* max content width */
```

Fonts are pulled from Google Fonts (`Source+Serif+4`, `IBM+Plex+Sans`,
`IBM+Plex+Mono`) via a `<link>` in each page's `<head>` — same URL pattern
copy-pasted across `index.html` and every project page.

**Keep any new page/section consistent with this palette and type system**
unless explicitly told otherwise.

## Project pages are self-contained

Each `projects/<slug>/index.html` embeds its own `<style>` block with the
full token set above, duplicated rather than linked to
`assets/css/style.css`. This is intentional: it keeps each project folder
portable (works if copied out, doesn't depend on relative paths back to the
shared stylesheet) and matches the pattern already established by the first
project page before this became a convention. When adding a new project
page, copy the token block and component patterns from an existing project
page rather than inventing new styles.

### Shared page pattern (both existing project pages follow this)

- `<a class="back-link" href="../../index.html">← Back to all projects</a>`
  at the top.
- A `.report-header` with an `.eyebrow` (small mono label), an `<h1>` title,
  and a byline.
- A sticky tab nav (`.tabs`) that switches `<section>` visibility via a small
  inline `<script>` (no framework, no router). **Important:** the tab nav
  uses `display: flex; flex-wrap: wrap; justify-content: center;` — NOT
  `overflow-x: auto; white-space: nowrap;`. The nowrap/scroll version was the
  original approach and caused tabs to require horizontal scrolling once
  there were enough of them; it was replaced with wrapping on both project
  pages specifically to fix that. Don't reintroduce horizontal tab scrolling.
- Section content styled via plain element selectors (`section h2`,
  `section h3`, `section p`, `table`, `figure`, `figcaption`, `pre`) rather
  than utility classes, since the source content (especially
  ocean-acidification, ported from a raw student report) uses plain tags.

## Current projects

1. **`projects/ocean-acidification/`** — "Predicting Ocean Acidification
   from Atmospheric CO2." Solo ML-course project (clustering, PCA, Naive
   Bayes, Decision Trees, XGBoost regression on BATS oceanographic data +
   NOAA atmospheric CO2 data). Originally a plain, un-styled tabbed report
   with a dark/green generic theme; it was restyled into the lab-notebook
   design system in place, and its content was later edited for
   accuracy/clarity/typos — but the underlying numbers and images are real
   results from the author's own notebooks, not fabricated. One genuinely
   interesting, still-unresolved finding threads through several tabs: the
   data cleanly splits into two clusters before/after 2016 (via both
   clustering and PCA independently), hypothesized but not confirmed to be
   tied to a 2016 El Niño-linked CO2 spike. If you touch this project's
   Results/Conclusions, keep that thread intact — it's the most novel result
   in the write-up.
2. **`projects/neural-dynamic-systems/`** — "Applications of Neural Networks
   in Continuous and Dynamic Systems," a CSCI 5922 (Fundamentals of Neural
   Networks and Deep Learning) final project **co-authored with Sean
   Fitzgerald** — credit him if you touch the byline/description. Compares
   MLP/RNN/LSTM/Transformer/Neural ODE/Neural Jump ODE on recovering the
   latent dynamics of synthetic non-stationary Bernoulli processes. Includes
   a `toy_data/` subfolder (data-generation package + pre-generated JSON) and
   an `extra-figures/` subfolder (result plots not linked from the page,
   kept for reference at the owner's request — leave unlinked unless asked).

Both entries live in `projects.json`; see that file for the exact
title/description/tags/date wording currently in use.

## Open Graph / social preview

`index.html` has OG + Twitter Card meta tags pointing at
`assets/img/og-banner.png`. That image was generated (not hand-designed) via
a small Pillow script using Windows system fonts (`georgiab.ttf` for the
serif title, `consola.ttf` for mono text) to match the site's own palette —
if it ever needs regenerating (e.g. after a name/tagline change), redo it
the same way rather than sourcing a new image, to keep it consistent with
the on-page look. No favicon has been added yet.

## Working conventions established this session

- **Verify before writing "results" prose.** When editing project write-ups,
  check claims against the actual source notebook (`.ipynb`) output rather
  than trusting the original phrasing — a real transcription error was
  caught this way (the XGBoost tab misstated its own GridSearchCV top-5
  results; the correct numbers were pulled from `XGBoost_code.ipynb`'s saved
  cell output).
- **Preserve first-person-singular voice** ("I", "my") in project write-ups.
  Stray "we/our" phrasing has been normalized out where found; don't
  reintroduce it.
- **Local preview:** run `python -m http.server <port>` from the repo root
  and open `http://localhost:<port>/index.html` — needed because of the
  `fetch()` restriction noted above. Kill the server when done reviewing.
- **Commits:** the owner reviews changes locally before committing, and
  commits manually via VS Code's Source Control panel most of the time.
  Don't assume you should commit — ask, unless explicitly told to.
- **`replace_all` on large HTML files in this repo has been unreliable** in
  this environment (silently fails to find strings that definitely exist,
  even right after a fresh read). When a literal string needs replacing many
  times, prefer a small Python script (read file → `str.replace()` → write
  file) over the Edit tool's `replace_all` flag.

## Known outstanding items (not yet done, not currently blocking)

- No favicon.
- `MIGRATION.md` is stale/historical and could be deleted.
- `README.md` and `HOW_TO_ADD_A_PROJECT.md` are accurate as of this writing;
  re-check them if the project-adding workflow changes.