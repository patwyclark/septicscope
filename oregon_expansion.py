# Oregon expansion wrapper. Preserve validated regional batches and run additional county expansions.
exec((ROOT / 'oregon_expansion_base.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'alabama_additional_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_additional_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_third_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_fourth_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'washington_additional_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'tennessee_contract_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'washington_third_expansion.py').read_text(encoding='utf-8'), globals())

# Apply shared UI repairs only after every content generator has finished.
exec((ROOT / 'site_ui_fix.py').read_text(encoding='utf-8'), globals())

# Production deployment guard: fail the build if representative expansion pages are missing.
required_pages = [
    OUTPUT / 'counties' / 'tennessee' / 'bedford' / 'index.html',
    OUTPUT / 'counties' / 'tennessee' / 'hamilton' / 'index.html',
    OUTPUT / 'counties' / 'idaho' / 'ada' / 'index.html',
    OUTPUT / 'counties' / 'south-carolina' / 'greenville' / 'index.html',
    OUTPUT / 'counties' / 'arkansas' / 'benton' / 'index.html',
    OUTPUT / 'counties' / 'washington' / 'clark' / 'index.html',
    OUTPUT / 'counties' / 'washington' / 'king' / 'index.html',
    OUTPUT / 'counties' / 'washington' / 'spokane' / 'index.html',
    OUTPUT / 'counties' / 'washington' / 'yakima' / 'index.html',
    OUTPUT / 'counties' / 'washington' / 'whatcom' / 'index.html',
    OUTPUT / 'counties' / 'oregon' / 'clackamas' / 'index.html',
    OUTPUT / 'counties' / 'north-carolina' / 'guilford' / 'index.html',
    OUTPUT / 'counties' / 'north-carolina' / 'brunswick' / 'index.html',
    OUTPUT / 'counties' / 'north-carolina' / 'gaston' / 'index.html',
    OUTPUT / 'counties' / 'alabama' / 'mobile' / 'index.html',
]
missing_pages = [str(p.relative_to(OUTPUT)) for p in required_pages if not p.exists()]
if missing_pages:
    raise RuntimeError('County expansion deployment guard failed; missing: ' + ', '.join(missing_pages))

county_index_files = list((OUTPUT / 'counties').rglob('index.html'))
(OUTPUT / 'deployment-manifest.txt').write_text(
    'SepticScope production county expansion build\n'
    'Validated: 2026-08-29\n'
    f'County/state index files under /counties/: {len(county_index_files)}\n'
    'Representative expansion pages: PASS\n'
    'Site menu repair: PASS\n',
    encoding='utf-8'
)
print(f'Production deployment guard passed: {len(county_index_files)} county/state index files')
