# SepticScope

SepticScope is a production static website for source-checked U.S. septic permitting information, county and county-equivalent lookup, homeowner education, and a developing local-service directory.

## Canonical production build

Run exactly:

```bash
python build_site.py
```

`build_site.py` is the single production orchestrator used by both Cloudflare Pages and GitHub Actions. It runs the preserved core generator, every registered county expansion, supplemental guides and tools, trust/privacy hardening, and the final national inventory. Do not add extra production-only build commands; that would allow CI and Cloudflare output to drift.

## Repository layout

- `build_site.py` — canonical production orchestrator
- `site_core_build.py` — preserved historical generator and county-expansion chain
- `*_expansion.py` — official-source county research batches
- `nationwide_county_lookup.py` — all 3,144 U.S. counties and county-equivalents, including useful noindex help pages for locations still under research
- `nationwide_data/` — compressed national county/county-equivalent source dataset
- `site_inventory.py` — national coverage manifest, keyword map, source catalog, provider inventory, quality summary and deployment fingerprint
- `data/providers.json` — source-controlled provider directory; only verified public business records belong here
- `data/quality-baseline.json` — regression guard for nationwide coverage and verified-guide count
- `audit_site.py` — internal, external-link and generated-site integrity checks
- `adsense_audit.py` — advertising, trust and county-source quality checks
- `site/` — generated output; created during builds and not committed

## Generated inventories

Every build publishes:

- `/build-info.json`
- `/data/national-coverage-manifest.json`
- `/data/keyword-map.json`
- `/data/source-catalog.json`
- `/data/provider-directory.json`
- `/data/project-audit-summary.json`
- `/data/project-audit-summary.txt`

A county is counted as verified only when its final page is indexable and contains both a permitting-authority section and visible official sources. Page existence alone is not verification.

## Cloudflare Pages

- Repository: `patwyclark/septicscope`
- Production branch: `main`
- Framework preset: None
- Build command: `python build_site.py`
- Build output directory: `site`
- Root directory: repository root
- Production domain: `https://septicscope.com`

Cloudflare Pages supplies `CF_PAGES_COMMIT_SHA`; the build records it in `/build-info.json`. A GitHub Actions production-smoke workflow waits for that SHA and confirms that the validated commit is actually live.

## Quality gates

On pushes and pull requests, GitHub Actions compiles Python sources, performs the complete production build, verifies national coverage and keyword manifests, scans internal and external links, and enforces AdSense/source-quality safeguards. A scheduled run repeats the audit daily.

County rules must come from authoritative government, public-health, code, or other recognized public sources. Do not infer regulations or mark a county verified without supporting sources.
