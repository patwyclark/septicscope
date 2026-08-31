# SepticScope Texas expansion — tenth verified county batch.
# Hays County verified from current Hays County and TCEQ sources on 2026-08-31.

TX10_STATE = 'https://www.tceq.texas.gov/permitting/ossf/ossfpermits.html'
TX10_LICENSES = 'https://www.tceq.texas.gov/licensing/licenses/ossflic'
HAYS_SEPTIC = 'https://www.hayscountytx.gov/496/Septic-Permits'
HAYS_ENV = 'https://www.hayscountytx.gov/354/Environmental-Health'
HAYS_FORMS = 'https://www.hayscountytx.gov/353/Development-Services-Documents-Forms'
HAYS_FEES = 'https://www.hayscountytx.gov/DocumentCenter/View/4797'
HAYS_RULES = 'https://www.hayscountytx.gov/DocumentCenter/View/1893/Hays-County-On-Site-Sewage-Facility-Regulations-PDF'
HAYS_CONTACT = 'https://www.hayscountytx.gov/863/Contact-Us'

hays_sections = [
    ('Hays County Development Services administers OSSF permits in the county’s regulated areas',
     'Hays County Development Services Environmental Health administers the local on-site sewage facility program. The county’s public permitting page says development and OSSFs in unincorporated Hays County require permits, while the county OSSF Order applies throughout Hays County except areas regulated under another existing OSSF order, ordinance or resolution. Owners near a city or other authorized jurisdiction should confirm which permitting authority controls before applying.'),
    ('Applications are submitted through MyGovernmentOnline with the design and site package',
     'Hays County directs applicants to MyGovernmentOnline. Its current OSSF checklist on the public permitting page calls for the OSSF application, site plan and design, location map, floor plan, tax-account summary, applicable fees, and—for advanced or aerobic systems—a maintenance affidavit and two-year initial maintenance contract. The county performs an administrative review followed by technical review; an Authorization to Construct may be issued during technical review, followed by the Notice of Approval when the review and required work are complete.'),
    ('The January 1, 2026 county fee schedule lists $610 for a single-family OSSF permit',
     'Hays County’s Development Services Fee Schedule effective January 1, 2026 lists $610 for a single-family residence OSSF permit application and $910 for a non-single-family residence. It also lists $150 for a reinspection or tie-in inspection, $150 for design resubmission, $310 for a minor system alteration, and $510 for a major system alteration. The schedule identifies a $10 TCEQ OSSF Grant Program fee within OSSF applications and lists OSSF renewal fees of $600 for single-family and $900 for non-single-family systems. Confirm the live fee sheet before paying because Commissioners Court can revise fees.'),
    ('Hays County requires an OSSF permit regardless of tract acreage',
     'Hays County expressly states that an OSSF permit is required regardless of lot size or acreage. That local requirement is stricter than the conditional Texas 10-acre permitting exemption described in TCEQ guidance, so property owners should not assume a large tract is exempt in Hays County.'),
    ('Site and soil evaluation drive system selection and local minimum lot requirements',
     'The Hays County OSSF Order incorporates the state Chapter 285 site-evaluation requirements and adds county-specific land-planning and minimum-lot rules that vary by location, water source, and whether the design is conventional or advanced. TCEQ instructs applicants to arrange a preconstruction site evaluation by a licensed Site Evaluator or Professional Engineer; that evaluation includes a survey of the lot, soil analysis in the proposed disposal area, and other suitability criteria. Hays County’s local acreage table is detailed and includes special categories for the Edwards Aquifer Recharge Zone and Contributing Zone, so applicants should use the county table and approved design rather than a generic statewide lot-size assumption.'),
    ('County-specific setbacks supplement the statewide separation table',
     'For lots covered by the current local separation provisions, Hays County supplements TCEQ Table X. Examples in the county order include 150 feet from listed major creeks and rivers to effluent dispersal areas, 20 feet from property lines to most effluent dispersal areas, 50 feet from public or private wells to tanks, and 150 feet from public wells to effluent dispersal areas. The order also establishes a 100-foot sanitary radius around private wells in which an effluent dispersal facility may not be located, subject to larger groundwater-district requirements. Because system type, lot history, drip design and other exceptions can change the applicable distance, the approved site plan and current county/state rules control.'),
    ('Construction must be inspected and completed within the county’s permit timelines',
     'The Hays County OSSF Order requires a construction inspection within 12 months after Authorization to Construct, completion of construction within 14 months after that authorization, and completion within 18 months after the permit application. The county’s application workflow culminates in its Notice of Approval; do not cover or operate a system contrary to the inspector’s instructions or approved design.'),
    ('Repairs and major alterations can trigger current permitting requirements',
     'Hays County’s current fee schedule separates minor and major system alterations, and the OSSF Order states that a replaced system or a system subjected to a major alteration must be re-permitted and upgraded to current OSSF requirements, except for the local minimum-lot-acreage requirement. A malfunctioning system may also be given a shorter repair deadline when the county finds an imminent public-health or environmental threat. Contact Environmental Health before replacing tanks, changing disposal methods, relocating components or performing other work that may exceed routine maintenance.'),
    ('Advanced and aerobic systems have ongoing maintenance, testing and reporting duties',
     'Hays County states that ongoing maintenance is required for all aerobic or advanced-treatment OSSFs. Its local order requires maintenance activities to be performed by appropriately licensed personnel, requires maintenance providers working under county contracts to register with Development Services, and generally requires maintained systems to be tested with reports submitted every four months unless the permit specifies otherwise. Owner maintenance is not treated as an automatic right; the local order conditions it on the owner completing an approved maintenance-provider course and test or another course approved by the authorized agent. Follow the individual permit, maintenance contract and current county instructions.'),
    ('Use TCEQ-licensed OSSF professionals and confirm owner-install eligibility before construction',
     'Texas licenses OSSF site evaluators, installers and maintenance providers. TCEQ allows limited owner installation only when state conditions are met and the local permitting authority allows it; anyone assisting with installation work generally must hold the appropriate installer license, subject to narrow state exceptions. Hays County applicants should verify credentials through TCEQ and confirm any proposed owner-install arrangement with Development Services before starting work.'),
]

hays_sources = [
    ('Hays County — Septic Permits', HAYS_SEPTIC),
    ('Hays County — Environmental Health', HAYS_ENV),
    ('Hays County — Development Services Documents & Forms', HAYS_FORMS),
    ('Hays County — Development Services Fee Schedule effective January 1, 2026', HAYS_FEES),
    ('Hays County / TCEQ — On-Site Sewage Facility Regulations and authorized-agent order', HAYS_RULES),
    ('Hays County Development Services — Contact Us', HAYS_CONTACT),
    ('Texas Commission on Environmental Quality — Getting a Permit for an OSSF', TX10_STATE),
    ('Texas Commission on Environmental Quality — OSSF Licensing', TX10_LICENSES),
]

hays_url = write_county_page(
    'Texas', 'texas', 'Hays',
    'Hays County Development Services — Environmental Health / On-Site Sewage Facility Program',
    'Hays County Development Services, 2171 Yarrington Road, Suite 100, Kyle, TX 78640; 512-393-2150. The county contact page directs OSSF inquiries to option 3 and permit/maintenance questions to Permit Administration.',
    hays_sections, hays_sources, verified='August 31, 2026'
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if hays_url not in sm:
        sm = sm.replace('</urlset>', f'<url><loc>{hays_url}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
        sitemap.write_text(sm, encoding='utf-8')

page = OUTPUT / 'counties' / 'texas' / 'hays' / 'index.html'
if not page.exists():
    raise RuntimeError('Hays verified county page was not generated')
text = page.read_text(encoding='utf-8')
for required in ('Official sources checked August 31, 2026', '$610', '$910', 'January 1, 2026', 'regardless of lot size or acreage', 'every four months', '150 feet', 'MyGovernmentOnline'):
    if required not in text:
        raise RuntimeError(f'Hays verified page missing required validated detail: {required}')
if 'Local septic rules not yet verified' in text:
    raise RuntimeError('Hays verified page was overwritten by an unverified fallback')

print('Texas tenth expansion complete: +1 verified Hays County guide')
exec((ROOT / 'texas_eleventh_expansion.py').read_text(encoding='utf-8'), globals())
