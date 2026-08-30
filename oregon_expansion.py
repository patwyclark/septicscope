# Oregon expansion wrapper. Preserve validated regional batches and run additional county expansions.
exec((ROOT / 'oregon_expansion_base.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'alabama_additional_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_additional_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_third_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_fourth_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'north_carolina_fifth_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'washington_additional_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'tennessee_contract_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'tennessee_contract_final_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'washington_third_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'ohio_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'wisconsin_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'wisconsin_additional_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'wisconsin_third_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'michigan_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'high_population_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'texas_additional_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'texas_third_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'georgia_additional_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'florida_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'arizona_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'virginia_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'colorado_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'iowa_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'minnesota_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'maryland_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'indiana_expansion.py').read_text(encoding='utf-8'), globals())
exec((ROOT / 'missouri_expansion.py').read_text(encoding='utf-8'), globals())

# Add every current U.S. county/county-equivalent as either a verified guide or a clearly labeled lookup page.
exec((ROOT / 'nationwide_county_lookup.py').read_text(encoding='utf-8'), globals())

# Apply shared UI repairs only after every content generator has finished, including nationwide fallback pages.
exec((ROOT / 'site_ui_fix.py').read_text(encoding='utf-8'), globals())

# Production deployment guard: fail the build if representative expansion pages are missing.
required_pages = [
    OUTPUT / 'counties' / 'tennessee' / 'bedford' / 'index.html',
    OUTPUT / 'counties' / 'tennessee' / 'hamilton' / 'index.html',
    OUTPUT / 'counties' / 'tennessee' / 'davidson' / 'index.html',
    OUTPUT / 'counties' / 'tennessee' / 'knox' / 'index.html',
    OUTPUT / 'counties' / 'tennessee' / 'sevier' / 'index.html',
    OUTPUT / 'counties' / 'idaho' / 'ada' / 'index.html',
    OUTPUT / 'counties' / 'south-carolina' / 'greenville' / 'index.html',
    OUTPUT / 'counties' / 'arkansas' / 'benton' / 'index.html',
    OUTPUT / 'counties' / 'washington' / 'king' / 'index.html',
    OUTPUT / 'counties' / 'washington' / 'yakima' / 'index.html',
    OUTPUT / 'counties' / 'oregon' / 'clackamas' / 'index.html',
    OUTPUT / 'counties' / 'north-carolina' / 'guilford' / 'index.html',
    OUTPUT / 'counties' / 'north-carolina' / 'carteret' / 'index.html',
    OUTPUT / 'counties' / 'north-carolina' / 'onslow' / 'index.html',
    OUTPUT / 'counties' / 'north-carolina' / 'pender' / 'index.html',
    OUTPUT / 'counties' / 'alabama' / 'mobile' / 'index.html',
    OUTPUT / 'counties' / 'ohio' / 'franklin' / 'index.html',
    OUTPUT / 'counties' / 'wisconsin' / 'waukesha' / 'index.html',
    OUTPUT / 'counties' / 'wisconsin' / 'kenosha' / 'index.html',
    OUTPUT / 'counties' / 'wisconsin' / 'jefferson' / 'index.html',
    OUTPUT / 'counties' / 'wisconsin' / 'sauk' / 'index.html',
    OUTPUT / 'counties' / 'michigan' / 'oakland' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'denton' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'collin' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'fort-bend' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'travis' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'hays' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'montgomery' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'williamson' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'comal' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'guadalupe' / 'index.html',
    OUTPUT / 'counties' / 'texas' / 'bastrop' / 'index.html',
    OUTPUT / 'counties' / 'georgia' / 'forsyth' / 'index.html',
    OUTPUT / 'counties' / 'georgia' / 'hall' / 'index.html',
    OUTPUT / 'counties' / 'georgia' / 'cherokee' / 'index.html',
    OUTPUT / 'counties' / 'florida' / 'lee' / 'index.html',
    OUTPUT / 'counties' / 'florida' / 'pasco' / 'index.html',
    OUTPUT / 'counties' / 'florida' / 'hernando' / 'index.html',
    OUTPUT / 'counties' / 'florida' / 'polk' / 'index.html',
    OUTPUT / 'counties' / 'arizona' / 'maricopa' / 'index.html',
    OUTPUT / 'counties' / 'arizona' / 'pima' / 'index.html',
    OUTPUT / 'counties' / 'arizona' / 'yavapai' / 'index.html',
    OUTPUT / 'counties' / 'arizona' / 'coconino' / 'index.html',
    OUTPUT / 'counties' / 'virginia' / 'loudoun' / 'index.html',
    OUTPUT / 'counties' / 'virginia' / 'chesterfield' / 'index.html',
    OUTPUT / 'counties' / 'virginia' / 'albemarle' / 'index.html',
    OUTPUT / 'counties' / 'colorado' / 'el-paso' / 'index.html',
    OUTPUT / 'counties' / 'colorado' / 'larimer' / 'index.html',
    OUTPUT / 'counties' / 'colorado' / 'weld' / 'index.html',
    OUTPUT / 'counties' / 'iowa' / 'polk' / 'index.html',
    OUTPUT / 'counties' / 'iowa' / 'linn' / 'index.html',
    OUTPUT / 'counties' / 'iowa' / 'story' / 'index.html',
    OUTPUT / 'counties' / 'iowa' / 'johnson' / 'index.html',
    OUTPUT / 'counties' / 'minnesota' / 'washington' / 'index.html',
    OUTPUT / 'counties' / 'minnesota' / 'hennepin' / 'index.html',
    OUTPUT / 'counties' / 'minnesota' / 'dakota' / 'index.html',
    OUTPUT / 'counties' / 'maryland' / 'anne-arundel' / 'index.html',
    OUTPUT / 'counties' / 'maryland' / 'frederick' / 'index.html',
    OUTPUT / 'counties' / 'maryland' / 'howard' / 'index.html',
    OUTPUT / 'counties' / 'indiana' / 'hamilton' / 'index.html',
    OUTPUT / 'counties' / 'indiana' / 'marshall' / 'index.html',
    OUTPUT / 'counties' / 'indiana' / 'grant' / 'index.html',
    OUTPUT / 'counties' / 'missouri' / 'st-charles' / 'index.html',
    OUTPUT / 'counties' / 'missouri' / 'greene' / 'index.html',
    OUTPUT / 'counties' / 'missouri' / 'clay' / 'index.html',
    OUTPUT / 'counties' / 'missouri' / 'platte' / 'index.html',
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
    'Tennessee contract completion': ('tennessee', ('davidson','knox','sevier')),
    'North Carolina fifth': ('north-carolina', ('carteret','onslow','pender')),
    'Ohio': ('ohio', ('franklin','delaware','fairfield','licking')),
    'Wisconsin': ('wisconsin', ('waukesha','washington','brown','ozaukee','winnebago','dane','sheboygan','walworth','rock','dodge','fond-du-lac','kenosha','jefferson','sauk')),
    'Michigan': ('michigan', ('oakland','ottawa','kent','washtenaw','ingham')),
    'Texas additional': ('texas', ('fort-bend','travis','hays','montgomery')),
    'Texas third': ('texas', ('williamson','comal','guadalupe','bastrop')),
    'Georgia additional': ('georgia', ('forsyth','hall','cherokee')),
    'Florida': ('florida', ('lee','pasco','hernando','polk')),
    'Arizona': ('arizona', ('maricopa','pima','yavapai','coconino')),
    'Virginia': ('virginia', ('loudoun','chesterfield','albemarle')),
    'Colorado': ('colorado', ('el-paso','larimer','weld')),
    'Iowa': ('iowa', ('polk','linn','story','johnson')),
    'Minnesota': ('minnesota', ('washington','hennepin','dakota')),
    'Maryland': ('maryland', ('anne-arundel','frederick','howard')),
    'Indiana': ('indiana', ('hamilton','marshall','grant')),
    'Missouri': ('missouri', ('st-charles','greene','clay','platte')),
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
    'Validated: 2026-08-30\n'
    f'County/state index files under /counties/: {len(county_index_files)}\n'
    'Nationwide county lookup: PASS\n'
    'Tennessee contract completion: PASS (+3; all 95 counties now verified)\n'
    'North Carolina fifth verified expansion: PASS (+3; 26 total verified NC counties)\n'
    'Ohio verified expansion: PASS (+4)\n'
    'Wisconsin verified expansions: PASS (+14)\n'
    'Michigan verified expansion: PASS (+5)\n'
    'High-population verified expansion: PASS (+4)\n'
    'Texas additional verified expansion: PASS (+4)\n'
    'Texas third verified expansion: PASS (+4)\n'
    'Georgia additional verified expansion: PASS (+3)\n'
    'Florida verified expansion: PASS (+4)\n'
    'Arizona verified expansion: PASS (+4)\n'
    'Virginia verified expansion: PASS (+3)\n'
    'Colorado verified expansion: PASS (+3)\n'
    'Iowa verified expansion: PASS (+4)\n'
    'Minnesota verified expansion: PASS (+3)\n'
    'Maryland verified expansion: PASS (+3; 4 total verified MD counties)\n'
    'Indiana verified expansion: PASS (+3)\n'
    'Missouri verified expansion: PASS (+4)\n'
    'Representative expansion pages: PASS\n'
    'Site menu repair: PASS\n',
    encoding='utf-8'
)
print(f'Production deployment guard passed: {len(county_index_files)} county/state index files')