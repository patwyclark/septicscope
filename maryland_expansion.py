# SepticScope Maryland expansion — verified county batch.
# Verified from Maryland Department of the Environment and official county/local health sources on 2026-08-31.

MD_MDE = 'https://mde.maryland.gov/programs/water/bayrestorationfund/onsitedisposalsystems/pages/onsitesystems.aspx'
MD_PROS = 'https://mde.maryland.gov/programs/water/wwp/Pages/State-Board-of-On-Site-Wastewater-Professionals.aspx'
MD_COUNTIES = [
    {
        'county': 'Anne Arundel',
        'authority': 'Anne Arundel County Department of Health — Bureau of Environmental Health, Sanitary Engineering Program',
        'contact': 'Sanitary Engineering Program: 410-222-7193; 3 Harry S. Truman Parkway, Annapolis, MD 21401.',
        'sources': [
            ('Anne Arundel County Health — Wells and Septic Systems', 'https://www.aahealth.org/environmental-health/wells-and-septic-systems'),
            ('Anne Arundel County Health — Perc Testing', 'https://www.aahealth.org/environmental-health/wells-and-septic-systems/perc-testing'),
            ('Anne Arundel County Health — Permit Fees', 'https://www.aahealth.org/environmental-health/permit-fees'),
            ('Anne Arundel County Health — Property Improvements', 'https://www.aahealth.org/environmental-health/wells-and-septic-systems/well-and-septic-applications-property-improvements'),
        ],
        'sections': [
            ('County Health reviews, permits, and inspects private septic systems', 'Anne Arundel County Health states that its Sanitary Engineering Program reviews and approves properties for private septic systems, conducts percolation tests, determines system design requirements, issues construction permits, and inspects private septic systems.'),
            ('Perc testing establishes the sewage disposal area', 'For properties using onsite disposal, the county requires testing in the proposed disposal area. Its current guidance generally calls for at least three satisfactory perc tests and enough suitable area for the initial system plus two replacement systems; additional testing may be required based on soils, topography, groundwater, or site size.'),
            ('Some properties can only be evaluated during wet season', 'Anne Arundel County identifies areas where septic suitability must be evaluated during wet-season groundwater conditions. The county announces the testing window based on groundwater monitoring rather than guaranteeing fixed calendar dates each year.'),
            ('Building additions can trigger septic review or system modifications', 'For property improvements served by septic, the proposed addition must meet sewage-disposal setbacks. County Health may require perc testing, excavation of existing components, tank replacement, or a new drainfield, drywell, or mound, and required septic modifications must be completed before Health signs off on the building permit.'),
            ('County publishes distinct septic installation fees', 'Anne Arundel County Health publishes separate current fees for complete systems, tank-only work, drainfields or drywells, distribution boxes, piping, pump pits, holding tanks, nitrogen-reducing systems, and commercial systems. Applicants should confirm the current fee schedule before filing.'),
        ],
    },
    {
        'county': 'Frederick',
        'authority': 'Frederick County Health Department — Environmental Health Services, Well & Septic Office',
        'contact': 'Well & Septic Office: 301-600-1726; Frederick County Health Department, 350 Montevue Lane, Frederick, MD 21702.',
        'sources': [
            ('Frederick County Health — Septic Repair', 'https://health.frederickcountymd.gov/379/Septic-Repair'),
            ('Frederick County Health — Building Permit Approval', 'https://health.frederickcountymd.gov/381/Building-Permit-Approval'),
            ('Frederick County Health — Percolation Test', 'https://health.frederickcountymd.gov/377/Percolation-Test'),
            ('Frederick County Government — Septic System Pump-Out Rebate', 'https://www.frederickcountymd.gov/7574/Septic-System-Pump-Out-Rebate'),
        ],
        'sections': [
            ('County Health is the local Well & Septic permitting office', 'Frederick County Health Department Environmental Health Services operates the county Well & Septic Office and handles septic repair permits, site evaluation/percolation testing, and health review associated with building permits.'),
            ('New onsite sewage plans must come from qualified private-sector designers', 'Frederick County Health states that, beginning August 1, 2022, it no longer prepares plans for issuance of an onsite sewage disposal system permit. Plans must be developed and submitted for approval by qualified private-sector designers under Maryland requirements.'),
            ('Soil evaluation and percolation testing determine system feasibility and capacity', 'The county states that soil evaluations and perc tests are used to determine soil absorption characteristics, the number of bedrooms a septic system can support, and the type of system needed. Testing is scheduled with the Health Department after the applicable planning review and fee process.'),
            ('Repairs require a county permit, licensed local installer, and final inspection', 'Frederick County requires an in-person septic repair permit application and selection of a licensed Frederick County septic installer. A Sanitarian performs the necessary site evaluation/testing, and completed repair work must remain uncovered until the final Health Department inspection. The county then issues a certificate documenting satisfactory completion.'),
            ('County offers a maintenance incentive tied to licensed haulers', 'Frederick County Government currently offers a septic pump-out rebate program, subject to funding and eligibility, for qualifying households using a county-licensed liquid waste hauler. The program is an incentive rather than a substitute for permit or repair requirements.'),
        ],
    },
    {
        'county': 'Howard',
        'authority': 'Howard County Health Department — Bureau of Environmental Health, Well & Septic Program',
        'contact': 'Well & Septic Program: 410-313-1771; Bureau of Environmental Health, 8930 Stanford Boulevard, Columbia, MD 21045.',
        'sources': [
            ('Howard County — Well & Septic Program', 'https://www.howardcountymd.gov/health/well-septic-program'),
            ('Howard County — Inspections & Enforcement Division', 'https://www.howardcountymd.gov/inspections-licenses-permits/inspections-enforcement-division'),
        ],
        'sections': [
            ('County Health reviews onsite sewage designs and inspects installations and repairs', 'Howard County states that its Well & Septic Program ensures proper installation and repair of onsite sewage disposal systems, reviews proposed system designs for compliance with state and local regulations, and has Environmental Health Specialists inspect onsite systems.'),
            ('Percolation testing can be seasonally restricted', 'Howard County operates wet-season percolation testing when groundwater conditions allow. For 2026, the Health Department announced that wet-season testing closed on March 27, illustrating that applicants with seasonally limited sites must follow the county’s current testing announcements rather than assume testing is available year-round.'),
            ('Well and septic questions and inspections are routed to Environmental Health', 'Howard County’s Inspections & Enforcement guidance directs well and septic questions to the Health Department Well & Septic Program at 410-313-1771, separate from the county building, plumbing, and public-utility inspection programs.'),
            ('State and local rules both apply to design review', 'Howard County explicitly states that proposed onsite sewage disposal designs are reviewed for both State and Local regulations. Applicants should therefore use the county program for property-specific requirements instead of relying only on statewide septic guidance.'),
        ],
    },
    {
        'county': 'Montgomery',
        'authority': 'Montgomery County Department of Permitting Services (DPS) — Land Development Division, Well & Septic Section',
        'contact': 'DPS Well & Septic Section: call MC311 at 311 in Montgomery County or 240-777-0311 from outside the county; inspections: 240-777-6306; 2425 Reedie Drive, 7th Floor, Wheaton, MD 20902.',
        'sources': [
            ('Montgomery County DPS — Septic Permit Process', 'https://www.montgomerycountymd.gov/department-permitting-services/all-permits/well-septic-permits/septic-permit-process'),
            ('Montgomery County DPS — Septic System Repair Permit Process', 'https://www.montgomerycountymd.gov/department-permitting-services/all-permits/well-septic-permits/septic-system-repair-permit-process'),
            ('Montgomery County DEP — Onsite System Testing and Permitting', 'https://www.montgomerycountymd.gov/DEP/water/water-supply-wastewater/onsite-system-testing-permitting.html'),
            ('Montgomery County DEP — Onsite Well and Septic Systems Management Program', 'https://www.montgomerycountymd.gov/department-environmental-protection/water/water-supply-wastewater/private-well-septic-page/onsite-well-septic-systems-management-program'),
        ],
        'sections': [
            ('DPS is the delegated local septic permitting authority', 'Montgomery County states that its Department of Permitting Services, acting on behalf of the Maryland Department of the Environment, is responsible for testing for and permitting wells and septic systems in the county. This differs from many Maryland jurisdictions where a local health department performs the same delegated function.'),
            ('New systems and certain building additions require a septic permit', 'A county septic permit is required to install a system for a new home and to upgrade or replace an existing system to accommodate a building addition. For building-permit applications received on or after July 1, 2024, when an addition or alteration requires septic components to be upgraded or relocated, the septic work and permit conditions must be completed before the related building permit can be approved and issued.'),
            ('Permit application, plan review, and fees are handled through DPS', 'Montgomery County allows online septic applications and requires a nonrefundable filing fee at application. For electronic applications, required plans must be uploaded within five business days or the application can be voided. The county directs applicants to its current DPS fee regulation rather than publishing a fixed fee in the septic process page, so SepticScope does not hard-code a dollar amount here.'),
            ('Permits expire after twelve months unless extended once', 'Montgomery County states that septic system permits are valid for 12 months from issuance and may receive one six-month extension. After expiration, a new application and fee are required.'),
            ('At least two installation inspections are required', 'Once a new septic installation begins, Montgomery County requires a minimum of two inspections. Final system approval is issued only after the system is complete, required inspections pass, and all permit conditions are satisfied. The county advises owners to retain the approved permit and as-built drawing.'),
            ('Failing-system replacements use a separate repair process', 'Replacement of a failing septic system requires a septic repair permit. Montgomery County states that repair permits are expedited based on available information, and the installer must request inspection before installation begins.'),
            ('County management program provides maintenance resources', 'Montgomery County Department of Environmental Protection operates an onsite well and septic systems management program that provides operation and maintenance guidance and a voluntary maintenance-reminder service. These resources support long-term system care but do not replace DPS permit or inspection requirements.'),
        ],
    },
    {
        'county': 'Harford',
        'authority': 'Harford County Health Department — Bureau of Environmental Health, Land & Water Resources & Permits Division',
        'contact': 'Environmental Health: 410-877-2300; 120 S. Hays Street, Suite 200, Bel Air, MD 21014.',
        'sources': [
            ('Harford County Health Department — 2025 Land & Water Resources & Permits Fee Schedule', 'https://harfordcountyhealth.com/wp-content/uploads/2024/10/V2-Combined-Fee-Schedules-Eff-1-1-2025.pdf'),
            ('Harford County Health Department — Soil Percolation Test Application Procedure', 'https://harfordcountyhealth.com/wp-content/uploads/2025/02/Soil-Percolation-Test-Application-Procedure-1-2025.pdf'),
            ('Harford County Health Department — New Home Construction: Building with a Well and Septic System', 'https://harfordcountyhealth.com/wp-content/uploads/2025/11/SFD-Booklet-Enclosures-v.11-2025-Jodi-Higgs-HCHD-.pdf'),
            ('Harford County Government — Building Inspections', 'https://www.harfordcountymd.gov/295/Building-Inspections'),
            ('Harford County Government — Plumbing/Mechanical Services and septic credentials', 'https://www.harfordcountymd.gov/338/PlumbingMechanical-Services'),
        ],
        'sections': [
            ('Health Department permits and inspects onsite sewage disposal systems', 'Harford County Health Department identifies its Septic Inspection program as the local program that issues onsite sewage disposal system permits and inspects new, replacement, and upgraded systems. County building-inspection guidance separately routes well and septic inspections to the Health Department.'),
            ('Perc testing is part of site review where public sewer is unavailable', 'The Health Department’s current soil-testing procedure states that, in the absence of public sewer, Harford County Code Chapter 216 and COMAR 26.04.02 require soil percolation testing as part of septic site review. An owner seeking a new system or repair/replacement must first obtain the required sanitary construction permit from the Health Department.'),
            ('Perc applications require a scaled site plan and documented nearby features', 'For non-repair percolation testing, Harford requires a site plan drawn to an accepted scale and showing property lines or easements, structures, driveways, the proposed or existing septic area, and wells, septic systems, or septic reserve areas within 200 feet. The applicant must also provide prior soil-test or relevant environmental-assessment information when available.'),
            ('Published 2025 septic fees are unusually specific', 'Harford County Health Department’s fee schedule effective January 1, 2025 lists $250 for a conventional soil percolation test per lot for up to five evaluations, $300 for a non-conventional or single-ring test for up to five evaluations, $400 for new sanitary construction, $210 for an upgrade to a septic system, $100 for correction to a septic tank or disposal area, $50 for correction to a sewer line or distribution box, and $25 for septic sizing including engineering-plan submissions. Applicants should confirm that the schedule remains current when filing.'),
            ('Septic review is integrated with new-home permitting', 'Harford County’s current new-home guidance is specifically for homes on lots served by a private well and/or onsite sewage disposal system and directs septic matters to the Bureau of Environmental Health. The Health Department also reviews subdivision and site plans for property served by onsite wells and septic systems.'),
            ('County has septic-specific local trade credentials', 'Harford County Government’s licensing information lists Journey Septic and Septic Certificate credentials among the regulated plumbing/septic categories. Property owners should verify that contractors performing regulated work hold the credentials required for the work being performed.'),
            ('Repairs and failing systems receive site-specific evaluation', 'Harford’s soil-testing program states that testing is also performed to establish criteria for design and repair of failing onsite sewage disposal systems. Its Bay Restoration Fund program may provide qualifying financial assistance for repair of failing systems through best-available-technology septic tanks or connection to public sewer when available.'),
        ],
    },
]

md_urls=[]
for d in MD_COUNTIES:
    sources=[
        ('Maryland Department of the Environment — Onsite Systems Division', MD_MDE),
        ('Maryland State Board of On-Site Wastewater Professionals', MD_PROS),
    ] + d['sources']
    sections=[
        ('Maryland state and local framework', 'Maryland Department of the Environment states that its Onsite Systems Division provides technical direction to County Health Departments and Local Approving Authorities for delegated onsite sewage disposal programs. MDE also states that small onsite systems below 5,000 gallons per day are generally permitted by local health departments, while larger systems can require state groundwater-discharge review.'),
        ('On-site wastewater professionals have state credential requirements', 'Maryland law established statewide credential requirements for people providing onsite wastewater services, including design, installation, operation and maintenance, pumping, repair, and property-transfer inspection. MDE states that local approving authorities verify applicable registration or licensing status when issuing septic construction permits, and local requirements may also apply.'),
    ] + d['sections']
    md_urls.append(write_county_page('Maryland','maryland',d['county'],d['authority'],d['contact'],sections,sources,verified='August 31, 2026'))

# The existing Prince George's County guide is already verified by the high-population expansion.
# Nationwide county generation rebuilds the Maryland hub after all verified pages are present.
sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists(): sm=sitemap.read_text(encoding='utf-8')
else: sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-31</lastmod></url>' for u in md_urls if u not in sm)
if entries:
    sm=sm.replace('</urlset>',entries+'</urlset>')
    sitemap.write_text(sm,encoding='utf-8')

print(f'Maryland expansion complete: +{len(md_urls)} verified county guides')
