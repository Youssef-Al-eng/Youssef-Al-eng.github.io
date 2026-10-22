# Premium Applied AI Engineering Portfolio — Design

**Status:** Approved direction: single-page static portfolio.
**Audience:** Research Master's supervisors, research collaborators, and engineering recruiters.
**Success:** A polished, accessible, responsive portfolio that communicates Youssef Alaa Abdelrady's applied AI work, links to all seven research repositories, and remains deployable by the existing GitHub Pages setup.

## Architecture

Keep the current GitHub Pages repository and its plain HTML, CSS, and JavaScript stack. Make `index.html` the complete portfolio with semantic sections and stable anchor IDs. Keep existing HTML routes as small, accessible entry pages that lead to the matching section on the homepage so saved links remain useful. Add `404.html`; do not add a framework, build system, backend, or runtime dependency.

Use `style.css` for the shared design system and responsive layout. Keep `nav.js` small: progressive enhancement for the mobile menu, project category filters, current year, and any anchor behavior. Core content and links remain present without JavaScript. Use a local SVG favicon and an inline SVG systems diagram; do not add remote fonts or heavy imagery. Keep the existing public GitHub avatar only where it adds value and provide a clear fallback.

## Information design

The homepage follows this sequence: hero and contact actions; technical expertise grouped by evidence-backed competencies; featured research with all seven exact repository links; short technical deep dives; selected applied work; research interests; education and verified professional experience; contact. Navigation uses anchors and a visible active state. Project filters are optional enhancement and default to showing every card.

Each research card names the problem, approach, verified technologies, and why the implementation is interesting. Include evaluation evidence only when the public README or source supports it, and label synthetic fixtures and prototype boundaries directly. Deep dives cover retrieval citations, risk-aware abstention, exact-record retention, domain adaptation with source retention, illumination-shift anomaly maps, English/Arabic layout retrieval, and durable workflow recovery. Applied-work entries use only details already stated in the public website/profile and link to the relevant repositories. The current public site and profile support the degree, four internships, technical skills, contact details, and selected applied projects. The only locally located CV is marked `DRAFT`; do not publish it or add a CV download. Do not add awards, leadership titles, metrics, publication claims, or employment details without a reliable public source.

## Visual direction

Use a dark ink base with high-contrast warm-white text, cool teal for links and interaction, and a small warm amber accent for status or emphasis. Pair an expressive display face available through a system stack with a legible sans-serif body stack. Give content generous spacing and a restrained editorial grid. The hero pairs a concise professional introduction with a lightweight SVG diagram showing a practical flow from data to model, evaluation, and deployment. Avoid gradients as decoration, floating shapes, fake terminal effects, testimonials, and progress bars.

Project cards use clear typographic hierarchy, compact tags, readable descriptions, evidence notes, and a direct GitHub action. Category filters use real buttons with keyboard behavior and a clear all-projects state. Motion is brief and optional; respect `prefers-reduced-motion`.

## Accessibility and technical requirements

Use landmarks, a skip link, correct heading order, descriptive link text, button labels, visible focus rings, and sufficient contrast. The mobile menu must work by keyboard and expose its expanded state. At narrow widths, cards become one column, navigation remains reachable, tap targets remain comfortable, and technical text avoids horizontal scrolling. Add page title, description, Open Graph metadata, theme color, favicon, and canonical URL. Keep every local link relative and every external link verified. Include a useful `404.html` that links home and to projects.

## Verification and release

Validate every local route, anchor, image, and external project URL. Check static HTML and links, inspect the production files, run the local site, and view desktop and mobile breakpoints. Confirm keyboard navigation, reduced-motion behavior, and mobile menu state. Preserve the current GitHub Pages deployment configuration and history. Commit the implementation in coherent commits, push to `main` without force, then confirm the Pages workflow/deployment and inspect the live site after deployment. Report only checks actually performed.

## Content provenance

Use repository READMEs and source for the seven research projects and their claim boundaries. Use the existing public profile and site for professional biography and applied-work statements. The CV found locally is marked as a draft; it is not a public download source. Do not add unverifiable awards, leadership, publications, degrees, endorsements, employment, or metrics.
