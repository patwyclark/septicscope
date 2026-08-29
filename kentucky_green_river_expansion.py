# SepticScope Kentucky expansion — Green River District Health Department
# Official-source pages validated against Kentucky CHFS/LRC and GRDHD current guidance.

KY_CHFS = 'https://www.chfs.ky.gov/agencies/dph/dphps/emb/Pages/environmentmgmt.aspx'
KY_LHD = 'https://www.chfs.ky.gov/agencies/dph/dafm/pages/lhd.aspx'
KY_PERMIT_REG = 'https://apps.legislature.ky.gov/law/kar/titles/902/010/110/'
KY_SYSTEM_REG = 'https://apps.legislature.ky.gov/law/kar/titles/902/010/085/'
GRDHD_SEPTIC = 'https://healthdepartment.org/onsite-sewage-septic-systems/'
GRDHD_CONTACT = 'https://healthdepartment.org/contact-locations/'
GRDHD_HOME = 'https://healthdepartment.org/'

GRDHD_COUNTIES = {
    'Daviess': ('270-686-7744', '1600 Breckenridge Street, Owensboro, KY 42303'),
    'Hancock': ('270-927-8803', '175 Harrison Street, Hawesville, KY 42348'),
    'Henderson': ('270-826-3951', '472 Klutey Park Plaza, Henderson, KY 42420'),
    'McLean': ('270-273-3062', '200 Hwy 81 N, Suite 101, Calhoun, KY 42327'),
    'Ohio': ('270-298-3663', '1336 Clay Street, Hartford, KY 42347'),
    'Union': ('270-389-1230', '218 W McElroy Street, Morganfield, KY 42437'),
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
    sources = [
        ('Kentucky CHFS — Onsite Sewage Disposal Systems Program', KY_CHFS),
        ('Kentucky CHFS — Local Health Departments', KY_LHD),
        ('902 KAR 10:110 — Issuance of onsite sewage disposal permits', KY_PERMIT_REG),
        ('902 KAR 10:085 — Kentucky onsite sewage disposal systems', KY_SYSTEM_REG),
        ('Green River District Health Department — Onsite Sewage and Septic Systems', GRDHD_SEPTIC),
        ('Green River District Health Department — county contacts and locations', GRDHD_CONTACT),
        ('Green River District Health Department — official site', GRDHD_HOME),
    ]
    url = write_county_page(
        'Kentucky', 'kentucky', county,
        'Green River District Health Department, administering Kentucky’s local onsite sewage program',
        contact, sections, sources, verified='August 29, 2026'
    )
    ky_grdhd_urls.append(url)
    ky_grdhd_links.append((county, 'Green River District Health Department'))

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
