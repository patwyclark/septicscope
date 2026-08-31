# SepticScope Texas expansion — ninth verified county batch.
# Williamson County verified from current Williamson County and TCEQ sources on 2026-08-31.

TX9_STATE = 'https://www.tceq.texas.gov/permitting/ossf/ossfpermits.html'
TX9_LICENSES = 'https://www.tceq.texas.gov/licensing/licenses/ossflic'
WILCO_OSSF = 'https://www.wilcotx.gov/644/On-Site-Sewage-Facilities-OSSF'
WILCO_OWNER = 'https://www.wilcotx.gov/650/Property-Owner'
WILCO_INSTALLER = 'https://www.wilcotx.gov/647/Installer'
WILCO_MAINT = 'https://www.wilcotx.gov/651/How-a-Septic-System-Works'
WILCO_FEES = 'https://www.wilcotx.gov/DocumentCenter/View/16737'
WILCO_CHECKLIST = 'https://www.wilcotx.gov/DocumentCenter/View/16752/OSSF-Application-Requirements-Checklist'
WILCO_ORDER = 'https://www.wilcotx.gov/DocumentCenter/View/3109/Williamson-County-Order-2021-PDF'
WILCO_RECORDS = 'https://www.wilcotx.gov/1485/Open-Records-Request'

williamson_sections = [
    ('Williamson County Engineer’s Office is the local OSSF authority except within the City of Austin',
     'Williamson County Environmental Services states that its OSSF program regulates septic systems throughout Williamson County except areas located within the City of Austin. The County Engineer’s Office is authorized by TCEQ to administer the local program under 30 TAC Chapter 285 and the Williamson County OSSF Order. Owners near municipal boundaries should confirm jurisdiction before applying.'),
    ('New systems, repairs and enlargements use the county’s online permit process',
     'Williamson County requires an application to install a new OSSF or to modify, repair or enlarge an existing system. Applications are submitted through MyGovernmentOnline; the county says it no longer accepts paper or emailed OSSF applications. When the property footprint changes, a Certificate of Compliance must be obtained before the OSSF application can be processed, while a proposed OSSF in a floodplain requires a Floodplain Permit instead of that certificate.'),
    ('The application package requires a soil evaluation, site plan and complete OSSF design',
     'The county’s application checklist requires a warranty deed, owner authorization when an agent applies, a survey when the property is not in a recorded subdivision, a complete OSSF design, a separate soil-evaluation report, a separate site-plan overview and a floor plan. The checklist says proprietary or non-standard designs, designs over the Edwards Aquifer Recharge Zone, and designs in the 100-year floodplain must be submitted by a Texas Registered Sanitarian or Professional Engineer.'),
    ('Current county permit fees range from $510 for residential conventional systems to $910 for commercial aerobic systems',
     'Williamson County’s OSSF fee sheet, updated September 12, 2025, lists $510 for a residential conventional permit, $610 for residential non-conventional/non-aerobic, $710 for residential aerobic treatment or other routine-maintenance systems, $810 for commercial non-aerobic, and $910 for commercial aerobic/routine-maintenance systems. It also lists $100 for an extra site visit or inspection, $150 for a new or additional design review, and $60 for an aerobic-system license renewal or transfer. Applicants should confirm the live county fee sheet before paying because schedules can change.'),
    ('County inspections occur during critical construction phases before final approval',
     'Williamson County publishes system-specific inspection sequences. Most systems include two inspections; for example, conventional and leaching-chamber systems are inspected at the tank/pipe-and-gravel stage and again at final landscaping, while aerobic systems are inspected with tanks and lines open and again at final electrical/landscape completion. The licensed installer must schedule inspections and be present with equipment to verify construction elevations. Homeowners seeking to install their own residence system must obtain written county approval and follow the inspection schedule issued by the county.'),
    ('Aerobic and other routine-maintenance systems require continuing maintenance documents',
     'For an aerobic or other routine-maintenance OSSF, the county application requires a maintenance contract signed by both the owner and maintenance provider plus a recorded maintenance affidavit. Williamson County says its aerobic systems are initially permitted for two years and that owners must maintain a valid service arrangement and renew the county OSSF license at least every two years. The county currently charges $60 for that renewal.'),
    ('Aerobic licenses must be transferred when the property changes ownership',
     'Williamson County instructs a buyer of property with an aerobic system to transfer the operating license to the new owner. The county currently lists a $60 transfer fee and provides a License Renewal / Transfer form. Owners should also make sure the required maintenance arrangement remains in place through the transfer.'),
    ('Unlicensed existing systems may require a permit and compliance work',
     'The current fee schedule specifically addresses inspection of an unlicensed OSSF and states that the owner must purchase the appropriate OSSF permit and bring the system into compliance if the system is found to be illegal. Because repairs and enlargements also require applications, owners should contact the county before uncovering, replacing or modifying an existing system.'),
    ('Septic permit records can be requested directly from the county',
     'Williamson County accepts OSSF open-records requests for septic information. The county asks requesters to provide the property address or property ID and, when available, subdivision lot/block information or prior owner names so staff can locate the permit record.'),
]

williamson_sources = [
    ('Williamson County — On-Site Sewage Facilities (OSSF) program', WILCO_OSSF),
    ('Williamson County — Property Owner OSSF application and maintenance requirements', WILCO_OWNER),
    ('Williamson County — OSSF Installer inspections', WILCO_INSTALLER),
    ('Williamson County — How a Septic System Works / maintenance licensing', WILCO_MAINT),
    ('Williamson County Engineer’s Office — OSSF Program Fees (updated September 12, 2025)', WILCO_FEES),
    ('Williamson County — OSSF Application Requirements Checklist (updated September 12, 2025)', WILCO_CHECKLIST),
    ('Williamson County / TCEQ — 2021 OSSF Order', WILCO_ORDER),
    ('Williamson County — Open Records Request / septic records', WILCO_RECORDS),
    ('Texas Commission on Environmental Quality — Getting a Permit for an OSSF', TX9_STATE),
    ('Texas Commission on Environmental Quality — OSSF Licensing', TX9_LICENSES),
]

williamson_url = write_county_page(
    'Texas', 'texas', 'Williamson',
    'Williamson County Department of Infrastructure — County Engineer’s Office, On-Site Sewage Facility Program',
    'Williamson County Department of Infrastructure, 3151 SE Inner Loop, Suite B, Georgetown, TX 78626; OSSF office 512-943-3330. Confirm jurisdiction and current office procedures before visiting.',
    williamson_sections, williamson_sources, verified='August 31, 2026'
)

sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    if williamson_url not in sm:
        sm = sm.replace('</urlset>', f'<url><loc>{williamson_url}</loc><lastmod>2026-08-31</lastmod></url></urlset>')
        sitemap.write_text(sm, encoding='utf-8')

page = OUTPUT / 'counties' / 'texas' / 'williamson' / 'index.html'
if not page.exists():
    raise RuntimeError('Williamson verified county page was not generated')
text = page.read_text(encoding='utf-8')
for required in ('Official sources checked August 31, 2026', '$510', '$710', '$910', 'September 12, 2025', 'MyGovernmentOnline', 'two years', 'City of Austin'):
    if required not in text:
        raise RuntimeError(f'Williamson verified page missing required validated detail: {required}')
if 'Local septic rules not yet verified' in text:
    raise RuntimeError('Williamson verified page was overwritten by an unverified fallback')

print('Texas ninth expansion complete: +1 verified Williamson County guide')
exec((ROOT / 'texas_tenth_expansion.py').read_text(encoding='utf-8'), globals())
