# SepticScope Indiana expansion — verified county batch.
# Verified from Indiana Department of Health and official county/local health sources on 2026-08-30.

IN_STATE = 'https://www.in.gov/health/eph/onsite-sewage-systems-program/'
IN_COUNTIES = [
    {
        'county': 'Hamilton',
        'authority': 'Hamilton County Health Department — On-Site Sewage Disposal Program',
        'contact': 'Hamilton County Health Department: 317-776-8500; 18030 Foundation Drive, Suite A, Noblesville, IN 46060.',
        'sources': [
            ('Hamilton County — On-Site Sewage Disposal Program', 'https://www.hamiltoncounty.in.gov/298/Sewage-Disposal-Program'),
            ('Hamilton County — Septic Permits', 'https://www.hamiltoncounty.in.gov/300/Permits'),
            ('Hamilton County — Health Department permits and forms', 'https://www.hamiltoncounty.in.gov/1601/Health-Dept-Permits-Applications-and-For'),
        ],
        'sections': [
            ('County Health performs site evaluation, permitting, and inspection', 'Hamilton County states that its On-Site Sewage Disposal Program conducts site evaluations, issues permits, and performs inspections to ensure onsite sewage systems are properly designed and installed.'),
            ('System sizing is tied to bedrooms and soil loading rate', 'Hamilton County says residential onsite system sizing uses 150 gallons per day per bedroom or bedroom equivalent. The design flow is divided by the applicable soil-loading rate under Indiana Rule 410 IAC 6-8.3.'),
            ('A registered soil scientist establishes the loading rate', 'The county requires an onsite soil evaluation by a Registered Soil Scientist to establish the soil-loading rate used in system design. Applicants are directed to the Health Department for the current lists of registered soil scientists and installers.'),
            ('County maintains separate forms for construction, abandonment, and holding tanks', 'Hamilton County publishes a septic permit application, new-construction procedures, an onsite sewage system abandonment form, and a permanent holding-tank application. Property owners should use the form that matches the proposed work rather than assuming an existing-system repair or abandonment is covered by a new-construction permit.'),
        ],
    },
    {
        'county': 'Marshall',
        'authority': 'Marshall County Health Department — Environmental Health / Onsite Sewage Systems',
        'contact': 'Marshall County Health Department Environmental Health administers residential onsite sewage permitting and inspection in Marshall County.',
        'sources': [
            ('Marshall County Health Department — Onsite Sewage Systems', 'https://www.in.gov/localhealth/marshallcounty/environmental/onsite-sewage-systems-septic-system/'),
        ],
        'sections': [
            ('County Health requires a soil profile for new construction and replacement', 'Marshall County directs applicants for new construction or system replacement to obtain a soil profile analysis from an Indiana-registered soil scientist. The county states that the scientist performs at least three soil borings in the proposed soil absorption field area and submits the analysis to the owner and Health Department.'),
            ('Soil profile analyses have a county-stated validity period', 'Marshall County states that a soil profile analysis is valid for seven years so long as the tested area remains undisturbed. If the proposed field area is unsuitable, additional testing is required.'),
            ('Commercial projects require state review plus a local county permit', 'For commercial septic systems, Marshall County directs applicants to Indiana Department of Health plan review and states that a Marshall County onsite sewage system permit is also required.'),
            ('Some newer technologies require operating permits', 'Marshall County states that certain newer onsite technologies require continuing operating permits and maintenance. Conventional systems, flood- and pressure-dose systems, and mounds generally do not require operating permits under the county guidance, while newer technologies may.'),
            ('Repairs should be cleared with County Health before proceeding', 'Marshall County directs owners to contact the Health Department when an onsite sewage system needs repair so staff can determine whether the repair requires a soil profile analysis and the applicable permit path.'),
        ],
    },
    {
        'county': 'Grant',
        'authority': 'Grant County Health Department — Environmental Division',
        'contact': 'Grant County Health Department Environmental Division administers residential onsite septic permits and installer registration in Grant County.',
        'sources': [
            ('Grant County Health Department — Residential Onsite Septic System', 'https://www.in.gov/localhealth/grantcounty/environmental-division/registered-installers/'),
        ],
        'sections': [
            ('County permit is required before construction, repair, replacement, or alteration', 'Grant County states that a septic permit from the Health Department is required before repairing, replacing, constructing, or otherwise altering a septic system. The county treats plumbing beyond two feet outside the foundation as part of the septic system for this purpose.'),
            ('County publishes separate permit categories and fees', 'Grant County publishes distinct current permit categories for a septic application, new construction, replacement systems, repairs, and holding-tank permits. Because fee schedules can change, applicants should confirm the current county amount before filing.'),
            ('Installers must satisfy county registration requirements', 'Grant County requires septic installers to register with the Health Department. The county accepts specified credentials such as IOWPA certification, passing the Grant County installer exam, or qualifying registration in another Indiana county with supporting documentation, subject to its current registration rules.'),
            ('County identifies off-lot discharge configurations as unlawful', 'Grant County explains that a lawful residential onsite sewage disposal system includes a septic tank and soil absorption system. Systems discharging to field tile, drains, creeks, streams, roadside ditches, or similar off-lot outlets are not treated as lawful residential septic systems under the county guidance.'),
        ],
    },
]

in_urls=[]
in_links=[]
for d in IN_COUNTIES:
    sources=[('Indiana Department of Health — Onsite Sewage Systems Program', IN_STATE)] + d['sources']
    sections=[
        ('Indiana state and local framework', 'The Indiana Department of Health states that local health departments issue permits for new and repaired residential onsite sewage systems. State rules establish the technical framework, while county health departments perform local permit review and inspections and may administer additional local procedures.')
    ] + d['sections']
    in_urls.append(write_county_page('Indiana','indiana',d['county'],d['authority'],d['contact'],sections,sources,verified='August 30, 2026'))
    in_links.append((d['county'], d['authority']))

write_hub(
    'Indiana','indiana',sorted(in_links),
    'Indiana Department of Health establishes the statewide residential onsite sewage framework, while local health departments issue permits and inspect systems. These guides are limited to counties with current official local guidance supporting the permitting authority and meaningful county-specific procedures.',
    'This verified Indiana batch covers Hamilton, Marshall, and Grant counties. SepticScope does not extrapolate one county’s soil-testing, installer-registration, operating-permit, repair, fee, or application requirements to other Indiana counties.'
)

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    if '/counties/indiana/' not in text:
        promo='<section><h2>Indiana</h2><p><a href="/counties/indiana/">Browse 3 verified Indiana county septic guides →</a></p></section>'
        text=text.replace('</main>',promo+'</main>',1) if '</main>' in text else text.replace('</body>',promo+'</body>',1)
        county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
new_urls=['https://septicscope.com/counties/indiana/']+in_urls
if sitemap.exists(): sm=sitemap.read_text(encoding='utf-8')
else: sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm=sm.replace('</urlset>',entries+'</urlset>')
    sitemap.write_text(sm,encoding='utf-8')

print(f'Indiana expansion complete: +{len(in_urls)} verified county guides')
