# CHANGELOG

## 2025-03-30 — Duplicate Consolidation + Nav Update

### Deleted (11 duplicate posts → 243 total)
The following files were confirmed duplicates with 301 redirect stubs already in `_redirects`. Content was merged into the canonical posts listed in parentheses before deletion.

- `blog/trump-stole-inauguration-funds.html` → merged into `trump-inaugural-committee-fraud`
- `blog/covid-mismanagement-woodward.html` → merged into `covid-death-toll-minimized`
- `blog/mueller-report-obstruction.html` → merged into `trump-obstruction-mueller-10-instances`
- `blog/mueller-report-findings.html` → merged into `trump-obstruction-mueller-10-instances`
- `blog/charlottesville-response.html` → merged into `charlottesville-very-fine-people`
- `blog/lafayette-square-clearing.html` → merged into `lafayette-square-bible-photo`
- `blog/trump-attacked-judge-curiel-race.html` → merged into `trump-attacks-judges`
- `blog/ukraine-aid-freeze.html` → merged into `ukraine-extortion-first-impeachment`
- `blog/student-loan-borrower-protections.html` → merged into `student-loan-scam-schools-protected`
- `blog/trump-infrastructure-week-meme.html` → merged into `trump-promised-infrastructure-week`
- `blog/trump-suggested-inject-disinfectant.html` → merged into `covid-hydroxychloroquine-bleach`

### Updated: `blog/index.html`
- Removed 11 post-item entries corresponding to deleted duplicate files
- Post count: 253 → 242 entries

### Updated: `sitemap.xml`
- Removed 11 `<loc>` entries for deleted duplicate URLs

### Updated: `index.html` (root)
- Damage counter: 247 → 243
- "All posts" link count: 253 → 243

### Updated: `_header.html`
- Added `/contradictions` and `/people` to main nav

### Updated: `_footer.html`
- Added `/contradictions` and `/people` to footer nav

### `_redirects` (unchanged)
- All 11 duplicate 301 rules retained — external links to old URLs will continue to resolve correctly

## 2025-03-30 — Broken Link Repair + Count Correction

### Fixed: 15 files with broken internal links
Replaced stale slug references with canonical URLs across 15 files:
- `corruption.html`
- `blog/rose-garden-superspreader-covid.html`
- `blog/covid-hydroxychloroquine-bleach.html`
- `blog/rfk-hhs-cdc-gutting.html`
- `blog/opioid-crisis-declared-emergency-did-nothing.html`
- `blog/trump-puerto-rico-hurricane-maria.html`
- `blog/travel-ban-expanded.html`
- `blog/trump-classified-intel-russia-lavrov.html`
- `blog/firing-james-comey.html`
- `blog/mueller-russia-pardons-cronies.html`
- `blog/sessions-recusal-backlash.html`
- `blog/kushner-security-clearance.html`
- `blog/epa-rollback-regulations.html`
- `blog/betsy-devos-education-corruption.html`
- `blog/masks-politicized-covid.html`

### Fixed: `index.html` (root) hardcoded count
- Damage counter and posts link corrected: 243 → 242
- (242 = post-item entries in blog/index.html; blog/index.html itself is not self-referential)
- `post-count.js` dynamically syncs this at runtime, but static fallback now matches

## 2026-03-30 — Major Content + Feature Expansion

### Fixed: Bugs
- Sitemap: normalized 6 malformed compact `<url>` entries, removed stale `/blog/test` entry
- Sitemap: added 5 missing posts (`iran-war-escalation-civilian-cost`, `kash-patel-email-hacked-iran`, `riverside-bianco-ballot-seizure-2026`, `senate-funds-tsa-not-ice-2am`, `tsa-funding-wont-fix-lines-overnight`)
- `receipts.html`: fixed dead link `/blog/musk-doge-conflicts-interest` → `/blog/elon-musk-conflicts-doge-tesla-spacex`
- `blog/index.html`: added missing `data-date="2017-02-04"` to trump-attacks-judges entry

### Added: people.html — 5 new cards
- **Elon Musk** — DOGE, $290M donation, billions in conflicts, 92K jobs killed
- **Matt Gaetz** — Ethics report, sex with a minor finding, resigned before it dropped
- **Rudy Giuliani** — Ukraine scheme, "trial by combat," $148M defamation judgment, law license revoked
- **Ryan Zinke** — Bears Ears gutted, lied to investigators, referred to DOJ
- **Mike Pence** — Pressured to reject electors, mob chanted "hang Mike Pence," Secret Service texted families goodbye

### Added: contradictions.html — 6 new entries
- Pre-Existing Conditions (four years trying to kill the ACA)
- Too Busy to Golf (308 rounds, $144M taxpayer cost)
- Tax Returns ($750 paid in 2016–2017, fought release for years)
- Voting Rights (Georgia call, fake electors, Jan 6)
- Trade War Wins (tariffs are a tax, $28B farmer bailout)
- Transparency (visitor logs hidden, IGs fired, FOIA blocked)

### Added: timeline.html
- Full chronological view of all 242 posts, dynamically built from blog/index.html
- Filterable by era (pre-2017 through 2026) and full-text search
- Year headers, tag display, auto-hides empty year blocks

### Added: search.html
- Dedicated search page with full-text search across all 242 posts
- Topic filter buttons (14 topics)
- Highlighted excerpts with query term matching
- Supports `?q=` URL parameter for deep linking

### Updated: Nav + Sitemap
- `_header.html` and `_footer.html`: added `/timeline` and `/search`
- `sitemap.xml`: added timeline and search pages

## 2026-03-30 — Footer Rebuild + Date Corrections

### Fixed: Footer layout
- Completely rewrote footer HTML and CSS — old nested column structure was overriding flex-row on the links
- New structure: `.footer-top` (logo + horizontal nav row) above `.footer-bottom` (copyright)
- Logo left, all nav links horizontal and wrapping, copyright below
- Removed conflicting responsive overrides that were stacking links vertically
- Removed dead `.footer-left`, `.footer-bottom` (old), `.footer-links` CSS selectors

### Fixed: 78 placeholder dates corrected to actual event dates
- All `YYYY-01-01` placeholder dates replaced with the specific date the event occurred
- Display labels updated in blog/index.html (removed all "First Term Record" prefix labels)
- Date metadata updated inside individual post HTML files
- Examples: trans-military-ban → 2017-07-26, supreme-court-stolen-seat → 2016-02-13, steve-bannon-arrest → 2020-08-20, e-jean-carroll-verdict → 2023-05-09

## 2026-03-30 — Footer Layout Fix (Round 3)

### Fixed: Footer
- Rebuilt as true vertical stack: logo → nav links → copyright, all left-aligned
- Nav links separated by pipe dividers (border-right), not run together as a sentence
- Forced `color: var(--text-dim) !important` on all nav links to override global red `a` color
- Only `breaking` gets accent red via `.footer-breaking` class
- Copyright sits below the nav row, not floating right
