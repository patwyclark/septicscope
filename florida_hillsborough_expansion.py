# SepticScope Florida Hillsborough County expansion — current local/state official guidance.
# Authoritative sources checked September 8, 2026.

HILLSBOROUGH_SEPTIC = 'https://hillsborough.floridahealth.gov/programs-and-services/environmental-public-health/septic-systems/'
HILLSBOROUGH_MAIN = 'https://hillsborough.floridahealth.gov/location/main-health-department/'
HILLSBOROUGH_RECORDS = 'https://hillsborough.floridahealth.gov/programs-and-services/environmental-public-health/public-records/'

hillsborough_contact = (
    'Florida Department of Health in Hillsborough County — Environmental Public Health / Septic Systems. '
    'Environmental Health: 813-307-8059; fax 813-272-7242; 1105 E. Kennedy Blvd., Tampa, FL 33602. '
    'DOH-Hillsborough publishes the local septic application and inspection process for Hillsborough County.'
)

hillsborough_sections = [
    (
        'DOH-Hillsborough is the current local septic permitting office',
        'Florida DEP’s current county-by-county permitting FAQ lists Hillsborough among the counties where OSTDS permits are issued by the Environmental Public Health Program of the local Florida Department of Health county office. DEP administers the statewide OSTDS statutes and Chapter 62-6 rules, but Hillsborough applicants currently file through DOH-Hillsborough rather than a DEP-administered county office.'
    ),
    (
        'The local program handles construction permits and inspections',
        'DOH-Hillsborough states that its septic services include septic-system construction permitting and inspection. The same program also handles land-application sites and pump-truck permitting and inspection, specified wastewater and performance-based treatment systems, septic-tank manufacturer facilities, contractor licensing, and operating permits and inspections for aerobic treatment units and commercial systems.'
    ),
    (
        'Use the project-specific application package',
        'DOH-Hillsborough publishes separate application packages for new construction, existing-system modifications, repairs, septic-system abandonment, and holding tanks. The county page states that applications may be submitted to Environmental Health by hand delivery, mail, fax, or email. Use the package that matches the proposed work instead of assuming a new-system application covers an existing-system repair or modification.'
    ),
    (
        'Site plans, floor plans, and a site evaluation are part of the state permitting path',
        'Florida DEP’s current permitting guidance for DOH-administered counties says applicants submit the construction application, a site plan, a building floor plan, and the required application fee to the county health department. A site evaluation is also required and must be performed by a qualified professional; the county health department may perform that evaluation for a fee. DEP notes that local ordinances can exceed statewide minimum requirements, so the final Hillsborough review controls for the parcel.'
    ),
    (
        'Existing permit and inspection records are available through Environmental Health',
        'DOH-Hillsborough provides its eBridge public-record system for Environmental Health files. The agency says users can retrieve available inspections, permits, and correspondence by fields such as permit number, facility name, street address, ZIP code, document date, or document type. Check the available county record before planning an addition, repair, replacement, or abandonment around an existing septic system.'
    ),
    (
        'Confirm current counter hours and submission details before traveling',
        'DOH-Hillsborough’s Main Office page places Environmental Health at 1105 E. Kennedy Blvd. in Tampa and lists Environmental Health at 813-307-8059. The septic-program page publishes separate application-counter hours and a midday closure, so call or use the current county page to confirm same-day Environmental Health availability, payment instructions, and the current application package before making a trip.'
    ),
]

hillsborough_sources = [
    ('Florida DEP — Onsite Sewage Program', FL_STATE),
    ('Florida DEP — Current OSTDS Permitting by County', FL_PERMITTING),
    ('Florida Department of Health in Hillsborough County — Septic Systems', HILLSBOROUGH_SEPTIC),
    ('Florida Department of Health in Hillsborough County — Main Office / Environmental Health', HILLSBOROUGH_MAIN),
    ('Florida Department of Health in Hillsborough County — Environmental Health Public Records', HILLSBOROUGH_RECORDS),
]

hillsborough_url = write_county_page(
    'Florida',
    'florida',
    'Hillsborough',
    'Florida Department of Health in Hillsborough County — Environmental Public Health / Septic Systems',
    hillsborough_contact,
    hillsborough_sections,
    hillsborough_sources,
    verified='September 8, 2026',
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if hillsborough_url not in sm:
        entry = f'<url><loc>{hillsborough_url}</loc><lastmod>2026-09-08</lastmod></url>'
        sitemap.write_text(sm.replace('</urlset>', entry + '</urlset>'), encoding='utf-8')

page = OUTPUT / 'counties' / 'florida' / 'hillsborough' / 'index.html'
if not page.exists():
    raise RuntimeError('Hillsborough County verified page is missing')
text = page.read_text(encoding='utf-8')
if 'Local septic rules not yet verified' in text or 'OFFICIAL SOURCES CHECKED' not in text.upper() or HILLSBOROUGH_SEPTIC not in text:
    raise RuntimeError('Hillsborough County verified guide failed its build assertion')

print('Florida Hillsborough expansion complete: +1 verified county guide')
