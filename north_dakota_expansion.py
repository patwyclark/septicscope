# SepticScope North Dakota expansion — Lake Region District Health Unit
# Official-source county pages validated against NDDEQ and LRDHU current guidance.

ND_DEQ = 'https://deq.nd.gov/WQ/2_NDPDES_Permits/7_SepticSystems/Septic.aspx'
ND_CODE = 'https://ndlegis.gov/cencode/t23-1c07-1.html'
ND_HHS_LOCAL = 'https://www.hhs.nd.gov/local-public-healthsites'
LRDHU_ENV = 'https://www.lrdhu.com/environmentalhealth'
LRDHU_LOCATIONS = 'https://www.lrdhu.com/locations'
LRDHU_HOME = 'https://www.lrdhu.com/'

# LRDHU Environmental Health explicitly states that its onsite sewage program serves
# Benson, Cavalier, Eddy, Pierce, Ramsey, Rolette, and Towner counties.
ND_LAKE_REGION_COUNTIES = ['Benson', 'Cavalier', 'Eddy', 'Pierce', 'Ramsey', 'Rolette', 'Towner']

nd_urls = []
nd_links = []
for county in ND_LAKE_REGION_COUNTIES:
    contact = (
        'Lake Region District Health Unit (LRDHU), Environmental Health Division — '
        '524 4th Ave NE Unit 9, Devils Lake, ND 58301; main phone 701-662-7040. '
        f'LRDHU states that its Environmental Health program administers onsite sewage treatment systems in {html.escape(county)} County.'
    )

    county_specific = ''
    if county in {'Cavalier', 'Rolette', 'Towner'}:
        county_specific = (
            f'LRDHU separately publishes {html.escape(county)} County onsite sewage treatment system regulations on its Environmental Health page. '
            'Because local requirements can supplement statewide standards, applicants should review that county-specific regulation before finalizing a design or installation schedule.'
        )
    else:
        county_specific = (
            'LRDHU publishes regional onsite sewage treatment regulations and application materials for this county. '
            'Confirm the current fee, form version, and any parcel-specific conditions with Environmental Health before work begins.'
        )

    sections = [
        ('Local permit is required before installation work',
         'North Dakota DEQ states that onsite wastewater installers must obtain a permit from the applicable local public health unit before beginning work. State law defines a permit as authorization from a local public health unit or other political subdivision for a specific site. In this county, LRDHU is the local Environmental Health program administering onsite sewage treatment system permits.'),
        ('New systems and repairs are both regulated',
         'LRDHU states that it licenses and permits all new onsite sewage treatment systems and repairs to existing systems, including septic tanks, drain fields, cesspools, and holding tanks. Do not assume a repair is exempt from local review.'),
        ('Application, legal description, site plan, and payment',
         'LRDHU’s current septic application procedure requires a completed permit application with the property legal description, owner contact information, a drawing of the current site and proposed system, the owner or authorized property representative’s signature, and payment. The contractor or installer is not the person who signs as the owner representative under that procedure.'),
        ('Preliminary permit and field verification',
         'After receiving the application and payment, LRDHU may issue a preliminary permit based on the submitted information. Once onsite, the installer must verify required setbacks and follow the approved permit. LRDHU’s published procedure specifically calls for a 100-foot setback from high-water marks of sloughs, lakes, rivers, creeks, and similar waters; proposed changes must be reviewed and approved by the inspector.'),
        ('Installation documentation and as-built record',
         'LRDHU’s procedure calls for installation photographs when requested and an as-built construction document after installation. The as-built is to be submitted within 30 days of installation and becomes part of the permit file. Existing permit copies can be requested from LRDHU.'),
        ('Installer licensing now has a state component',
         'North Dakota DEQ oversees licensing of onsite wastewater treatment system installers under NDCC Chapter 23.1-07.1. DEQ states that installers must hold the required state license and also secure the local public-health permit. A property owner installing a system on the owner’s own premises for the owner’s use is exempt from the state installer-license requirement under the statute, but the site-specific permit requirement still applies.'),
        ('County-specific and local rules', county_specific),
    ]

    sources = [
        ('North Dakota DEQ — On-Site Wastewater Treatment Systems', ND_DEQ),
        ('North Dakota Century Code Chapter 23.1-07.1 — Onsite Wastewater Treatment Systems', ND_CODE),
        ('North Dakota HHS — Local Public Health Units', ND_HHS_LOCAL),
        ('Lake Region District Health Unit — Environmental Health / onsite sewer treatment systems', LRDHU_ENV),
        ('Lake Region District Health Unit — locations and contacts', LRDHU_LOCATIONS),
        ('Lake Region District Health Unit — official site', LRDHU_HOME),
    ]

    url = write_county_page(
        'North Dakota', 'north-dakota', county,
        'Lake Region District Health Unit (LRDHU) Environmental Health, with North Dakota Department of Environmental Quality statewide installer oversight',
        contact, sections, sources, verified='August 29, 2026'
    )
    nd_urls.append(url)
    nd_links.append((county, 'Lake Region District Health Unit Environmental Health'))

write_hub(
    'North Dakota', 'north-dakota',
    [(county, authority) for county, authority in sorted(nd_links)],
    'North Dakota uses local public health units for site-specific onsite wastewater permits while the North Dakota Department of Environmental Quality provides statewide installer licensing and program oversight. This batch covers the seven counties for which Lake Region District Health Unit explicitly identifies itself as the Environmental Health authority for onsite sewage treatment systems.',
    'Included counties: Benson, Cavalier, Eddy, Pierce, Ramsey, Rolette, and Towner. LRDHU publishes a regional septic application process and identifies all seven counties in its Environmental Health service area; it also publishes separate county OSTS regulations for Cavalier, Rolette, and Towner counties.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    if '/counties/north-dakota/' not in text:
        promo = '<section><h2>North Dakota</h2><p><a href="/counties/north-dakota/">Browse 7 verified North Dakota county septic guides →</a></p></section>'
        text = text.replace('</main>', promo + '</main>', 1) if '</main>' in text else text.replace('</body>', promo + '</body>', 1)
        county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/north-dakota/'] + nd_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'North Dakota expansion complete: +{len(nd_urls)} verified county guides')
