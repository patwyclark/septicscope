# SepticScope North Carolina expansion — sixth validated county batch.
# Johnston County verified from current county Environmental Health sources on 2026-08-31.

JOHNSTON_STATE = 'https://www.dph.ncdhhs.gov/programs/environmental-health/site-water-protection-branch/site-wastewater-program'
JOHNSTON_EH = 'https://www.johnstonnc.com/envhealth/'
JOHNSTON_APP = 'https://www.johnstonnc.com/envhealth/files/SepticApp25.pdf'
JOHNSTON_EXISTING = 'https://www.johnstonnc.com/envhealth/files/AppESU.pdf'
JOHNSTON_FEES = 'https://www.johnstonnc.com/envhealth/ftblPDF.cfm'
JOHNSTON_STATUS = 'https://www.johnstonnc.com/envhealth/content.cfm?pd=permits'
JOHNSTON_STAFF = 'https://www.johnstonnc.com/envhealth/content.cfm?pd=staff'

johnston_sections = [
    ('Johnston County Environmental Health is the local permitting office',
     'Johnston County Public Health’s Environmental Health Department administers well and septic permits. The county’s current staff directory identifies an On-Site Wastewater supervisor, soil specialists, and On-Site Wastewater program specialists at the Smithfield Environmental Health office.'),
    ('New systems require an application, site plan, zoning document, and fee',
     'Johnston County’s septic application instructs applicants to submit a completed application, site plan, zoning document from the appropriate zoning district, and the required fee for each lot. The form provides separate application paths for a new system, repair, replacement, and an open-permit revision requiring a site visit.'),
    ('Prepare the property for the site and soil evaluation',
     'The county’s septic-application instructions require a completed site plan and, for new-system evaluations, accessible site conditions and flagged property corners. The guidance warns against disturbing or reshaping the soil in the proposed septic or repair area because site disturbance can affect suitability or an existing permit.'),
    ('Current county septic fees are published',
     'Johnston County’s Environmental Health fee schedule is effective July 1, 2025. It lists $500 for a septic-system permit at 480 gallons or less, $575 for large-system design above 480 gallons, $250 for an existing-system upgrade or replacement, $175 for an open-permit revision requiring a site visit, $50 for a revision not requiring a site visit, $150 for Existing System Approval, and $100 for installation or reinspection. The schedule lists septic repair as no charge. Applicants should still confirm the current category before filing.'),
    ('Existing systems have a separate approval path',
     'Johnston County publishes a separate Application for the Approval to Use an Existing Wastewater System. That application requires a site plan and fee and identifies Local Health Department, AOWE, and Certified Inspector pathways, so reuse of an existing system for a new project should not be assumed without the applicable approval.'),
    ('Inspection and permit status can be checked online',
     'Johnston County provides a public Environmental Health search for septic and well inspection status by address or permit number. The county directs owners who cannot locate a septic permit through the search to contact Environmental Health for a copy.'),
]

johnston_sources = [
    ('Johnston County Environmental Health', JOHNSTON_EH),
    ('Johnston County — septic system and well application', JOHNSTON_APP),
    ('Johnston County — approval to use an existing wastewater system', JOHNSTON_EXISTING),
    ('Johnston County Environmental Health — current fee schedule', JOHNSTON_FEES),
    ('Johnston County — septic and well permit / inspection status search', JOHNSTON_STATUS),
    ('Johnston County Environmental Health — staff directory', JOHNSTON_STAFF),
    ('NCDHHS — On-Site Wastewater Program', JOHNSTON_STATE),
]

johnston_url = write_county_page(
    'North Carolina', 'north-carolina', 'Johnston',
    'Johnston County Public Health — Environmental Health Department, On-Site Wastewater Program',
    'Johnston County Environmental Health: 919-989-5180; 309 E. Market Street, Smithfield, NC 27577; envhealth@johnstonnc.gov.',
    johnston_sections, johnston_sources, verified='August 31, 2026'
)

# The earlier North Carolina generators leave the accumulated verified link list in globals.
# Add Johnston and rebuild the hub so the new guide is discoverable without dropping prior counties.
if 'nc_links' not in globals():
    raise RuntimeError('Johnston expansion expected accumulated North Carolina county links')
if not any(c == 'Johnston' for c, _ in nc_links):
    nc_links.append(('Johnston', 'Johnston County Public Health — Environmental Health, On-Site Wastewater Program'))

write_hub(
    'North Carolina','north-carolina',sorted(nc_links),
    'North Carolina’s On-Site Water Protection Branch provides statewide oversight for onsite wastewater systems, while local health departments perform the property-level permitting and inspection work. These guides are limited to counties with current, substantive local government guidance.',
    'This North Carolina set now covers 27 verified counties. SepticScope does not extrapolate one county’s workflow, fees, permit duration, inspection schedule, site-evaluation procedure, or local documentation requirements to another county.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    text = text.replace('Browse 26 verified North Carolina county septic guides →', 'Browse 27 verified North Carolina county septic guides →')
    county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if johnston_url not in sm:
        sm = sm.replace('</urlset>', f'<url><loc>{johnston_url}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
        sitemap.write_text(sm, encoding='utf-8')

p = OUTPUT / 'counties' / 'north-carolina' / 'johnston' / 'index.html'
t = p.read_text(encoding='utf-8')
if 'Local septic rules not yet verified' in t or 'OFFICIAL SOURCES CHECKED' not in t.upper() or 'Official sources' not in t:
    raise RuntimeError('Johnston County verified page failed production checks')
if '$500' not in t or '$575' not in t or 'no charge' not in t.lower():
    raise RuntimeError('Johnston County current fee details are missing')

print('North Carolina sixth expansion complete: +1 verified Johnston County guide (27 total verified NC counties)')
