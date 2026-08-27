# SepticScope

SEO-focused septic rules and homeowner information website.

- Static production site: `site/`
- Structured source data: `data/`
- Generator: `build_site.py`
- Cloudflare instructions: `CLOUDFLARE.md`
- Deployment checklist: `DEPLOYMENT.md`

The site is generated with `python build_site.py`. For Cloudflare Pages, use build command `python build_site.py` and output directory `site`.

The production canonical URL can be set with the `SITE_BASE_URL` environment variable. Until a custom domain is confirmed, the generator defaults to `https://septicscope.pages.dev`.
