# SepticScope Hawaii completion — source-checked statewide onsite-wastewater routing for all five county equivalents.
# Official Hawaii Department of Health and county-government sources reviewed September 2, 2026.
#
# Hawaii administers individual wastewater-system review through the state Department of Health.
# County building, land-use, grading, shoreline, and development approvals remain separate. These pages
# therefore distinguish the statewide wastewater path from county assistance instead of inventing a
# county septic program, county fee, setback, form, or records portal that the cited sources do not confirm.

HI_DOH_WASTEWATER = 'https://health.hawaii.gov/wastewater/'
HI_DOH_RULES = 'https://health.hawaii.gov/opppd/department-of-health-administrative-rules-title-11/'
HI_DOH_CONTACT = (
    'Hawaii Department of Health, Environmental Management Division, Wastewater Branch; '
    '2827 Waimano Home Road, Room 207, Pearl City, HI 96782; 808-586-4294. '
    'Use the Wastewater Branch website for the current individual wastewater-system application, '
    'rules, forms, staff routing, and project-specific instructions.'
)

HI_COUNTIES = [
    {
        'county': 'Hawaii',
        'local_label': 'County of Hawaii official website',
        'local_url': 'https://www.hawaiicounty.gov/',
        'routing': (
            'For property in Hawaii County, start with the state Wastewater Branch for the onsite '
            'wastewater approval path. Use the County of Hawaii website to identify the current building, '
            'planning, zoning, grading, and other development contacts that may apply to the same project.'
        ),
    },
    {
        'county': 'Honolulu',
        'local_label': 'City and County of Honolulu official website',
        'local_url': 'https://www.honolulu.gov/',
        'routing': (
            'For property in the City and County of Honolulu, start with the state Wastewater Branch for '
            'individual wastewater-system review. Use the City and County website for the separate building, '
            'planning, zoning, shoreline, grading, or development approvals associated with the property.'
        ),
    },
    {
        'county': 'Kalawao',
        'local_label': 'Hawaii Department of Health — Kalaupapa program',
        'local_url': 'https://health.hawaii.gov/kalaupapa/',
        'routing': (
            'Kalawao County does not operate like an ordinary county permitting jurisdiction. Start with the '
            'state Wastewater Branch and the Department of Health Kalaupapa program so the responsible state '
            'office can confirm access, land-management, public-health, wastewater, and project-review routing.'
        ),
    },
    {
        'county': 'Kauai',
        'local_label': 'County of Kauai official website',
        'local_url': 'https://www.kauai.gov/',
        'routing': (
            'For property in Kauai County, start with the state Wastewater Branch for individual '
            'wastewater-system review. Use the County of Kauai website to identify current building, planning, '
            'zoning, grading, shoreline, and related development contacts before filing connected permits.'
        ),
    },
    {
        'county': 'Maui',
        'local_label': 'County of Maui official website',
        'local_url': 'https://www.mauicounty.gov/',
        'routing': (
            'For property in Maui County, start with the state Wastewater Branch for the onsite wastewater '
            'approval path. Use the County of Maui website to identify the current building, planning, zoning, '
            'grading, shoreline, and development contacts for the island and parcel involved.'
        ),
    },
]

hi_urls = []
hi_links = []
for item in HI_COUNTIES:
    county = item['county']
    sections = [
        (
            'Start with the Hawaii Department of Health Wastewater Branch',
            'Hawaii Department of Health maintains the statewide Wastewater Branch and the Department’s '
            'Title 11 administrative-rule library. For an individual wastewater system, use the current '
            'state materials and contact the branch before treating a county building or planning approval '
            'as authorization to install, replace, alter, close, or place a wastewater system into service.'
        ),
        (
            'Describe the exact project before selecting a form',
            'Tell the Wastewater Branch whether the work involves a new system, an existing system, repair, '
            'replacement, alteration, expansion, abandonment, or a cesspool-related project. SepticScope does '
            'not substitute one application path for another because the required submittal and review can '
            'change with the proposed work and the facility served.'
        ),
        (
            'Site and design requirements remain parcel-specific',
            'Do not copy a system layout, capacity, setback, disposal method, or approval from another island '
            'or parcel. Confirm current requirements for wastewater flow, water supply, lot layout, soils, '
            'treatment and disposal area, reserve needs, professional design, construction review, and any '
            'inspection stage directly from the state’s current rule and application materials.'
        ),
        (
            'County development review is a separate checkpoint',
            item['routing']
        ),
        (
            'Repairs, failures, records, and inspections need current agency direction',
            'For surfacing wastewater, a damaged tank or disposal area, an unpermitted system, a property '
            'transaction, or missing records, contact the Wastewater Branch before work is covered or made '
            'inaccessible. Ask the branch which records are available, whether emergency work can proceed, '
            'which inspections are required, and what documentation must be retained for the property.'
        ),
        (
            'County-specific details not independently confirmed',
            'SepticScope did not locate an official county source establishing a separate county septic '
            'approval program, county septic fee schedule, county-specific setback table, or county septic '
            'records portal for this page. The state Wastewater Branch and the applicable county office should '
            'confirm current project-specific requirements before a design, purchase, or construction decision.'
        ),
    ]
    sources = [
        ('Hawaii Department of Health — Wastewater Branch', HI_DOH_WASTEWATER),
        ('Hawaii Department of Health — Administrative Rules, Title 11', HI_DOH_RULES),
        (item['local_label'], item['local_url']),
    ]
    url = write_county_page(
        'Hawaii',
        'hawaii',
        county,
        'Hawaii Department of Health — Environmental Management Division, Wastewater Branch',
        HI_DOH_CONTACT,
        sections,
        sources,
        verified='September 2, 2026',
    )
    hi_urls.append(url)
    hi_links.append((county, 'Hawaii Department of Health Wastewater Branch'))

write_hub(
    'Hawaii',
    'hawaii',
    sorted(hi_links),
    'Hawaii administers individual wastewater-system review through the state Department of Health Wastewater Branch. All five county and county-equivalent guides identify that statewide starting point and separately route users to the applicable county or state-administered local resource.',
    'All 5 Hawaii county and county-equivalent pages now have source-checked SepticScope guidance. The pages do not invent county septic fees, setbacks, forms, or approval authority where current official county sources do not establish them.',
)

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/hawaii/'] + hi_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(
    f'<url><loc>{url}</loc><lastmod>2026-09-02</lastmod></url>'
    for url in new_urls
    if url not in sm
)
if entries:
    sitemap.write_text(sm.replace('</urlset>', entries + '</urlset>'), encoding='utf-8')

hub_path = OUTPUT / 'counties' / 'hawaii' / 'index.html'
if not hub_path.exists():
    raise RuntimeError('Hawaii state hub was not generated')
hub_text = hub_path.read_text(encoding='utf-8')
if 'All 5 Hawaii county and county-equivalent pages' not in hub_text:
    raise RuntimeError('Hawaii state hub completion message is missing')

for item in HI_COUNTIES:
    slug = slugify(item['county'])
    page = OUTPUT / 'counties' / 'hawaii' / slug / 'index.html'
    if not page.exists():
        raise RuntimeError(f'Hawaii county guide missing: {item["county"]}')
    text = page.read_text(encoding='utf-8')
    compact = text.replace(' ', '').lower()
    if 'localsepticrulesnotyetverified' in compact or 'noindex,follow' in compact:
        raise RuntimeError(f'Hawaii verified guide was replaced by fallback: {item["county"]}')
    for required in ('Official sources', 'Hawaii Department of Health', 'County-specific details not independently confirmed'):
        if required.lower() not in text.lower():
            raise RuntimeError(f'Hawaii guide is missing required scope text for {item["county"]}: {required}')

print('Hawaii county completion: +5 source-checked guides; all 5 county equivalents covered')
