# SepticScope Washington expansion — official Washington State and county/local government sources
# Limited to counties with current, substantive local OSS permitting guidance independently validated.

WA_STATE_ROLE = 'https://doh.wa.gov/community-and-environment/wastewater-management/site-sewage-systems-oss/management-strategy/management-roles'
WA_RULE_REVISION = 'https://doh.wa.gov/community-and-environment/wastewater-management/rules-and-regulations/site-rule-revision'

WA_COUNTIES = {
    'Clark': {
        'authority': 'Clark County Public Health — On-site Septic Program',
        'contact': 'Clark County Public Health On-site Septic Program — 564-397-8428. Clark County Public Health administers local OSS permitting, professional certification, records, and operation-and-maintenance requirements.',
        'sources': [
            ('Clark County Public Health — On-site Septic Systems', 'https://clark.wa.gov/public-health/site-septic-systems'),
            ('Clark County — OSS non-compliance fee', 'https://clark.wa.gov/public-health/oss-non-compliance-fee'),
        ],
        'sections': [
            ('Local permitting and design review',
             'Washington Department of Health states that local health jurisdictions permit and manage onsite sewage systems. Clark County Public Health describes its local program as responsible for proper OSS placement, design, installation, and maintenance and provides the county permit process, forms, fees, and certified-provider lists.'),
            ('County-certified septic professionals',
             'Clark County requires people offering septic pumping, inspection, maintenance, repair, or installation services to be certified by Clark County Public Health. The county states that these certifications are renewed annually and directs property owners to its current certified provider lists.'),
            ('Required inspection intervals',
             'Clark County publishes local operation-and-maintenance inspection intervals by system type: conventional gravity systems every three years, pressure-distribution systems every two years, and advanced systems such as sand filters, sand mounds, aerobic treatment units, and similar systems every year. Food-establishment systems are inspected every year regardless of type.'),
            ('Property-sale record requirement',
             'Clark County tells realtors and homeowners to ensure a current Report of System Status is on file before listing a home for sale. For this county requirement, the report is considered current if completed within one year of the sale date.'),
            ('Annual operating fee and overdue-inspection fee',
             'Clark County states that properties with an onsite sewage system pay an annual OSS operating-permit fee. Under the county policy approved in 2025, an additional non-compliance fee can be placed on the property-tax bill when a required inspection is more than one year overdue as of December 31.'),
            ('Existing septic records',
             'Clark County makes permits, as-built drawings, and inspection information available through its Property Information Center. Search by address or tax account number and use the Environmental tab; if documents are unavailable, the county directs users to Public Health.'),
        ],
    },
    'Island': {
        'authority': 'Island County Public Health — Environmental Health Onsite Sewage Program',
        'contact': 'Island County Environmental Health — 360-679-7350 (Coupeville) or 360-678-8261 (Camano). The county reviews new and replacement septic systems and maintains parcel/as-built records.',
        'sources': [
            ('Island County — Onsite Sewage (Septic) Systems', 'https://www.islandcountywa.gov/190/Onsite-Sewage-Septic-Systems'),
            ('Island County — Septic Permitting', 'https://www.islandcountywa.gov/673/Permitting'),
            ('Island County — Building Permit Requirements', 'https://www.islandcountywa.gov/540/Building-Permits'),
            ('Island County — Parcel and As-built Information', 'https://islandcountywa.gov/686/Parcel-and-Asbuilt-Information---Public-'),
        ],
        'sections': [
            ('Site registration comes first',
             'Island County describes a three-stage septic process. A licensed designer first evaluates soil depth, texture, groundwater conditions, and other site factors and submits a Site Registration to the county. The county states that the registration does not expire unless site conditions are significantly changed, such as through grading or logging.'),
            ('Design approval and construction permit',
             'After site registration, a licensed designer prepares the system design based on the planned use of the property. Island County Public Health reviews the application and, when approved, issues the septic construction permit. The county states that an approved septic permit is valid for three years.'),
            ('As-built record after installation',
             'After installation, Island County requires an as-built drawing documenting the system as actually installed. The county says the installer prepares the scaled as-built showing component locations and relevant equipment or operating information.'),
            ('Septic documentation before a building-permit submittal',
             'Island County Planning and Building states that, for building-permit submittals under the requirements effective March 1, 2024, applicants must have a site registration and a septic design prepared by a qualified septic designer, along with the other listed access, address, and water-availability documentation.'),
            ('Existing records',
             'Island County provides parcel and septic as-built information through its public portal and directs users to onlineRME for septic inspection and pumping reports.'),
        ],
    },
    'Okanogan': {
        'authority': 'Okanogan County Public Health District (OCPHD) — Environmental Health / Liquid Waste Program',
        'contact': 'Okanogan County Public Health District Environmental Health — 509-422-7140; 1240 South 2nd Avenue, Okanogan, WA 98840.',
        'sources': [
            ('Okanogan County — Onsite Septic / Liquid Waste', 'https://www.okanogancounty.gov/507/Onsite-Septic-Liquid-Waste'),
            ('Okanogan County — Environmental Health', 'https://www.okanogancounty.gov/258/Environmental-Health'),
            ('Okanogan County — OSS Construction Standards', 'https://www.okanogancounty.gov/DocumentCenter/View/1774/Onsite-Sewage-System-OSS-Construction-Standards-for-Onsite-Sewage-Systems-PDF'),
        ],
        'sections': [
            ('County permit and final inspection',
             'Okanogan County Public Health District reviews OSS designs under its local onsite sewage disposal regulations. The county states that the process requires site visits for test holes, a permit before installation, and a final inspection to confirm proper installation.'),
            ('Local jurisdiction for systems below 3,500 gallons per day',
             'OCPHD states that it enforces liquid-waste regulations for onsite sewage systems with design flows below 3,500 gallons per day. The county directs larger-system questions to the applicable Washington Department of Health or Department of Ecology program.'),
            ('Resident-homeowner gravity-system option',
             'Okanogan County’s published construction standards state that resident homeowners may design and install their own gravity-flow septic systems. Other installations must be performed by an onsite sewage system installer licensed in Okanogan County.'),
            ('No construction before design approval',
             'The county construction standards state that construction may not begin until the OSS design has been submitted, approved, and a permit has been issued. The design/site-plan requirements include test-hole locations, system components and installation depths, a reserve area, property lines, and existing and proposed structures.'),
            ('Records and current provider lists',
             'OCPHD Environmental Health publishes current licensed OSS installer and pumper/operation-and-maintenance specialist lists and provides a parcel-information public-record request process for environmental-health records.'),
        ],
    },
    'Skamania': {
        'authority': 'Skamania County Community Development — Environmental Health On-Site Sewage Program',
        'contact': 'Skamania County Environmental Health — 509-427-3900; permitcenter@co.skamania.wa.us. Septic applications and inspections are handled through the county permit center and CloudPermit.',
        'sources': [
            ('Skamania County — On-Site Sewage Program', 'https://www.skamaniacounty.gov/departments-offices/community-development/environmental-health/onsite-sewage'),
        ],
        'sections': [
            ('Site evaluation for new builds, expansions, and certain repairs',
             'Skamania County’s current septic process calls for a site evaluation for new construction, expansions, and repairs when prior soil records are unavailable. Applicants prepare the required site plan and test pits and submit the county site-evaluation application.'),
            ('Water-adequacy verification',
             'The county septic workflow includes water-adequacy documentation: applicants using public water submit the public-water letter, while properties using a private or shared well follow the county Water Adequacy Verification application process.'),
            ('Licensed designer and installer',
             'Skamania County directs applicants to use licensed septic designers for system design and licensed installers for installation, using the county’s current professional lists and licensing requirements.'),
            ('Final inspection before covering',
             'Skamania County requires the installed system to receive its final inspection before the septic system is covered. The inspection can be scheduled through the county permit system or permit center.'),
            ('Final as-built drawing',
             'After installation and inspection, the county process requires submission of the final as-built drawing using the county’s as-built checklist.'),
            ('Operation and maintenance',
             'Skamania County states that inspection frequency depends on system type and describes a one-to-three-year inspection range for residential systems, while proprietary systems require periodic maintenance contracts. Property owners remain responsible for operating and maintaining their systems.'),
        ],
    },
}

wa_urls = []
wa_links = []
for county, data in WA_COUNTIES.items():
    sources = [
        ('Washington State Department of Health — OSS management roles', WA_STATE_ROLE),
        ('Washington State Department of Health — Chapter 246-272A rule revision', WA_RULE_REVISION),
    ] + data['sources']
    sections = [
        ('Washington local-health-jurisdiction framework',
         'Washington State Department of Health states that local health jurisdictions permit and manage onsite sewage systems in their counties. Local programs review and approve system locations, designs, installations, and repairs and may adopt local rules that meet or exceed Chapter 246-272A WAC.')
    ] + data['sections']
    url = write_county_page(
        'Washington', 'washington', county,
        data['authority'], data['contact'], sections, sources,
        verified='August 29, 2026'
    )
    wa_urls.append(url)
    wa_links.append((county, data['authority']))

write_hub(
    'Washington', 'washington', sorted(wa_links),
    'Washington delegates onsite sewage system permitting and management to local health jurisdictions. These guides cover counties where the local agency’s current permit process and meaningful county-specific requirements were verified directly from government sources.',
    'This initial Washington batch is intentionally limited to Clark, Island, Okanogan, and Skamania counties. SepticScope is not extrapolating one county’s local rules to the rest of Washington; additional counties will be added only after their local permitting authority and procedures are independently validated.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    if '/counties/washington/' not in text:
        promo = '<section><h2>Washington</h2><p><a href="/counties/washington/">Browse the first 4 verified Washington county septic guides →</a></p></section>'
        text = text.replace('</main>', promo + '</main>', 1) if '</main>' in text else text.replace('</body>', promo + '</body>', 1)
        county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/washington/'] + wa_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'Washington expansion complete: +{len(wa_urls)} verified county guides')
exec((ROOT / 'oregon_expansion.py').read_text(encoding='utf-8'), globals())
