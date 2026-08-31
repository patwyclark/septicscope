# SepticScope Texas expansion — fourth verified county batch.
# Brazoria County verified from current TCEQ and Brazoria County government sources on 2026-08-31.

TX4_STATE = 'https://www.tceq.texas.gov/permitting/ossf/ossfpermits.html'
TX4_LICENSES = 'https://www.tceq.texas.gov/licensing/licenses/ossflic'
BRAZORIA_PROCESS = 'https://www.brazoriacountytx.gov/departments/environmental-health/forms-permit-applications/ossf-permitting-process'
BRAZORIA_FORMS = 'https://www.brazoriacountytx.gov/departments/environmental-health/forms-permit-applications'
BRAZORIA_FEES = 'https://www.brazoriacountytx.gov/departments/environmental-health/permit-fees'
BRAZORIA_CONTACT = 'https://www.brazoriacountytx.gov/departments/environmental-health/contact-us'
BRAZORIA_RULES = 'https://www.brazoriacountytx.gov/departments/environmental-health/regulations'

brazoria_sections = [
    ('Brazoria County Environmental Health administers the local OSSF program',
     'Brazoria County Environmental Health regulates on-site sewage facilities and publishes the county permitting process, forms, OSSF rules, maintenance resources, and septic contact information. The county process requires an OSSF permit before installation and before issuance of the associated building permit, unless a specific exemption applies.'),
    ('The application package requires a site evaluation and scaled design materials',
     'Brazoria County requires a 911-compliant address, property and legal-description information, a site evaluation by a Professional Engineer or licensed Site Evaluator, and a design package prepared by a Registered Sanitarian or Professional Engineer as required. The design must show the tract and applicable features under 30 TAC Chapter 285, including existing structures and utilities.'),
    ('Installer and maintenance-provider credentials are checked locally',
     'The county permitting checklist states that the installer and the maintenance provider, when maintenance is required, must be registered with Brazoria County. TCEQ separately licenses OSSF site evaluators, installers, maintenance providers, and maintenance technicians; owners should verify both the state credential and any county registration required for the project.'),
    ('Authorization to Construct comes after county review and payment',
     'Initial permit packages are submitted to Brazoria County for review in person or by mail; the county states that initial submissions are not accepted by email. Permit fees are due after the application packet has been reviewed and approved, and the county then issues the Authorization to Construct. Because the county fee page points to a separate current schedule and older fee PDFs remain indexed, SepticScope does not hard-code a dollar amount here; confirm the live schedule before payment.'),
    ('Inspection and final approval control operation and future transfer',
     'Brazoria County states that the OSSF is inspected and must receive final approval. After final approval, the permit can transfer to future property owners. A new permit application is required if the system will be altered, repaired, or extended, so owners should not treat an existing permit as blanket authorization for later system work.'),
    ('An unpermitted existing system cannot simply be retroactively permitted',
     'The county explicitly states that an existing OSSF without a permit cannot be retroactively permitted. Owners who discover an undocumented system should contact Environmental Health before planning additions, repairs, sale-related work, or other development rather than assuming a standard new-system filing will legalize the existing installation.'),
    ('The county publishes a conditional 10-acre permitting exception',
     'Brazoria County describes the Texas 10-acre exception for a single-family dwelling on one tract of at least 10 acres when all parts of the OSSF are at least 100 feet inside the property boundaries, the dwelling is the only dwelling on the tract, and all other applicable rules are met. TCEQ likewise warns owners to confirm exemptions with the local permitting authority and to comply with all other planning, construction, and installation requirements.'),
    ('Maintenance documents are part of the county application when required',
     'The county application checklist calls for a recorded Affidavit to the Public and maintenance contract when the proposed system requires them. Brazoria County also publishes dedicated OSSF maintenance forms and contact channels for maintenance contracts and reports, so advanced-system owners should follow the approved design and continuing maintenance obligations rather than applying conventional-system assumptions.'),
]

brazoria_sources = [
    ('Brazoria County Environmental Health — OSSF Permitting Process', BRAZORIA_PROCESS),
    ('Brazoria County Environmental Health — Forms & Permit Applications', BRAZORIA_FORMS),
    ('Brazoria County Environmental Health — current Permit Fees page', BRAZORIA_FEES),
    ('Brazoria County Environmental Health — OSSF Regulations', BRAZORIA_RULES),
    ('Brazoria County Environmental Health — Contact Us', BRAZORIA_CONTACT),
    ('Texas Commission on Environmental Quality — Getting a Permit for an OSSF', TX4_STATE),
    ('Texas Commission on Environmental Quality — OSSF Licensing', TX4_LICENSES),
]

brazoria_url = write_county_page(
    'Texas', 'texas', 'Brazoria',
    'Brazoria County Environmental Health Department — On-Site Sewage Facility (OSSF) Program',
    'Brazoria County Environmental Health, 451 N. Velasco, Suite 270, Angleton, TX 77515; 979-864-1600; ehadmin@brazoriacountytx.gov. The county publishes a separate OSSF inspector email and maintenance contact on its current contact page.',
    brazoria_sections, brazoria_sources, verified='August 31, 2026'
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if brazoria_url not in sm:
        sm = sm.replace('</urlset>', f'<url><loc>{brazoria_url}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
        sitemap.write_text(sm, encoding='utf-8')

page = OUTPUT / 'counties' / 'texas' / 'brazoria' / 'index.html'
if not page.exists():
    raise RuntimeError('Brazoria verified county page was not generated')
text = page.read_text(encoding='utf-8')
for required in ('Official sources checked August 31, 2026', 'Authorization to Construct', '10-acre', 'Brazoria County Environmental Health'):
    if required not in text:
        raise RuntimeError(f'Brazoria verified page missing required validated detail: {required}')
if 'Local septic rules not yet verified' in text:
    raise RuntimeError('Brazoria verified page was overwritten by an unverified fallback')

print('Texas fourth expansion complete: +1 verified Brazoria County guide')
