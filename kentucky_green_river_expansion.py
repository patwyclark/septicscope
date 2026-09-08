# SepticScope Kentucky expansion — Green River District Health Department
# Official-source pages validated against Kentucky CHFS/LRC and GRDHD current guidance.

KY_CHFS = 'https://www.chfs.ky.gov/agencies/dph/dphps/emb/Pages/environmentmgmt.aspx'
KY_LHD = 'https://www.chfs.ky.gov/agencies/dph/dafm/pages/lhd.aspx'
KY_PERMIT_REG = 'https://apps.legislature.ky.gov/law/kar/titles/902/010/110/'
KY_SYSTEM_REG = 'https://apps.legislature.ky.gov/law/kar/titles/902/010/085/'
GRDHD_SEPTIC = 'https://healthdepartment.org/onsite-sewage-septic-systems/'
GRDHD_CONTACT = 'https://healthdepartment.org/contact-locations/'
GRDHD_HOME = 'https://healthdepartment.org/'
GRDHD_HENDERSON = 'https://healthdepartment.org/location/henderson-county-health-center/'
BRDHD_EDMONSON = 'https://www.barrenriverhealth.org/locations/edmonson-county-health-department'

GRDHD_COUNTIES = {
    'Daviess': ('270-686-7744', '1600 Breckenridge Street, Owensboro, KY 42303'),
    'Hancock': ('270-927-8803', '175 Harrison Street, Hawesville, KY 42348'),
    'Henderson': ('270-826-3951', '472 Klutey Park Plaza, Henderson, KY 42420'),
    'McLean': ('270-273-3062', '200 Hwy 81 N, Suite 101, Calhoun, KY 42327'),
    'Ohio': ('270-298-3663', '1336 Clay Street, Hartford, KY 42347'),
    'Union': ('270-389-1230', '218 W McElroy Street, Morganfield, KY 42409'),
    'Webster': ('270-639-9315', '80 Clayton Avenue, Dixon, KY 42409'),
}

ky_grdhd_urls = []
ky_grdhd_links = []
for county, (phone, address) in GRDHD_COUNTIES.items():
    contact = (
        f'Green River District Health Department serves {html.escape(county)} County. '
        f'County health center: {html.escape(phone)}; {html.escape(address)}. '
        'GRDHD directs applicants to apply for the site evaluation through their county health center.'
    )
    sections = [
        ('Start with a site evaluation',
         'Green River District Health Department states that a site evaluation is required before construction or septic installation when a property is not served by municipal sewer. An Environmental Health professional evaluates soil texture and structure, restrictive layers, and site conditions that can affect onsite wastewater disposal.'),
        ('What to bring for the evaluation',
         'GRDHD instructs applicants to apply through the county health center and bring a location map plus a site drawing showing property lines and lot dimensions, structures, wells, ponds, streams, gullies, swamps or similar features, and easements, roads, driveways, or rights-of-way. A plat or survey and floor plans or blueprints may also be required depending on the county and project.'),
        ('Published district site-evaluation fee',
         'GRDHD currently publishes a $200 site-evaluation fee and directs applicants to confirm current procedures with their county health center. Fees and forms can change, so verify the amount before submitting an application.'),
        ('Permit before construction, installation, or alteration',
         'Kentucky regulation 902 KAR 10:110 provides that a person may not construct, install, or alter a regulated onsite sewage disposal system without first obtaining an onsite sewage disposal permit from the local health department. The regulation requires the construction application and applicable state and local-board fees.'),
        ('Who may receive the construction permit',
         'Kentucky generally issues permits to certified onsite sewage installers. A qualifying homeowner may receive a homeowner permit if the regulatory conditions are met, including personally performing the work except for specifically allowed excavation, backfilling, or licensed electrical work.'),
        ('District review and inspection',
         'GRDHD states that after a site is approved, the health department can issue the septic construction permit to a certified contractor and inspect the installation. Kentucky’s statewide program likewise states that local health department septic inspectors perform site evaluations and inspections.'),
        ('Permit duration and site-specific limitations',
         'Kentucky regulation 902 KAR 10:085 states that the construction permit is issued by a certified inspector and expires one year from issuance unless an extension is granted. The approved system depends on the site evaluation, including soil, slope, groundwater, restrictive horizons, available area, setbacks, and other parcel-specific conditions.'),
    ]
    if county == 'Daviess':
        sections.append(
            ('Residential septic tank capacity is tied to bedroom count',
             'Kentucky 902 KAR 10:085 Section 6 sets minimum working liquid capacity for a single-family residential septic tank by bedroom count. Table 2 requires at least 1,000 gallons for three or fewer bedrooms without a garbage disposal (1,250 gallons with one), 1,250 or 1,500 gallons for four bedrooms, and 1,500 or 1,750 gallons for five bedrooms; each additional bedroom adds 250 gallons. These are statewide minimums, not a substitute for the Daviess County site evaluation or permitted design. Soil group, site conditions, pretreatment requirements, and other parcel-specific factors can change what Green River District Health Department approves.')
        )
    if county == 'Henderson':
        sections.append(
            ('Henderson County local starting point',
             'GRDHD directs site-evaluation applicants to apply in person at their county health center and to contact the Environmentalist at the local center for onsite-sewage questions. For Henderson County, GRDHD lists the Henderson County Health Center at 472 Klutey Park Plaza, Henderson, KY 42420, phone 270-826-3951, with public hours of 7:45 a.m. to 4:30 p.m. Monday through Friday. Confirm current Environmental Health availability and any county-specific plat, survey, or floor-plan requirements before making a trip or submitting plans.')
        )
    sources = [
        ('Kentucky CHFS — Onsite Sewage Disposal Systems Program', KY_CHFS),
        ('Kentucky CHFS — Local Health Departments', KY_LHD),
        ('902 KAR 10:110 — Issuance of onsite sewage disposal permits', KY_PERMIT_REG),
        ('902 KAR 10:085 — Kentucky onsite sewage disposal systems', KY_SYSTEM_REG),
        ('Green River District Health Department — Onsite Sewage and Septic Systems', GRDHD_SEPTIC),
        ('Green River District Health Department — county contacts and locations', GRDHD_CONTACT),
        ('Green River District Health Department — official site', GRDHD_HOME),
    ]
    if county == 'Henderson':
        sources.append(
            ('Green River District Health Department — Henderson County Health Center', GRDHD_HENDERSON)
        )
    if county == 'Daviess':
        verified_date = 'September 7, 2026'
    elif county == 'Henderson':
        verified_date = 'September 8, 2026'
    else:
        verified_date = 'August 29, 2026'
    url = write_county_page(
        'Kentucky', 'kentucky', county,
        'Green River District Health Department, administering Kentucky’s local onsite sewage program',
        contact, sections, sources, verified=verified_date
    )
    ky_grdhd_urls.append(url)
    ky_grdhd_links.append((county, 'Green River District Health Department'))

# Add one county-specific quality improvement to the earlier Barren River batch.
# This directly addresses the quality gate's repeated-county-pattern warning without
# inventing local rules: the contact, forms, and office URL are published by BRDHD.
edmonson_page = OUTPUT / 'counties' / 'kentucky' / 'edmonson' / 'index.html'
if not edmonson_page.exists():
    raise RuntimeError('Expected verified Edmonson County page is missing')
edmonson_text = edmonson_page.read_text(encoding='utf-8')
edmonson_heading = 'Edmonson County onsite-sewage contact and forms'
if edmonson_heading not in edmonson_text:
    edmonson_section = (
        '<h2>Edmonson County onsite-sewage contact and forms</h2>'
        '<p>Barren River District Health Department currently lists Brenna Wilson at '
        '270-597-2194 ext. 302 for onsite-sewage work in Edmonson and Warren counties. '
        'The district’s onsite-sewage page provides the DFS-319 site-evaluation application, '
        'DFS-326 existing-system application, DFS-330 installer affidavit, and owner affidavit. '
        'For an Edmonson County project, start with the county health department and confirm '
        'which forms and site-evaluation steps apply before submitting or scheduling work.</p>'
    )
    marker = '<h2>Official sources</h2>'
    if marker not in edmonson_text:
        raise RuntimeError('Edmonson County official-sources marker is missing')
    edmonson_text = edmonson_text.replace(marker, edmonson_section + marker, 1)
location_source = (
    f'<li><a href="{html.escape(BRDHD_EDMONSON)}" rel="nofollow">'
    'Barren River District Health Department — Edmonson County Health Department'
    '</a></li>'
)
sources_marker = '<h2>Official sources</h2><ul>'
if BRDHD_EDMONSON not in edmonson_text:
    if sources_marker not in edmonson_text:
        raise RuntimeError('Edmonson County official-source list is missing')
    edmonson_text = edmonson_text.replace(sources_marker, sources_marker + location_source, 1)
edmonson_text = edmonson_text.replace(
    'Official sources checked August 28, 2026',
    'Official sources checked September 7, 2026',
    1,
)
edmonson_page.write_text(edmonson_text, encoding='utf-8')
if edmonson_heading not in edmonson_text or BRDHD_EDMONSON not in edmonson_text:
    raise RuntimeError('Edmonson County quality enhancement failed')

# Rebuild the Kentucky hub so it retains the prior Barren River batch and adds Green River.
ky_all_links = [
    ('Barren', 'Barren River District Health Department'),
    ('Butler', 'Barren River District Health Department'),
    ('Edmonson', 'Barren River District Health Department'),
    ('Hart', 'Barren River District Health Department'),
    ('Logan', 'Barren River District Health Department'),
    ('Metcalfe', 'Barren River District Health Department'),
    ('Simpson', 'Barren River District Health Department'),
    ('Warren', 'Barren River District Health Department'),
] + ky_grdhd_links
write_hub(
    'Kentucky', 'kentucky',
    sorted(ky_all_links),
    'Kentucky administers onsite sewage disposal through local health departments. Local certified inspectors perform parcel-specific site evaluations and inspections, while statewide regulations establish the permit, installer, design, and site-evaluation framework.',
    'This hub currently includes 15 verified counties across the Barren River and Green River public-health districts. Each county guide identifies the applicable local health authority and links to current state and district sources.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    old = 'Browse 8 verified Kentucky county septic guides'
    if old in text:
        text = text.replace(old, 'Browse 15 verified Kentucky county septic guides')
        county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ky_grdhd_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'Kentucky Green River expansion complete: +{len(ky_grdhd_urls)} verified county guides')

# Continue with the next validated local-authority batch.
exec((ROOT / 'virginia_rappahannock_rapidan_expansion.py').read_text(encoding='utf-8'), globals())
