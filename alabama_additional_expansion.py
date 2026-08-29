# SepticScope Alabama expansion — additional counties with substantive current local guidance.
# Sources are limited to Alabama Department of Public Health or the Mobile County Health Department.

AL2_STATE='https://www.alabamapublichealth.gov/onsite/index.html'
AL2_BEFORE='https://www.alabamapublichealth.gov/onsite/before-construction.html'
AL2_RECORDS='https://www.alabamapublichealth.gov/onsite/septic-tanks.html'

AL2_COUNTIES={
    'Madison': {
        'authority':'Madison County Health Department — Community and Environmental Protection / Onsite Sewage Disposal',
        'contact':'Madison County Health Department Environmental Services: 256-533-8726; 301 Max Luther Drive NW, Huntsville, AL 35811.',
        'sources':[
            ('Madison County — Environmental Services','https://www.alabamapublichealth.gov/madison/environmental-services.html'),
            ('Madison County — Contact Us','https://www.alabamapublichealth.gov/madison/contact.html'),
        ],
        'sections':[
            ('Local permit and occupancy sequence','Madison County states that homes and businesses not connected to public sanitary sewer must obtain a local health department permit before installing a new onsite system or repairing an existing system. The county also directs installers to schedule an inspection before installation and states that an Approval for Use is issued before the building can be occupied.'),
            ('Local licensing reminder','Madison County specifically states that septic tank installers and pumpers must be licensed by the Alabama Onsite Wastewater Board.'),
        ],
    },
    'Mobile': {
        'authority':'Mobile County Health Department — Environmental Health, Onsite Services',
        'contact':'Mobile County Health Department Environmental Health: 251 North Bayou Street, Mobile, AL 36603. MCHD main phone: 251-690-8158.',
        'sources':[
            ('Mobile County Health Department — Environmental Health / Onsite Services','https://mchd.org/environmental-health/'),
            ('ADPH — County Health Department Locations','https://www.alabamapublichealth.gov/about/locations.html'),
        ],
        'sections':[
            ('County onsite division is the permitting authority','Mobile County Health Department states that its Onsite Sewage division regulates permitting, installation, and inspection of residential and commercial onsite sewage disposal systems in Mobile County under the ADPH Onsite Sewage Treatment and Disposal Rules.'),
            ('Industry licensing and pumper oversight','Mobile County states that persons involved in the onsite sewage disposal industry must be licensed by the Alabama Onsite Wastewater Board. Its Onsite division also regulates septic and sewage tank pumpers and requires annual inspection of pumper trucks before use.'),
        ],
    },
    'Etowah': {
        'authority':'Etowah County Health Department — Environmental Office (Alabama Department of Public Health)',
        'contact':'Etowah County Health Department Environmental Office: 256-439-2586; 709 East Broad Street, Gadsden, AL 35903.',
        'sources':[
            ('Etowah County — Environmental Fee Schedule','https://www.alabamapublichealth.gov/Etowah/environmental-fees.html'),
            ('Etowah County — Contact Us','https://www.alabamapublichealth.gov/Etowah/contact.html'),
        ],
        'sections':[
            ('County publishes separate onsite permit categories','Etowah County publishes separate local fee categories for conventional and engineered residential sewage permits, commercial conventional and engineered permits, and expedited review. The county has announced a revised fee schedule effective September 1, 2026; applicants should verify the fee in effect on the filing date rather than relying on an older amount.'),
            ('Environmental Office handles septic requests','The current Etowah County Health Department contact page directs septic-tank requests to the Environmental Office and provides a dedicated environmental phone number.'),
        ],
    },
    'Lowndes': {
        'authority':'Lowndes County Health Department / Alabama Department of Public Health onsite sewage program',
        'contact':'Lowndes County Health Department: 334-548-2564; 507 East Tuskeena Street, Hayneville, AL 36040. ADPH also operates a Lowndes County Septic System Improvement Program for qualifying households.',
        'sources':[
            ('ADPH — Lowndes County septic agreement and program','https://www.alabamapublichealth.gov/blog/2023/06/nr-06.html'),
            ('ADPH — Lowndes County program anniversary update','https://www.alabamapublichealth.gov/blog/2024/05/nr-06.html'),
            ('ADPH — County Health Department Locations','https://www.alabamapublichealth.gov/about/locations.html'),
        ],
        'sections':[
            ('County has a special sanitation-improvement program','ADPH established a Lowndes County Septic System Improvement Program to support installation or repair of ADPH-approved systems designed for difficult local soil conditions. This is a county-specific assistance program and does not replace the ordinary requirement to obtain approval for onsite sewage work.'),
            ('Special enforcement agreement does not eliminate permitting','Under the ADPH interim agreement described for Lowndes County, qualifying residents with straight pipes or failing septic systems are not referred for criminal enforcement merely because of those conditions while participating in specified processes. ADPH still directs residents toward approved onsite systems designed for the property and the applicable approval process.'),
        ],
    },
}

al2_urls=[]
for county,data in AL2_COUNTIES.items():
    sections=[
        ('Alabama permit framework','Alabama requires a permit from the local health department before installing a new onsite sewage disposal system or repairing an existing system. State guidance calls for site and soil evaluation, permit review, licensed installation, and health-department approval before use.'),
        ('Existing septic records','ADPH says property owners or their agents may request existing septic-system information from the local health department. A completed Approval for Use may include a diagram of the installed system.'),
    ] + data['sections']
    sources=[
        ('ADPH — Soil and Onsite Sewage Branch',AL2_STATE),
        ('ADPH — Before Construction',AL2_BEFORE),
        ('ADPH — Septic Tank Systems and Records',AL2_RECORDS),
    ] + data['sources']
    url=write_county_page('Alabama','alabama',county,data['authority'],data['contact'],sections,sources,verified='August 29, 2026')
    al2_urls.append(url)
    if county not in al_links: al_links.append(county)

write_hub(
    'Alabama','alabama',[(c,'County or local health department onsite authority') for c in sorted(al_links)],
    'Alabama’s Soil and Onsite Sewage Branch coordinates onsite sewage regulation through county health departments. SepticScope includes only counties whose local authority and useful permit guidance have been validated from current public-health sources.',
    'This Alabama set now includes 11 verified counties. County-specific fees, special programs, and local workflow details are included only where an authoritative local source supports them.'
)

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    text=text.replace('Browse the first 7 verified Alabama county septic guides →','Browse 11 verified Alabama county septic guides →')
    county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists(): sm=sitemap.read_text(encoding='utf-8')
else: sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>' for u in al2_urls if u not in sm)
if entries:
    sm=sm.replace('</urlset>',entries+'</urlset>')
    sitemap.write_text(sm,encoding='utf-8')

print(f'Alabama additional expansion complete: +{len(al2_urls)} verified county guides')
