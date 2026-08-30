# SepticScope Oregon additional expansion — official Oregon DEQ and county sources.
# Verified on 2026-08-30. Adds only counties with substantive local onsite guidance.

OR2_DEQ_ROLE = 'https://www.oregon.gov/deq/Residential/Pages/Onsite-Contacts.aspx'
OR2_DEQ_PROGRAM = 'https://www.oregon.gov/deq/residential/pages/onsite.aspx'
OR2_DEQ_LICENSE = 'https://www.oregon.gov/deq/Residential/Pages/Onsite-Licensing.aspx'

OR2_COUNTIES = {
    'Yamhill': {
        'authority': 'Yamhill County Planning & Development — Sanitation Program / County Sanitarian, administering Oregon onsite sewage rules',
        'contact': 'Yamhill County Planning & Development — 503-434-7516; 400 NE Baker Street, 2nd Floor, McMinnville, OR 97128. Sanitarian office hours are by appointment.',
        'sources': [
            ('Yamhill County — Sanitation', 'https://www.co.yamhill.or.us/309/Sanitation'),
            ('Yamhill County — Planning & Development', 'https://www.co.yamhill.or.us/283/Planning-Development'),
            ('Yamhill County Code Chapter 10.50 — Septic System Enforcement Code', 'https://www.co.yamhill.or.us/DocumentCenter/View/16551/YCC-1050-YAMHILL-COUNTY-SEPTIC-SYSTEM-ENFORCEMENT-CODE-PDF'),
        ],
        'sections': [
            ('County Sanitarian approval follows land-use approval', 'Yamhill County states that, after land-use approval, subsurface sewage-disposal approval must be obtained from the County Sanitarian. The county describes this as a two-step process: first determining soil suitability for a drainfield, then obtaining the permit and installing the septic tank and drainfield system.'),
            ('Site evaluation is required before installation', 'The county requires a site-evaluation application before a new septic tank and drainfield are installed. The applicant prepares test holes, and county staff investigate the soil to determine whether the proposed drainfield area is suitable for effluent disposal.'),
            ('Installation permit and county inspection follow soil approval', 'After soil suitability is approved, Yamhill County requires an onsite disposal permit before installation. The county states that the permitted work is subject to onsite inspections to verify correct installation.'),
            ('Existing systems can require county evaluation', 'Yamhill County states that an Existing System Evaluation may be needed for development on parcels of three acres or less or for loan approval. The review can include an onsite investigation and county records review.'),
            ('Bedroom additions, replacement homes, and failures have separate septic paths', 'Changing the use of an existing septic system, including adding bedrooms or replacing a home, may require a septic Authorization. A failing system requires a septic repair permit.'),
            ('County has direct delegated enforcement authority', 'Yamhill County Code Chapter 10.50 states that the county implements authority delegated by the State of Oregon for onsite septic systems and adopts the applicable statewide onsite rules for local enforcement.'),
        ],
    },
    'Linn': {
        'authority': 'Linn County Environmental Health — Septic Systems Program, administering Oregon onsite wastewater rules',
        'contact': 'Linn County Environmental Health — 541-967-3821; LinnEH@linncountyhealth.org; 315 SW 4th Avenue, 1st Floor, Albany, OR 97321.',
        'sources': [
            ('Linn County — Environmental Health Contact / Septic Systems', 'https://www.linncountyor.gov/eh/custom-contact-page/environmental-health-contact-information'),
            ('Linn County — Construction/Installation or Minor Repair/Alteration Permit Fact Sheet', 'https://www.linncountyor.gov/media/26946'),
        ],
        'sections': [
            ('Environmental Health administers the county septic program', 'Linn County Environmental Health maintains the county septic-system program, including applications, pre-cover inspection requests, archived permit searches, installer information, onsite fees, maintenance guidance, and Oregon onsite rules.'),
            ('Approved site evaluation is required for new construction permits', 'Linn County’s current permit fact sheet states that a Construction/Installation Permit is used for a new sewage-disposal system serving new site development and that an approved site evaluation is required before the construction-permit application.'),
            ('County distinguishes minor repair from minor alteration', 'Linn County defines a Minor Repair Permit for repair or replacement of a failing septic tank or distribution unit when the drainfield is not involved. A Minor Alteration Permit is used to replace or relocate a septic tank or distribution unit when the drainfield is not being changed.'),
            ('Permit applicants must control the property', 'The county states that onsite permits are issued only to the property owner, a contract purchaser in control of the property, or the owner’s legal representative.'),
            ('Permits have a one-year validity period', 'Linn County states that these onsite permits expire one year after issuance. The original permittee may renew before expiration or seek reinstatement within one year after expiration under the county’s published process.'),
            ('Pre-cover inspection is part of the county workflow', 'Linn County Environmental Health provides a dedicated pre-cover inspection request process for septic systems, reinforcing that covered work must be coordinated with county inspection before completion.'),
        ],
    },
    'Columbia': {
        'authority': 'Columbia County Land Development Services — On-site Wastewater Program, administering Oregon DEQ onsite rules',
        'contact': 'Columbia County Land Development Services — 503-397-1501; onsite@columbiacountyor.gov; septic inspections 503-397-7269; 445 Port Avenue, St. Helens, OR 97051.',
        'sources': [
            ('Columbia County — On-site Wastewater Program', 'https://www.columbiacountyor.gov/on-site-program'),
            ('Columbia County — On-site Wastewater Application Guides and Forms', 'https://www.columbiacountyor.gov/departments/LandDevelopment/on-site-application-guides-forms'),
            ('Columbia County — Land Development Services Contact Information', 'https://www.columbiacountyor.gov/contact-information'),
        ],
        'sections': [
            ('County regulates septic installation, repair, and maintenance', 'Columbia County states that its Land Development Services Department manages the On-site Wastewater Program and regulates installation, repair, and maintenance of septic systems for homes and businesses not served by community sewer.'),
            ('County performs site evaluations and permitting', 'The county identifies site evaluations and onsite sewage-system permitting as core services and states that it administers the Oregon State Onsite Wastewater Treatment Rules issued by Oregon DEQ.'),
            ('Authorization Notice is required for specified existing-system changes', 'Columbia County’s application guide states that an Authorization Notice is required when placing an existing onsite system into service, reconnecting to it, changing its use, or increasing projected daily sewage flow.'),
            ('Separate residential and commercial application paths are published', 'The county publishes separate onsite applications for single-family residential systems and commercial/industrial systems, allowing applicants to use the locally specified permit path rather than a generic septic application.'),
            ('Building approval requires onsite wastewater clearance where septic is used', 'Columbia County’s current building-permit materials direct applicants to obtain approval from the local sewer district or the Columbia County onsite-wastewater Sanitarian before building-permit review where private wastewater disposal applies.'),
            ('County provides direct septic inspection contacts', 'Land Development Services publishes a separate septic-inspection phone number in addition to its general permitting contact, reflecting county responsibility for required onsite inspection work.'),
        ],
    },
}

or2_urls=[]
for county,data in OR2_COUNTIES.items():
    sources=[
        ('Oregon DEQ — County office and residential onsite septic agents', OR2_DEQ_ROLE),
        ('Oregon DEQ — Onsite Wastewater Management Program', OR2_DEQ_PROGRAM),
        ('Oregon DEQ — Sewage Disposal Service Business Licensing', OR2_DEQ_LICENSE),
    ] + data['sources']
    sections=[
        ('Oregon county-agent framework', 'Oregon DEQ states that under OAR 340-071-0120 it may authorize counties as its agents for onsite-system permitting, including receiving and processing applications, issuing permits, enforcing onsite requirements, and performing required inspections. Oregon also requires sewage-disposal service businesses performing regulated installation or pumping work to hold the applicable state license.')
    ] + data['sections']
    or2_urls.append(write_county_page('Oregon','oregon',county,data['authority'],data['contact'],sections,sources,verified='August 30, 2026'))

sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in or2_urls if u not in sm)
    if entries:
        sitemap.write_text(sm.replace('</urlset>',entries+'</urlset>'),encoding='utf-8')

print(f'Oregon additional expansion complete: +{len(or2_urls)} verified county guides')
