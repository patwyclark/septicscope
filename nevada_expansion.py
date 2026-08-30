# SepticScope Nevada expansion — verified county batch.
# Verified from Nevada NDEP and official local public-health/county sources on 2026-08-30.

NV_NDEP = 'https://ndep.nv.gov/water/water-pollution-control/permitting/onsite-sewage-disposal-system-program'

NV_COUNTIES = [
    {
        'county': 'Clark',
        'authority': 'Southern Nevada Health District — Individual Sewage Disposal System (ISDS) / Septic System Program',
        'contact': 'Southern Nevada Health District, Environmental Health; septic program contact and applications are provided through the SNHD ISDS program. SNHD identifies itself as the permitting, inspection, and regulatory authority for residential septic systems in Clark County.',
        'sources': [
            ('Southern Nevada Health District — Sewage/Septic Disposal Systems (ISDS)', 'https://www.southernnevadahealthdistrict.org/permits-and-regulations/sewage-septic-disposal-systems-isds/'),
            ('Southern Nevada Health District — Residential Septic System Permit Requirements', 'https://www.southernnevadahealthdistrict.org/permits-and-regulations/sewage-septic-disposal-systems-isds/residential-isds-permits/residential-septic-tank-permit-requirements/'),
            ('Southern Nevada Health District — ISDS and Water Well Certification Procedures', 'https://www.southernnevadahealthdistrict.org/permits-and-regulations/sewage-septic-disposal-systems-isds/residential-isds-permits/certification-procedures-for-individual-sewage-disposal-system-isds-and-or-water-well/'),
            ('Southern Nevada Health District — Septic program facts and current requirements', 'https://www.southernnevadahealthdistrict.org/permits-and-regulations/sewage-septic-disposal-systems-isds/did-you-know/'),
        ],
        'sections': [
            ('SNHD is the local septic authority in Clark County', 'The Southern Nevada Health District states that its ISDS program permits, inspects, and regulates residential septic systems throughout Clark County. Under its agreement with Nevada NDEP, SNHD also permits commercial holding tanks and qualifying smaller commercial onsite systems.'),
            ('New residential septic eligibility depends on sewer availability', 'SNHD requires septic permit applications to include documentation that community sewer connection is unavailable. Its current residential guidance states that it continues to issue new ISDS permits where the proposed system is more than 400 feet from the nearest community sewer point of connection, subject to the remaining eligibility requirements.'),
            ('Water-source documentation is part of the permit package', 'Clark County applicants must document an approved water source. SNHD lists water-district approval or commitment documentation for properties within applicable service areas, while well-served properties must provide a well log and obtain any necessary Nevada water rights.'),
            ('Colorado River water can bar a new septic permit without a waiver', 'SNHD states that Nevada law effective June 6, 2023 prohibits new septic-system installation on properties receiving Colorado River water unless the Southern Nevada Water Authority grants the required waiver. SNHD cannot issue the new-system permit in those cases without the waiver.'),
            ('Real-estate septic certification is available through SNHD', 'SNHD offers official septic certifications, commonly requested during real-estate transactions or by lenders. The district states that it is the sole entity in the Clark County area that can issue the official septic-system certification, which is distinct from a private structural inspection.'),
            ('Local operating rules restrict use of the septic area', 'SNHD states that current rules prohibit paving or vehicular traffic over the septic system and prohibit trees within ten feet of the system. It also states that residential RV waste may not be discharged into the residential septic system.'),
            ('Abandonment requires documentation even when no permit fee applies', 'SNHD states that no permit or fee is required to abandon a septic system, but an abandonment form and supporting documentation must be submitted so the Health District can update its records.'),
        ],
    },
    {
        'county': 'Washoe',
        'authority': 'Northern Nevada Public Health — Environmental Health Services, Septic Systems & Liquid Waste Program',
        'contact': 'Northern Nevada Public Health Environmental Health Services, 1001 E. Ninth Street, Building B, Reno, NV 89512. Septic applications and test-trench permits are submitted through the OneNV permitting portal.',
        'sources': [
            ('Northern Nevada Public Health — Septic Systems & Liquid Waste', 'https://nnph.org/programs-and-services/environmental-health/land-development/septic-liquid-waste.php'),
        ],
        'sections': [
            ('NNPH regulates residential sewage disposal in Washoe County', 'Northern Nevada Public Health states that its Environmental Health Services division has regulatory authority over sewage and wastewater disposal within Washoe County, including residential onsite sewage disposal systems, pumping contractors, portable-toilet operators, dump stations, and sewage-release complaints.'),
            ('Commercial septic systems follow a different state path', 'NNPH explicitly states that commercial septic systems do not fall under its authority by state statute and directs commercial projects to the Nevada Division of Environmental Protection Bureau of Water Pollution Control. This makes residential versus commercial use a threshold permitting question in Washoe County.'),
            ('A test-trench inspection begins new residential septic planning', 'NNPH states that the first step in planning a new residential septic system is a test-trench inspection. Environmental Health staff examine limiting layers, develop a soil profile, and determine whether percolation testing is required.'),
            ('Required percolation testing must be performed by an engineer', 'When NNPH determines that percolation testing is necessary after the test-trench inspection, the county health program states that a licensed engineer performs the testing. Applicants should therefore avoid assuming a perc test is always required before the county has reviewed the trench.'),
            ('Test-trench applications are submitted through the county health permitting portal', 'NNPH directs applicants to submit test-trench permit applications through the OneNV online permitting portal. This review precedes final septic design and helps establish the site constraints used for the system design.'),
            ('Current local sewage regulations were adopted in 2026', 'NNPH states that the Washoe County District Board of Health approved updated Sewage, Wastewater and Sanitation regulations on January 22, 2026. Applicants should use those current local rules rather than older archived requirements.'),
            ('County septic and well records can be requested', 'Northern Nevada Public Health provides a septic and well records request process for property research. Historic records can be important when evaluating existing-system location, permitted capacity, or future additions.'),
        ],
    },
    {
        'county': 'Nye',
        'authority': 'Nye County Building and Safety for qualifying local ISDS; Nevada Division of Environmental Protection for systems outside local delegated scope',
        'contact': 'Nye County Building and Safety, Pahrump office; 775-751-6280. Nevada NDEP identifies Nye County as the local permitting authority for qualifying systems 3,000 gallons per day or smaller under an existing agreement.',
        'sources': [
            ('Nye County — Building Department', 'https://www.nyecountynv.gov/322/Building-Department'),
            ('Nye County — Application Submittal', 'https://www.nyecountynv.gov/992/Application-Submittal'),
        ],
        'sections': [
            ('NDEP identifies Nye County Building and Safety as a local septic permitting authority', 'Nevada NDEP states that residential septic approvals are handled by local health authorities or county building departments rather than NDEP. For Nye County, NDEP specifically states that systems 3,000 gallons per day or smaller are permitted by Nye County Building and Safety under an existing agreement.'),
            ('Pahrump has an additional nitrogen-management requirement', 'NDEP identifies Pahrump as a Nitrogen Management Area and states that advanced treatment systems are required there. This is a location-specific constraint that can materially change system design and cost compared with a conventional septic assumption elsewhere in the county.'),
            ('Larger or out-of-scope systems can require NDEP permitting', 'NDEP administers commercial onsite sewage disposal permitting outside the local delegated exceptions. Projects above Nye County’s locally identified 3,000-gallon-per-day scope, unusual systems, or other projects outside the local agreement should confirm the state permit path with NDEP before design.'),
            ('Nye County provides a dedicated ISDS development checklist', 'Nye County’s Building and Safety application resources include an ISDS checklist alongside its development and building-permit materials. Applicants should use the current county checklist with the building application rather than treating septic approval as an informal field step.'),
            ('County building applications are submitted through the Citizen Services process', 'Nye County directs applicants to its online application system for building permits and provides current submittal instructions and payment procedures. Septic-related development documents should be coordinated through the county process when the project is within local jurisdiction.'),
        ],
    },
]

nv_urls=[]
for d in NV_COUNTIES:
    sources=[('Nevada Division of Environmental Protection — Onsite Sewage Disposal System Program', NV_NDEP)] + d['sources']
    sections=[
        ('Nevada state and local permitting framework', 'Nevada NDEP distinguishes residential septic systems from the commercial onsite systems it directly permits. Residential approvals are issued by the applicable local health authority or county building department; commercial systems generally fall under NDEP unless a local agreement applies. Confirm project use and design flow before relying on a local residential permit path.')
    ] + d['sections']
    nv_urls.append(write_county_page('Nevada','nevada',d['county'],d['authority'],d['contact'],sections,sources,verified='August 30, 2026'))

# Preserve sitemap coverage for this new state batch if write_county_page does not already add the entries.
sitemap=OUTPUT/'sitemap.xml'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    entries=''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in nv_urls if u not in sm)
    if entries:
        sitemap.write_text(sm.replace('</urlset>',entries+'</urlset>'),encoding='utf-8')

# Guard this validated batch before nationwide fallback generation.
for d in NV_COUNTIES:
    p=OUTPUT/'counties'/'nevada'/slugify(d['county'])/'index.html'
    t=p.read_text(encoding='utf-8')
    if 'Local septic rules not yet verified' in t or 'VERIFIED' not in t.upper() or 'Official sources' not in t:
        raise RuntimeError(f'Nevada verified page failed: {d["county"]}')

print(f'Nevada expansion complete: +{len(nv_urls)} verified county guides')
