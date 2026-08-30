# SepticScope Kentucky additional expansion — Northern Kentucky Health Department batch.
# Verified from Kentucky regulations and official NKY Health sources on 2026-08-30.

NKY_SEPTIC = 'https://nkyhealth.org/septic/'
NKY_TRUCKS = 'https://nkyhealth.org/septictrucks/'
KY_PERMIT_REG = 'https://apps.legislature.ky.gov/law/kar/titles/902/010/110/'
KY_SYSTEM_REG = 'https://apps.legislature.ky.gov/law/kar/titles/902/010/085/'

NKY_COUNTIES = ['Boone','Campbell','Grant','Kenton']
nky_urls=[]
for county in NKY_COUNTIES:
    contact=(f'Northern Kentucky Health Department serves {county} County and provides septic-system '
             'site evaluation, permitting, and inspection services for Boone, Campbell, Grant, and Kenton counties.')
    sections=[
        ('Local health department permit authority','Kentucky regulation 902 KAR 10:110 requires an onsite sewage disposal permit from the local health department before a regulated onsite sewage system is constructed, installed, or altered. Northern Kentucky Health Department identifies Boone, Campbell, Grant, and Kenton as the counties covered by its septic inspection program.'),
        ('Site evaluation is the first approval step','Northern Kentucky Health Department directs applicants for a new septic system to submit a site-evaluation application before system approval. The application identifies the property location, requires property boundaries and dimensions to be staked or documented by survey plat, and asks the applicant to show existing structures, wells, ponds, streams, easements, roads, drives, the proposed structure, and the proposed septic area.'),
        ('Soil and site findings determine the system that can be approved','Kentucky 902 KAR 10:085 establishes site-evaluation and system-selection standards based on conditions such as soil depth, restrictive horizons, groundwater, and site limitations. Northern Kentucky Health Department uses the local site evaluation to determine whether the proposed location can support an onsite system and what design path applies.'),
        ('Construction permit goes to a certified installer or qualifying homeowner','Kentucky regulation 902 KAR 10:110 generally limits construction permits to certified installers but allows a homeowner permit when the regulatory conditions are met. The homeowner must personally perform the regulated work except for the specified excavation/backfill and electrical exceptions, and Kentucky limits homeowner construction permits to one in a five-year period except for necessary repair or alteration of that originally permitted system.'),
        ('Permit validity is limited','Kentucky regulation 902 KAR 10:085 states that onsite sewage permits expire one year after issuance unless an extension is granted. Applicants should therefore confirm that an older permit remains active before scheduling construction.'),
        ('Inspection is part of the local program','Northern Kentucky Health Department states that it provides septic-system inspections throughout Boone, Campbell, Grant, and Kenton counties. Septic work should remain available for the required inspection and approval rather than being covered before the local inspector has completed the applicable review.'),
        ('Septage hauling is also locally inspected','Northern Kentucky Health Department separately inspects septic trucks and approved disposal sites operating in the same four counties at least annually. This does not replace the construction permit, but it provides a local compliance check for companies pumping and transporting septage.')
    ]
    sources=[
        ('Northern Kentucky Health Department — Septic System Inspections', NKY_SEPTIC),
        ('Northern Kentucky Health Department — Septic Trucks and Disposal Sites', NKY_TRUCKS),
        ('Kentucky 902 KAR 10:110 — onsite sewage permit issuance', KY_PERMIT_REG),
        ('Kentucky 902 KAR 10:085 — onsite sewage systems and site evaluation', KY_SYSTEM_REG),
    ]
    nky_urls.append(write_county_page('Kentucky','kentucky',county,'Northern Kentucky Health Department — Environmental Health / Septic Program',contact,sections,sources,verified='August 30, 2026'))

# Rebuild the Kentucky hub to include the original Barren River District batch plus this verified district.
existing=[(c,'Barren River District Health Department') for c in ky_links]
added=[(c,'Northern Kentucky Health Department') for c in NKY_COUNTIES]
write_hub(
    'Kentucky','kentucky',sorted(existing+added),
    'Kentucky requires onsite sewage disposal permits through local health departments. SepticScope adds counties district-by-district only after the local permitting authority and current process are supported by official health-department and state regulatory sources.',
    'Kentucky now includes the eight verified Barren River District counties plus Boone, Campbell, Grant, and Kenton counties served by Northern Kentucky Health Department. Other counties remain on the nationwide lookup layer until their local program is independently validated.'
)

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    text=text.replace('Browse the first 8 verified Kentucky county septic guides →','Browse 12 verified Kentucky county septic guides →')
    county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in nky_urls if u not in sm)
    if entries:
        sitemap.write_text(sm.replace('</urlset>',entries+'</urlset>'),encoding='utf-8')

for county in NKY_COUNTIES:
    p=OUTPUT/'counties'/'kentucky'/slugify(county)/'index.html'
    t=p.read_text(encoding='utf-8')
    if 'Local septic rules not yet verified' in t or 'OFFICIAL SOURCES CHECKED' not in t.upper() or 'Official sources' not in t:
        raise RuntimeError(f'Northern Kentucky verified page failed: {county}')

print(f'Northern Kentucky expansion complete: +{len(nky_urls)} verified county guides')
