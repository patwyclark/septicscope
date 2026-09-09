# SepticScope

SepticScope is a source-based U.S. septic information website for property owners, buyers, sellers, and people planning maintenance or repairs.

The project is in **quality-recovery mode** after an AdSense low-value-content rejection. The previous strategy emphasized county-page volume and scheduled automation. The current strategy deliberately does the opposite: fewer indexable pages, stronger local evidence, substantive national guides, transparent editorial standards, and no ads on unfinished or navigation-only pages.

## Public experience

- `/` — quality-first homepage with ZIP, city/state, county/state, browser-location, and county-FIPS lookup
- `/counties/` — searchable national index of all 3,144 U.S. counties and county-equivalents
- `/guides/` — only the long-form guides that pass the substantive-content and source gate
- `/faq/` — one comprehensive septic FAQ replacing thin, overlapping answer pages
- `/about/` — sourcing, automation, advertising, corrections, and publication-status standards
- `/privacy/` and `/contact/` — privacy and public correction routes

The background provider dataset is retained, but `/providers/` and `/septic-services-near-me/` remain noindex, ad-free, absent from the sitemap, and unpromoted until all 3,144 county-equivalents have at least one source-reviewed provider relationship.

## Quality-recovery policy

A generated county page is not automatically a published guide. The final build evaluates previously indexable county pages for:

- Substantive main content
- Multiple public sources
- At least one local or regional source
- Useful local process, contact, records, inspection, fee, code, or maintenance details
- Low dependence on wording repeated across other county pages
- No unfinished or unverified-language signals

Pages that do not pass are marked `noindex,follow`, stripped of AdSense code, removed from the sitemap, and excluded from public county-guide promotion. State hubs are navigation-only, noindex, and ad-free. The county lookup still retains all 3,144 FIPS records, but only quality-approved local guides are marked as published destinations.

The final build writes:

- `/data/adsense-quality-recovery.json`
- `/data/adsense-quality-recovery.txt`

These reports identify the approved and withheld county pages, evidence signals, retained guides, consolidated content, and focused sitemap size.

## What was retired

The following behavior is intentionally disabled:

- Scheduled hourly content changes
- Scheduled internal-link insertion
- Repository auto-commits from the hourly workflow
- Page-count minimums that forced weak county pages to remain indexable
- Thin standalone FAQ leaves
- Ads on noindex, trust, navigation, or unfinished pages
- State-completion workflows that treated every statewide template as a finished county guide

The former hourly workflow is now a manual research and audit workflow. It can inspect official provider sources and run the complete build, SEO, internal-link, indexing, external-source, and AdSense-quality suite without publishing changes automatically.

## Canonical production build

Run exactly:

```bash
python build_site.py
```

`build_site.py` is the single production orchestrator used by Cloudflare Pages and GitHub Actions. It runs the historical county generators, substantive guide builders, provider and lookup layers, the final quality-recovery gate, navigation cleanup, redirect-budget enforcement, inventory generation, and page-level SEO validation.

## Main repository components

- `build_site.py` — canonical production build
- `site_core_build.py` — preserved historical generator and county-expansion chain
- `quality_recovery.py` — final county, guide, FAQ, advertising, homepage, lookup, and sitemap quality gate
- `quality_recovery_finalize.py` — strengthens the FAQ/About resources and retires legacy Indiana routes
- `quality_recovery_navigation.py` — rebuilds guide and state navigation without withheld-page links
- `recovery_redirect_hygiene.py` — keeps Cloudflare Pages redirects within platform limits
- `homebuyer_guide_quality.py` — substantive homebuyer septic due-diligence guide
- `county_lookup_experience.py` — national ZIP, city/state, county/state, FIPS, and geolocation search
- `site_inventory.py` — post-recovery manifest, keyword map, source catalog, metrics, and deployment fingerprint
- `audit_site.py` — internal, external-link, canonical, sitemap, noindex, and AdSense-placement integrity
- `adsense_audit.py` — advertising, trust, content-similarity, and county-source checks
- `tools/indexing_hygiene.py` — robots, canonical, redirect, and sitemap audit
- `tools/seo_hourly_audit.py` — title, H1, description, canonical, keyword-intent, and anchor review
- `data/quality-baseline.json` — quality floors and maximum public-footprint thresholds
- `data/growth-links.json` — intentionally empty while scheduled link mutation is disabled
- `ADSENSE_RECOVERY.md` — diagnosis, release criteria, monitoring, and resubmission checklist

## Provider evidence standard

Provider research may use ordinary public search for discovery, but a search-result snippet is never publication evidence. A company-owned website or official directory must support the identity, public contact information, septic or onsite-wastewater services, and geographic relationship shown.

Ordinary records are not endorsements or rankings. SepticScope does not copy consumer reviews, manufacture ratings, infer countywide coverage from an office address, or present partial coverage as a guarantee for every property.

## Cloudflare Pages

- Repository: `patwyclark/septicscope`
- Production branch: `main`
- Build command: `python build_site.py`
- Build output directory: `site`
- Root directory: repository root
- Production domain: `https://septicscope.com`

The production workflow waits for the exact validated commit to reach Cloudflare, then confirms the quality-recovery report, county lookup, homepage, FAQ, About page, guide hub, approved/withheld county behavior, focused sitemap, service-directory gate, robots file, and ads.txt authorization.

## Release standard

A green build requires:

- All 3,144 county/FIPS lookup records remain available
- Only locally differentiated county pages remain indexable
- At least eight substantive national guides survive the quality gate
- One consolidated, source-based FAQ hub
- No AdSense code on noindex, trust, navigation, or unfinished pages
- No indexable page without a primary keyword, self-canonical, title, H1, and description
- No broken internal links or confirmed external 404/410 source links
- A focused sitemap below the source-controlled maximum
- No scheduled content mutation or repetitive growth-link automation
- Exact-commit production verification after deployment

See `ADSENSE_RECOVERY.md` for the operating plan after release.
