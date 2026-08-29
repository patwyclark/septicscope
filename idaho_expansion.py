# SepticScope Idaho expansion — official-source county pages
# Executed after the New Mexico expansion.

ID_DEQ = 'https://www.deq.idaho.gov/water-quality/wastewater/septic-and-septage/'
ID_DHW_DISTRICTS = 'https://healthandwelfare.idaho.gov/health-wellness/community-health/public-health-districts'
ID_DHW_COUNTY_MAP = 'https://healthandwelfare.idaho.gov/health-wellness/community-health/food-safety'
ID_TGM = 'https://www.deq.idaho.gov/advisory-groups-and-committees/septic-technical-guidance-committee/'

# Idaho DEQ states that the seven public health districts administer IDAPA 58.01.03,
# conduct site evaluations, issue septic permits, inspect installations, and answer
# property-specific permit/record questions. County-to-district assignments below are
# from Idaho DHW's current public-health district/county listings (updated July 23, 2026).
ID_DISTRICTS = {
    'Panhandle Health District (District 1)': {
        'phone': '208-415-5100',
        'address': '8500 N. Atlas Road, Hayden, ID 83835',
        'counties': ['Benewah', 'Bonner', 'Boundary', 'Kootenai', 'Shoshone'],
    },
    'Public Health – Idaho North Central District (District 2)': {
        'phone': '208-799-3100',
        'address': '215 10th Street, Lewiston, ID 83501',
        'counties': ['Clearwater', 'Idaho', 'Latah', 'Lewis', 'Nez Perce'],
    },
    'Southwest District Health (District 3)': {
        'phone': '208-455-5300',
        'address': '13307 Miami Lane, Caldwell, ID 83607',
        'counties': ['Adams', 'Canyon', 'Gem', 'Owyhee', 'Payette', 'Washington'],
    },
    'Central District Health (District 4)': {
        'phone': '208-375-5211',
        'address': '707 N. Armstrong Place, Boise, ID 83704-0825',
        'counties': ['Ada', 'Boise', 'Elmore', 'Valley'],
    },
    'South Central Public Health District (District 5)': {
        'phone': '208-737-5900',
        'address': '1020 Washington Street N., Twin Falls, ID 83301-3156',
        'counties': ['Blaine', 'Camas', 'Cassia', 'Gooding', 'Jerome', 'Lincoln', 'Minidoka', 'Twin Falls'],
    },
    'Southeastern Idaho Public Health (District 6)': {
        'phone': '208-233-9080',
        'address': '1901 Alvin Ricken Drive, Pocatello, ID 83201',
        'counties': ['Bannock', 'Bear Lake', 'Bingham', 'Caribou', 'Franklin', 'Oneida', 'Power'],
    },
    'Eastern Idaho Public Health (District 7)': {
        'phone': '208-522-0310',
        'address': '1250 Hollipark Drive, Idaho Falls, ID 83401',
        'counties': ['Bonneville', 'Butte', 'Clark', 'Custer', 'Fremont', 'Jefferson', 'Lemhi', 'Madison', 'Teton'],
    },
}

id_urls = []
id_links = []
for district, info in ID_DISTRICTS.items():
    for county in info['counties']:
        contact = (
            f'{html.escape(district)} serves {html.escape(county)} County. District contact listed by the '
            f'Idaho Department of Health and Welfare: {html.escape(info["phone"])}; '
            f'{html.escape(info["address"])}. Idaho DEQ directs property-specific septic permitting and '
            'permit-record questions to the public health district for the county where the property is located.'
        )
        sections = [
            ('Your public health district issues the septic permit',
             'Idaho DEQ states that Idaho’s seven public health districts administer the Individual/Subsurface Sewage Disposal Rules under an agreement with DEQ. The district conducts site evaluations, determines site suitability, issues septic-system permits, inspects installations, and assists with existing permit records and property-specific questions.'),
            ('Get the site evaluated before installation',
             'For an individual septic system, DEQ advises the property owner to have a site evaluation performed by the public health district and a licensed septic installer before purchasing property and applying for a permit. Soil, slope, groundwater, bedrock, water bodies and other site conditions can affect the design that will be approved.'),
            ('Permit and inspection are part of the installation process',
             'DEQ states that a property owner must obtain a permit from the public health district before installing an individual septic system. After issuance, the system should be installed by a properly licensed installer and inspected by the public health district before the installation is treated as complete.'),
            ('Installer rules and the homeowner exception',
             'Idaho requires septic systems to be installed by a licensed basic or complex installer, except that a homeowner may establish a standard/basic system on the homeowner’s own property without hired help when the state conditions for that exception are satisfied. Complex work still requires the appropriate licensed installer.'),
            ('Large systems require additional review',
             'A Large Soil Absorption System is designed to receive at least 2,500 gallons of wastewater per day. DEQ says an LSAS permit application must include a nutrient-pathogen evaluation, the design must be prepared by an Idaho-licensed professional engineer, DEQ must review the plans and specifications, and a licensed complex installer is required.'),
            ('Some sites can require nutrient-pathogen review or enhanced treatment',
             'DEQ requires nutrient-pathogen evaluations for certain proposed systems, including central systems in nitrate-priority areas, systems over sensitive-resource aquifers, and all proposed LSAS facilities. DEQ, the health district, or a county agency may also require evaluation where conditions such as shallow soil, coarse sediment, shallow groundwater, fractured bedrock, or existing contamination raise water-quality concerns.'),
            ('Alternative treatment systems have ongoing obligations',
             'For extended treatment package systems, DEQ requires at least one operation-and-maintenance event each year and annual monitoring. A certified service provider performs required service and monitoring, and the annual report is due to the public health district by July 31; the property owner remains responsible for permit compliance.'),
            ('Existing septic permits and records',
             'For an existing system, DEQ specifically directs owners to the county’s public health district for permit status and permit records. Have the property address, parcel information and any known permit or installation details available when requesting a search.')
        ]
        sources = [
            ('Idaho DEQ — Septic and Septage', ID_DEQ),
            ('Idaho Department of Health and Welfare — Public Health District contacts', ID_DHW_DISTRICTS),
            ('Idaho Department of Health and Welfare — current county-to-district listings', ID_DHW_COUNTY_MAP),
            ('Idaho DEQ — Septic Technical Guidance Committee and Technical Guidance Manual', ID_TGM),
        ]
        url = write_county_page(
            'Idaho', 'idaho', county,
            district,
            contact, sections, sources, verified='August 28, 2026'
        )
        id_urls.append(url)
        id_links.append((county, district))

write_hub(
    'Idaho', 'idaho',
    [(county, district) for county, district in sorted(id_links)],
    'Idaho DEQ establishes statewide onsite wastewater standards, while the state’s seven public health districts administer the septic program county-by-county. This expansion maps every Idaho county to its current public health district and pairs that local permitting authority with current DEQ requirements.',
    'All 44 Idaho counties are included. The district assignments and central district contacts are based on current Idaho Department of Health and Welfare listings, while septic permitting duties and technical requirements are supported by Idaho DEQ.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    if '/counties/idaho/' not in text:
        promo = '<section><h2>Idaho</h2><p><a href="/counties/idaho/">Browse all 44 verified Idaho county septic guides →</a></p></section>'
        text = text.replace('</main>', promo + '</main>', 1) if '</main>' in text else text.replace('</body>', promo + '</body>', 1)
        county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/idaho/'] + id_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-28</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'Idaho expansion complete: +{len(id_urls)} verified county guides')
