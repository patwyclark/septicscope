# SepticScope Tennessee contract-county completion — Davidson, Knox, and Sevier.
# Verified from TDEC and official metropolitan/county sources on 2026-08-30.

TN_FINAL_CONTRACT_COUNTIES = {
    'Davidson': {
        'authority': 'Metro Public Health Department — Environmental Health, Septic and Sewage Disposal Systems / Environmental Engineering Services',
        'contact': 'Metro Public Health Department handles septic and sewage-disposal review in Nashville and Davidson County. Septic questions: 615-340-5630. The program provides onsite-system engineering, soils interpretation, development review, records, and septic-related permitting coordination.',
        'sources': [
            ('Metro Nashville — Septic and Sewage Disposal Systems','https://www.nashville.gov/departments/health/environmental-health/septic-and-sewage-disposal-systems'),
            ('Metro Nashville — Codes permitting contact list','https://www.nashville.gov/departments/codes/construction-and-permits/contact-list'),
            ('Metro Nashville — feasibility assessments for private septic systems','https://www.nashville.gov/departments/health/environmental-health/septic-and-sewage-disposal-systems/how-many-bedrooms'),
            ('Metro Public Health — public records requests','https://www.nashville.gov/departments/health/services/submit-public-records-request-health'),
        ],
        'sections': [
            ('Metro Public Health is the local septic authority','TDEC identifies Davidson County/Nashville as a contract jurisdiction that provides its own groundwater-protection and septic services. Metro Public Health’s Septic and Sewage Disposal Systems program states that it performs soils interpretation, onsite-system design, technical consulting, land-use and development review, percolation-test monitoring, groundwater protection, and enforcement of rules governing subsurface sewage disposal.'),
            ('Septic review is part of Metro development permitting','Metro Codes’ current permitting contact list identifies the Health Department as the septic contact for building-permit coordination and directs septic questions to the Environmental Engineering program at 615-340-5630. Applicants should resolve septic feasibility and required Health Department review before assuming a Codes building permit can proceed independently.'),
            ('Parcel identification is required for property-specific research','Metro’s septic program states that property questions require the map-and-parcel number or tax ID. The program provides a property-file search for scanned Environmental Engineering files and a separate process to obtain existing approval, inspection, and bedroom information.'),
            ('New-residence feasibility can be checked before final design','Metro Public Health provides a feasibility-assessment process for newly constructed residences that proposes use of a private septic system. The Environmental Engineering Services Program searches its files and reports available property information; existing homes use the separate septic-system assessment or records process.'),
            ('Public sanitary sewer availability can change the path','Metro’s septic information form notes that a property may appear to have public sanitary sewer available and directs owners to Metro Water Services or the responsible utility to confirm availability and line location. Sewer availability should therefore be resolved early rather than assuming an onsite system will be accepted.'),
        ],
    },
    'Knox': {
        'authority': 'Knox County Health Department — Environmental Health, Groundwater Protection Division',
        'contact': 'Knox County Health Department Groundwater Protection Division, 140 Dameron Avenue, Knoxville, TN 37917. Septic permit and groundwater-services questions: 865-215-5200.',
        'sources': [
            ('Knox County Health Department — Groundwater Protection','https://www.knoxcounty.org/health/groundwater_protection.php'),
        ],
        'sections': [
            ('County Health regulates every local SSDS not on public sewer','Knox County states that its Groundwater Protection Division enforces the laws governing onsite wastewater systems and regulates installation of subsurface sewage disposal systems. Residential and commercial facilities that are not connected to public sanitary sewer must have an SSDS to receive and treat the wastewater they generate.'),
            ('County specialists evaluate, design, and inspect systems','The Groundwater Protection Division states that its environmental specialists assist property owners with evaluation, design, and inspection of SSDS installed in Knox County. TDEC rules and statutes remain the governing statewide framework, but Knox is the local contract-county program for permit services.'),
            ('Permits cover new builds, remodels, and repairs','Knox County specifically states that its Groundwater Division issues septic permits for new builds, remodels, and repairs to existing systems when required. Depending on the project, the county may require a soil map and/or site plan before preparing the SSDS permit, drainfield layout, certification, or verification.'),
            ('Existing records can reveal prior soils and repair history','Knox County provides SSDS file searches for existing properties. The county notes that a file search can help a buyer determine whether an existing system is documented and can reveal prior soil mapping or repair records associated with the parcel.'),
            ('Installers and pumpers need an annual Knox County permit','Knox County states that septic-tank installers and pumpers working in the county must obtain an annual county permit. This is a local credential requirement in addition to the statewide installer/pumper framework, so contractors should verify both current state and Knox County status.'),
        ],
    },
    'Sevier': {
        'authority': 'Sevier County Environmental Health',
        'contact': 'Sevier County Environmental Health, 227 Cedar Street, Sevierville, TN 37862; 865-429-1766. The department accepts septic, repair, inspection-letter, and site-evaluation applications and provides local installer, pumper, engineer/surveyor, and soil-scientist resources.',
        'sources': [
            ('Sevier County — Environmental Health','https://www.seviercountytn.gov/government/departments/services/environmental_health.php'),
        ],
        'sections': [
            ('Sevier County runs the local septic application process','TDEC identifies Sevier as a contract county, and Sevier County Environmental Health publishes the local septic permit, repair permit, site evaluation, inspection letter, subdivision evaluation, installer/pumper resources, and property-information process. Applicants should use this county workflow rather than the ordinary TDEC online application used in non-contract counties.'),
            ('The county accepts several applications online','Sevier County states that septic permit, repair permit, well-water test, inspection-letter, and site-evaluation applications may be submitted through its online application system. The county notes that processing does not begin until payment and all required material are received; subdivision and large-conventional-system services continue to use the county’s other filing procedures.'),
            ('Certain subdivisions require a current survey','Sevier County specifically requires current surveys for applications in Shagbark, Sky Harbor, and English Mountain. The county states that those surveys must be original surveyor prints at 1 inch = 50 feet or 1 inch = 100 feet, and an inspector may request a survey elsewhere when lot lines are uncertain or the property has not been surveyed recently.'),
            ('Failed final inspections trigger a county reinspection process','Effective June 1, 2024, Sevier County requires a reinspection application and a $100 reinspection fee after a septic final inspection fails the initial inspection. The installer must correct the cited issue and then follow the county process to schedule the return inspection.'),
            ('The county publishes current project-specific septic fees','Sevier County’s Environmental Health page currently lists a $300 septic permit, $75 repair permit, $100 inspection letter, and subdivision evaluation fees, while also linking its current fee schedule. Because fees can change, applicants should confirm the posted schedule when filing.'),
            ('One- and two-bedroom homes have published minimum home-size criteria','Sevier County publishes an effective August 14, 2023 local notice stating minimum home sizes of 1,200 square feet for a one-bedroom home and 1,500 square feet for a two-bedroom home in the cited septic guidance. Property owners planning a small dwelling should confirm the current applicability of that county criterion before finalizing plans.'),
        ],
    },
}

final_contract_urls=[]
final_contract_links=[]
for county,data in TN_FINAL_CONTRACT_COUNTIES.items():
    sections=[
        ('Tennessee contract-county framework','TDEC’s current septic-services page identifies Davidson, Knox, and Sevier among the jurisdictions that provide their own groundwater-protection services. SepticScope therefore follows the local metropolitan or county process below instead of substituting the standard TDEC field-office workflow used in most Tennessee counties.')
    ] + data['sections']
    sources=[
        ('TDEC — local/contract county septic-services routing','https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/wr-sds-online-application-for-ground-water-protection-services.html'),
        ('TDEC — Septic System Construction Permit','https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/permit-water-septic-system-construction-permit.html'),
        ('TDEC — licensed septic installers and pumpers','https://www.tn.gov/environment/permits/water/septic-systems-permits/ssp/wr-sds-active-installers-pumpers.html'),
    ] + data['sources']
    url=write_county_page('Tennessee','tennessee',county,data['authority'],data['contact'],sections,sources,verified='August 30, 2026')
    final_contract_urls.append(url)
    final_contract_links.append((county,data['authority']))

# Complete the Tennessee hub: 86 TDEC-served counties + all 9 locally administered contract counties.
tn_complete_links=[(c,f'TDEC {o} Environmental Field Office') for c,o in tn_links] + contract_links + final_contract_links
write_hub(
    'Tennessee','tennessee',sorted(tn_complete_links),
    'Tennessee uses TDEC’s statewide Subsurface Sewage Disposal System program in most counties and locally administered groundwater-protection programs in nine contract counties. SepticScope identifies the correct permitting path for each county instead of applying a single workflow statewide.',
    'All 95 Tennessee counties now have an official-source permitting guide. The nine locally administered contract jurisdictions are Blount, Davidson, Hamilton, Jefferson, Knox, Madison, Sevier, Shelby, and Williamson; the remaining counties use the appropriate TDEC Environmental Field Office path.'
)

county_index=OUTPUT/'counties'/'index.html'
if county_index.exists():
    text=county_index.read_text(encoding='utf-8')
    text=text.replace('Browse 92 verified Tennessee county septic guides →','Browse all 95 verified Tennessee county septic guides →')
    text=text.replace('Browse 86 verified Tennessee county septic guides →','Browse all 95 verified Tennessee county septic guides →')
    county_index.write_text(text,encoding='utf-8')

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
else:
    sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in final_contract_urls if u not in sm)
if entries:
    sm=sm.replace('</urlset>',entries+'</urlset>')
    sitemap.write_text(sm,encoding='utf-8')

print(f'Tennessee contract-county completion: +{len(final_contract_urls)} verified county guides; all 95 Tennessee counties covered')
