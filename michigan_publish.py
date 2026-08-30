# Run the verified Michigan county expansion, then publish a curated Michigan hub and sitemap entries.
exec((ROOT / 'michigan_expansion.py').read_text(encoding='utf-8'), globals())

mi_counties=list(MI_COUNTIES.keys())
items=''.join(f'<li><a href="/counties/michigan/{slugify(c)}/">{html.escape(c)} County</a></li>' for c in sorted(mi_counties))
hub=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Michigan Septic Permit Guides by County | SepticScope</title><meta name="description" content="Official-source Michigan septic permit guides by county."><link rel="canonical" href="https://septicscope.com/counties/michigan/"><style>{COMMON_STYLE}</style>{ga_tag}{adsense_tag}</head><body><header><div class="nav"><a class="brand" href="/">SepticScope</a></div></header><main><p><a href="/counties/">← All county guides</a></p><h1>Michigan septic permits by county</h1><p>Michigan treats onsite wastewater management as a required local-health-department service. These guides cover counties where SepticScope verified the local permitting authority and substantive county procedures from current official sources.</p><div class="note">County sanitary codes and procedures differ. SepticScope is adding Michigan counties only when the local requirements can be supported from government sources.</div><h2>Verified county guides</h2><ul class="grid">{items}</ul></main><footer><div>© 2026 SepticScope</div></footer></body></html>'''
hubdir=OUTPUT/'counties'/'michigan'; hubdir.mkdir(parents=True,exist_ok=True); (hubdir/'index.html').write_text(hub,encoding='utf-8')

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    if '/counties/michigan/' not in text:
        promo=f'<section><h2>Michigan</h2><p><a href="/counties/michigan/">Browse {len(mi_counties)} verified Michigan county septic guides →</a></p></section>'
        text=text.replace('</main>',promo+'</main>',1) if '</main>' in text else text.replace('</body>',promo+'</body>',1)
        county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    urls=['https://septicscope.com/counties/michigan/']+[f'https://septicscope.com/counties/michigan/{slugify(c)}/' for c in mi_counties]
    entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in urls if u not in sm)
    if entries:
        sitemap.write_text(sm.replace('</urlset>',entries+'</urlset>'),encoding='utf-8')

for c in mi_counties:
    p=OUTPUT/'counties'/'michigan'/slugify(c)/'index.html'
    text=p.read_text(encoding='utf-8')
    if 'Official sources checked' not in text or 'Official sources' not in text:
        raise RuntimeError(f'Michigan verified guide regression: {c}')

# Continue to the separately researched Iowa batch.
exec((ROOT / 'iowa_expansion.py').read_text(encoding='utf-8'), globals())
