# SepticScope Texas expansion — eighth verified county batch.
# Denton County verified from current Denton County and TCEQ sources on 2026-08-31.

TX8_STATE = 'https://www.tceq.texas.gov/permitting/ossf/ossfpermits.html'
TX8_LICENSES = 'https://www.tceq.texas.gov/licensing/licenses/ossflic'
DENTON_EH = 'https://www.dentoncounty.gov/657/Environmental-Health-Division'
DENTON_PACKET = 'https://www.dentoncounty.gov/DocumentCenter/View/1440/Septic-Permit-Application-Packet-PDF'
DENTON_MAINT = 'https://www.dentoncounty.gov/660/Septic-System-Maintenance-Management'
DENTON_COMPLAINTS = 'https://www.dentoncounty.gov/658/Complaint-Procedures'
DENTON_DEVELOPMENT = 'https://www.dentoncounty.gov/667/Development-Services'

denton_sections = [
    ('Denton County Public Health Environmental Health is the local OSSF authority in unincorporated areas',
     'Denton County Public Health Environmental Health administers the county on-site sewage facility order throughout the unincorporated portions of Denton County. The county says its staff reviews OSSF designs, issues permits to construct, performs specialized final inspections, and enforces applicable state and county requirements. Properties inside a municipality should confirm which permitting authority has jurisdiction before relying on the county process.'),
    ('The current county packet requires a complete permit application, site evaluation and scaled site plan',
     'Denton County’s septic permit packet states that the application must be complete before processing and that a valid site evaluation for the area where each system will be installed must be submitted. The required scaled site plan must show the lot and buildings, septic tank and drainfield, water wells within 150 feet, ponds/creeks/rivers/drainage ditches or swimming pools, potable water lines, slope information, easements, and floodplain status. A complete flood-elevation certificate is required when the building is in a designated special flood hazard area.'),
    ('The published septic application and inspection fee is $310',
     'The Denton County Public Health septic permit packet currently posted by the county lists a $310 application fee for authorization to construct and inspection and directs payment to Denton County. The packet is marked revised November 26, 2024. Because fee schedules can change, applicants should confirm the amount on the live county packet or with Environmental Health before paying.'),
    ('Installation is subject to county inspection before the system is placed in service',
     'The county permit application authorizes Denton County Environmental Health and applicable state agencies to enter the property for OSSF inspections. Denton County’s program page states that Environmental Health conducts specialized final inspections as part of its permitting duties. Applicants should coordinate inspection timing with the county and should not assume an installed system may be covered or operated until the permitting authority has completed the required approval process.'),
    ('System type, installer information and state credentials are part of the permit record',
     'The Denton County application asks the applicant to identify the proposed system type and provide the installer’s name, contact information and OSSF license number. TCEQ requires OSSF installers, maintenance providers and maintenance technicians to hold the applicable license or registration, while site evaluations must satisfy state and local requirements. Owners should verify current credentials before hiring.'),
    ('OSSFs that require maintenance have recorded and continuing obligations',
     'The county packet includes a Certification of OSSF Requiring Maintenance. For systems subject to that requirement, Denton County requires deed-record notice, proof of recording to the permitting authority, and continuous maintenance under the county OSSF order. The certification states that signed maintenance contracts must be submitted to Environmental Health within 30 days after a property transfer when applicable and that the owner must request transfer of the OSSF permit to the buyer or new owner.'),
    ('Conventional septic maintenance guidance recommends regular tank cleaning, but it is guidance rather than a blanket permit condition',
     'Denton County’s maintenance page advises owners not to treat a septic system like a municipal sewer, to protect the disposal field from structures and vehicle loading, and to establish a regular tank-cleaning schedule. The county specifically recommends cleaning at roughly two-to-three-year intervals because most homeowners cannot directly judge sludge and scum levels. This is county maintenance guidance; system-specific permits and maintenance-contract requirements control when they impose a different obligation.'),
    ('Repairs, failures and complaints should be coordinated with Environmental Health before work',
     'Denton County inspectors investigate complaints involving existing OSSFs and can conduct on-site inspections and follow-up enforcement when a violation exists. Texas rules also distinguish ordinary permitted repairs from limited emergency repairs that may be reported after work begins. Owners should contact Denton County Environmental Health before repair or replacement work to determine the local permit, design and inspection path for the specific failure.'),
    ('A separate county development permit may also be required',
     'Denton County Development Services states that development in unincorporated Denton County generally requires a Development Permit and separately notes that an OSSF/septic permit may be required through Public Health Environmental Health. Septic approval therefore may be only one part of the county development process for a new home, addition or other project.'),
]

denton_sources = [
    ('Denton County Public Health — Environmental Health Division / OSSF Program', DENTON_EH),
    ('Denton County Public Health — Septic Permit Application Packet', DENTON_PACKET),
    ('Denton County — Septic System Maintenance & Management', DENTON_MAINT),
    ('Denton County — OSSF Complaint Procedures', DENTON_COMPLAINTS),
    ('Denton County Development Services — development and septic permit coordination', DENTON_DEVELOPMENT),
    ('Texas Commission on Environmental Quality — Getting a Permit for an OSSF', TX8_STATE),
    ('Texas Commission on Environmental Quality — OSSF Licensing', TX8_LICENSES),
]

denton_url = write_county_page(
    'Texas', 'texas', 'Denton',
    'Denton County Public Health — Environmental Health Division, On-Site Sewage Facility program',
    'Denton County Environmental Health Division, 3900 Morse Street, Denton, TX 76208; 940-349-2920 (additional county number 972-434-8862). Confirm current office hours and jurisdiction before visiting.',
    denton_sections, denton_sources, verified='August 31, 2026'
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if denton_url not in sm:
        sm = sm.replace('</urlset>', f'<url><loc>{denton_url}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
        sitemap.write_text(sm, encoding='utf-8')

page = OUTPUT / 'counties' / 'texas' / 'denton' / 'index.html'
if not page.exists():
    raise RuntimeError('Denton verified county page was not generated')
text = page.read_text(encoding='utf-8')
for required in ('Official sources checked August 31, 2026', '$310', '150 feet', 'November 26, 2024', 'continuous maintenance', 'two-to-three-year'):
    if required not in text:
        raise RuntimeError(f'Denton verified page missing required validated detail: {required}')
if 'Local septic rules not yet verified' in text:
    raise RuntimeError('Denton verified page was overwritten by an unverified fallback')

print('Texas eighth expansion complete: +1 verified Denton County guide')
