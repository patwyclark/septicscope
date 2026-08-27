# SepticScope — Cloudflare Pages deployment

## Project settings
- Git repository: `patwyclark/septicscope`
- Production branch: `main`
- Framework preset: None
- Build command: `python build_site.py`
- Build output directory: `site`
- Root directory: repository root

Every push to `main` can rebuild and deploy after Git integration is enabled.

## Temporary domain
The generator defaults to `https://septicscope.pages.dev`. If Cloudflare assigns a different Pages URL, set production environment variable `SITE_BASE_URL=https://<actual-project>.pages.dev` and redeploy before indexing.

## Custom domain
After a final domain is registered, set `SITE_BASE_URL=https://<final-domain>`, attach that domain to the Pages project, and redeploy.

## AdSense
Do not add live AdSense code until approval. Reserved ad locations and an `ads.txt` placeholder are already included in generated output.
