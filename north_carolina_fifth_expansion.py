# SepticScope North Carolina expansion — fifth validated county batch.
# Runs after the first four NC batches and uses their statewide source constants and accumulated nc_links.

NC5_COUNTIES = {
    'Carteret': {
        'authority': 'Carteret County Health Department — Environmental Health, Onsite Wastewater Program',
        'contact': 'Carteret County Environmental Health: 252-728-8499; 3820 Bridges Street, Suite A, Morehead City, NC 28557.',
        'sources': [
            ('Carteret County — Environmental Health', 'https://www.carteretcountync.gov/139/Environmental-Health'),
            ('Carteret County — Septic System Permits', 'https://www.carteretcountync.gov/207/Septic-System-Permits'),
            ('Carteret County — Improvement Permit', 'https://www.carteretcountync.gov/213/Improvement-Permit'),
            ('Carteret County — Operation Permit', 'https://www.carteretcountync.gov/214/Operation-Permit'),
            ('Carteret County — Expansion of an Existing System', 'https://www.carteretcountync.gov/212/Expansion-of-an-Existing-System'),
        ],
        'sections': [
            ('County Environmental Health permits, inspects, and approves onsite systems', 'Carteret County lists permitting, inspection, and approval of onsite wastewater systems among Environmental Health services and also performs compliance inspections of permitted wastewater systems.'),
            ('Improvement Permit documents the approved system and reserve area', 'After Environmental Health determines that a site is suitable, the county Improvement Permit identifies the initial system and reserve area, wells and water lines, structures and other improvements, and the proposed system type and conditions. Carteret states that the permit is valid for 60 months, or can be issued without expiration when the qualifying plat requirements are met.'),
            ('Operation Permit is required before Certificate of Occupancy release', 'Carteret County issues the Operation Permit only after final inspection confirms compliance with the Improvement Permit, Construction Authorization, and applicable wastewater rules. The county states that the Operation Permit is required before the building inspector releases the Certificate of Occupancy.'),
            ('Expansions require county review when wastewater flow increases', 'Carteret County requires wastewater-system expansion review when a proposed change increases design flow, including added bedrooms, increased retail area, or added restaurant seats or food-preparation area. The owner applies for an Improvement Permit, and Environmental Health inspects the existing system and site before an Improvement Permit and Construction Authorization can be issued.'),
            ('Certain advanced systems have continuing permit and operator obligations', 'Carteret County states that some low-pressure, filter, and pretreatment systems require certified operator or maintenance arrangements. Type V and VI pretreatment-system Operation Permits are valid for 60 months, with renewal applications required six months before expiration.'),
        ],
    },
    'Onslow': {
        'authority': 'Onslow County Health Department — Environmental Health Division, Onsite Wastewater',
        'contact': 'Onslow County Environmental Health: 910-938-5851; 234 NW Corridor Boulevard, Jacksonville, NC 28540.',
        'sources': [
            ('Onslow County — Environmental Health Division', 'https://www.onslowcountync.gov/EnvironmentalHealth'),
            ('Onslow County — Soil Evaluations', 'https://www.onslowcountync.gov/710/Soil-Evaluations'),
            ('Onslow County — Existing Septic Systems', 'https://www.onslowcountync.gov/679/Existing-Septic-Systems'),
            ('Onslow County — Environmental Health Fees', 'https://www.onslowcountync.gov/684/Application-Fees'),
        ],
        'sections': [
            ('County soil evaluation starts the ordinary new-system process', 'Onslow County requires a soil evaluation when an owner proposes a septic system, wants to relocate the system, or changes the permitted bedroom count. The county requires an application, accurately dimensioned property map, proposed layout, marked property corners, and the applicable fee before evaluation.'),
            ('Onslow uses a three-permit sequence', 'The county describes its onsite wastewater process as three stages: Improvement Permit, Construction Authorization, and Operation Permit. Construction Authorization is required to install the septic system and to obtain building permits, and the Operation Permit follows completion and approval of installation inspections.'),
            ('County publishes site-plan setback instructions for evaluations', 'Onslow County instructs applicants to show the proposed septic area, structures, water line, driveway, and existing systems on the property drawing. Its current soil-evaluation guidance states that proposed septic areas should be shown at least 10 feet from property lines and 5 feet from a dwelling, subject to the full applicable rules and site review.'),
            ('Existing System Authorization is required for qualifying additions', 'When an addition does not increase bedrooms and does not encroach on the septic system or well, Onslow County requires an Existing System Authorization with an application, floor plan, and site plan. County staff visit the site and issue the authorization before the building permit when the system is acceptable.'),
            ('Bedroom increases or septic relocation generally require new permit review', 'Onslow County states that increasing the number of bedrooms or relocating a septic system will likely require an Improvement Permit and Construction Authorization rather than the simpler Existing System Authorization process.'),
        ],
    },
    'Pender': {
        'authority': 'Pender County Health Department — Environmental Health, On-Site Wastewater Program',
        'contact': 'Pender County Health Department / Environmental Health: 910-259-1233; 805 S. Walker Street, Burgaw, NC 28425.',
        'sources': [
            ('Pender County — On-Site Wastewater Program & Wells', 'https://pendercountync.gov/230/On-Site-Wastewater-Program-Wells'),
            ('Pender County — Environmental Health Permit Application', 'https://pendercountync.gov/DocumentCenter/View/2736/Repair-Application-for-Environmental-Health-Permits'),
            ('Pender County — Unified Development Ordinance', 'https://pendercountync.gov/DocumentCenter/View/265/Pender-County-Unified-Development-Ordinance-UDO-PDF'),
        ],
        'sections': [
            ('County Environmental Health evaluates soils and oversees septic design and construction', 'Pender County states that its On-Site Wastewater Program works to ensure septic systems are appropriately designed, constructed, and operated. Environmental Health Specialists perform soil testing for septic suitability and provide technical guidance on new systems, repairs, and maintenance.'),
            ('Construction Authorization is required for installation and a building permit', 'Pender County’s Environmental Health application states that a Construction Authorization is needed to obtain a building permit and to install a septic system. The county uses this authorization for new construction, expansions, relocations, revisions, and repairs as applicable.'),
            ('County application distinguishes Improvement Permit, Construction Authorization, and existing-system review', 'Pender publishes separate application categories for site evaluation/Improvement Permit, Construction Authorization, repair of an existing system, private permitting options, and Existing System Authorization when there is no increase in wastewater flow.'),
            ('Subdivision and off-site proposals require planning-approved documents', 'Pender County’s septic application states that subdivision, recombination, and off-site proposals require a final plat or plan approved by Pender County Planning and Zoning. The county also requires applicable parcels, easements, and declarations to be recorded before Construction Authorization is issued.'),
            ('Final-platted lots must document an approved wastewater path', 'Pender County’s Unified Development Ordinance requires final-platted development lots to document an approved wastewater method, such as an Environmental Health Improvement Permit, qualifying engineered option, or the ordinance’s specified soil-suitability path. Lots without an approved wastewater method must carry the ordinance’s development limitation until an approved system is permitted.'),
        ],
    },
}

nc5_urls=[]
for county, data in NC5_COUNTIES.items():
    sources=[
        ('NCDHHS — On-Site Wastewater Program', NC_STATE),
        ('NCDHHS — On-Site Water Protection Branch', NC_BRANCH),
        ('NCDHHS — Homeowner septic permits and inspections guidance', NC_HOMEOWNER),
    ] + data['sources']
    sections=[
        ('North Carolina state and local framework', 'The N.C. Division of Public Health On-Site Water Protection Branch provides statewide regulatory oversight and technical guidance for subsurface onsite wastewater systems, while local health departments carry out county permitting and inspection functions. NCDHHS directs homeowners to the local health department for septic questions, permits, and inspections.')
    ] + data['sections']
    url=write_county_page('North Carolina','north-carolina',county,data['authority'],data['contact'],sections,sources,verified='August 30, 2026')
    nc5_urls.append(url)
    if not any(c == county for c, _ in nc_links):
        nc_links.append((county,data['authority']))

write_hub(
    'North Carolina','north-carolina',sorted(nc_links),
    'North Carolina’s On-Site Water Protection Branch provides statewide oversight for onsite wastewater systems, while local health departments perform the property-level permitting and inspection work. These guides are limited to counties with current, substantive local government guidance.',
    'This North Carolina set now covers 26 verified counties. SepticScope does not extrapolate one county’s workflow, fees, permit duration, inspection schedule, site-evaluation procedure, or local documentation requirements to another county.'
)

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    text=text.replace('Browse 23 verified North Carolina county septic guides →','Browse 26 verified North Carolina county septic guides →')
    county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists(): sm=sitemap.read_text(encoding='utf-8')
else: sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in nc5_urls if u not in sm)
if entries:
    sm=sm.replace('</urlset>',entries+'</urlset>')
    sitemap.write_text(sm,encoding='utf-8')

print(f'North Carolina fifth expansion complete: +{len(nc5_urls)} verified county guides')
