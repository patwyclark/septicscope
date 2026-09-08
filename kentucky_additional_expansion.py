# SepticScope Kentucky additional expansion — Northern Kentucky Health Department batch.
# Verified from Kentucky regulations and official local-health-department sources.

NKY_SEPTIC = 'https://nkyhealth.org/septic/'
NKY_TRUCKS = 'https://nkyhealth.org/septictrucks/'
NKY_REQUESTS = 'https://nkyhealth.org/requests/'
NKY_LOCATIONS = 'https://nkyhealth.org/ourlocations/'
KY_PERMIT_REG = 'https://apps.legislature.ky.gov/law/kar/titles/902/010/110/'
KY_SYSTEM_REG = 'https://apps.legislature.ky.gov/law/kar/titles/902/010/085/'
KY_ONSITE_PROGRAM = 'https://www.chfs.ky.gov/agencies/dph/dphps/emb/Pages/environmentmgmt.aspx'
FAYETTE_ONSITE = 'https://www.lfchd.org/onsite-sewage-septic-tank-program/'
FAYETTE_PERMITS = 'https://www.lfchd.org/get-a-permit/'

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
    if county == 'Campbell':
        sections.append(
            ('Residential septic tank capacity is tied to bedroom count',
             'Kentucky 902 KAR 10:085 Section 6 sets minimum working liquid capacity for a single-family residential septic tank by bedroom count. Table 2 requires at least 1,000 gallons for three or fewer bedrooms without a garbage disposal (1,250 gallons with one), 1,250 or 1,500 gallons for four bedrooms, and 1,500 or 1,750 gallons for five bedrooms; each additional bedroom adds 250 gallons. These are state minimums, not a substitute for the permitted design: Northern Kentucky Health Department should confirm the final system because site conditions, soil group, and approved pretreatment type can change what is required.')
        )
    if county == 'Grant':
        sections.extend([
            ('Grant County local starting point',
             'Northern Kentucky Health Department lists the Grant County Health Center at 234 Barnes Road, Williamstown, KY 41097, with a published phone number of 859-824-5074. Use the septic program for site-evaluation, permit, and inspection questions; the county health-center listing is a useful local starting point when you need help reaching the appropriate environmental-health staff.'),
            ('How to request existing septic records',
             'Northern Kentucky Health Department says an onsite-septic public-record request requires both its Open Records Request Form and the Onsite Sewage Request for Public Records Attachment Form. This is the documented records route for owners, buyers, inspectors, and contractors trying to locate an existing septic permit or related onsite-sewage record in Grant County; follow the current submission instructions on the Health Department records page rather than relying on an informal search alone.')
        ])
    if county == 'Kenton':
        sections.extend([
            ('Kenton County local starting point',
             'Northern Kentucky Health Department lists the Kenton County Health Center at 1415 James Simpson Jr. Way, Covington, KY 41011, with a published phone number of 859-431-3345. Septic permitting and inspection work is handled through the district Environmental Health and Safety program; NKY Health says its District Office at 8001 Veterans Memorial Drive in Florence is where environmental-health permit and inspection fees, plans, forms, and associated costs can be handled.'),
            ('How to request an existing Kenton County septic record',
             'Northern Kentucky Health Department says an onsite-septic public-record request requires both its Open Records Request Form and the Onsite Sewage Request for Public Records Attachment Form. The department directs completed forms to its records contact or to the District Office at 8001 Veterans Memorial Drive, Florence, KY 41042. This is the documented route for owners, buyers, inspectors, and contractors trying to locate an existing onsite-sewage record in Kenton County.')
        ])
    sources=[
        ('Northern Kentucky Health Department — Septic System Inspections', NKY_SEPTIC),
        ('Northern Kentucky Health Department — Septic Trucks and Disposal Sites', NKY_TRUCKS),
        ('Kentucky 902 KAR 10:110 — onsite sewage permit issuance', KY_PERMIT_REG),
        ('Kentucky 902 KAR 10:085 — onsite sewage systems and site evaluation', KY_SYSTEM_REG),
    ]
    if county in {'Grant','Kenton'}:
        sources.extend([
            ('Northern Kentucky Health Department — locations and county health centers', NKY_LOCATIONS),
            ('Northern Kentucky Health Department — onsite septic public-record requests', NKY_REQUESTS),
        ])
    nky_urls.append(write_county_page('Kentucky','kentucky',county,'Northern Kentucky Health Department — Environmental Health / Septic Program',contact,sections,sources,verified='September 8, 2026' if county in {'Grant','Kenton'} else 'August 30, 2026'))

# Lexington-Fayette has its own local health department and publishes a specific onsite
# sewage workflow. Keep this separate from the Northern Kentucky district batch so the
# guide never implies that NKY Health has jurisdiction in Fayette County.
fayette_contact=(
    'Lexington-Fayette County Health Department Environmental Health administers the local onsite '
    'sewage program. The department lists 650 Newtown Pike, Lexington, KY 40508; Environmental '
    'Health questions at 859-231-9791; onsite@lfchd.org; and current onsite-program hours of '
    'Tuesday and Thursday, 8:00-9:30 a.m. Confirm current hours before traveling.'
)
fayette_sections=[
    ('Fayette County requires the local health department permit',
     'Lexington-Fayette County Health Department states that all individual sewage disposal systems installed in Fayette County must be permitted through the health department. Kentucky 902 KAR 10:110 likewise requires a local-health-department onsite sewage permit before a regulated system is constructed, installed, or altered.'),
    ('Start with the lot and soil evaluation',
     'When a lot-approval application is received, Lexington-Fayette County Health Department says an environmentalist performs a site evaluation to determine whether the property is suitable and where the sewage system can be located. The department says that evaluation also determines the design, type, and size of the system, so an online sizing rule should not be treated as the permitted design.'),
    ('Existing-system evaluations are available for property transactions',
     'The local onsite-sewage program says it also performs lot evaluations on properties that are for sale to check the functioning of existing onsite sewage systems. Owners and buyers should contact Environmental Health for the current request process and any access or documentation requirements before relying on an older system record.'),
    ('Installation still follows Kentucky statewide permit rules',
     'Kentucky 902 KAR 10:110 generally issues construction permits to certified installers, while a qualifying homeowner may receive a homeowner permit when the regulation’s conditions are met. Kentucky CHFS says local health department inspectors perform site evaluations and inspections and that certified Kentucky installers must install systems based on the site evaluation.'),
    ('Report onsite sewage problems to the local program',
     'Lexington-Fayette County Health Department says its onsite sewage program investigates public complaints concerning onsite sewage problems. Use the current Environmental Health contact information for a Fayette County sewage complaint or project-specific question.')
]
fayette_sources=[
    ('Lexington-Fayette County Health Department — Onsite Sewage Program', FAYETTE_ONSITE),
    ('Lexington-Fayette County Health Department — Environmental Health permits', FAYETTE_PERMITS),
    ('Kentucky CHFS — Onsite Sewage Disposal Systems Program', KY_ONSITE_PROGRAM),
    ('Kentucky 902 KAR 10:110 — onsite sewage permit issuance', KY_PERMIT_REG),
    ('Kentucky 902 KAR 10:085 — onsite sewage systems and site evaluation', KY_SYSTEM_REG),
]
fayette_url=write_county_page(
    'Kentucky','kentucky','Fayette',
    'Lexington-Fayette County Health Department — Environmental Health / Onsite Sewage Program',
    fayette_contact,fayette_sections,fayette_sources,verified='September 8, 2026'
)

# Do not rebuild the Kentucky hub here. Earlier Kentucky expansion layers already
# maintain the complete statewide county index. Replacing that hub with only this
# verified subset would drop existing county links and break the nationwide audit.

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    dated_urls=[(u,'2026-08-30') for u in nky_urls] + [(fayette_url,'2026-09-08')]
    entries=''.join(f'<url><loc>{u}</loc><lastmod>{lastmod}</lastmod></url>' for u,lastmod in dated_urls if u not in sm)
    if entries:
        sitemap.write_text(sm.replace('</urlset>',entries+'</urlset>'),encoding='utf-8')

for county in NKY_COUNTIES + ['Fayette']:
    p=OUTPUT/'counties'/'kentucky'/slugify(county)/'index.html'
    t=p.read_text(encoding='utf-8')
    if 'Local septic rules not yet verified' in t or 'OFFICIAL SOURCES CHECKED' not in t.upper() or 'Official sources' not in t:
        raise RuntimeError(f'Kentucky verified page failed: {county}')

print(f'Northern Kentucky expansion complete: +{len(nky_urls)} verified county guides')
print('Lexington-Fayette County quality expansion complete: +1 verified county guide')
exec((ROOT / 'illinois_expansion.py').read_text(encoding='utf-8'), globals())
