# SepticScope North Carolina expansion — six additional counties validated from county/local government sources.
# This script runs after north_carolina_expansion.py and preserves the initial NC batch.

NC2_COUNTIES = {
    'Cabarrus': {
        'authority': 'Cabarrus Health Alliance — Environmental Health, Onsite Wastewater Program',
        'contact': 'Cabarrus Health Alliance Environmental Health / Onsite Wastewater: 980-439-1097; 300 Mooresville Road, Kannapolis, NC 28081.',
        'sources': [
            ('Cabarrus Health Alliance — Onsite Wastewater', 'https://www.cabarrushealth.org/132/Onsite-Wastewater'),
        ],
        'sections': [
            ('County applications use the Accela Citizen Portal', 'Cabarrus Health Alliance directs onsite wastewater applications through the Accela Citizen Portal, including new soil evaluations, septic expansions and repairs, and Existing System Approval requests.'),
            ('Soil evaluations and installation inspections', 'Environmental Health performs soil evaluations to determine suitability for ground-absorption sewage disposal and inspects installation of new sewage disposal systems for compliance with applicable rules.'),
            ('Existing-system approval for development around septic', 'Cabarrus states that inspections of existing septic systems are used for building-permit purposes when projects such as structural additions, replacement mobile homes, or swimming pools are proposed. Permits are also issued for needed septic repairs.'),
        ],
    },
    'Durham': {
        'authority': 'Durham County Department of Public Health — Environmental Health, On-Site Water Protection',
        'contact': 'Durham County Environmental Health Division: 919-560-7800; healthinspector@dconc.gov; 414 East Main Street, Durham, NC 27701.',
        'sources': [
            ('Durham County — On Site Water Protection', 'https://dconc.gov/Public-Health/Environmental-Health/On-Site-Water-Protection'),
            ('Durham County — Environmental Health', 'https://dconc.gov/Public-Health/Environmental-Health'),
            ('Durham County — Septic and Well Records', 'https://dconc.gov/Public-Health/Health-Data-and-Records/Septic-and-Well-Records'),
        ],
        'sections': [
            ('County onsite section provides regulatory oversight', 'Durham County states that its On-Site Water Protection section provides regulatory oversight and enforcement for laws and rules governing onsite wastewater systems and private wells.'),
            ('Site evaluations and construction inspections', 'The county lists septic site evaluations and septic-system construction inspections among the services performed by On-Site Water Protection, along with complaint investigations involving septic systems.'),
            ('Existing permit records are available by request', 'Durham County allows anyone to request existing septic and well records from Environmental Health by providing identifying information such as the site address and, when available, parcel or PIN information.'),
        ],
    },
    'Forsyth': {
        'authority': 'Forsyth County Department of Public Health — Environmental Health, Wastewater/Septic Systems',
        'contact': 'Forsyth County Environmental Health: 336-703-3225; 799 North Highland Avenue, Winston-Salem, NC 27101.',
        'sources': [
            ('Forsyth County — Environmental Health', 'https://www.forsyth.cc/PublicHealth/EnvironmentalHealth/'),
            ('Forsyth County — Wastewater / Septic Systems', 'https://forsyth.cc/publichealth/environmentalhealth/septic_main.aspx'),
            ('Forsyth County — Wastewater / Septic FAQ', 'https://www.forsyth.cc/publichealth/environmentalhealth/septic_faqs.aspx'),
        ],
        'sections': [
            ('County performs soil/site evaluations and installation inspections', 'Forsyth County Environmental Health enforces onsite sewage-disposal laws and rules, performs soil and site evaluations for property not served by public sewer, and inspects septic-system installations.'),
            ('Repair authorization is required for malfunctioning systems', 'Forsyth County instructs owners with a malfunctioning septic system to submit an Application for Authorization for Wastewater System Construction Repair. An Environmental Health Specialist then visits the property to assess the problem and prepare the repair approval.'),
            ('County distinguishes repair work from routine pumping', 'Forsyth states that preventive septic-tank pumping does not require a health-department permit, while repair work follows the county authorization process. The county also states that septic-system contractors performing repair work must be registered with the Forsyth County Department of Public Health.'),
        ],
    },
    'Guilford': {
        'authority': 'Guilford County Public Health — Environmental Health, On-site Wastewater Program',
        'contact': 'Guilford County On-site Wastewater / Environmental Health: 336-641-7613; Guilford County Government, 301 W. Market St., Greensboro, NC 27401.',
        'sources': [
            ('Guilford County — On-site Wastewater', 'https://www.guilfordcountync.gov/government/departments-and-agencies/health-and-human-services-agency/public-health/environmental-health/site-wastewater'),
            ('Guilford County — Environmental Health Fee Schedule', 'https://www.guilfordcountync.gov/government/departments-and-agencies/department-health-and-human-services/public-health/environmental-health/fee-schedule'),
        ],
        'sections': [
            ('County handles evaluation, permitting, inspection, repair, and monitoring', 'Guilford County states that its On-site Wastewater Program oversees site evaluations, permitting, installation inspections, repairs, monitoring, and abandonment of onsite sewage systems. The county issues Improvement Permits, Construction Authorizations, and Operation Permits through that process.'),
            ('Inspection required before new construction around an existing system', 'Guilford County requires an inspection when new construction is begun on property with an existing septic system and/or well.'),
            ('Published local O&M inspection intervals', 'Guilford publishes routine operation-and-maintenance inspection frequencies for qualifying systems: Type III single-pump systems every five years, Type IV systems every three years, and Type V and VI systems every year or six months depending on the system.'),
            ('County publishes wastewater-specific local fees', 'Guilford County publishes separate fees for residential soil evaluations, construction authorizations by system type, alternative designs, and existing-system O&M inspections. Applicants should verify the current fee category before filing.'),
        ],
    },
    'Mecklenburg': {
        'authority': 'Mecklenburg County Environmental Health — Groundwater and Wastewater Services',
        'contact': 'Mecklenburg County Environmental Health: 980-314-1620; Groundwater and Wastewater septic questions: 980-314-1680; 3205 Freedom Drive, Suite 8000, Charlotte, NC 28208.',
        'sources': [
            ('Mecklenburg County — Groundwater and Wastewater Services', 'https://eh.mecknc.gov/water'),
            ('Mecklenburg County — Septic System Fee Schedule', 'https://eh.mecknc.gov/environmental-health/groundwater-and-wastewater-services/septic-system-fee-schedule'),
            ('Mecklenburg County — Basic Steps for a New Septic System', 'https://eh.mecknc.gov/news/basic-steps-new-septic-system'),
        ],
        'sections': [
            ('County Groundwater and Wastewater program permits onsite systems', 'Mecklenburg County Environmental Health states that Groundwater and Wastewater Services provides plan review, permitting, and evaluation of onsite wastewater systems and accepts septic applications online through Accela.'),
            ('Scaled site plan and soil/site evaluation are part of the new-system process', 'For a new septic system, Mecklenburg requires an Improvement Permit application with a site plan drawn to scale. The county then performs the soil/site evaluation before an Improvement Permit can be issued or denied.'),
            ('Construction authorization, installation approval, and operation permit', 'Mecklenburg publishes a staged permitting sequence that includes Improvement Permit review, Construction Authorization, installation approval, and a final inspection before the Operation Permit is issued and a Certificate of Occupancy can be obtained.'),
            ('County publishes separate permit fees and repair treatment', 'Mecklenburg publishes separate residential and commercial fees for new systems, soil-test/Improvement-Permit-only applications, alterations, and use of an existing system. The county lists septic-system repair as permit-required with no local application fee.'),
        ],
    },
    'Union': {
        'authority': 'Union County Environmental Health — On-site Water Protection Program',
        'contact': 'Union County Environmental Health: 704-283-3553; 500 N. Main St., Suite 47, Monroe, NC 28112.',
        'sources': [
            ('Union County — On-site Wastewater Disposal (Septic) Systems', 'https://www.unioncountync.gov/government/departments-a-e/environmental-health/septic-systems'),
            ('Union County — Environmental Health Fees', 'https://www.unioncountync.gov/government/departments-a-e/environmental-health/environmental-health-fees'),
            ('Union County — Environmental Health', 'https://www.unioncountync.gov/government/departments-a-e/environmental-health'),
        ],
        'sections': [
            ('County program performs design, permitting, inspection, and repairs', 'Union County states that its On-site Water Protection Program performs soil and site evaluations, designs and permits new septic systems, inspects installations, and handles permitting for repairs to existing systems.'),
            ('Applicant must arrange a backhoe for new-system evaluation', 'After an application is processed and the fee is paid, Union County schedules the soil/site evaluation. For new-system evaluations, the property owner or applicant is responsible for having a backhoe and operator onsite for the scheduled evaluation.'),
            ('Construction Authorization is required before installation and building permit', 'Union County states that a Construction Authorization is required to install septic-system components and to obtain the building permit. Depending on the soil evaluation and application type, additional information may be required before the authorization is issued.'),
            ('Existing-system inspection before new construction', 'Union County requires an existing-system inspection before new construction on property served by septic, including projects such as garages, decks, swimming pools, irrigation systems, and additions.'),
            ('Three-acre evaluation limit for Improvement Permit applications', 'Union County publishes a maximum evaluation area of three acres per Improvement Permit/site-evaluation application and maintains separate local fees by permit and system category.'),
        ],
    },
}

nc2_urls=[]
for county, data in NC2_COUNTIES.items():
    sources=[
        ('NCDHHS — On-Site Wastewater Program', NC_STATE),
        ('NCDHHS — On-Site Water Protection Branch', NC_BRANCH),
        ('NCDHHS — Homeowner septic permits and inspections guidance', NC_HOMEOWNER),
    ] + data['sources']
    sections=[
        ('North Carolina state and local framework', 'The N.C. Division of Public Health On-Site Water Protection Branch provides statewide regulatory oversight and technical guidance for subsurface onsite wastewater systems, while local health departments carry out county permitting and inspection functions. NCDHHS directs homeowners to the local health department for septic questions, permits, and inspections.')
    ] + data['sections']
    url=write_county_page('North Carolina','north-carolina',county,data['authority'],data['contact'],sections,sources,verified='August 29, 2026')
    nc2_urls.append(url)
    if not any(c == county for c, _ in nc_links):
        nc_links.append((county,data['authority']))

write_hub(
    'North Carolina','north-carolina',sorted(nc_links),
    'North Carolina’s On-Site Water Protection Branch provides statewide oversight for onsite wastewater systems, while local health departments perform the property-level permitting and inspection work. These guides are limited to counties with current, substantive local government guidance.',
    'This North Carolina set now covers 12 verified counties. SepticScope does not extrapolate one county’s workflow, fees, permit duration, inspection schedule, or local documentation requirements to another county.'
)

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    text=text.replace('Browse 6 verified North Carolina county septic guides →','Browse 12 verified North Carolina county septic guides →')
    county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists(): sm=sitemap.read_text(encoding='utf-8')
else: sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>' for u in nc2_urls if u not in sm)
if entries:
    sm=sm.replace('</urlset>',entries+'</urlset>')
    sitemap.write_text(sm,encoding='utf-8')

print(f'North Carolina additional expansion complete: +{len(nc2_urls)} verified county guides')