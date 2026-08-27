# SepticScope

SEO-focused septic rules and homeowner information website.

## Repository layout
- `build_site.py` — dependency-free static site generator
- `data/counties.json` — verified county source data
- `data/faqs.json` — national FAQ content
- `data/guides.json` — cornerstone guide content
- `site/` — generated output (created during builds; not committed)

## Build
```bash
python build_site.py
```

The build produces the complete static site in `site/`.

## Cloudflare Pages
- Production branch: `main`
- Framework preset: None
- Build command: `python build_site.py`
- Build output directory: `site`
- Root directory: repository root

Until a custom domain is registered, the generator defaults canonical URLs to `https://septicscope.pages.dev`. Set `SITE_BASE_URL` in Cloudflare Pages when the final production domain is known.
