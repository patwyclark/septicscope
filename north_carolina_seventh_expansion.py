# SepticScope North Carolina expansion — seventh validated county batch.
# Cabarrus and Union Counties verified from current local government / public-health sources on 2026-08-31.

NC_STATE = 'https://www.dph.ncdhhs.gov/programs/environmental-health/site-water-protection-branch/site-wastewater-program'

CABARRUS_EH = 'https://www.cabarrushealth.org/132/Onsite-Wastewater'
CABARRUS_FEES = 'https://www.cabarrushealth.org/737/Environmental-Health-Fee-Schedule'
CABARRUS_COUNTY = 'https://www.cabarruscounty.us/Government/Departments/Planning/Zoning-Division/Environmental-Health-Site-Evaluations-for-Onsite-Wastewater-and-Wells'
CABARRUS_GUIDE = 'https://www.cabarruscounty.us/files/assets/public/v/1/planning-and-development/planning-and-zoning/documents/septic-site-evaluation-requirements.pdf'

cabarrus_sections = [
    ('Cabarrus Health Alliance is the septic permitting authority',
     'Cabarrus County states that onsite wastewater and well permits are processed and issued by Cabarrus Health Alliance. CHA Environmental Health performs soil evaluations, permits new systems and repairs, inspects existing systems for projects such as additions and pools, and inspects new installations for compliance.'),
    ('Applications are submitted through the Accela Citizen Portal',
     'CHA directs applicants to its Accela Citizen Portal for new soil evaluations, septic expansions and repairs, and Existing System Approval requests. The county also points applicants to CHA for site evaluations and identifies the Environmental Health Division as the office that determines whether a proposed site is suitable for ground-absorption sewage disposal.'),
    ('The site plan and property must be ready for evaluation',
     'Cabarrus guidance requires a completed application and an acceptable site plan showing property lines and dimensions, existing and proposed structures, wells, driveways and excavations, surface waters, and the preferred septic and well areas. Property lines and corners must be clearly marked and the site must be accessible; dense vegetation may need to be thinned before the Environmental Health Specialist can complete the evaluation.'),
    ('Improvement Permit and Authorization to Construct serve different purposes',
     'Cabarrus guidance explains that an Improvement Permit establishes site suitability but does not itself authorize installation. An Authorization to Construct is required before the septic contractor installs the system. The county guidance describes a five-year Improvement Permit when based on a site plan and a non-expiring Improvement Permit when the required plat is provided and site conditions remain unchanged; it also describes the Authorization to Construct as valid for five years if lot conditions do not change.'),
    ('Current county septic fees are published',
     'CHA’s current Environmental Health fee schedule lists $350 for the first-acre soil-evaluation application, $50 for a repair application, $100 for a repair permit, and Construction Authorization fees of $350 for systems at or below 360 gallons per day, $450 for systems at or below 600 gallons per day, and $550 for systems at 601 gallons per day or more. It also lists $150 for Existing System Approval and a $75 site revisit plus $25 for each additional visit. Applicants should confirm the applicable category before filing.'),
    ('Repairs, existing-system approvals, inspections, and contractor credentials are addressed locally',
     'CHA publishes separate application paths for repairs/expansions and Existing System Approval. Its onsite wastewater page states that new installations are inspected for compliance and links owners to the North Carolina Onsite Wastewater Contractor Inspector Certification Board for certified septic installers.'),
]

cabarrus_sources = [
    ('Cabarrus Health Alliance — Onsite Wastewater', CABARRUS_EH),
    ('Cabarrus Health Alliance — Environmental Health Fee Schedule', CABARRUS_FEES),
    ('Cabarrus County — Environmental Health Site Evaluations for Onsite Wastewater and Wells', CABARRUS_COUNTY),
    ('Cabarrus County — septic site evaluation requirements', CABARRUS_GUIDE),
    ('NCDHHS — On-Site Wastewater Program', NC_STATE),
]

cabarrus_url = write_county_page(
    'North Carolina', 'north-carolina', 'Cabarrus',
    'Cabarrus Health Alliance — Environmental Health, Onsite Wastewater',
    'Cabarrus Health Alliance Environmental Health: 704-920-1207; 300 Mooresville Road, Kannapolis, NC 28081.',
    cabarrus_sections, cabarrus_sources, verified='August 31, 2026'
)

UNION_SEPTIC = 'https://www.unioncountync.gov/government/departments-a-e/environmental-health/septic-systems'
UNION_FEES = 'https://www.unioncountync.gov/government/departments-a-e/environmental-health/environmental-health-fees'
UNION_FORMS = 'https://www.unioncountync.gov/government/departments-a-e/environmental-health/applications-and-forms'
UNION_APP = 'https://lfportal.unioncountync.gov/Forms/SepticSystemApplication'

union_sections = [
    ('Union County Environmental Health administers the On-site Water Protection Program',
     'Union County Environmental Health performs soil and site evaluations, issues septic permits, inspects new onsite wastewater systems, evaluates existing systems, and administers repair permitting. The county identifies its On-site Water Protection Program as the local office responsible for design, permitting, inspection, repairs, complaints, and certain existing-system inspections.'),
    ('The county publishes a step-by-step septic permitting process',
     'Applicants first apply for a soil/site evaluation. After the application is processed and the fee is paid, Union County schedules the evaluation. The evaluation is performed by an Environmental Health Specialist or Licensed Soil Scientist. If the site is approved, additional information may be requested before permits are issued. A Construction Authorization is required before septic components are installed and is also required to obtain a building permit.'),
    ('New-system soil evaluations require a backhoe and trained operator',
     'Union County requires the property owner or applicant to provide a backhoe with at least a two-foot-wide bucket and a trained operator for new-system soil/site evaluations. The county’s application guidance specifies pits at least three feet wide and 48 inches deep with a notched access step. This backhoe requirement does not apply to evaluations of an existing system for repair or expansion or when qualifying Licensed Soil Scientist documentation is submitted.'),
    ('Current septic fees are detailed by permit and system type',
     'Union County currently lists $400 for a residential Improvement Permit application and $500 for a commercial site evaluation. Construction Authorization fees are published by system type: $200 for Type IIc, $300 for Type IIIb, $450 for Type IVa, $600 for Type V, and $1,200 for Type VI. The county also lists $100 for a septic repair permit, $100 for component replacement, $125 for redesign, $125 for an existing-system compliance inspection, and $75 for a site revisit.'),
    ('Repairs and existing-system projects receive separate review',
     'For a malfunctioning system, Union County directs the homeowner or representative to request a repair evaluation; an Environmental Health Specialist or Licensed Soil Scientist visits the site and makes recommendations before the repair permit is issued. Existing-system inspections are required before new construction such as garages, decks, pools, irrigation systems, or additions on property served by septic.'),
    ('Some systems have ongoing operation and maintenance inspections',
     'Union County states that its Operation and Maintenance Program is state-mandated and sets inspection frequencies for certain system types. The county specifically identifies low-pressure pipe, pretreatment, and pump systems as examples that must be inspected and provides certified-operator resources for systems subject to the program.'),
    ('Environmental Health applications have moved to the MyHD Dashboard',
     'Union County’s current Environmental Health forms page directs applicants to the MyHD Dashboard for applications, service requests, payments, and status information. The county states that Environmental Health application submissions moved to the dashboard beginning July 1, 2025.'),
]

union_sources = [
    ('Union County Environmental Health — On-site Wastewater Disposal (Septic) Systems', UNION_SEPTIC),
    ('Union County Environmental Health — current fees', UNION_FEES),
    ('Union County Environmental Health — applications and forms / MyHD Dashboard', UNION_FORMS),
    ('Union County — septic system application guidance', UNION_APP),
    ('NCDHHS — On-Site Wastewater Program', NC_STATE),
]

union_url = write_county_page(
    'North Carolina', 'north-carolina', 'Union',
    'Union County Environmental Health — On-site Water Protection Program',
    'Union County Environmental Health: 704-283-3553; 500 N. Main Street, Monroe, NC 28112; unioncountyeh@unioncountync.gov.',
    union_sections, union_sources, verified='August 31, 2026'
)

if 'nc_links' not in globals():
    raise RuntimeError('North Carolina seventh expansion expected accumulated North Carolina county links')
for county, authority in [
    ('Cabarrus', 'Cabarrus Health Alliance — Environmental Health, Onsite Wastewater'),
    ('Union', 'Union County Environmental Health — On-site Water Protection Program'),
]:
    if not any(c == county for c, _ in nc_links):
        nc_links.append((county, authority))

write_hub(
    'North Carolina','north-carolina',sorted(nc_links),
    'North Carolina’s On-Site Water Protection Branch provides statewide oversight for onsite wastewater systems, while local health departments perform the property-level permitting and inspection work. These guides are limited to counties with current, substantive local government guidance.',
    'This North Carolina set now covers 29 verified counties. SepticScope does not extrapolate one county’s workflow, fees, permit duration, inspection schedule, site-evaluation procedure, or local documentation requirements to another county.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    text = text.replace('Browse 27 verified North Carolina county septic guides →', 'Browse 29 verified North Carolina county septic guides →')
    county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    for url in (cabarrus_url, union_url):
        if url not in sm:
            sm = sm.replace('</urlset>', f'<url><loc>{url}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
    sitemap.write_text(sm, encoding='utf-8')

for slug, required_terms in {
    'cabarrus': ('$350', '$550', 'Cabarrus Health Alliance'),
    'union': ('$400', '$1,200', 'Operation and Maintenance'),
}.items():
    p = OUTPUT / 'counties' / 'north-carolina' / slug / 'index.html'
    t = p.read_text(encoding='utf-8')
    if 'Local septic rules not yet verified' in t or 'Official sources' not in t:
        raise RuntimeError(f'{slug} verified page failed production checks')
    if any(term not in t for term in required_terms):
        raise RuntimeError(f'{slug} verified page is missing required validated details')

print('North Carolina seventh expansion complete: +2 verified Cabarrus and Union County guides (29 total verified NC counties)')
