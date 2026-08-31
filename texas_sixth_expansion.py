# SepticScope Texas expansion — sixth verified county batch.
# Montgomery County verified from current Montgomery County and TCEQ sources on 2026-08-31.

TX6_STATE = 'https://www.tceq.texas.gov/permitting/ossf/ossfpermits.html'
TX6_LICENSES = 'https://www.tceq.texas.gov/licensing/licenses/ossflic'
MONTGOMERY_GUIDE = 'https://www.mctx.org/document_center/1%20Environmental%20Health/How%20to%20Obtain%20a%20Septic.pdf'
MONTGOMERY_PACKET = 'https://www.mctx.org/PACKET-RESIDENTIAL%20NEW%20SEPTIC%20SYSTEM.pdf'

montgomery_sections = [
    ('Montgomery County Environmental Health Services administers the local OSSF permit process',
     'Montgomery County Environmental Health Services, within Permits/Floodplain Administration, publishes the county process for obtaining a permit to construct an on-site sewage facility and the Notice of Approval required before operation. The county process applies alongside TCEQ Chapter 285 requirements.'),
    ('A registered site evaluation and professional system design are required',
     'Before applying for a new septic system, Montgomery County requires a site evaluation including soil analysis by a Registered Site Evaluator in the area where the system will be installed. The county also requires the OSSF design under seal of a Registered Sanitarian or Registered Professional Engineer, plus floor plans for residential and commercial buildings showing applicable bedrooms, restrooms and square footage.'),
    ('Floodplain status and lot size are part of the county review',
     'Applicants must obtain the property floodplain status from the Permit Office, and Montgomery County states that it will not issue a septic permit for a system located within the regulatory floodway. The county guide says lots should be at least 0.75 acre without a private well and 1.5 acres when both septic and a private well are proposed, while documented pre-December 1, 1986 lots may receive special consideration if minimum separation distances and other conditions can be met.'),
    ('The permit package includes legal, building and utility documentation',
     'The county application guidance calls for the site evaluation, sealed OSSF design, legal description, owner-signed floor plans and, when applicable, an original notarized power of attorney. The current residential packet also calls for public-water documentation when service comes from a utility, stormwater paperwork, applicable culvert verification, a property map, and three sets each of the soil analysis and septic design.'),
    ('Installation must remain uncovered until county inspection and approval',
     'Montgomery County requires a Notice of Approval after installation and before the system is backfilled or used. The county directs installers or applicants to request the inspection by 3:00 p.m. two business days before the inspection is needed. Only after Environmental Health approves the system and grants permission to backfill is the Notice of Approval to operate issued.'),
    ('Published county fees are dated March 22, 2023 and should be confirmed before payment',
     'The county septic guide currently publishes $285 plus the $10 TCEQ assessment fee for a new residential system ($295 total), $335 plus $10 for a new commercial system ($345 total), and $135 plus $10 for a licensed add-on modification ($145 total). It also lists $285 subdivision review, $135 floodplain variance and a $135 reinspection fee. Because the county document is marked revised March 22, 2023, applicants should confirm the amount still in effect before paying.'),
    ('The county publishes system-specific minimum separation distances',
     'Montgomery County publishes a separation-distance table for tanks, soil absorption, surface application and drip irrigation. Examples include 50 feet from tanks to public water wells, 150 feet from soil absorption or spray/drip areas to public water wells, and generally 5 feet from tanks and soil-absorption areas to foundations, buildings, surface improvements, property lines, easements, swimming pools and other structures. The full table includes system-specific exceptions and footnotes, so the approved design and current county/TCEQ table control for an individual property.'),
    ('Aerobic systems require an initial two-year maintenance contract',
     'The county residential septic packet requires a two-year initial maintenance contract for aerobic systems. It states that the owner must sign the contract and that the owner and installer must complete the two-year maintenance contract before final inspection. Owners should follow the approved system design and current TCEQ maintenance requirements after the initial contract period.'),
    ('Texas licensing and repair/alteration permitting rules still apply',
     'TCEQ licenses or registers OSSF site evaluators, installers, maintenance providers and maintenance technicians. Texas permitting rules generally require approval to construct, install, alter, extend or repair an OSSF unless a specific exemption applies; owners planning a repair or replacement should confirm the required local filing with Montgomery County Environmental Health before work begins.'),
]

montgomery_sources = [
    ('Montgomery County Environmental Health — How to Obtain a Septic Permit and Notice of Approval', MONTGOMERY_GUIDE),
    ('Montgomery County — Residential New Septic System Packet', MONTGOMERY_PACKET),
    ('Texas Commission on Environmental Quality — Getting a Permit for an OSSF', TX6_STATE),
    ('Texas Commission on Environmental Quality — OSSF Licensing', TX6_LICENSES),
]

montgomery_url = write_county_page(
    'Texas', 'texas', 'Montgomery',
    'Montgomery County Environmental Health Services — On-Site Sewage Facility permitting',
    'Montgomery County Environmental Health Services / Permits-Floodplain Administration, 501 N. Thompson, Suite 100, Conroe, TX 77301. The county septic guidance lists 936-539-7836 for the office and 936-539-7839 for septic questions; confirm current contact details before visiting.',
    montgomery_sections, montgomery_sources, verified='August 31, 2026'
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if montgomery_url not in sm:
        sm = sm.replace('</urlset>', f'<url><loc>{montgomery_url}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
        sitemap.write_text(sm, encoding='utf-8')

page = OUTPUT / 'counties' / 'texas' / 'montgomery' / 'index.html'
if not page.exists():
    raise RuntimeError('Montgomery verified county page was not generated')
text = page.read_text(encoding='utf-8')
for required in ('Official sources checked August 31, 2026', 'Registered Site Evaluator', 'Notice of Approval', 'two-year initial maintenance contract', 'March 22, 2023'):
    if required not in text:
        raise RuntimeError(f'Montgomery verified page missing required validated detail: {required}')
if 'Local septic rules not yet verified' in text:
    raise RuntimeError('Montgomery verified page was overwritten by an unverified fallback')

print('Texas sixth expansion complete: +1 verified Montgomery County guide')
