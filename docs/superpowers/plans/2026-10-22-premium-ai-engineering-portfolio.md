# Premium Applied AI Engineering Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the plain academic-style homepage with a premium, accessible, responsive single-page Applied AI Engineer portfolio while preserving GitHub Pages deployment and existing page URLs.

**Architecture:** Keep plain HTML, CSS, and vanilla JavaScript. Put all portfolio content and stable section anchors in `index.html`, keep older page URLs as accessible redirects to their corresponding anchors, and add `404.html` and local SVG branding. Add a dependency-free Python `unittest` check for required sections and repository links.

**Tech Stack:** HTML5, CSS, vanilla JavaScript, inline/local SVG, Python 3 standard library for checks; no runtime dependencies or build system.

**Spec:** `docs/superpowers/specs/2026-10-22-premium-ai-engineering-portfolio-design.md`

## Global Constraints

- Preserve the current GitHub Pages deployment method and Git history; never force-push.
- Use no framework, backend, or runtime dependency.
- Keep all core content and project links available without JavaScript.
- Use verified content from the public profile/site and seven project READMEs/source; do not publish the draft CV.
- Label synthetic data and prototype limits; do not add unverified credentials, awards, employment, publications, metrics, or endorsements.
- Support keyboard navigation, visible focus, semantic HTML, responsive mobile layout, and `prefers-reduced-motion`.
- Verify and preserve all seven exact GitHub repository URLs and professional contact links.

## Review Focus

- JavaScript disabled: all section content and project links remain visible; test the HTML source for every required section and URL.
- Unknown project filter value or JavaScript initialization failure: all projects stay visible by default; test the default filter state and manually exercise filter buttons.
- Small viewport and long project text: no horizontal overflow and navigation remains usable; inspect at 375px and 768px widths.
- Keyboard-only use: skip link, navigation toggle, filters, and links remain reachable with visible focus; manually verify in the browser.
- Reduced-motion preference: nonessential transitions are disabled; inspect the matching CSS media query and browser behavior.

---

### Task 1: Add static portfolio content checks

**Files:**
- Create: `tests/test_portfolio.py`

**Interfaces:**
- Produces: standard-library `unittest` checks for the required homepage IDs, seven exact repository links, key metadata, and absence of local absolute paths in published HTML/CSS/JS.

- [ ] Add failing tests named `test_required_sections_exist`, `test_all_seven_research_repositories_are_linked`, `test_homepage_metadata_and_favicon_exist`, and `test_published_sources_contain_no_local_absolute_paths`.
- [ ] Run `python -m unittest discover -s tests -v`; confirm failures identify the missing new portfolio structure.
- [ ] Keep the checks limited to standard-library HTML parsing and filesystem reads; add no package dependency.
- [ ] Commit as `test: define portfolio content and link requirements`.

### Task 2: Build the semantic single-page portfolio

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: the section and link assertions from `tests/test_portfolio.py`.
- Produces: stable IDs `home`, `expertise`, `projects`, `deep-dives`, `applied-work`, `interests`, `experience`, `education`, and `contact`; seven research cards with exact repository links; semantic page landmarks.

- [ ] Replace the academic-style homepage markup with a semantic page containing a skip link, header/navigation, `main`, the nine sections, and footer.
- [ ] Write the hero as “Applied AI Engineer,” include the full name and verified email, GitHub, and LinkedIn links; omit CV download because no publication-ready CV is available.
- [ ] Group evidence-backed skills without ratings; include only tools supported by the public profile/site or repositories.
- [ ] Add seven detailed project cards covering problem, approach, verified technologies, interesting engineering decision, and evidence/limitation notes where applicable; label synthetic experiments and prototypes.
- [ ] Add short project-grounded deep dives and selected applied-work entries drawn from the existing public profile/site; include the verified B.Eng. institution and four internships without inventing dates or awards.
- [ ] Add concise research interests and a professional contact section.
- [ ] Add inline SVG data-to-model-to-evaluation-to-deployment diagram with accessible title/description.
- [ ] Run the Task 1 tests and confirm they pass; commit as `feat: build applied AI engineering portfolio homepage`.

### Task 3: Establish the visual system and responsive layout

**Files:**
- Modify: `style.css`

**Interfaces:**
- Consumes: semantic classes and IDs from `index.html`.
- Produces: dark ink theme, high-contrast type, restrained teal/amber accents, responsive grid/cards, mobile navigation layout, visible focus, and reduced-motion support.

- [ ] Replace the light academic page styling with CSS custom properties for color, spacing, type scale, content width, borders, and shadows.
- [ ] Style hero, diagram, skill groups, project cards, deep dives, timeline, and contact with consistent editorial spacing and hierarchy.
- [ ] Add responsive layouts at 900px and 600px; verify cards collapse cleanly and text does not cause horizontal scrolling at 375px.
- [ ] Add `:focus-visible` treatment, contrast-conscious muted text, touch-sized controls, and `@media (prefers-reduced-motion: reduce)` rules.
- [ ] Run the static content tests and inspect desktop, tablet, and mobile browser screenshots; commit as `style: add responsive dark portfolio design system`.

### Task 4: Add accessible navigation and optional project filters

**Files:**
- Modify: `nav.js`
- Modify: `index.html`
- Test: `tests/test_portfolio.py`

**Interfaces:**
- Produces: menu button with `aria-expanded`, project filter buttons with category values, and a no-JavaScript default showing all project cards.

- [ ] Add a failing test named `test_navigation_and_project_filters_have_accessible_defaults` for toggle labeling/state, filter labels, and unhidden cards in source markup.
- [ ] Run the test and confirm it fails because the new controls are absent.
- [ ] Implement only progressive enhancement: toggle menu state, filter cards by category, keep “All” as default, close the menu after choosing a link, and update footer year.
- [ ] Run the full unittest suite; manually verify Enter/Space, Escape, focus visibility, filter state, and all-projects reset in browser.
- [ ] Commit as `feat: add accessible portfolio navigation and filters`.

### Task 5: Preserve legacy routes and add metadata/branding

**Files:**
- Modify: `about.html`, `projects.html`, `research.html`, `experience.html`, `education.html`, `contact.html`
- Create: `404.html`, `favicon.svg`
- Modify: `index.html`, `tests/test_portfolio.py`

**Interfaces:**
- Produces: legacy URLs that redirect to matching homepage anchors with a usable fallback link, a branded favicon, search/social metadata, and a useful not-found page.

- [ ] Add tests named `test_legacy_routes_point_to_matching_sections` and `test_not_found_page_has_recovery_links`.
- [ ] Run tests and confirm the legacy route and 404 assertions fail before implementation.
- [ ] Add lightweight meta-refresh plus visible fallback links on legacy pages: About→`#expertise`, Projects→`#projects`, Research→`#deep-dives`, Experience→`#experience`, Education→`#education`, Contact→`#contact`.
- [ ] Add title, description, canonical, Open Graph title/description/URL, theme color, and local favicon links; add `404.html` with home/projects recovery links.
- [ ] Run the full unittest suite and verify each legacy route and 404 page through the local server; commit as `feat: preserve legacy routes and add portfolio metadata`.

### Task 6: Verify, commit, push, and confirm GitHub Pages deployment

**Files:**
- Verify: all changed site files and generated static output; no new build output is required.

**Interfaces:**
- Consumes: completed static portfolio and tests.
- Produces: verified commit(s) on `main` and a confirmed live deployment at `https://youssef-al-eng.github.io/`.

- [ ] Run `python -m unittest discover -s tests -v`, `git diff --check`, local-link/anchor validation, and external link checks for all seven projects and professional contacts.
- [ ] Serve the static root locally and inspect the homepage and legacy routes at desktop (1440px), tablet (768px), and mobile (375px); test keyboard navigation and reduced motion.
- [ ] Inspect final Git diff and status; confirm no CV, transcript, secret, absolute local path, or unrelated user change is included.
- [ ] Commit any final fixes in a focused commit, push `main` without force, and inspect GitHub Pages workflow/deployment status.
- [ ] Open the live URL after deployment and verify hero, navigation, all seven cards, contact links, 404 page, and mobile layout; report actual results and blockers.
