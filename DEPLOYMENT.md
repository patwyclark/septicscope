# SepticScope production deployment

## Current production configuration

- Repository: `patwyclark/septicscope`
- Production branch: `main`
- Cloudflare Pages build command: `python build_site.py`
- Build output directory: `site`
- Canonical domain: `https://septicscope.com`
- Analytics: Google Analytics and Cloudflare Web Analytics
- Advertising: Google AdSense code and `ads.txt` are generated centrally
- Consent: Google-certified consent management is configured in AdSense

The production build command must remain a single `python build_site.py` invocation. That orchestrator is responsible for county expansions, all guides and tools, trust/privacy hardening, the provider-directory shell, keyword mapping, and national coverage inventories. GitHub Actions uses the same command.

## Deployment verification

Each build writes `/build-info.json` with the source commit SHA and final coverage totals. After the validation workflow succeeds, the production-smoke workflow polls the public site until Cloudflare serves that same SHA, then checks:

- Homepage
- National county directory
- Guides hub and recent guides
- FAQ hub
- Provider-directory route
- Sitemap
- Robots file
- National county total and quality gate

A change is not considered publicly deployed until the production-smoke workflow passes or the live endpoints are otherwise verified.

## Search and indexing safeguards

- Canonical URLs use `https://septicscope.com`.
- Verified county guides and state hubs are included in the sitemap.
- Unfinished county help pages remain useful but use `noindex,follow`.
- Thin ZIP pages must not be created. ZIP lookup requires a real many-to-many ZIP-to-county mapping.
- Redirects must be retained when public URLs change.

## Content deployment rules

1. Research authoritative sources.
2. Update structured source data or a reviewable expansion script.
3. Run `python build_site.py`.
4. Run `python site_inventory.py --check`, `python audit_site.py`, `python audit_site.py --external`, and `python adsense_audit.py`.
5. Review representative generated pages.
6. Commit and push to `main`.
7. Confirm the validation workflow.
8. Confirm the production-smoke workflow and public URLs.

Never report a county as verified or live solely because source code was committed.
