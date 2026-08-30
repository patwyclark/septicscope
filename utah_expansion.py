# SepticScope Utah expansion — verified county batch.
# Verified from Utah DEQ and official county/local health department sources on 2026-08-30.

UT_DEQ_RULE = 'https://lf-public.deq.utah.gov/WebLink/ElectronicFile.aspx?docid=10701&eqdocs=DWQ-2023-004248'

UT_COUNTIES = [
    {
        'county': 'Salt Lake',
        'authority': 'Salt Lake County Health Department, Environmental Health Division — Water Quality Bureau',
        'contact': 'Salt Lake County Health Department Water Quality Bureau — 385-468-3862; 788 East Woodoak Lane (5380 South), Murray, UT 84107.',
        'sources': [
            ('Salt Lake County — Septic & Onsite Wastewater Systems', 'https://www.saltlakecounty.gov/health/waste/septic/'),
            ('Salt Lake County Health Regulation #13 — Wastewater Disposal', 'https://prod.saltlakecounty.gov/globalassets/1-site-files/health/regs/wastewater.pdf'),
            ('Salt Lake County — Subdivision Approval', 'https://www.saltlakecounty.gov/health/construction-contractors/subdivision-approval/'),
        ],
        'sections': [
            ('County permits onsite systems up to 5,000 gallons per day', 'Salt Lake County Health Department states that it reviews and permits new onsite wastewater systems handling 5,000 gallons per day or less of domestic wastewater. Larger flows or nondomestic wastewater are directed to the Utah Department of Environmental Quality.'),
            ('Public sewer availability must be resolved before septic permitting', 'The county requires applicants to obtain a sewer-service letter and states that connection is required when sewer is available within 300 feet of the property. Applicants must also resolve municipal land-use requirements and provide water-availability documentation.'),
            ('Certified onsite professionals must perform soil work and design', 'Salt Lake County requires a Utah Division of Water Quality-certified onsite professional to conduct soil exploration and design the system. Level 2 professionals may design conventional systems, while alternative systems require Level 3 design credentials.'),
            ('County has specific site-feasibility limits', 'Salt Lake County identifies soil conditions, hydraulic loading rate, slope, and setbacks as core site-feasibility factors. Drainfields are not allowed on slopes above 35 percent; slopes from 25 to 35 percent require a slope-stability study.'),
            ('Permit application, inspections, and expiration', 'The county requires the construction permit application, soil/percolation results, design plans, building plans, water documentation, and applicable sewer or watershed letters. Approved permits expire one year after issuance unless extended. The system must be inspected by the Health Department before backfilling.'),
            ('Certain systems require annual operating permits', 'Salt Lake County requires operating permits for alternative systems, pressure-distribution systems, and holding tanks. The county states these permits must be renewed yearly and maintenance/service records must be submitted to the Water Quality Bureau.'),
        ],
    },
    {
        'county': 'Davis',
        'authority': 'Davis County Health Department — Environmental Health Division, Onsite Wastewater Systems',
        'contact': 'Davis County Health Department, 22 S. State Street, Clearfield, UT 84015; main phone 801-525-5000.',
        'sources': [
            ('Davis County Health Department — Onsite Wastewater Systems', 'https://www.daviscountyutah.gov/health/environmental-health-division/permits/onsite-wastewater-systems-new'),
            ('Davis County Health Department — Environmental Health', 'https://www.daviscountyutah.gov/health/'),
        ],
        'sections': [
            ('County permit is required to install an onsite wastewater system', 'Davis County Health Department states that permits must be obtained from its office to install an onsite wastewater system. The permit process includes review of the proposed location and intermediate and final inspections.'),
            ('Undeveloped property requires a Statement of Feasibility', 'For raw or undeveloped property, Davis County requires a Statement of Feasibility. The Health Department conducts a GIS assessment, records search, site assessment, and soil evaluation and oversees required percolation testing and groundwater monitoring before determining whether the property can support an onsite system.'),
            ('Construction cannot be backfilled before county approval', 'Davis County inspects excavation and installation for compliance with the approved plan and Utah Rule R317-4. The county states that excavation cannot be backfilled until the health inspector gives final approval.'),
            ('County can help locate existing septic records', 'Owners seeking an existing septic-system location may submit the county onsite wastewater application so Environmental Health can search its records and provide available system information.'),
            ('Sewer availability and abandonment have separate requirements', 'Davis County notes that municipal and state laws may require sewer connection for occupied buildings when public sewer is within 300 feet. For abandonment, the owner must notify the Health Department within 72 hours before excavation or construction, after which the tank must be pumped and removed, crushed and void-filled, or completely filled with approved material.'),
            ('Operating permits and local fees are part of the county program', 'Davis County publishes separate fees for feasibility work, plan review, construction permits, operating permits, extensions, additional inspections, and refinance inspections. Applicants should use the current county fee table when planning a project.'),
        ],
    },
    {
        'county': 'Tooele',
        'authority': 'Tooele County Health Department — Environmental Health',
        'contact': 'Tooele County Health Department Environmental Health — 435-277-2440; eh@tooeleco.gov; 151 N. Main Street, Tooele, UT 84074.',
        'sources': [
            ('Tooele County Health Department Regulation #12 — Wastewater Disposal', 'https://tooelehealth.org/wp-content/uploads/2019/08/Reg-12-Wastewater-Disposal-with-Alternatives-section-redlined.pdf'),
            ('Tooele County — Septic/Wastewater Permit Application', 'https://tooelehealth.org/wp-content/uploads/2016/01/Updated-Application-for-Septic-Wastewater-Permit.pdf'),
            ('Tooele County Health Department — Environmental Health Contact', 'https://tooelehealth.org/contact-us/'),
            ('Tooele County Health Department — Environmental Record Searches', 'https://tooelehealth.org/record-search-requests/'),
        ],
        'sections': [
            ('County permit and inspection process is governed by local Regulation #12', 'Tooele County Health Department administers local wastewater-disposal requirements in addition to Utah Rule R317-4. Its regulation establishes septic permitting, percolation testing, onsite inspections, fees, and local enforcement requirements.'),
            ('New systems require certified design', 'Tooele County states in its septic permit application that new onsite wastewater systems must be designed by a Utah State Level II Certified onsite wastewater designer, with the completed design submitted to the Health Department as part of the permit application.'),
            ('Local application requires a detailed property map', 'Tooele County requires a property map showing applicable buildings, water service, wells, property lines, septic tank and absorption area, watercourses, soil and percolation test locations, driveways, contours when required, easements or drainage rights-of-way, and lot dimensions.'),
            ('Percolation testing is controlled by local regulation', 'County Regulation #12 requires percolation tests in the proposed absorption area under Utah R317-4. The testing is performed at the owner’s expense by a registered sanitarian, registered engineer, or another qualified person approved by the Health Department.'),
            ('Two-stage county inspection before backfill', 'Tooele County requires the installer to request onsite inspection at least 24 hours in advance. A designated Health Department agent inspects after trench excavation and again before backfill.'),
            ('County permits are valid for 24 months', 'Tooele County Regulation #12 states that an individual septic-system permit is valid for 24 months. Starting work without first obtaining the required permit can trigger a separate investigation and investigation fee in addition to the permit fee.'),
            ('Environmental record searches are available', 'Tooele County Health Department accepts Environmental Record Search Requests for existing records. The county requires an application and fee before processing the search.'),
        ],
    },
]

ut_urls=[]
ut_links=[]
for d in UT_COUNTIES:
    sources=[('Utah DEQ — R317-4 Onsite Wastewater Systems / local health department jurisdiction', UT_DEQ_RULE)] + d['sources']
    sections=[
        ('Utah state and local framework', 'Utah Rule R317-4 assigns local health departments jurisdiction to administer the onsite wastewater rule. Local health departments may adopt stricter requirements, assess local fees, require operating permits and servicing, protect groundwater through local policy, and regulate alternative onsite systems within their jurisdictions.')
    ] + d['sections']
    ut_urls.append(write_county_page('Utah','utah',d['county'],d['authority'],d['contact'],sections,sources,verified='August 30, 2026'))
    ut_links.append((d['county'], d['authority']))

write_hub(
    'Utah','utah',sorted(ut_links),
    'Utah Rule R317-4 establishes the statewide onsite wastewater framework while local health departments administer permits and may adopt stricter local requirements. These guides cover counties where current local government sources support both the permitting authority and substantive local procedures.',
    'This first Utah batch covers Salt Lake, Davis, and Tooele counties. Each page uses the applicable local health department process rather than extrapolating a generic statewide workflow to counties that have not yet been independently validated.'
)

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    if '/counties/utah/' not in text:
        promo='<section><h2>Utah</h2><p><a href="/counties/utah/">Browse 3 verified Utah county septic guides →</a></p></section>'
        text=text.replace('</main>',promo+'</main>',1) if '</main>' in text else text.replace('</body>',promo+'</body>',1)
        county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
new_urls=['https://septicscope.com/counties/utah/']+ut_urls
if sitemap.exists(): sm=sitemap.read_text(encoding='utf-8')
else: sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm=sm.replace('</urlset>',entries+'</urlset>')
    sitemap.write_text(sm,encoding='utf-8')

print(f'Utah expansion complete: +{len(ut_urls)} verified county guides')