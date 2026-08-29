# SepticScope South Carolina expansion — official-source county pages
# Executed after the Idaho expansion.

SC_SEPTIC = 'https://des.sc.gov/permits-regulations/septic-tanks'
SC_RESIDENTIAL = 'https://www.des.sc.gov/permits-regulations/septic-tanks/permits-licenses/septic-tanks-residential-single-home-builder'
SC_LOCAL = 'https://www.des.sc.gov/about-scdes/locations/scdes-local-offices'
SC_WHO_CALL = 'https://www.des.sc.gov/permits-regulations/septic-tanks/septic-tanks-who-call'
SC_FORMS = 'https://des.sc.gov/permits-regulations/septic-tanks/septic-tanks-regulation-forms-fact-sheets'
SC_RECORDS = 'https://www.des.sc.gov/permits-regulations/septic-tanks/homeowner-resources/how-locate-septic-tank'
SC_INSTALLERS = 'https://www.des.sc.gov/permits-regulations/septic-tanks/licensing-septic-system-installers'
SC_PLAT = 'https://des.sc.gov/permits-regulations/septic-tanks/county-plat-or-deed'
# Current SCDES county-to-local-office coverage is also published in agency permit materials.
SC_OFFICE_MAP_SOURCE = 'https://des.sc.gov/sites/des/files/Documents/BOW/GPSCG360000.pdf'

# SCDES local office coverage verified from current agency materials.
SC_OFFICES = {
    'Anderson': {
        'phone': '864-260-5585',
        'counties': ['Anderson', 'Oconee', 'Laurens'],
    },
    'Greenwood': {
        'phone': '864-227-5915',
        'counties': ['Abbeville', 'Greenwood', 'McCormick'],
    },
    'Greenville': {
        'phone': '864-372-3273',
        'counties': ['Greenville', 'Pickens', 'Cherokee', 'Spartanburg', 'Union'],
    },
    'Columbia': {
        'phone': '803-896-0620',
        'counties': ['Fairfield', 'Lexington', 'Newberry', 'Richland'],
    },
    'Lancaster': {
        'phone': '803-285-7461',
        'counties': ['Chester', 'Lancaster', 'York', 'Kershaw'],
    },
    'Aiken': {
        'phone': '803-642-1637',
        'counties': ['Aiken', 'Barnwell', 'Edgefield', 'Saluda'],
    },
    'Florence': {
        'phone': '843-661-4825',
        'counties': ['Chesterfield', 'Darlington', 'Dillon', 'Florence', 'Marion', 'Marlboro'],
    },
    'Sumter': {
        'phone': '803-778-6548',
        'counties': ['Clarendon', 'Lee', 'Sumter'],
    },
    'Myrtle Beach': {
        'phone': '843-238-4378',
        'counties': ['Georgetown', 'Horry', 'Williamsburg'],
    },
    'Charleston': {
        'phone': '843-953-0150',
        'counties': ['Berkeley', 'Charleston', 'Dorchester'],
    },
    'Beaufort': {
        'phone': '843-846-9400',
        'counties': ['Beaufort', 'Colleton', 'Hampton', 'Jasper'],
    },
    'Orangeburg': {
        'phone': '803-533-5490',
        'counties': ['Allendale', 'Bamberg', 'Calhoun', 'Orangeburg'],
    },
}

sc_urls = []
sc_links = []
for office, info in SC_OFFICES.items():
    for county in info['counties']:
        contact = (
            f'South Carolina Department of Environmental Services (SCDES), {html.escape(office)} local office — '
            f'{html.escape(info["phone"])}. Current SCDES county-coverage materials assign '
            f'{html.escape(county)} County to this local office. For onsite-wastewater questions after an '
            'application is submitted, SCDES directs applicants to the appropriate local office.'
        )
        sections = [
            ('SCDES approval is required before septic installation',
             'South Carolina requires site approval and a permit for septic systems. For a home or manufactured home that will not be served by a public or community sewer, SCDES states that its approval and a permit to install the septic system must be obtained first; the county cannot issue the building permit without the required septic approval.'),
            ('Residential applications are filed through ePermitting',
             'SCDES directs residential applicants to submit the Onsite Wastewater System Application (D-1740) through the state ePermitting Portal. The current residential process lists a $150 application fee and requires a copy of the property plat or deed with the application.'),
            ('Site and soil conditions control what can be approved',
             'SCDES evaluates the proposed site before issuing a construction permit. Wet conditions can delay soil evaluation because saturated soil may prevent an accurate review. SCDES also notes that sites above the South Carolina Fall Line can require backhoe pits when rock conditions prevent an adequate hand-auger evaluation; confirm the required evaluation method for the specific parcel with the assigned office.'),
            ('Use an appropriately licensed septic installer',
             'SCDES licenses onsite-wastewater installers and separates installer authority into tiers. The system type determines the level of installer qualification needed; specialized systems can require higher-tier licensing. Verify the contractor’s current South Carolina license before construction or repair work begins.'),
            ('Final inspection and approval to operate',
             'The installation must satisfy SCDES final-inspection requirements before it is treated as complete. When an installer is authorized to self-inspect, SCDES requires the Final Inspection Form to be submitted within two business days of completing the installation, with an as-built site drawing and required measurements; incomplete submissions can delay Approval to Operate.'),
            ('Existing septic permits and records',
             'For homes built within roughly the last 20 years, SCDES advises contacting one of its offices to determine whether a septic permit is on file. Providing the tax map number, lot or block number, property address, approximate installation or construction date, original permit holder, and subdivision name can speed the search. SCDES also publishes a Customer Support line for copies of permits and final inspections.'),
            ('Plat or deed documentation',
             'SCDES requires a property plat or deed with a septic permit application. The agency states that plats must show property dimensions and deeds must be descriptive, and it provides county-by-county links for obtaining these records from the applicable Register of Deeds or Clerk of Court.')
        ]
        sources = [
            ('SCDES — Septic Tanks program', SC_SEPTIC),
            ('SCDES — Residential single-home septic permit process', SC_RESIDENTIAL),
            ('SCDES — Local Offices', SC_LOCAL),
            ('SCDES — Onsite Wastewater: Who to Call', SC_WHO_CALL),
            ('SCDES — county-to-local-office coverage in current agency permit materials', SC_OFFICE_MAP_SOURCE),
            ('SCDES — Regulation, forms and final-inspection guidance', SC_FORMS),
            ('SCDES — How to locate a septic tank / permit records', SC_RECORDS),
            ('SCDES — septic installer licensing', SC_INSTALLERS),
            ('SCDES — county plat or deed guidance', SC_PLAT),
        ]
        url = write_county_page(
            'South Carolina', 'south-carolina', county,
            'South Carolina Department of Environmental Services (SCDES) — Onsite Wastewater Program',
            contact, sections, sources, verified='August 28, 2026'
        )
        sc_urls.append(url)
        sc_links.append((county, office))

write_hub(
    'South Carolina', 'south-carolina',
    [(county, f'SCDES {office} local office') for county, office in sorted(sc_links)],
    'South Carolina administers onsite wastewater permitting through the South Carolina Department of Environmental Services (SCDES). This expansion maps every county to the current SCDES local office shown in agency county-coverage materials and pairs that contact with the state residential permit, inspection, installer and records process.',
    'All 46 South Carolina counties are included. County-to-office assignments and office phone numbers were validated against current SCDES materials, while the permitting requirements come from the SCDES Septic Tanks program and residential application guidance.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    if '/counties/south-carolina/' not in text:
        promo = '<section><h2>South Carolina</h2><p><a href="/counties/south-carolina/">Browse all 46 verified South Carolina county septic guides →</a></p></section>'
        text = text.replace('</main>', promo + '</main>', 1) if '</main>' in text else text.replace('</body>', promo + '</body>', 1)
        county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/south-carolina/'] + sc_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-28</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'South Carolina expansion complete: +{len(sc_urls)} verified county guides')
exec((ROOT / 'north_dakota_expansion.py').read_text(encoding='utf-8'), globals())
