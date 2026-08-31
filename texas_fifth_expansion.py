# SepticScope Texas expansion — fifth verified county batch.
# Fort Bend County verified from current Fort Bend County and TCEQ sources on 2026-08-31.

TX5_STATE = 'https://www.tceq.texas.gov/permitting/ossf/ossfpermits.html'
TX5_LICENSES = 'https://www.tceq.texas.gov/licensing/licenses/ossflic'
FORT_BEND_PROGRAM = 'https://www.fortbendcountytx.gov/government/departments/health-and-human-services/environmental-health/on-site-sewage-facility-ossf-program'
FORT_BEND_PROCESS = 'https://www.fortbendcountytx.gov/government/departments/health-and-human-services/environmental-health/on-site-sewage-facility-permits-packets'
FORT_BEND_FEES = 'https://www.fortbendcountytx.gov/government/departments/health-and-human-services/environmental-health/permitting/permit-fees'
FORT_BEND_FORMS = 'https://www.fortbendcountytx.gov/government/departments/health-and-human-services/environmental-health/forms-library/forms-library/-parent-8892/-folder-682'
FORT_BEND_MAINT = 'https://www.fortbendcountytx.gov/government/departments/health-and-human-services/environmental-health/annual-maintenance-contract-renewal-fee'
FORT_BEND_CONTACT = 'https://www.fortbendcountytx.gov/government/departments/health-and-human-services/environmental-health/contact-us'

fort_bend_sections = [
    ('Fort Bend County Environmental Health administers the local OSSF program',
     'Fort Bend County Environmental Health regulates the location, design, construction, installation, operation, maintenance, modification and repair of on-site sewage facilities handling no more than 5,000 gallons per day. The county reviews applications and planning materials, performs pre-construction and installation inspections, issues final approvals, and investigates OSSF complaints.'),
    ('Applications and maintenance contracts are submitted through the county online portal',
     'Fort Bend County directs applicants to submit OSSF applications and maintenance contracts online through its Environmental Health portal. The county states that application review occurs in received order and that the permitting authority must approve or deny a complete OSSF application within 30 days. Approval of an application is not permission to install or operate: the county separately issues the permit to construct and, after required inspections, the license to operate.'),
    ('A soil and site evaluation plus scaled design are required',
     'The county procedure requires a survey or plat showing boundaries, easements and rights-of-way; proposed locations of the home, OSSF, water well and other improvements; and a soil and site evaluation addressing soil suitability, setback requirements and system selection. The site evaluation must be performed by a Professional Engineer or state-registered Site Evaluator. A Professional Engineer or Registered Sanitarian must then prepare the septic design or planning material to scale.'),
    ('Lot size and setbacks are evaluated as part of the local review',
     'Fort Bend County says property should contain at least one acre when both a well and septic system are proposed. For property smaller than one acre that was platted or subdivided before 1988, the county requires a professional design by a Professional Engineer or Registered Sanitarian. The county also publishes a separate official minimum-separation-distance resource; project-specific setbacks must come from the approved site evaluation and design rather than a generic county summary.'),
    ('Construction, repair and modification require permits and inspections',
     'Existing OSSFs are not treated as grandfathered for later work. Fort Bend County states that modifications — including relocating sprinklers or adding lines — require a new permit and approval process, a complete new design, application and associated fee before the modification. The OSSF program performs new-construction, modification and repair inspections as well as final approval inspections.'),
    ('Texas licensing rules apply to septic professionals',
     'Fort Bend County directs owners to TCEQ licensing resources when selecting installers and designers. TCEQ requires OSSF installers, maintenance providers and maintenance technicians to hold the applicable state license or registration, and county review may also require appropriately credentialed site evaluators, Registered Sanitarians or Professional Engineers for the evaluation and design work described in the approved process.'),
    ('The county publishes permit and inspection fees, with an explicit schedule date',
     'Fort Bend County\'s live Environmental Health fee page lists $575 for single-family residential OSSF permits and $575 for non-single-family dwelling permits, each including the $10 TCEQ fee and two inspections plus plan review; commercial and industrial permits are listed at $650. Additional inspections are $225, variance requests $200, redesigns $300, and the aerobic-system annual maintenance fee $50. The county page itself says all fees are current as of May 26, 2023, so owners should confirm the live fee page before payment rather than assuming those amounts have been re-adopted in 2026.'),
    ('Aerobic and other maintained systems have continuing contract obligations',
     'After the initial two-year maintenance contract expires, Fort Bend County requires each ATU or other OSSF requiring routine maintenance to submit a renewing maintenance contract and annual maintenance-contract renewal fee. The county states that aerobic-system contracted maintenance must be performed by a certified maintenance provider unless the owner is themselves a certified maintenance provider for that unit. Late or missing renewal contracts can trigger a Notice of Violation.'),
]

fort_bend_sources = [
    ('Fort Bend County Environmental Health — OSSF Program', FORT_BEND_PROGRAM),
    ('Fort Bend County Environmental Health — OSSF Permits / Packets', FORT_BEND_PROCESS),
    ('Fort Bend County Environmental Health — Permit / Inspection Fees', FORT_BEND_FEES),
    ('Fort Bend County Environmental Health — OSSF Forms Library', FORT_BEND_FORMS),
    ('Fort Bend County Environmental Health — Annual Maintenance Contract Renewal', FORT_BEND_MAINT),
    ('Fort Bend County Environmental Health — Contact Us', FORT_BEND_CONTACT),
    ('Texas Commission on Environmental Quality — Getting a Permit for an OSSF', TX5_STATE),
    ('Texas Commission on Environmental Quality — OSSF Licensing', TX5_LICENSES),
]

fort_bend_url = write_county_page(
    'Texas', 'texas', 'Fort Bend',
    'Fort Bend County Environmental Health — On-Site Sewage Facility (OSSF) Program',
    'Fort Bend County Environmental Health, 4520 Reading Rd., Suite A-800, Rosenberg, TX 77471; 281-342-7469. Confirm current office hours and online-submission instructions on the county contact and OSSF pages before visiting.',
    fort_bend_sections, fort_bend_sources, verified='August 31, 2026'
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if fort_bend_url not in sm:
        sm = sm.replace('</urlset>', f'<url><loc>{fort_bend_url}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
        sitemap.write_text(sm, encoding='utf-8')

page = OUTPUT / 'counties' / 'texas' / 'fort-bend' / 'index.html'
if not page.exists():
    raise RuntimeError('Fort Bend verified county page was not generated')
text = page.read_text(encoding='utf-8')
for required in ('Official sources checked August 31, 2026', 'soil and site evaluation', 'May 26, 2023', 'Fort Bend County Environmental Health'):
    if required not in text:
        raise RuntimeError(f'Fort Bend verified page missing required validated detail: {required}')
if 'Local septic rules not yet verified' in text:
    raise RuntimeError('Fort Bend verified page was overwritten by an unverified fallback')

print('Texas fifth expansion complete: +1 verified Fort Bend County guide')
