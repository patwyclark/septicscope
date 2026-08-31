# SepticScope Texas expansion — eleventh verified county batch.
# Comal County verified from current Comal County and TCEQ sources on 2026-08-31.

TX11_STATE = 'https://www.tceq.texas.gov/permitting/ossf/ossfpermits.html'
TX11_LICENSES = 'https://www.tceq.texas.gov/licensing/licenses/ossflic'
COMAL_ENV = 'https://www.comalcounty.gov/274/Environmental-Health'
COMAL_STEPS = 'https://www.comalcounty.gov/793/Steps-to-Obtain-an-OSSF-Permit'
COMAL_PERMITS = 'https://www.comalcounty.gov/286/Permits'
COMAL_FEES = 'https://www.comalcounty.gov/DocumentCenter/View/2142/Environmental-Health-Department-Fees-PDF'
COMAL_APP = 'https://www.comalcounty.gov/DocumentCenter/View/2143/OSSF-Application-for-Permit-to-Construct-PDF'
COMAL_RULES = 'https://www.comalcounty.gov/DocumentCenter/View/2141/Comal-County-Rules-for-On-Site-Sewage-Facility-PDF'
COMAL_RECORDS = 'https://cceo.comalcounty.gov/environmental/searches/record_search.html'

comal_sections = [
    ('Comal County Environmental Health is the local OSSF permitting authority',
     'Comal County Environmental Health, within the County Engineer’s Office, reviews OSSF designs, issues permits and enforces county and state onsite-wastewater requirements. The county states that before building, altering, extending or operating an OSSF, the owner must have a permit and approved plans from TCEQ or its authorized agent. Its building-permit guidance identifies the OSSF permit as a required county permit in unincorporated areas, while interlocal agreements can affect jurisdiction near municipalities; confirm the controlling authority for the parcel before filing.'),
    ('Start with a qualified site and soil evaluation, then submit the owner application and planning materials',
     'The county’s nine-step process begins with a qualified site evaluator preparing a site/soil report and survey showing features that have required separation distances. The current application checklist calls for the completed application, a site/soil evaluation by a certified Site Evaluator or Professional Engineer, scaled planning materials and system specifications, the required fee, and a recorded deed. Comal County also offers an online permit portal.'),
    ('The county’s currently posted fee sheet is dated January 1, 2019, so amounts should be confirmed before payment',
     'The fee PDF presently linked from Comal County Environmental Health is labeled effective January 1, 2019. It lists $300 for a sewerage-facility permit under 500 gallons per day, $500 for more than 500 gallons per day, $80 for permit renewal within 12 months, $150 for renewal after 12 months, $100 for a remodel permit, $150 for reinspection, and $150 for a holding-tank permit. Because the county continues to link this older schedule from its live 2026 page, SepticScope reports the published amounts with their date rather than implying they were newly adopted in 2026; verify the live sheet with Environmental Health before paying.'),
    ('Authorization to Construct must be issued before installation begins',
     'After reviewing the application, site/soil evaluation, system type and supporting materials, the permitting authority issues an Authorization to Construct. Comal County says authorization can be withheld for incomplete or contradictory application information, a missing required floodplain development permit, or noncompliance with county subdivision regulations. Licensed installers or apprentices may begin construction only after authorization, and proposed changes to the approved design must be approved before they are made.'),
    ('Comal County requires three construction inspections and at least 24 hours notice',
     'The county states that three inspections are required as the OSSF is installed and that Environmental Health must be notified at least one day (24 hours) before an inspection is needed. If the system fails inspection or is not ready when the designated representative arrives, the installer is responsible for the published $150 reinspection fee. The same inspection requirements apply to OSSFs needing alteration or repair.'),
    ('A License to Operate is required before the system is put into use',
     'After the required inspections are completed and the facility is approved, Comal County issues a Notice of Approval or License to Operate. The county expressly states that the license to operate is required before the facility is put into use. Owners should keep that approval with the property records and can use the county’s public septic-permit search for existing records.'),
    ('Repairs, alterations and remodel-related septic work remain subject to county review',
     'Comal County’s permit instructions say the inspection and approval requirements also apply to systems in need of alteration or repair, and its published fee sheet includes a separate remodel permit. Contact Environmental Health before replacing tanks, relocating disposal components, expanding wastewater flow or changing an approved system; the county can determine whether new planning materials, authorization, inspections or a revised permit are required.'),
    ('Aerobic and surface-application systems require recorded maintenance documentation and a maintenance contract',
     'For a surface-application or aerobic treatment system, the county application checklist requires a recorded Certification of OSSF Requiring Maintenance/Affidavit to the Public and a signed maintenance contract effective when the License to Operate is issued. Comal County also maintains portals for licensed maintenance providers to upload maintenance contracts and maintenance reports. Follow the individual permit and current TCEQ maintenance rules for testing, reporting and service frequency.'),
    ('Edwards Aquifer and floodplain conditions can add requirements before construction authorization',
     'The current county application asks whether the property is in the Edwards Aquifer Recharge or Contributing Zone and whether a TCEQ Water Pollution Abatement Plan or Contributing Zone Plan applies. For Recharge Zone properties, the application states that planning materials must be completed by a Registered Sanitarian or Professional Engineer and asks whether there is at least one acre per single-family dwelling under 30 TAC 285.40(c)(1). The form also says an Authorization to Construct will not be issued until required aquifer-plan and floodplain reviews are complete.'),
    ('Use appropriately licensed Texas OSSF professionals',
     'Comal County’s process distinguishes the site evaluator, designer, installer and designated representative. Its guidance identifies Professional Engineers and Registered Sanitarians as professional designers for systems that require that level of planning, while installation proceeds through appropriately licensed installers or apprentices after authorization. TCEQ licenses OSSF site evaluators, installers and maintenance providers; verify credentials and the required license class for the approved system before work starts.'),
]

comal_sources = [
    ('Comal County — Environmental Health / OSSF program', COMAL_ENV),
    ('Comal County — Steps to Obtain an OSSF Permit', COMAL_STEPS),
    ('Comal County — Required Permits in Unincorporated Areas', COMAL_PERMITS),
    ('Comal County — Environmental Health Department Fees (posted county schedule, effective January 1, 2019)', COMAL_FEES),
    ('Comal County — OSSF Development Application and Permit Checklist', COMAL_APP),
    ('Comal County — Rules for On-Site Sewage Facilities', COMAL_RULES),
    ('Comal County — Septic Permit Record Search', COMAL_RECORDS),
    ('Texas Commission on Environmental Quality — Getting a Permit for an OSSF', TX11_STATE),
    ('Texas Commission on Environmental Quality — OSSF Licensing', TX11_LICENSES),
]

comal_url = write_county_page(
    'Texas', 'texas', 'Comal',
    'Comal County Engineer’s Office — Environmental Health / On-Site Sewage Facility Program',
    'Comal County Engineer’s Office / Environmental Health, 195 David Jonas Drive, New Braunfels, TX 78132; 830-608-2090. Office hours published by the county are Monday–Friday, 8:00 a.m.–4:30 p.m.',
    comal_sections, comal_sources, verified='August 31, 2026'
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if comal_url not in sm:
        sm = sm.replace('</urlset>', f'<url><loc>{comal_url}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
        sitemap.write_text(sm, encoding='utf-8')

page = OUTPUT / 'counties' / 'texas' / 'comal' / 'index.html'
if not page.exists():
    raise RuntimeError('Comal verified county page was not generated')
text = page.read_text(encoding='utf-8')
for required in ('Official sources checked August 31, 2026', '$300', '$500', 'January 1, 2019', 'three inspections', '24 hours', 'License to Operate', 'Edwards Aquifer'):
    if required not in text:
        raise RuntimeError(f'Comal verified page missing required validated detail: {required}')
if 'Local septic rules not yet verified' in text:
    raise RuntimeError('Comal verified page was overwritten by an unverified fallback')

print('Texas eleventh expansion complete: +1 verified Comal County guide')
