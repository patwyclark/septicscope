# SepticScope Florida Duval County expansion — current local/state official guidance.
# Authoritative sources checked September 8, 2026.

DUVAL_SEPTIC = 'https://duval.floridahealth.gov/programs-and-services/environmental-public-health/onsite-sewage-disposal/'
DUVAL_PRIVATE_INSPECTIONS = 'https://floridadep.gov/water/onsite-sewage/content/private-provider-inspections-ostds'


duval_contact = (
    'Florida Department of Health in Duval County — Environmental Health / Onsite Sewage Disposal. '
    'Environmental Health: 904-253-1280; DuvalEH@FLHealth.gov; '
    '921 N. Davis St., Building B, Suite 350, Jacksonville, FL 32209. '
    'DOH-Duval lists a separate mailing address at 921 N. Davis St., Building A, Suite 251, MC-45, Jacksonville, FL 32209.'
)


duval_sections = [
    (
        'DOH-Duval is the current local septic permitting office',
        'Florida DEP’s current county-by-county permitting FAQ lists Duval County among the counties where OSTDS permits are issued by the Environmental Public Health Program of the local Florida Department of Health county office. DOH-Duval likewise states that county health department offices continue septic permitting and inspection while DEP administers the statewide statutes and Chapter 62-6 rules.'
    ),
    (
        'A construction-permit application needs property and site information',
        'For DOH-administered counties such as Duval, Florida DEP currently directs applicants to submit the construction application, a site plan, a building floor plan, and the required application fee to the county health department. A site evaluation is also required to document property conditions and must be completed by a qualified professional; applicants may hire a private evaluator or ask the county health department to perform the evaluation for a fee.'
    ),
    (
        'Use the local Environmental Health office for filing and payment details',
        'DOH-Duval publishes Environmental Health contact information at 921 N. Davis St., Building B, Suite 350 in Jacksonville, phone 904-253-1280, fax 904-253-2390, and email DuvalEH@FLHealth.gov. Its onsite-sewage page states that Environmental Health bills and fees can be paid in person, by mail, or through the MyFloridaEHPermit bill-pay site. Confirm the current application package, total fee, and accepted submission method before filing because project type and local fees can affect the total.'
    ),
    (
        'Private-provider inspections are available under Florida law',
        'Florida DEP states that owners, or contractors with owner authorization, may hire a qualified private provider to perform OSTDS inspections. For counties that remain administered by DOH, including Duval under the current permitting FAQ, private-provider inspectors continue to submit through the DOH Private Inspector Portal and county health department staff review the submitted inspection information.'
    ),
    (
        'Check for project-specific local requirements before design decisions',
        'Florida DEP notes that counties can have local ordinances that exceed statewide OSTDS requirements. Duval County applicants should therefore use the state requirements as the baseline and confirm any current local siting, design, fee, or documentation requirements with DOH-Duval before purchasing equipment, finalizing a design, or scheduling construction.'
    ),
]


duval_sources = [
    ('Florida DEP — Onsite Sewage Program', FL_STATE),
    ('Florida DEP — Current OSTDS Permitting by County', FL_PERMITTING),
    ('Florida Department of Health in Duval County — Onsite Sewage Disposal', DUVAL_SEPTIC),
    ('Florida DEP — Private Provider Inspections of OSTDS', DUVAL_PRIVATE_INSPECTIONS),
]


duval_url = write_county_page(
    'Florida',
    'florida',
    'Duval',
    'Florida Department of Health in Duval County — Environmental Health / Onsite Sewage Disposal',
    duval_contact,
    duval_sections,
    duval_sources,
    verified='September 8, 2026',
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if duval_url not in sm:
        entry = f'<url><loc>{duval_url}</loc><lastmod>2026-09-08</lastmod></url>'
        sitemap.write_text(sm.replace('</urlset>', entry + '</urlset>'), encoding='utf-8')

page = OUTPUT / 'counties' / 'florida' / 'duval' / 'index.html'
if not page.exists():
    raise RuntimeError('Duval County verified page is missing')
text = page.read_text(encoding='utf-8')
if 'Local septic rules not yet verified' in text or 'OFFICIAL SOURCES CHECKED' not in text.upper() or DUVAL_SEPTIC not in text:
    raise RuntimeError('Duval County verified guide failed its build assertion')

print('Florida Duval expansion complete: +1 verified county guide')
