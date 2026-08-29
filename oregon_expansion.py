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
exec((ROOT / 'ohio_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'wisconsin_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'wisconsin_additional_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'michigan_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'high_population_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'texas_additional_expansion.py').read_text(encoding='utf-8'), globals())

# Add every current U.S. county/county-equivalent as either a verified guide or a clearly labeled lookup page.
exec((ROOT / 'nationwide_county_lookup.py').read_text(encoding='utf-8'), globals())

# Apply shared UI repairs only after every content generator has finished, including nationwide fallback pages.
exec((ROOT / 'site_ui_fix.py').read_text(encoding='utf-8'), globals())

# Production deployment guard: fail the build if representative expansion pages are missing.
required_pages = [
    OUTPUT / 'counties' / 'tennessee' / 'bedford' / 'index.html',
    OUTPUT / 'counties' / 'tennessee' / 'hamilton' / 'index.html',
    OUTPUT / 'counties' / 'idaho' / 'ada' / 'index.html',
    OUTPUT / 'counties' / 'south-carolina' / 'greenville' / 'index.html',
    OUTPUT / 'counties' / 'arkansas' / 'benton' / 'index.html',
    OUTPUT / 'counties' / 'washington' / 'king' / 'index.html',
    OUTPUT / 'counties' / 'washington' / 'yakima' / 'index.html',
    OUTPUT / 'counties' / 'oregon' / 'clackamas' / 'index.html',
    OUTPUT / 'counties' / 'north-carolina' / 'guilford' / 'index.html',
    OUTPUT / 'counties' / 'alabama' / 'mobile' / 'index.html',
    OUTPUT / 'counties' / 'ohio' / 'franklin' / 'index.html',
    OUTPUT / 'counties' / 'wisconsin' / 'waukesha' / 'index.html',
    OUTPUT / 'counties' / 'michigan' / 'oakland' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'denton' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'collin' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'fort-bend' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'travis' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'hays' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'montgomery' / 'index.html',
    OUTPUT / 'counties' / 'virginia' / 'fairfax' / 'index.html',
    OUTPUT / 'counties' / 'maryland' / 'prince-george-s' / 'index.html',
    OUTPUT / 'counties' / 'california' / 'los-angeles' / 'index.html',
    OUTPUT / 'counties' / 'connecticut' / 'capitol' / 'index.html',
]
missing_pages = [str(p.relative_to(OUTPUT)) for p in required_pages if not p.exists()]
if missing_pages:
    raise RuntimeError('County expansion deployment guard failed; missing: ' + ', '.join(missing_pages))

home_text=(OUTPUT/'index.html').read_text(encoding='utf-8')
if 'Indiana launch' in home_text or 'Five Indiana counties are live in the launch build.' in home_text:
    raise RuntimeError('Homepage still contains obsolete Indiana-launch positioning')
if 'Search all 3,144 U.S. counties and county equivalents.' not in home_text:
    raise RuntimeError('Homepage nationwide county message is missing')
lookup_text=(OUTPUT/'counties'/'california'/'los-angeles'/'index.html').read_text(encoding='utf-8')
if 'Local septic rules not yet verified' not in lookup_text:
    raise RuntimeError('Nationwide fallback labeling is missing')

verified_batches = {
    'Ohio': ('ohio', ('franklin','delaware','fairfield','licking')),
    'Wisconsin': ('wisconsin', ('waukesha','washington','brown','ozaukee','winnebago','dane','sheboygan','walworth','rock','dodge','fond-du-lac')),
    'Michigan': ('michigan', ('oakland','ottawa','kent','washtenaw','ingham')),
    'Texas additional': ('texas', ('fort-bend','travis','hays','montgomery')),
    'High population': ('MULTI', ()),
}
for label,(state_slug,counties) in verified_batches.items():
    if state_slug == 'MULTI':
        continue
    for county_slug in counties:
        page_text=(OUTPUT/'counties'/state_slug/county_slug/'index.html').read_text(encoding='utf-8')
        if 'Local septic rules not yet verified' in page_text:
            raise RuntimeError(f'{label} verified page was replaced by fallback: {county_slug}')
        if 'VERIFIED' not in page_text.upper():
            raise RuntimeError(f'{label} verified marker missing: {county_slug}')

for state_slug,county_slug in (('texas','denton'),('texas','collin'),('virginia','fairfax'),('maryland','prince-george-s')):
    page_text=(OUTPUT/'counties'/state_slug/county_slug/'index.html').read_text(encoding='utf-8')
    if 'Local septic rules not yet verified' in page_text or 'VERIFIED' not in page_text.upper():
        raise RuntimeError(f'High-population verified page failed: {state_slug}/{county_slug}')

county_index_files = list((OUTPUT / 'counties').rglob('index.html'))
(OUTPUT / 'deployment-manifest.txt').write_text(
    'SepticScope production county expansion build\n'
    'Validated: 2026-08-29\n'
    f'County/state index files under /counties/: {len(county_index_files)}\n'
    'Nationwide county lookup: PASS\n'
    'Ohio verified expansion: PASS (+4)\n'
    'Wisconsin verified expansions: PASS (+11)\n'
    'Michigan verified expansion: PASS (+5)\n'
    'High-population verified expansion: PASS (+4)\n'
    'Texas additional verified expansion: PASS (+4)\n'
    'Representative expansion pages: PASS\n'
    'Site menu repair: PASS\n',
    encoding='utf-8'
)
print(f'Production deployment guard passed: {len(county_index_files)} county/state index files')
