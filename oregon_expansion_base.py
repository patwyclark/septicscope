# SepticScope Oregon expansion — official Oregon DEQ and county government sources
# Limited to counties with current, substantive local onsite permitting guidance independently validated.

OR_DEQ_ROLE = 'https://www.oregon.gov/deq/Residential/Pages/Onsite-Contacts.aspx'
OR_DEQ_PROGRAM = 'https://www.oregon.gov/deq/residential/pages/onsite.aspx'
OR_DEQ_RECORDS = 'https://www.oregon.gov/deq/residential/pages/onsite-records.aspx'

OR_COUNTIES = {
    'Clackamas': {
        'authority': 'Clackamas County Development Services — Septic / Onsite Program, acting under Oregon DEQ onsite rules',
        'contact': 'Clackamas County septic permitting: 503-742-4740; soilsconcern@clackamas.us. Applications are submitted through the county Development Direct system.',
        'sources': [
            ('Clackamas County — How to Apply for a Septic Permit', 'https://www.clackamas.us/building/permit-septic'),
            ('Clackamas County — How to Apply for a Permit', 'https://www.clackamas.us/building/how-to-apply-for-a-permit'),
        ],
        'sections': [
            ('County permit process for new systems, repairs, and changes',
             'Clackamas County states that its septic applications cover new installations, repairs, alterations, connections to existing systems, and changes such as adding bedrooms. The county uses different application types depending on the work proposed, so an applicant may need more than one approval.'),
            ('Authorization Notice for changes affecting an existing system',
             'The county requires an Authorization Notice when a proposed change may affect an existing septic system, including connecting a new or replacement structure, changing the use of a property, or increasing projected daily sewage flow such as by adding a bedroom.'),
            ('Site evaluation and land-use documentation',
             'For a new system or an alteration, Clackamas County lists a Land Use Compatibility Statement among the permit documents. If a drainfield will be installed or modified, the application also requires the file number or a copy of an approved site evaluation.'),
            ('Electronic plan submittal and inspections',
             'Clackamas County requires septic drawings and supporting documents to be submitted electronically through Development Direct rather than by paper or email. Approved plans and permits must be available on site, and the applicant must schedule the inspections required for the project.'),
        ],
    },
    'Deschutes': {
        'authority': 'Deschutes County Community Development Department — Environmental Soils / Onsite Wastewater Program',
        'contact': 'Deschutes County Community Development Department — 541-388-6575; 117 NW Lafayette Street, Bend, OR 97703. Onsite applications are available through Oregon ePermitting.',
        'sources': [
            ('Deschutes County — Site Evaluation Guide', 'https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/11743/site_evaluation_guide_with_test_pit_requirements.pdf'),
            ('Deschutes County — Onsite Permit Requirements', 'https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/775/es-onsite_permits.pdf'),
            ('Deschutes County — Site Evaluation Procedures', 'https://www.deschutes.org/sites/default/files/fileattachments/community_development/page/731/es-evaluation_procedures_handout.pdf'),
        ],
        'sections': [
            ('Site evaluation before septic or building permits',
             'Deschutes County states that a site evaluation is required before onsite wastewater or building permits can be issued for an existing lot, unless a valid evaluation already exists and remains usable. The evaluation determines whether the property can adequately treat wastewater and identifies the approved initial and replacement disposal areas and system type.'),
            ('County test-pit requirements',
             'The county requires the applicant to prepare test pits before the evaluation. Its published procedure calls for at least two test pits, encourages additional pits where needed to demonstrate suitable soil, and describes the dimensions and safe-access configuration required for county soil inspection.'),
            ('Detailed onsite permit plan',
             'Deschutes County’s onsite permit guidance requires a scaled plot plan showing property dimensions, slopes, test-hole locations, septic components, initial and reserve drainfield areas, and distances to features such as waterways, wells, water lines, structures, utilities, property lines, easements, cuts, fills, and escarpments.'),
            ('Southern Deschutes County can have additional standards',
             'The county specifically advises applicants to check with the field sanitarian for area-specific requirements and states that special standards apply in southern Deschutes County to new construction, major alterations, and major repairs. Property-specific review is therefore important before relying on a generic system design.'),
        ],
    },
    'Lane': {
        'authority': 'Lane County Public Works, Land Management Division — On-Site Wastewater Program',
        'contact': 'Lane County Land Management Division — 541-682-4651; 3050 N. Delta Highway, Eugene, OR 97408. Septic applications are available through ePASS and through the county Land Management Division.',
        'sources': [
            ('Lane County — On-Site Wastewater', 'https://www.lanecountyor.gov/government/county_departments/public_works/land_management_division/on-_site_wastewater'),
            ('Lane County — Septic Required Documents', 'https://www.lanecountyor.gov/government/county_departments/public_works/land_management_division/building_safety/required_documents'),
            ('Lane County — Test Pit Information', 'https://www.lanecountyor.gov/government/county_departments/public_works/land_management_division/on-_site_wastewater/test_pit_information'),
            ('Lane County — Septic Inspections', 'https://www.lanecountyor.gov/government/county_departments/public_works/land_management_division/building_safety/inspections'),
            ('Lane County — General Onsite Information', 'https://www.lanecountyor.gov/government/county_departments/public_works/land_management_division/on-_site_wastewater/subsurface_sanitation_permits_general_information'),
        ],
        'sections': [
            ('County regulates installation, repair, alteration, and maintenance',
             'Lane County states that its On-Site Wastewater Program regulates installation, repair, alteration, and maintenance of septic systems serving residential and commercial properties that are not served by community sewer.'),
            ('Site evaluation before installation',
             'For vacant land, Lane County generally requires a site evaluation before a system is installed. The county explains that the inspector evaluates test pits, soil drainage capability, and proposed wastewater flow to determine the appropriate system type; a separate installation permit is then required to construct the system.'),
            ('Specific test-pit and plot-plan instructions',
             'Lane County publishes unusually specific local test-pit guidance: at least two pits are required, preferably three; pits should be spaced about 50 to 100 feet apart and sized to allow inspection of the soil profile. The plot plan must identify test pits, property lines, development features, and wells, including neighboring wells near the property.'),
            ('Final septic inspection and completion record',
             'The installation permit identifies required inspections. Lane County states that, after the system is completed and approved, it issues a Certificate of Satisfactory Completion and Final Inspection Report. Septic inspections must be completed before final building inspection where applicable.'),
            ('Existing permit records',
             'Lane County provides building, sanitation, land-use, and other property permit history through its LMD-PRO property records portal, including records dating back to the 1970s where available.'),
        ],
    },
    'Marion': {
        'authority': 'Marion County Public Works — Building Inspection, Onsite Sewage Disposal Program (Oregon DEQ contract agent)',
        'contact': 'Marion County Building Inspection / Onsite Sewage Disposal Program — 503-588-5147. The county states that it issues septic permits as a contract agent of Oregon DEQ.',
        'sources': [
            ('Marion County — Onsite Sewage Disposal Program', 'https://www.co.marion.or.us/PW/BuildingInspection/Pages/onsite.aspx'),
            ('Marion County — Site Evaluation Permit Packet', 'https://www.co.marion.or.us/PW/BuildingInspection/Pages/sitepack.aspx'),
            ('Marion County — Where to Apply for Permits', 'https://www.co.marion.or.us/PW/BuildingInspection/Pages/permits.aspx'),
        ],
        'sections': [
            ('County is the DEQ contract agent for septic permitting',
             'Marion County expressly states that Building Inspection issues septic system permits within the county as a contract agent of Oregon DEQ. County permits are issued under Oregon’s DEQ onsite sewage disposal rules, except for community-sewer properties and systems reserved to DEQ under Water Pollution Control Facilities rules.'),
            ('Site evaluation determines sewage-disposal feasibility',
             'The county requires a septic site evaluation to determine sewage-disposal feasibility for a specific property before construction of a new onsite system. Its site-evaluation packet requires a site plan and test pits and provides county setback guidance.'),
            ('Land Use Compatibility Statement in specified locations',
             'Marion County states that a Land Use Compatibility Statement is required with a site-evaluation application for properties inside urban growth boundaries, in the Urban Transition zone, and inside city limits.'),
            ('Large-flow systems are referred to Oregon DEQ',
             'Marion County directs applicants with systems over 2,500 gallons per day to Oregon DEQ for Water Pollution Control Facilities permitting rather than the normal county residential onsite process.'),
            ('County septic-history records',
             'Marion County provides online scanned septic records for many properties and directs users to the onsite office when a property’s septic history cannot be located online.'),
        ],
    },
    'Washington': {
        'authority': 'Washington County Environmental Health — Onsite Sewage Program',
        'contact': 'Washington County Environmental Health Septic — 503-846-8722. Septic applications are submitted through the county Public Permitting and Services Portal.',
        'sources': [
            ('Washington County — Onsite Sewage', 'https://www.washingtoncountyor.gov/environmental-health/onsite-sewage'),
            ('Washington County — Onsite Sewage Permits', 'https://www.washingtoncountyor.gov/environmental-health/onsite-sewage-permits'),
            ('Washington County — Site Evaluation', 'https://www.washingtoncountyor.gov/environmental-health/onsite-wastewater-site-evaluation'),
            ('Washington County — Authorization Notice', 'https://www.washingtoncountyor.gov/environmental-health/onsite-sewage-authorization'),
            ('Washington County — Existing System Evaluation', 'https://www.washingtoncountyor.gov/environmental-health/onsite-wastewater-existing-system'),
        ],
        'sections': [
            ('County Environmental Health issues household septic permits',
             'Washington County Environmental Health states that it issues septic permits for households not served by public sewer. Permits are required for installation of new onsite systems and for repair or alteration of existing systems, tanks, or drainfields.'),
            ('Site evaluation and reserve area',
             'Washington County requires a site evaluation to determine whether a property is suitable and what type and size of system can be used. The evaluation considers soil, groundwater, slope, streams, wells, cuts and fills, and parcel size. The county also requires enough suitable area for the initial system and an equal repair area.'),
            ('Connection to available community sewer',
             'Washington County states that if community sewer is available, the property must connect to sewer service rather than use the normal onsite septic route.'),
            ('Authorization Notice for changes in use or flow',
             'An Authorization approval may be required when a property change could affect an existing septic system, including adding bedrooms, replacing a dwelling, adding a hardship dwelling connection, or changing a system from residential to commercial use.'),
            ('Existing-system evaluations and records',
             'The county uses Existing System Evaluations to document system location, component size, and functioning status, including for some older unpermitted systems and certain treatment technologies. Septic as-built records can be requested through the county public-records portal.'),
        ],
    },
}

or_urls = []
or_links = []
for county, data in OR_COUNTIES.items():
    sources = [
        ('Oregon DEQ — County office and residential onsite septic agents', OR_DEQ_ROLE),
        ('Oregon DEQ — Onsite Wastewater Management Program', OR_DEQ_PROGRAM),
        ('Oregon DEQ — Septic system records', OR_DEQ_RECORDS),
    ] + data['sources']
    sections = [
        ('Oregon county-agent framework',
         'Oregon DEQ states that it may authorize counties as its agents for onsite septic permitting under OAR 340-071-0120. County agents can receive and process applications, issue permits, enforce onsite requirements, and perform required inspections. Property-specific local instructions should be followed because application and land-use procedures vary by county.')
    ] + data['sections']
    url = write_county_page(
        'Oregon', 'oregon', county,
        data['authority'], data['contact'], sections, sources,
        verified='August 29, 2026'
    )
    or_urls.append(url)
    or_links.append((county, data['authority']))

write_hub(
    'Oregon', 'oregon', sorted(or_links),
    'Oregon DEQ administers statewide onsite wastewater rules and authorizes local counties to act as permitting agents in much of the state. These guides are limited to counties where current local government sources provide a substantive septic permit, site-evaluation, inspection, or records process.',
    'This initial Oregon batch covers Clackamas, Deschutes, Lane, Marion, and Washington counties. SepticScope is intentionally not extrapolating one county’s local workflow to the rest of Oregon; additional counties will be added only after their current permitting authority and useful local requirements are independently validated.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    if '/counties/oregon/' not in text:
        promo = '<section><h2>Oregon</h2><p><a href="/counties/oregon/">Browse the first 5 verified Oregon county septic guides →</a></p></section>'
        text = text.replace('</main>', promo + '</main>', 1) if '</main>' in text else text.replace('</body>', promo + '</body>', 1)
        county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/oregon/'] + or_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'Oregon expansion complete: +{len(or_urls)} verified county guides')
