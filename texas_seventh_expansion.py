# SepticScope Texas expansion — seventh verified county batch.
# Collin County verified from current Collin County and TCEQ sources on 2026-08-31.

TX7_STATE = 'https://www.tceq.texas.gov/permitting/ossf/ossfpermits.html'
TX7_LICENSES = 'https://www.tceq.texas.gov/licensing/licenses/ossflic'
COLLIN_OSSF = 'https://www.collincountytx.gov/services/engineering/development-services/on-site-sewage-facilities'
COLLIN_DEV = 'https://www.collincountytx.gov/services/engineering/development-services'
COLLIN_INSPECTION = 'https://www.collincountytx.gov/docs/default-source/development-services/documents/ossf-inspection-list.pdf?sfvrsn=4e391400_0'

collin_sections = [
    ('Collin County Development Services is the local OSSF authority for applicable properties',
     'Collin County Engineering Development Services administers OSSF permitting where Collin County is the authorized agent. The county says properties outside city limits must apply through the county Citizen Self-Service portal. Inside city limits, applicants should confirm the authorized agent because some municipalities administer their own OSSF programs.'),
    ('New construction starts with the development permit and county portal',
     'For a new structure that will connect to a new OSSF, Collin County directs applicants to apply for the development permit first; county staff then sends the associated OSSF permit through the portal. The county specifically cautions applicants not to submit separate development and OSSF permits for that situation.'),
    ('A qualified professional must evaluate the site and design the system',
     'Collin County says a new OSSF or repair design must be prepared by a currently licensed Registered Sanitarian or Professional Engineer. The county also publishes a Site Evaluator information sheet and directs users to TCEQ licensing resources for installers and maintenance providers. Site suitability and the final design must comply with both Chapter 285 and the county court order.'),
    ('Current county lot-size rules depend on when the lot was divided and whether a well is present',
     'The county FAQ says lots divided between 1983 and 2008 generally start with a minimum of 1 acre, or 1.5 acres with a water well. Lots divided in 2008 or later generally start with 1 usable acre; with a water well, the starting minimum is 1.5 acres with 1 usable acre. The county defines usable acreage as area usable for OSSF components or disposal, excluding most easements, ponds and similar constraints. Older undersized lots may require proof of pre-1983 existence and still must satisfy current design requirements.'),
    ('Published OSSF fees are available on the county Development Services page',
     'The current county fee table lists residential OSSF permits at $310 without maintenance and $335 with maintenance; nonresidential/commercial permits are $450 without maintenance and $475 with maintenance. Repair or upgrade fees are $100 for less than 100 feet of line and $150 for more than 100 feet. A review of an existing septic system is $50. The live table also lists a $75 OSSF reinspection fee after failure of the second reinspection and a $50 OSSF re-review fee. Applicants should confirm the live fee table before paying.'),
    ('Major repairs can trigger a new-system permit',
     'Collin County’s current fee table states that if 50 percent of the system will be repaired or upgraded, the project must be permitted as a new OSSF. For additions, altered structures, or swimming pools on property with an existing OSSF, the county requires an existing-OSSF review for new construction or improvement through the Citizen Self-Service portal when Collin County is the permitting authority.'),
    ('Installation is inspected before the system is covered',
     'The inspection handout currently linked by Collin County says the installation must match the Registered Sanitarian or Professional Engineer design and that septic tanks and lines cannot be covered before the installation inspection. The handout also describes a final inspection for spray-irrigation aerobic systems and says both inspections may be performed at the same time. Because the handout itself is marked revised August 30, 2011, installers should confirm current scheduling and inspection details with Development Services before work.'),
    ('Permits expire after extended inactivity',
     'Collin County states that OSSF permits expire after 365 days of no activity from the date of issuance. Owners and contractors should verify permit status before resuming a delayed installation or repair.'),
    ('Aerobic-system ownership changes require updated maintenance paperwork',
     'When property with an aerobic OSSF is sold, Collin County requires a Change of Ownership form, an Aerobic Wastewater Homeowner Information sheet, and a maintenance contract in the new owner’s name from a licensed maintenance provider. The county directs owners to submit contracts, maintenance reports and ownership-change forms through its OSSF Report Portal.'),
    ('County and state OSSF rules both apply',
     'Collin County expressly states that its local court order contains additional, more stringent OSSF requirements in addition to Texas Chapter 285. TCEQ licenses or registers OSSF professionals including installers, site evaluators, maintenance providers and maintenance technicians, so applicants should verify current credentials before hiring.'),
]

collin_sources = [
    ('Collin County Development Services — On Site Sewage Facilities', COLLIN_OSSF),
    ('Collin County Development Services — current permit fees and online permitting', COLLIN_DEV),
    ('Collin County — OSSF Inspection List (county-linked handout; revised 2011)', COLLIN_INSPECTION),
    ('Texas Commission on Environmental Quality — Getting a Permit for an OSSF', TX7_STATE),
    ('Texas Commission on Environmental Quality — OSSF Licensing', TX7_LICENSES),
]

collin_url = write_county_page(
    'Texas', 'texas', 'Collin',
    'Collin County Engineering Development Services — On-Site Sewage Facility permitting',
    'Collin County Development Services handles county OSSF permitting and directs applicants to its online Citizen Self-Service system. The county currently emphasizes email support at developmentservices@co.collin.tx.us; verify current office/contact details on the official Development Services page before visiting.',
    collin_sections, collin_sources, verified='August 31, 2026'
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if collin_url not in sm:
        sm = sm.replace('</urlset>', f'<url><loc>{collin_url}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
        sitemap.write_text(sm, encoding='utf-8')

page = OUTPUT / 'counties' / 'texas' / 'collin' / 'index.html'
if not page.exists():
    raise RuntimeError('Collin verified county page was not generated')
text = page.read_text(encoding='utf-8')
for required in ('Official sources checked August 31, 2026', 'Citizen Self-Service', '365 days', '$335', '50 percent', '1 usable acre', 'Change of Ownership'):
    if required not in text:
        raise RuntimeError(f'Collin verified page missing required validated detail: {required}')
if 'Local septic rules not yet verified' in text:
    raise RuntimeError('Collin verified page was overwritten by an unverified fallback')

print('Texas seventh expansion complete: +1 verified Collin County guide')
exec((ROOT / 'texas_eighth_expansion.py').read_text(encoding='utf-8'), globals())
