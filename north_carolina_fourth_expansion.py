# SepticScope North Carolina expansion — fourth validated county batch.
# Runs after the first three NC batches; uses statewide NC source constants and accumulated nc_links.

NC4_COUNTIES = {
    'Gaston': {
        'authority': 'Gaston County Department of Health and Human Services — Environmental Health, On-Site Wastewater Program',
        'contact': 'Gaston County Environmental Health: 991 W Hudson Blvd, Gastonia, NC 28052; 704-853-5200.',
        'sources': [
            ('Gaston County — On-Site Wastewater and Wells', 'https://www.gastongov.com/1220/On-Site-Wastewater-and-Wells'),
            ('Gaston County — Environmental Health', 'https://www.gastongov.com/399/Environmental-Health'),
            ('Gaston County — Environmental Health Fee Schedule', 'https://www.gastongov.com/1235/Fee-Schedule'),
        ],
        'sections': [
            ('County handles soil evaluation, permitting, design approval, and inspections', 'Gaston County Environmental Health administers the onsite wastewater program for properties not served by municipal wastewater. Environmental Health Specialists conduct soil and site evaluations, coordinate permit and design approval, inspect installed systems, and investigate failing systems.'),
            ('Improvement Permit and Construction Authorization precede final approval', 'For a new septic system, Gaston County directs applicants to obtain an Improvement Permit, then an Authorization to Construct. The county states that the Improvement Permit is valid for five years and that the Authorization to Construct is valid for five years from the corresponding Improvement Permit date.'),
            ('Operation Permit is required before occupancy approval', 'After a certified septic contractor installs the system and Environmental Health approves the installation, Gaston County issues the Operation Permit and notifies Building Inspections. The county states that the septic permit and final approval must be issued before the Certificate of Occupancy.'),
            ('Expansion and repair use separate local permit paths', 'Gaston County requires a Septic Expansion Permit when a proposed change increases wastewater flow, such as adding bedrooms, retail area, restaurant seats, or food-preparation area. Septic repairs use a separate repair-permit application, and projects near an existing system may require Existing System Approval.'),
        ],
    },
    'Moore': {
        'authority': 'Moore County Health Department — Environmental Health, Onsite Wastewater/Septic Systems Program',
        'contact': 'Moore County Environmental Health: 1042 Carriage Oaks Drive, Carthage, NC 28327; 910-947-6283.',
        'sources': [
            ('Moore County — Septic / Wells', 'https://www.moorecountync.gov/256/Septic-Wells'),
            ('Moore County — Environmental Health', 'https://www.moorecountync.gov/244/Environmental-Health'),
        ],
        'sections': [
            ('County Health Department administers septic placement and installation oversight', 'Moore County states that its Health Department protects public health and groundwater by ensuring proper placement, installation, maintenance, and operation of septic systems.'),
            ('Different applications are used for new work, repairs, and existing systems', 'Moore County publishes separate Environmental Health applications for new septic systems, expansions or relocations, septic-system repairs, and Existing Septic System Approval. Property owners should use the application matching the proposed work rather than assuming an old permit covers a new project.'),
            ('Planning review may also apply to development projects', 'Moore County Environmental Health directs applicants developing property or performing construction in unincorporated areas to coordinate with the county Planning Department as applicable in addition to the Environmental Health septic process.'),
        ],
    },
    'Nash': {
        'authority': 'Nash County Health Department — Environmental Health, Onsite Wastewater Program',
        'contact': 'Nash County Environmental Health administers septic design, permitting, site evaluation, and installation inspections for the county.',
        'sources': [
            ('Nash County — Environmental Health', 'https://nashcountync.gov/232/Environmental-Health'),
        ],
        'sections': [
            ('County performs septic design, permitting, and installation inspections', 'Nash County lists septic design, permitting, and installation inspections among the services performed by Environmental Health. The department also evaluates building sites to determine whether they are suitable for septic systems.'),
            ('Site suitability is evaluated before relying on a septic layout', 'Because Nash County Environmental Health evaluates proposed building sites for septic suitability, owners should obtain the applicable county evaluation and approval before committing to a building location, wastewater layout, or construction plan dependent on onsite treatment.'),
            ('Environmental Health also addresses failing systems and improper sewage disposal', 'Nash County identifies proper sewage disposal as an Environmental Health responsibility. Property-specific repairs or malfunctioning systems should therefore be handled through the county Environmental Health program rather than treated as ordinary plumbing work.'),
        ],
    },
    'Randolph': {
        'authority': 'Randolph County Public Health — Environmental Health, On-Site Water Protection Program',
        'contact': 'Randolph County Environmental Health: 336-318-6262; Central Permitting, 204 E Academy Street, Asheboro, NC 27203.',
        'sources': [
            ('Randolph County — On-Site Water Protection Program', 'https://randolphcountync.gov/397/On-Site-Water-Protection-Program'),
            ('Randolph County — Septic Systems', 'https://www.randolphcountync.gov/429/Septic-Systems'),
            ('Randolph County — Central Permitting', 'https://randolphcountync.gov/409/Central-Permitting'),
        ],
        'sections': [
            ('County program evaluates, designs, permits, and inspects septic systems', 'Randolph County Environmental Health conducts soil evaluations for subsurface wastewater suitability, designs and permits onsite systems, and inspects final installations. The program also performs inspections associated with repairs and existing-system connections.'),
            ('Applications require site preparation and a matching site plan', 'Randolph County instructs applicants to complete the application, prepare the property according to county site-preparation instructions, submit a site plan containing the required elements, and stake or mark those same elements on the property. Existing utilities must also be marked through 811 when applicable.'),
            ('Zoning is the first county development permit', 'Randolph County Central Permitting states that the first development permit required in the county is the Planning Department Zoning Permit. Environmental Health and Building Inspections permits are then obtained as applicable to the project.'),
            ('Existing systems are inspected before certain new connections', 'Randolph County states that aboveground inspections of existing wastewater systems are performed before authorizing new connections to those systems, so reuse of an existing septic system should not be assumed without county approval.'),
        ],
    },
    'Rockingham': {
        'authority': 'Rockingham County Division of Public Health — Environmental Health, On-Site Wastewater Program',
        'contact': 'Rockingham County Governmental Center: 371 NC Hwy 65, Reidsville, NC 27320; county main line 336-342-8100.',
        'sources': [
            ('Rockingham County — On-Site Wastewater Program', 'https://www.rockinghamcountync.gov/21402'),
            ('Rockingham County — Septic Permitting Process', 'https://www.rockinghamcountync.gov/21404/Septic-Permitting-Process'),
            ('Rockingham County — Operation and Maintenance Inspections', 'https://www.rockinghamcountync.gov/21405/Operation-and-Maintenance-Inspections'),
            ('Rockingham County — Manufactured Home Process', 'https://www.rockinghamcountync.gov/21284'),
        ],
        'sections': [
            ('County program permits and oversees septic installation', 'Rockingham County states that its On-Site Wastewater Program is responsible for permitting and overseeing installation of subsurface septic systems, performing soil and site evaluations, handling repairs, and investigating failing systems.'),
            ('Operation Permit follows approved installation', 'Rockingham County states that after the septic system is installed correctly, Environmental Health issues the Operation Permit. This final approval should be obtained before relying on the system as approved for the permitted use.'),
            ('Repairs are evaluated by Environmental Health', 'Rockingham County says its Environmental Health staff investigate failing septic systems, determine feasible repair solutions, and use a repair-permitting process similar to that for a new lot. The county currently states that its septic repair evaluation is performed without a permit fee.'),
            ('Reconnect approval is required before reusing an existing system for a new home', 'When an owner wants to place a new home or manufactured home on a lot with an existing septic system, Rockingham County requires a reconnect permit. Environmental Health evaluates the system and states that a building permit or home placement cannot proceed until the reconnect permit is issued.'),
            ('Some system types have ongoing inspection requirements', 'Rockingham County explains that certain systems require recurring operation-and-maintenance inspections, including conventional systems with pumps, low-pressure pipe systems, and systems with pretreatment, in addition to monitoring by a certified subsurface operator where required by state rules.'),
        ],
    },
}

nc4_urls=[]
for county, data in NC4_COUNTIES.items():
    sources=[
        ('NCDHHS — On-Site Wastewater Program', NC_STATE),
        ('NCDHHS — On-Site Water Protection Branch', NC_BRANCH),
        ('NCDHHS — Homeowner septic permits and inspections guidance', NC_HOMEOWNER),
    ] + data['sources']
    sections=[
        ('North Carolina state and local framework', 'The N.C. Division of Public Health On-Site Water Protection Branch provides statewide regulatory oversight and technical guidance for subsurface onsite wastewater systems, while local health departments carry out county permitting and inspection functions. NCDHHS directs homeowners to the local health department for septic questions, permits, and inspections.')
    ] + data['sections']
    url=write_county_page('North Carolina','north-carolina',county,data['authority'],data['contact'],sections,sources,verified='August 29, 2026')
    nc4_urls.append(url)
    if not any(c == county for c, _ in nc_links):
        nc_links.append((county,data['authority']))

write_hub(
    'North Carolina','north-carolina',sorted(nc_links),
    'North Carolina’s On-Site Water Protection Branch provides statewide oversight for onsite wastewater systems, while local health departments perform the property-level permitting and inspection work. These guides are limited to counties with current, substantive local government guidance.',
    'This North Carolina set now covers 23 verified counties. SepticScope does not extrapolate one county’s workflow, fees, permit duration, inspection schedule, site-evaluation procedure, or local documentation requirements to another county.'
)

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    text=text.replace('Browse 18 verified North Carolina county septic guides →','Browse 23 verified North Carolina county septic guides →')
    county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists(): sm=sitemap.read_text(encoding='utf-8')
else: sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>' for u in nc4_urls if u not in sm)
if entries:
    sm=sm.replace('</urlset>',entries+'</urlset>')
    sitemap.write_text(sm,encoding='utf-8')

print(f'North Carolina fourth expansion complete: +{len(nc4_urls)} verified county guides')
