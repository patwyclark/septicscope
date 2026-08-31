# SepticScope — Cloudflare Pages configuration

## Project settings

- Git repository: `patwyclark/septicscope`
- Production branch: `main`
- Framework preset: None
- Build command: `python build_site.py`
- Build output directory: `site`
- Root directory: repository root
- Custom domain: `https://septicscope.com`

Do not duplicate guide-generator commands in Cloudflare. The root `build_site.py` is the canonical orchestrator and produces the same complete output validated by GitHub Actions.

## Deployment fingerprint

Cloudflare Pages provides the `CF_PAGES_COMMIT_SHA` environment variable. `site_inventory.py` records that SHA in `/build-info.json`. The GitHub Actions production-smoke workflow uses it to confirm that the live site matches the validated `main` commit.

## Canonical domain and temporary Pages URL

All indexable pages, sitemap entries and robots references must use `https://septicscope.com`. The `*.pages.dev` hostname is not a second canonical site and should redirect to the custom domain through the existing Cloudflare redirect configuration.

## Analytics, advertising and consent

- Cloudflare Web Analytics is enabled in the Pages project.
- Google Analytics measurement ID is injected by the build.
- Google AdSense code and the publisher's `ads.txt` record are generated centrally.
- Auto ads are removed from noindex, unfinished county, contact, privacy and error pages by the AdSense hardening pass.
- Google's certified consent-management message is managed in AdSense for applicable regions.

## Troubleshooting

When a production-smoke run fails:

1. Check the matching Cloudflare Pages deployment for the expected commit.
2. Review the Cloudflare build log for `python build_site.py`.
3. Compare `/build-info.json` with the expected GitHub SHA.
4. Do not work around a build failure by changing canonical domains or bypassing validation.
