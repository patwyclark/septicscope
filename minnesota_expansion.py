# SepticScope Minnesota expansion — verified county batch.
# Verified from Minnesota Pollution Control Agency and official county sources on 2026-08-30.

MN_MPCA = 'https://www.pca.state.mn.us/business-with-us/local-septic-system-programs'
MN_COUNTIES = [
    {
        'county': 'Washington',
        'authority': 'Washington County Public Health & Environment — Septic / SSTS Program',
        'contact': 'Washington County Public Health & Environment — Septic: 651-430-6655; Government Center, 14949 62nd Street North, Stillwater, MN 55082.',
        'sources': [
            ('Washington County — Subsurface Sewage Treatment Systems', 'https://www.co.washington.mn.us/septic'),
        ],
        'sections': [
            ('County permits are required for new systems, repairs, replacements, and certain building changes', 'Washington County requires an SSTS permit to install new septic tanks or soil treatment areas, repair or replace an existing system or component, or change the use, expand, or modify the building or facility served by the system.'),
            ('Installation work must remain available for county inspection', 'Washington County requires installation inspections and directs applicants to schedule them at least 24 hours in advance. Soil treatment areas, rough-up/scarification work, and specified tanks require inspection before backfilling or before the next construction step described by the county.'),
            ('Property transfers generally trigger a compliance inspection', 'Washington County states that a compliance inspection is required before selling or transferring a property with a septic system unless a qualifying inspection was completed within the previous three years or a new system was installed within the previous five years and has a valid certificate of compliance.'),
            ('Type IV and Type V systems require operating permits', 'Washington County requires an operating permit for Type IV or Type V systems and publishes separate initial and annual renewal materials for residential and commercial systems.'),
            ('Standalone abandonment has its own county process', 'When a septic system is abandoned without a replacement installation, Washington County requires a septic abandonment application, the applicable county fee, the MPCA abandonment reporting form, and documentation of the abandonment. Abandonment performed as part of a permitted replacement is handled within that installation permit.'),
        ],
    },
    {
        'county': 'Hennepin',
        'authority': 'Hennepin County Environmental Health — SSTS Program, except cities that administer their own septic programs',
        'contact': 'Hennepin County Environmental Health administers most septic systems in the county. The county lists Dayton, Hopkins, Independence, Loretto, Medina, New Hope, Orono, Richfield, St. Louis Park, and Woodland as cities with their own septic programs; properties there should contact the city directly.',
        'sources': [
            ('Hennepin County — Septic Systems', 'https://www.hennepincounty.gov/septic'),
            ('Hennepin County — Subsurface Sewage Treatment Systems Standards Ordinance', 'https://www.hennepincounty.gov/government/about/ordinances/solid-waste-ordinances/subsurface-sewage-treatment-systems-standards-ordinance'),
        ],
        'sections': [
            ('Hennepin County regulates most, but not all, septic systems in the county', 'Hennepin County states that it regulates most septic systems, including inspections and enforcement, but identifies a specific set of cities that operate their own septic programs. SepticScope therefore does not treat the county as the permit authority for every parcel.'),
            ('A county permit is required before most system construction or alteration in county jurisdiction', 'The county ordinance requires a permit before an SSTS within Hennepin County jurisdiction is installed, replaced, abandoned, altered, repaired, rejuvenated, or extended. The ordinance also lists narrow maintenance exceptions such as certain pump, baffle, inspection-pipe, cover, and line repairs.'),
            ('County septic permits expire after 12 months', 'Hennepin County Ordinance Section 6.1 states that septic permits are not transferable as to person or place and expire 12 months after issuance.'),
            ('Certain systems require an annual operating permit', 'Hennepin County requires operating permits for holding tanks, Type IV and Type V systems, and midsized SSTS covered by Minnesota Rule Chapter 7081. The ordinance states that sewage cannot be discharged to a system requiring an operating permit until installation is certified, final record drawings are received, and a valid operating permit is issued. Operating permits are valid for 12 months.'),
            ('Standalone septic abandonment requires county documentation in county jurisdiction', 'Hennepin County provides an abandonment permit process for systems under county jurisdiction when no new construction is involved. The county directs owners to obtain the permit, have the tank pumped by a licensed pumper/maintainer, document the tank being crushed, filled, or removed, and submit the abandonment reporting form.'),
        ],
    },
    {
        'county': 'Dakota',
        'authority': 'Dakota County Environmental Resources for specified jurisdictions; otherwise the applicable city or township SSTS program',
        'contact': 'Dakota County Environmental Resources: 952-891-7557; environ@co.dakota.mn.us. Dakota County states that it directly regulates Hastings, Randolph, New Trier, Randolph Township, Waterford Township, and septic systems in shoreland/floodplain areas or unincorporated portions; most other cities and townships administer their own programs.',
        'sources': [
            ('Dakota County — Septic Systems', 'https://dakotacountymn.gov/residents/land-water/septic-system'),
        ],
        'sections': [
            ('Permitting authority is split between Dakota County and local municipalities', 'Dakota County directly regulates septic systems in the cities of Hastings, Randolph, and New Trier; Randolph and Waterford townships; and shoreland/floodplain areas or unincorporated portions of the county. The county states that most other cities and townships administer their own septic permitting, inspections, and enforcement.'),
            ('County Ordinance 113 can be stricter than the Minnesota minimums', 'Dakota County states that County Ordinance 113 and Minnesota Rule Chapter 7080 establish septic standards and that the county maintains a list of ordinance provisions more restrictive than state rules. Applicants should check both the applicable local program and the county ordinance rather than assuming the state minimum is sufficient.'),
            ('Septic work must be performed by a licensed septic professional', 'Dakota County states that work on a septic system must be done by a licensed septic professional and directs property owners to the Minnesota Pollution Control Agency license list for designers, installers, inspectors, and pumpers/maintainers.'),
            ('A bedroom addition requires a compliance inspection', 'Dakota County requires a compliance inspection before a bedroom is added to a home. The inspector must determine whether the septic tank and soil absorption system are large enough for the proposed additional bedroom.'),
            ('Compliance reports go to the local authority with jurisdiction', 'Dakota County directs compliance inspectors to submit completed reports to the municipality or other local program that has septic-system jurisdiction for the property. This is important in Dakota County because the permit authority changes by city, township, and special county-jurisdiction areas.'),
        ],
    },
]

mn_urls=[]
mn_links=[]
for d in MN_COUNTIES:
    sources=[('Minnesota Pollution Control Agency — Local Septic System Programs', MN_MPCA)] + d['sources']
    sections=[
        ('Minnesota state and local framework', 'The Minnesota Pollution Control Agency states that counties must adopt SSTS ordinances and administer programs meeting state rules. Cities and townships may also regulate septic systems, and when they do their ordinances must be at least as stringent as the county ordinance. Local programs review plans, approve permits, inspect systems, and may impose requirements stricter than statewide minimums.')
    ] + d['sections']
    mn_urls.append(write_county_page('Minnesota','minnesota',d['county'],d['authority'],d['contact'],sections,sources,verified='August 30, 2026'))
    mn_links.append((d['county'], d['authority']))

write_hub(
    'Minnesota','minnesota',sorted(mn_links),
    'Minnesota Pollution Control Agency rules establish the statewide SSTS framework, while counties, cities, and townships administer local septic programs. These guides are limited to counties where current official sources clearly support the permitting authority and substantive local requirements.',
    'This initial Minnesota batch covers Washington, Hennepin, and Dakota counties. Hennepin and Dakota include important jurisdiction exceptions, so SepticScope identifies when a city or township rather than the county is the actual permitting authority.'
)

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    if '/counties/minnesota/' not in text:
        promo='<section><h2>Minnesota</h2><p><a href="/counties/minnesota/">Browse 3 verified Minnesota county septic guides →</a></p></section>'
        text=text.replace('</main>',promo+'</main>',1) if '</main>' in text else text.replace('</body>',promo+'</body>',1)
        county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
new_urls=['https://septicscope.com/counties/minnesota/']+mn_urls
if sitemap.exists(): sm=sitemap.read_text(encoding='utf-8')
else: sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm=sm.replace('</urlset>',entries+'</urlset>')
    sitemap.write_text(sm,encoding='utf-8')

print(f'Minnesota expansion complete: +{len(mn_urls)} verified county guides')
