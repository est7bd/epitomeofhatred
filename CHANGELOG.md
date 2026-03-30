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
