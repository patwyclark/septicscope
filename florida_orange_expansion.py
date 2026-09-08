# SepticScope Florida Orange County expansion — current local/state official guidance.
# Authoritative sources checked September 8, 2026.

ORANGE_SEPTIC = 'https://orange.floridahealth.gov/programs-and-services/environmental-public-health/onsite-sewage-disposal/'
ORANGE_INSPECTION = 'https://orange.floridahealth.gov/programs-and-services/environmental-public-health/onsite-sewage-disposal/septic-inspection-request/'
ORANGE_EH = 'https://orange.floridahealth.gov/location/environmental-public-health/'

orange_contact = (
    'Florida Department of Health in Orange County — Environmental Public Health / Onsite Sewage Disposal. '
    'Environmental Public Health: 407-858-1497; OrangeEVHPermitApplications@FLHealth.gov; '
    '1001 Executive Center Drive, Suite 200, Orlando, FL 32803. '
    'DOH-Orange lists OSTDS among the services handled by this office.'
)

orange_sections = [
    (
        'DOH-Orange is the current local septic permitting office',
        'Florida DEP’s current county-by-county permitting FAQ lists Orange County among the counties where OSTDS permits are issued by the Environmental Public Health Program of the local Florida Department of Health county office. DOH-Orange likewise directs property owners to continue working with the county health department for septic permitting and inspection needs while DEP administers the statewide statutes and Chapter 62-6 rules.'
    ),
    (
        'A complete construction application includes site and building information',
        'For DOH-administered counties such as Orange, Florida DEP currently directs applicants to submit the construction application, a site plan, a building floor plan, and the required application fee to the county health department. A site evaluation is also required to assess soil, topography, and other conditions; applicants may use a qualified private site evaluator or ask the county health department to perform the evaluation for a fee.'
    ),
    (
        'Orange County provides a dedicated inspection-request workflow',
        'DOH-Orange publishes a septic inspection request form for contractors and homeowners seeking OSTDS construction, final, or private-inspection processing. The county page states that requests submitted before 4:00 p.m. are responded to by the next business day, while after-hours submissions are treated as received the following day. Follow the permit-specific inspection sequence and do not cover regulated work before the required inspection is complete.'
    ),
    (
        'Operating permits apply to specified advanced and nonresidential systems',
        'DOH-Orange states that operating permits are required for aerobic treatment units, performance-based treatment systems, commercial septic systems, and septic systems serving industrial or manufacturing-zoned or equivalent properties. The county publishes a dedicated email route for operating-permit documentation, so owners of these systems should confirm current renewal and maintenance requirements with Environmental Public Health.'
    ),
    (
        'Private-provider inspections remain available under the state process',
        'Florida DEP states that owners, or contractors with owner authorization, may hire a qualified private provider to perform OSTDS inspections. In DOH-administered counties, private-provider inspection records continue through the Florida Department of Health process. DOH-Orange publishes a dedicated submission address for private-inspection notifications and records.'
    ),
    (
        'Use the Environmental Public Health office for current local filing details',
        'DOH-Orange lists Environmental Public Health at 1001 Executive Center Drive, Suite 200 in Orlando, with phone 407-858-1497, email OrangeEVHPermitApplications@FLHealth.gov, and published weekday hours of 8:00 a.m. to 5:00 p.m. Confirm the current application package, invoice, payment method, and any project-specific Orange County requirements before filing or traveling to the office.'
    ),
]

orange_sources = [
    ('Florida DEP — Onsite Sewage Program', FL_STATE),
    ('Florida DEP — Current OSTDS Permitting by County', FL_PERMITTING),
    ('Florida Department of Health in Orange County — Onsite Sewage Disposal', ORANGE_SEPTIC),
    ('Florida Department of Health in Orange County — Septic Inspection Request', ORANGE_INSPECTION),
    ('Florida Department of Health in Orange County — Environmental Public Health Office', ORANGE_EH),
]

orange_url = write_county_page(
    'Florida',
    'florida',
    'Orange',
    'Florida Department of Health in Orange County — Environmental Public Health / Onsite Sewage Disposal',
    orange_contact,
    orange_sections,
    orange_sources,
    verified='September 8, 2026',
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if orange_url not in sm:
        entry = f'<url><loc>{orange_url}</loc><lastmod>2026-09-08</lastmod></url>'
        sitemap.write_text(sm.replace('</urlset>', entry + '</urlset>'), encoding='utf-8')

page = OUTPUT / 'counties' / 'florida' / 'orange' / 'index.html'
if not page.exists():
    raise RuntimeError('Orange County verified page is missing')
text = page.read_text(encoding='utf-8')
if 'Local septic rules not yet verified' in text or 'OFFICIAL SOURCES CHECKED' not in text.upper() or ORANGE_SEPTIC not in text:
    raise RuntimeError('Orange County verified guide failed its build assertion')

print('Florida Orange expansion complete: +1 verified county guide')
