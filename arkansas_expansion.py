# SepticScope Arkansas expansion — official Arkansas Department of Health sources
# County pages are limited to counties whose current Local Health Unit contact was independently verified.

AR_ONSITE = 'https://healthy.arkansas.gov/programs-services/public-health-safety/onsite-wastewater/'
AR_FAQ = 'https://healthy.arkansas.gov/programs-services/public-health-safety/onsite-wastewater/onsite-wastewater-faqs/'
AR_RULES = 'https://healthy.arkansas.gov/wp-content/uploads/Onsite-Wastewater-Rule.pdf'
AR_DIRECTORY = 'https://healthy.arkansas.gov/wp-content/uploads/LOCAL-HEALTH-UNIT-DIRECTORY.pdf'

AR_COUNTIES = {
    'Arkansas': [('DeWitt', '870-659-2056'), ('Stuttgart', '870-659-2086')],
    'Baxter': [('Mountain Home', '870-425-3072')],
    'Benton': [('Rogers', '479-986-1300'), ('Siloam Springs', '479-549-3794')],
    'Boone': [('Harrison', '870-743-5244')],
    'Carroll': [('Berryville', '870-423-2923')],
    'Craighead': [('Jonesboro', '870-933-4585')],
    'Faulkner': [('Conway', '501-450-4941')],
    'Garland': [('Hot Springs', '501-624-3394')],
    'Pulaski': [('North Little Rock', '501-791-8551'), ('Southwest Little Rock', '501-565-9311'), ('Central Little Rock', '501-280-3100'), ('Jacksonville', '501-982-7477')],
    'Saline': [('Benton', '501-303-5650')],
    'Sebastian': [('Fort Smith', '479-452-8600')],
}

ar_urls = []
ar_links = []
for county, offices in AR_COUNTIES.items():
    office_text = '; '.join(f'{html.escape(city)} — {html.escape(phone)}' for city, phone in offices)
    contact = (
        f'Arkansas Department of Health, {html.escape(county)} County Local Health Unit. '
        f'Current ADH directory contacts: {office_text}. '
        'ADH instructs property owners seeking a septic permit or an existing septic permit record to call the health unit in the county where the property is located and ask for the Onsite Environmental Specialist.'
    )
    sections = [
        ('County health unit is the local septic contact',
         'Arkansas Department of Health sets statewide onsite-wastewater policy and works with Environmental Health Specialists in county health departments. For an individual septic permit, ADH specifically directs applicants to the health unit in the county where the property is located and to ask for the Onsite Environmental Specialist, who can provide the local list of licensed private professionals who perform soil testing and system design.'),
        ('Construction approval comes before installation',
         'Arkansas’s 2024 onsite-wastewater rules state that Part I of the permit is the Permit for Construction. It must be completed by a Designated Representative and approved by ADH or its Authorized Agent before construction begins. The permit information includes soil or percolation findings, lot dimensions, system design, system layout, and other required site information.'),
        ('Inspection and Permit for Operation',
         'Part II of the Arkansas permit process is the installation inspection. The installer must notify the Authorized Agent or approved Designated Representative when the installation is ready for inspection and submit required installation documentation to the local health unit within five days. Part III is the Permit for Operation, and the system may not be used until that operating permit is issued.'),
        ('Licensed designers and installers',
         'ADH maintains statewide license information for Designated Representatives and septic installers. The agency’s FAQ directs property owners to search the ADH license database for a Designated Representative when system design is needed and for an appropriately licensed septic installer for construction work.'),
        ('Site suitability, wells, and lot size',
         'ADH states there is no single statewide minimum lot size for a septic system. Required space depends on soil suitability and the number of bedrooms, and the agency identifies a 100-foot setback from water wells. ADH also explains that soil pits are used to identify limiting conditions such as rock, impervious layers, and seasonal groundwater.'),
        ('Existing septic permit records',
         'For an existing septic permit, ADH directs the requester to the county health unit and the Onsite Environmental Specialist. The agency says searches are easier when the requester can provide the approximate home-construction year, subdivision and lot number, and the original owner or developer name.'),
        ('Limited ten-acre permit exemption',
         'ADH describes a narrow permit exemption for a single residence on ten or more acres when every part of the sewage system is more than 200 feet from every property line, including roads. The exemption is only from obtaining the septic permit; the system must still comply with state requirements and may not create a nuisance. ADH says an exemption letter can be obtained from the local health unit.'),
    ]
    sources = [
        ('Arkansas Department of Health — Onsite Wastewater', AR_ONSITE),
        ('Arkansas Department of Health — Onsite Wastewater FAQs', AR_FAQ),
        ('Arkansas Department of Health — 2024 Rules Pertaining to Onsite Wastewater Systems', AR_RULES),
        ('Arkansas Department of Health — Local Health Unit Directory', AR_DIRECTORY),
    ]
    url = write_county_page(
        'Arkansas', 'arkansas', county,
        f'Arkansas Department of Health — {county} County Local Health Unit / Onsite Environmental Specialist',
        contact, sections, sources, verified='August 29, 2026'
    )
    ar_urls.append(url)
    ar_links.append((county, 'Arkansas Department of Health Local Health Unit'))

write_hub(
    'Arkansas', 'arkansas', sorted(ar_links),
    'Arkansas Department of Health administers the statewide onsite-wastewater program in cooperation with Environmental Health Specialists in county health departments. ADH directs septic permit applicants and septic-record requests to the Local Health Unit in the county where the property is located.',
    'This initial Arkansas batch includes only counties whose current ADH Local Health Unit contact information was validated against the state directory. The pages summarize the current statewide construction-permit, inspection, operation-permit, professional licensing, site-suitability, record-request, and limited ten-acre exemption rules without inventing unsupported county-specific requirements.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    if '/counties/arkansas/' not in text:
        promo = '<section><h2>Arkansas</h2><p><a href="/counties/arkansas/">Browse 11 verified Arkansas county septic guides →</a></p></section>'
        text = text.replace('</main>', promo + '</main>', 1) if '</main>' in text else text.replace('</body>', promo + '</body>', 1)
        county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/arkansas/'] + ar_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'Arkansas expansion complete: +{len(ar_urls)} verified county guides')
exec((ROOT / 'washington_expansion.py').read_text(encoding='utf-8'), globals())
