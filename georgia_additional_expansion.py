# SepticScope Georgia additional expansion — validated from official government/public-health sources on 2026-08-29.

GA_ADD_STATE = 'https://dph.georgia.gov/environmental-health/onsite-sewage'
GA_ADD_COUNTIES = {
    'Forsyth': {
        'authority': 'Forsyth County Environmental Health — Land Use Section',
        'contact': 'Forsyth County Environmental Health: 770-781-6909; 2435 Freedom Pkwy, Suite 2400, Cumming, GA 30041.',
        'sources': [
            ('Forsyth County Environmental Health — Sewage Disposal', 'https://www.forsythhd.com/pages/environmental/Sewage/Sewage.html'),
            ('Forsyth County Environmental Health — Current Fees', 'https://www.forsythhd.com/pages/environmental/Environmental_Health_Fees.html'),
            ('Forsyth County Environmental Health — Permitting Information', 'https://www.forsythhd.com/pages/environmental/permitting%20information.html'),
        ],
        'sections': [
            ('Environmental Health issues permits and performs final inspections', 'Forsyth County Environmental Health states that its Land Use Section issues onsite sewage management system permits and performs final inspections. Septic approval is required before a building permit for a septic-served property when building or remodeling a home or adding a building or pool.'),
            ('New systems, repairs, additions and existing-system reviews use separate processes', 'The county publishes separate application and requirement materials for new septic systems, repairs, additions or modifications, commercial systems, pool-related performance evaluations and other existing-system evaluations. Applicants should use the form that matches the proposed work rather than assuming a new-system application covers a repair or modification.'),
            ('Allow time for review', 'Forsyth County Environmental Health warns that an application or review may take twenty business days or more. Completed forms and required documents can be submitted to Environmental Health using the county instructions.'),
            ('Published 2024 residential septic fees', 'The county fee schedule lists a new residential septic permit at $350 for seven rooms or fewer and $550 for eight rooms or more; residential repair is $150, and a residential addition or modification is $350. Because fee schedules can change, confirm the current amount before payment.'),
            ('Use state-certified professionals where required', 'Forsyth links directly to Georgia DPH lists of approved soil classifiers, certified septic installers and certified pumpers. Verify current certification before hiring a contractor or soil professional.'),
        ],
    },
    'Hall': {
        'authority': 'Hall County Environmental Health',
        'contact': 'Hall County Environmental Health: 770-531-3973; environmental@hallcounty.org; 2875 Browns Bridge Road, Gainesville, GA 30504.',
        'sources': [
            ('Hall County — Environmental Health', 'https://www.hallcounty.org/192/Environmental-Health'),
            ('Hall County — Septic System Permit Application Requirements for New Construction', 'https://www.hallcounty.org/DocumentCenter/View/134/Septic-Permit-Application-Requirements-PDF'),
        ],
        'sections': [
            ('Environmental Health review comes before the building permit', 'For properties in unincorporated Hall County that are served by septic, Hall County directs applicants to Environmental Health for review before applying for the county building permit. A valid issued septic permit is required before a new-construction building permit.'),
            ('New-system applications require property, soil and site information', 'Hall County’s published new-construction checklist requires a recorded plat when available, proof of ownership, a Level III soil analysis when soil information is not already on file, a complete septic application and a scaled site plan. The site plan must show the house, primary and reserve septic areas, improvements and applicable water features or wells with required setbacks.'),
            ('House location must be staked before site evaluation', 'The county requires the proposed house location to be staked before the Environmental Health site evaluation. If the structure is not staked, the county warns that a return visit can generate a re-inspection fee.'),
            ('Well permitting can run with the septic application', 'If public water is unavailable and there is no existing well, Hall County instructs the applicant to apply for a well permit at the same time as the septic permit. The well location must be shown on the property plan according to the county checklist.'),
            ('Installation inspection is coordinated through Environmental Health', 'Hall County tells certified septic contractors to request septic installation inspections through Environmental Health. The county page currently directs same-day inspection requests to be called in between 8:00 and 9:00 a.m.; later requests are scheduled for the next working day.'),
        ],
    },
    'Cherokee': {
        'authority': 'Cherokee County Environmental Health — North Georgia Health District',
        'contact': 'Cherokee County Environmental Health: 770-479-0444; 1130 Bluffs Parkway, Canton, GA 30114.',
        'sources': [
            ('North Georgia Health District — Cherokee County Environmental Health', 'https://nghd.org/nghd-locations-listing/item/cherokee-county-eh'),
            ('North Georgia Health District — On-Site Sewage Management Systems', 'https://www.nghd.org/nghd-services/item/on-site-sewage-management-systems-ossms'),
            ('North Georgia Health District — Environmental Health FAQs', 'https://www.nghd.org/eh-faqs'),
        ],
        'sections': [
            ('Local Environmental Health evaluates septic sites and permits systems', 'North Georgia Health District identifies Cherokee County Environmental Health as the local office for onsite sewage management systems and describes its work as including property evaluation for septic permits, plan review, homeowner education and septic-system oversight.'),
            ('A permit is required before new installation, addition, modification or repair', 'North Georgia Health District states that an onsite sewage permit must be obtained before installation and that the requirement includes new septic systems, additions, modifications and repairs.'),
            ('County-specific lot-size rules can apply', 'The district warns that each county in its service area has local Board of Health adopted lot sizes. Cherokee property owners should obtain the current Cherokee requirements from the local Environmental Health office rather than relying on another county’s minimum lot size.'),
            ('Soil information and existing septic drawings are handled through Environmental Health', 'The district directs owners needing a soil test, existing soil information, septic permit application or septic drawing to the county Environmental Health office. Existing septic drawings are not presented as a public online database; the office can provide available property records on request.'),
            ('Use Georgia-certified septic professionals', 'Georgia DPH maintains statewide certification lists for septic installers, pumpers and soil classifiers. The district directs property owners to those lists when septic professional services are needed.'),
        ],
    },
}

ga_add_urls = []
existing_ga_names = set(ga_links) if 'ga_links' in globals() else set()
for county, data in GA_ADD_COUNTIES.items():
    sources = [('Georgia Department of Public Health — Onsite Sewage', GA_ADD_STATE)] + data['sources']
    sections = [
        ('Georgia onsite-sewage framework', 'Georgia Department of Public Health regulates onsite sewage statewide while locally related permits, inspections, records and property-specific questions are handled through local County Environmental Health offices.')
    ] + data['sections']
    url = write_county_page(
        'Georgia', 'georgia', county,
        data['authority'], data['contact'], sections, sources,
        verified='August 29, 2026'
    )
    ga_add_urls.append(url)
    existing_ga_names.add(county)

# Preserve the earlier verified Georgia counties while refreshing the state hub.
ga_links = sorted(existing_ga_names)
write_hub(
    'Georgia', 'georgia',
    [(county, 'Verified local Environmental Health septic guide') for county in ga_links],
    'Georgia DPH regulates onsite sewage statewide while County Environmental Health offices administer property-level septic permitting, inspection and records. SepticScope verifies local authority and county-specific process details before promoting a county from lookup status.',
    f'This Georgia collection now includes {len(ga_links)} verified county guides. Requirements such as application documents, fees, local lot-size rules, site evaluation and inspection procedures are included only when supported by current government or public-health sources.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    import re
    text = re.sub(r'Browse \d+ verified Georgia county septic guides →', f'Browse {len(ga_links)} verified Georgia county septic guides →', text)
    county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>' for u in ga_add_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'Georgia additional expansion complete: +{len(ga_add_urls)} verified county guides; {len(ga_links)} total verified Georgia counties')
