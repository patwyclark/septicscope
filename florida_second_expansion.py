# SepticScope Florida second expansion — current county-health permitting and locally published requirements.
# Authoritative sources checked 2026-08-31.

FL2_COUNTIES = [
    {
        'county': 'Brevard',
        'authority': 'Florida Department of Health in Brevard County — Environmental Public Health Services / OSTDS',
        'contact': 'DOH-Brevard Environmental Public Health Services: 321-633-2100; Brevard.EHS@FLHealth.gov; 2725 Judge Fran Jamieson Way, Suite A116, Viera, FL 32940.',
        'sources': [
            ('DOH-Brevard — Onsite Sewage Disposal', 'https://brevard.floridahealth.gov/programs-and-services/environmental-public-health/onsite-sewage-disposal/'),
            ('DOH-Brevard — New OSTDS Application Packet and Fee Schedule', 'https://brevard.floridahealth.gov/wp-content/uploads/sites/8/2025/04/new-systems.pdf'),
            ('DOH-Brevard — OSTDS Operating Permits', 'https://brevard.floridahealth.gov/programs-and-services/environmental-public-health/onsite-sewage-disposal/operating-permits/'),
        ],
        'sections': [
            ('DOH-Brevard is the current local permitting office', 'Florida DEP’s current county-by-county permitting FAQ lists Brevard among the counties where OSTDS permits are issued by the Environmental Public Health Program of the local Florida Department of Health county office. DOH-Brevard also states directly that it continues to handle Brevard septic permitting and inspection.'),
            ('New-system applications and published fees', 'DOH-Brevard’s published new-system packet lists $510 for a new system when the county performs the site evaluation and $395 when a qualifying site evaluation is submitted with the application. The packet also lists a $115 site-evaluation-only fee, $75 reinspection fee, $50 site re-evaluation fee and separate charges for specified additional services. Confirm the current invoice before payment because fee schedules may change.'),
            ('The new-system packet requires detailed property and design information', 'The Brevard application packet requires a complete application, legal description, building floor plan and site plan, plus professional soil or engineering information when applicable. Residential floor plans must identify bedroom count and total square footage, and the site plan must provide the property information needed for county review.'),
            ('Accessory structures require septic plan review', 'DOH-Brevard states that sheds, pools and fences require a septic plan review when applicable. The county requires an application and a scaled site plan or survey showing the existing septic tank and drainfield together with the proposed structure, and currently lists a $30 plan-review fee.'),
            ('Operating permits apply to advanced and specified nonresidential systems', 'DOH-Brevard states that operating permits are required for aerobic treatment units, performance-based treatment systems, commercial septic systems, and industrial or manufacturing-zoned or equivalent septic systems. The county conducts routine operating-permit inspections and provides separate contacts for renewals, service contracts and maintenance reports.'),
            ('Keep installation work accessible for inspection', 'The county’s new-system packet states that connection piping from the structure drain to the septic tank must remain available for inspection by Environmental Health and the applicable building department. Owners and contractors should follow the permit-specific inspection sequence and avoid covering regulated work before approval.'),
        ],
    },
    {
        'county': 'Citrus',
        'authority': 'Florida Department of Health in Citrus County — Environmental Public Health / OSTDS',
        'contact': 'DOH-Citrus Environmental Health: 352-513-6100; EH.Feedback@FLHealth.gov; 3600 W. Sovereign Path, Lecanto, FL 34461.',
        'sources': [
            ('DOH-Citrus — Onsite Sewage Disposal', 'https://citrus.floridahealth.gov/programs-and-services/environmental-health/onsite-sewage-disposal/'),
            ('DOH-Citrus — Environmental Health Office', 'https://citrus.floridahealth.gov/location/environmental-health/'),
            ('DOH-Citrus — December 2025 Enhanced Nitrogen-Reducing Septic Requirement Notice', 'https://citrus.floridahealth.gov/2025/10/09/citrus-reminds-residents-of-septic-permitting/'),
            ('DOH-Citrus — Environmental Public Health and Septic Records', 'https://citrus.floridahealth.gov/programs-and-services/environmental-health/'),
        ],
        'sections': [
            ('DOH-Citrus remains the local permitting and inspection office', 'Florida DEP’s current permitting FAQ lists Citrus among the counties where OSTDS permits are issued by the local Florida Department of Health Environmental Public Health Program. DOH-Citrus states that the local office continues septic permitting and inspection and provides online invoice payment and permit access.'),
            ('Applications follow the county-health process under statewide OSTDS rules', 'For DOH-administered counties such as Citrus, Florida DEP directs applicants to submit the construction application, site plan, building floor plan and required fee to the local county health department. Property-specific design and siting decisions remain subject to the current Chapter 62-6 requirements and county review.'),
            ('Enhanced nitrogen reduction applies in specified spring-protection areas', 'DOH-Citrus states that applications received on or after December 15, 2025 for repairs or modifications to existing septic systems on all lot sizes in Priority Focus Areas within the applicable Basin Management Action Plan areas must use an enhanced nitrogen-reducing system. The county notice specifically identifies the Crystal River/Kings Bay and Chassahowitzka Springs Groups areas, so owners should confirm whether the parcel lies inside an affected Priority Focus Area before selecting a repair design.'),
            ('Operating permits apply to advanced and specified nonresidential systems', 'DOH-Citrus states that operating permits are required for aerobic treatment units, performance-based treatment systems, commercial septic systems, and industrial or manufacturing-zoned or equivalent septic systems.'),
            ('County septic records are available through Environmental Public Health', 'DOH-Citrus provides public access instructions for its eBridge system, including a septic-permit file cabinet used to retrieve available local inspection reports and documents. Property owners researching an existing system should check the county record before planning additions, repairs or replacement work.'),
        ],
    },
]

fl2_urls = []
for d in FL2_COUNTIES:
    sources = [
        ('Florida DEP — Onsite Sewage Program', FL_STATE),
        ('Florida DEP — Current OSTDS Permitting by County', FL_PERMITTING),
        ('Florida DEP — Enhanced Nitrogen-Reducing OSTDS Requirements', FL_ENR),
    ] + d['sources']
    sections = [
        ('Florida regulatory framework', 'Florida DEP administers statewide OSTDS statutes and Chapter 62-6 rules. During the current transition, the permitting office depends on county; DEP’s live permitting FAQ is the statewide directory for whether applicants file with DEP or the local Florida Department of Health Environmental Public Health Program.'),
    ] + d['sections']
    fl2_urls.append(write_county_page('Florida', 'florida', d['county'], d['authority'], d['contact'], sections, sources, verified='August 31, 2026'))

# The nationwide layer detects these pages as verified and builds the Florida hub accordingly.
sitemap = OUTPUT / 'sitemap.xml'
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
    entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-31</lastmod></url>' for u in fl2_urls if u not in sm)
    if entries:
        sitemap.write_text(sm.replace('</urlset>', entries + '</urlset>'), encoding='utf-8')

print(f'Florida second expansion complete: +{len(fl2_urls)} verified county guides')
