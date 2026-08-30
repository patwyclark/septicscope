# SepticScope Colorado expansion — verified county batch.
# Verified from Colorado state law/regulation and official county/local public-health sources on 2026-08-30.

CO_RULES = 'https://www.sos.state.co.us/CCR/GenerateRulePdf.do?fileName=5+CCR+1002-43&ruleVersionId=7614'
CO_STATUTES = 'https://content.leg.colorado.gov/sites/default/files/images/olls/crs2024-title-25.pdf'

CO_COUNTIES = [
    {
        'county': 'El Paso',
        'authority': 'El Paso County Public Health — Water Quality / Onsite Wastewater Treatment System Program',
        'contact': 'El Paso County Public Health regulates and inspects OWTS in the county. Water Quality / OWTS questions: 719-578-3199, option 3. The county provides online permit submission, records access, installer licensing, and inspection resources.',
        'sources': [
            ('El Paso County Public Health — Onsite Wastewater Treatment Systems', 'https://www.elpasocountyhealth.org/licenses-permits-inspections-water-testing/onsite-wastewater-treatment-systems/'),
            ('El Paso County Public Health — OWTS Permits', 'https://www.elpasocountyhealth.org/licenses-permits-inspections-water-testing/onsite-wastewater-treatment-systems/owts-permits/'),
            ('El Paso County Public Health — Licensed Installers', 'https://www.elpasocountyhealth.org/licenses-permits-inspections-water-testing/onsite-wastewater-treatment-systems/licensed-installers/'),
            ('El Paso County Public Health — 2026 OWTS Program Updates', 'https://www.elpasocountyhealth.org/licenses-permits-inspections-water-testing/onsite-wastewater-treatment-systems/2026-owts-program-updates/'),
        ],
        'sections': [
            ('County Public Health is the permitting and inspection authority', 'El Paso County Public Health states that it inspects and regulates onsite wastewater treatment systems serving residential and commercial facilities that are not connected to municipal wastewater service. Its program reviews placement, design, installation, and maintenance rather than treating septic approval as only a building-department matter.'),
            ('Permit applications must be submitted by a county-licensed installer', 'El Paso County states that, effective January 1, 2024, OWTS permit applications must be submitted by a licensed OWTS installer. The county maintains its own current installer list and licensing program, so an owner should verify local credentials before assuming a contractor is eligible to submit the permit.'),
            ('Certain Highway 24 West sites have an extra profile-pit requirement', 'For sites along the Highway 24 West corridor, El Paso County states that profile pits must remain open for county site inspection before an OWTS permit is issued. This is a county-specific field-review requirement that can affect scheduling and should be coordinated before the pits are closed or disturbed.'),
            ('Engineered systems have tighter installer limits', 'The county distinguishes installer license tiers and states that homeowners may not install systems that require engineering. Tier 2 licensed system contractors may install conventional or engineer-designed OWTS, so the approved design determines who may perform the work.'),
            ('2026 rules add requirements for some advanced or remediated systems', 'El Paso County’s 2026 program update states that remediation technologies require an EPCPH permit and certified inspections every three months for one year unless otherwise specified. The update also adds design and material documentation requirements for higher-level treatment and certain mound or sand-filter systems.'),
            ('County septic records are available online when records exist', 'El Paso County provides OWTS records through the county Assessor property-search system. The county cautions that not every parcel has complete records on file and provides a septic-information contact for records that cannot be located online.'),
        ],
    },
    {
        'county': 'Larimer',
        'authority': 'Larimer County Department of Health and Environment — Environmental Health, On-Site Wastewater Treatment Systems Program',
        'contact': 'Larimer County Department of Health and Environment, Environmental Health Services, 1525 Blue Spruce Drive, Fort Collins, CO 80524. OWTS applications are available through the county online portal.',
        'sources': [
            ('Larimer County — Septic Systems (OWTS)', 'https://www.larimer.gov/health/environmental-health/septic-systems/septic-systems-owts'),
        ],
        'sections': [
            ('Larimer County Health requires a permit before building or repairing an OWTS', 'Larimer County states that state and county law require a permit from the Department before building or fixing a septic system. The county publishes its own OWTS application, instructions, fees, regulations, inspection guidance, and record-request process.'),
            ('The permit category depends on the scope of work', 'Larimer distinguishes new-system, major-repair, minor-repair, sealed-vault, remodel-or-upgrade, and site-evaluation applications. A major repair includes replacement, expansion, or alteration of the soil treatment area, while tank replacement is treated as a minor repair.'),
            ('Bedroom additions can trigger an OWTS upgrade review', 'Larimer states that a remodel or upgrade permit is used when the soil treatment area must be upgraded for a home addition or basement finish that adds bedrooms. Owners should therefore resolve OWTS capacity before assuming a residential building permit can proceed independently.'),
            ('Sewer proximity affects new-system eligibility', 'Larimer’s current permit guidance states that a new OWTS is used for new construction or an additional building when a sewer connection is not available within 400 feet. Applicants should confirm sewer availability as part of the early feasibility review.'),
            ('Limited-use systems are restricted', 'Larimer allows sealed vaults, vaulted privies, composting toilets, and similar limited-use systems only in qualifying circumstances. The county explains that seasonal or part-time use by itself is not enough to justify a limited-use system when a full OWTS can serve the property.'),
            ('Graywater may not simply be discharged to the ground', 'Larimer County states that graywater from showers, laundry, and sinks must be treated and disposed of as wastewater under its OWTS regulations; direct discharge from a home or RV to the ground is prohibited.'),
            ('County permit records can be checked before design or purchase decisions', 'Larimer provides online septic documents through its property-record system when available and a formal OWTS permit-record request process. It notes that many homes built before 1973 may not have permit records unless the system was repaired or upgraded later.'),
        ],
    },
    {
        'county': 'Weld',
        'authority': 'Weld County Department of Public Health and Environment — Environmental Health Services Division',
        'contact': 'Weld County Department of Public Health and Environment, Environmental Health Services Division; OWTS questions: 970-400-6415. The division oversees OWTS permitting for systems with design flows below 2,000 gallons per day.',
        'sources': [
            ('Weld County — Septic Systems (On-site Wastewater Treatment Systems)', 'https://www.weld.gov/Government/Departments/Health-and-Environment/Environmental-Health-Services/Septic-Systems'),
            ('Weld County — New System, Repair, Vault, and Statement of Existing', 'https://www.weld.gov/Government/Departments/Health-and-Environment/Environmental-Health-Services/Septic-Systems/New-System-Repair-Vault-and-Statement-of-Existing'),
            ('Weld County — Zoning Permits and Bedroom Additions', 'https://www.weld.gov/Government/Departments/Health-and-Environment/Environmental-Health-Services/Septic-Systems/Zoning-Permits-and-Bedroom-Additions'),
            ('Weld County — Loan Approval Inspections', 'https://www.weld.gov/Government/Departments/Health-and-Environment/Environmental-Health-Services/Septic-Systems/Loan-Approval-Inspections'),
        ],
        'sections': [
            ('Environmental Health Services administers local OWTS permits', 'Weld County states that its Environmental Health Services Division oversees permitting for onsite wastewater treatment systems with flows below 2,000 gallons per day, including site evaluations, design review, and inspections. County policy favors public sewer where feasible and limits OWTS to locations where public sewer is not feasible.'),
            ('New systems, repairs, upgrades, reconnections, and vaults use county applications', 'Weld County requires an application to install a new system, repair or upgrade an existing system, reconnect to an approved existing system, or install a vault. Vaults are allowed only in specific circumstances, so applicants are directed to confirm eligibility with Environmental Health before relying on that option.'),
            ('The permit package requires site and design documentation', 'Weld’s published requirements include the septic information form and fee plus a site-and-soils evaluation, design document, engineered design when necessary, site plan, and parcel number. The county states that qualifying site and soil information less than ten years old may be accepted.'),
            ('Bedroom additions can require an OWTS evaluation and inspection', 'For residences served by OWTS, Weld County requires an OWTS evaluation and inspection when a building-permit application increases the number of bedrooms. The process includes the county evaluation form and a pumping receipt from within the prior two years from a septic cleaner licensed by the Health Department.'),
            ('Weld does not mandate a transfer-of-title septic inspection', 'Weld County expressly states that it does not have a mandatory Transfer of Title Inspection or Use Permit program. The county recommends inspection and tank cleaning before ownership changes, but distinguishes that recommendation from a county requirement.'),
            ('Older or undocumented systems may require a Statement of Existing', 'For certain loan or owner-requested evaluations, Weld states that if no permit is on file, or an old permit lacks a system diagram, a notarized Statement of Existing must document the system size, type, and location. This can be relevant when historic records are incomplete.'),
        ],
    },
    {
        'county': 'Douglas',
        'authority': 'Douglas County Health Department — Environmental Health, On-Site Wastewater Treatment Systems Program',
        'contact': 'Douglas County Health Department administers local OWTS permitting, use permits, inspections, contractor licensing, and enforcement. Environmental Health OWTS materials direct applications and questions to eh@douglas.co.us; the department’s main published phone number is 720-643-2400.',
        'sources': [
            ('Douglas County Health Department — OWTS Regulation 26-01 (effective April 26, 2026)', 'https://www.douglas.co.us/documents/proposed-douglas-county-health-department-regulation-26-01-for-owts.pdf/'),
            ('Douglas County Health Department — current fee schedule', 'https://www.douglas.co.us/documents/fee-schedule.pdf/'),
            ('Douglas County Health Department — OWTS Use Permit application', 'https://www.douglas.co.us/documents/011326_usepermitapplication.pdf/'),
        ],
        'sections': [
            ('Douglas County Health Department is the local OWTS authority', 'Douglas County’s Regulation 26-01 states that the Health Department administers permitting, installation, repair, use permits, contractor licensing, inspections, and enforcement for onsite wastewater treatment systems in the county under Colorado Regulation 43 and state law.'),
            ('Public sewer availability can prevent an OWTS permit', 'The county regulation states that an OWTS permit will not be issued when the property is within a municipality or special district that provides public sewer service, unless the sewer connection is determined infeasible by that provider or the provider otherwise authorizes the OWTS. Applicants should resolve sewer-service status before paying for a septic design.'),
            ('Repairs and expansions have defined permit categories', 'Douglas County requires a Major Repair Permit for work such as replacing, adding, or expanding a soil treatment area and for soil-based remediation. A Minor Repair Permit covers work such as adding or replacing a septic tank or adding a lift station or pump not included in the original system. A major remodel that exceeds the system’s original design can require an Expansion Permit, and a complete system replacement requires a new-install permit.'),
            ('Use Permits are required for specific post-installation and change-of-use events', 'Under Regulation 26-01, a Use Permit or renewal is required after a new installation, construction, alteration, or repair; for a major remodel; for a residential-to-commercial change of use; for an auxiliary building or accessory structure with plumbing; for an ADU; before county approval of a short-term rental; and for certain other listed events. The current regulation specifically excludes covered property transactions from this Use Permit trigger, so owners should not rely on older Douglas County material that treated every sale as requiring a Use Permit.'),
            ('Use Permit inspections require a qualified inspector and recent pumping verification', 'A Use Permit application must include an inspection report completed within the prior 12 months by a licensed systems inspector with an accepted certification. The current regulation requires verification that the septic tank was pumped within 12 months of the Use Permit inspection and requires documentation of the tank, soil treatment area, mechanical components, deficiencies, and specified photographs.'),
            ('Licensed system contractors must handle regulated repair work', 'Douglas County’s current regulation provides a local Systems Contractor licensing program and states that malfunctioning systems requiring repair must be repaired by a licensed Systems Contractor. Systems determined to be in failure must be reported to the Health Department within 48 hours, and required repair permits must be obtained before repair work is completed.'),
            ('Published 2026 fees distinguish new, repair, and use permits', 'The Douglas County Board of Health fee schedule effective November 1, 2025 lists an OWTS new permit at $1,060, a major repair or expansion permit at $695, a minor repair permit at $390, and a Use Permit application at $65. It also lists separate renewal, reinspection, installer-license, cleaner-license, and enforcement fees. Because fee schedules can change, applicants should confirm the current schedule before payment.'),
            ('Higher-level treatment systems carry ongoing maintenance obligations', 'For higher-level treatment systems, Regulation 26-01 requires additional Use Permit information including the treatment technology and service provider plus an operation-and-maintenance service contract of at least one year. Inspections and maintenance must be performed by a licensed O&M contractor under the manufacturer’s recommendations or the county’s more stringent requirements.'),
        ],
    },
]

new_urls=[]
for d in CO_COUNTIES:
    sources=[
        ('Colorado Secretary of State — Regulation 43, On-site Wastewater Treatment System Regulation', CO_RULES),
        ('Colorado Revised Statutes Title 25 — local boards of health and OWTS rules', CO_STATUTES),
    ] + d['sources']
    sections=[
        ('Colorado state and local framework', 'Colorado Regulation 43 establishes statewide minimum standards for onsite wastewater treatment systems. Colorado law also requires local boards of health to adopt detailed OWTS rules for their jurisdictions consistent with state requirements, so the county or local public-health agency is the key permitting authority for ordinary residential systems and may impose locally adopted procedures or requirements.')
    ] + d['sections']
    new_urls.append(write_county_page('Colorado','colorado',d['county'],d['authority'],d['contact'],sections,sources,verified='August 30, 2026'))

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in new_urls if u not in sm)
    if entries:
        sitemap.write_text(sm.replace('</urlset>',entries+'</urlset>'),encoding='utf-8')

print(f'Colorado expansion complete: +{len(new_urls)} verified county guides')
