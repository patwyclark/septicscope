# SepticScope Arizona additional expansion — authoritative ADEQ and county sources.
# Verified on 2026-08-30. Adds only counties with substantive local onsite guidance.

AZ2_STATE = 'https://azdeq.gov/onsitewastewater'
AZ2_DELEGATION = 'https://azdeq.gov/delegation-agreements'
AZ2_TRANSFER = 'https://azdeq.gov/wqd-onsite-wastewater-notice-transfer-and-inspection'

AZ2_COUNTIES = [
    {
        'county': 'Pinal',
        'authority': 'Pinal County Community Development — Aquifer Protection Division',
        'contact': 'Pinal County Aquifer Protection Division; 85 N. Florence Street, First Floor, Florence, AZ 85132; 520-509-3555. Septic applications and inspections are administered through Community Development.',
        'sources': [
            ('Pinal County — Wells & Septic', 'https://www.pinal.gov/185/Wells-Septic'),
            ('Pinal County — Community Development / Aquifer Protection FAQ', 'https://www.pinal.gov/184/Community-Development'),
            ('Pinal County — Environmental Health Code', 'https://explore.pinal.gov/879/Environmental-Health-Code'),
            ('Pinal County — Current Community Development Fee Schedules', 'https://www.pinal.gov/1359/Fee-Schedules'),
        ],
        'sections': [
            ('Aquifer Protection administers local septic permitting and inspection', 'Pinal County states that its Aquifer Protection Program carries out permitting and inspections for conventional onsite wastewater systems up to 24,000 gallons per day and alternative systems up to 3,000 gallons per day. The county issues construction permits, inspects system construction, tracks septic locations, regulates alternative-system installation, and inspects and permits septic pumpers and waste haulers.'),
            ('A county permit is required before new construction, repair, or alteration', 'Chapter XI of the Pinal County Environmental Health Code states that no person may begin construction of a new onsite wastewater treatment facility, or repair or alter an existing facility, without an onsite wastewater permit from Pinal County.'),
            ('A qualified site inspection is part of the application path', 'Pinal County directs applicants without a sewer connection option to apply for a septic permit and states that a site inspection by a qualified inspector is required. The county also maintains separate site-investigation and percolation/seepage-pit evaluation services.'),
            ('County jurisdiction distinguishes conventional and alternative system sizes', 'Pinal County publishes separate program limits for conventional and alternative systems. Applicants with larger, unusual, or multi-permit projects should verify whether the county or ADEQ will perform the applicable review rather than assuming the residential septic workflow applies.'),
            ('Septic abandonment has a specific closure procedure', 'Pinal County states that a separate permit is not required for septic abandonment, but the tank must be pumped, electrical and mechanical components disconnected and removed, the tank removed/collapsed or completely filled with approved material, and the abandoned building sewer cut and plugged. The county must be notified within 30 days of closure.'),
            ('Current county fees distinguish permit, alteration, transfer, and inspection work', 'Pinal County publishes Aquifer Protection fees for Type 4 permits, transfers, alternative design review, onsite investigation, and related services. Applicants should use the current county fee schedule because system type and design flow affect the applicable fee.'),
        ],
    },
    {
        'county': 'Cochise',
        'authority': 'Cochise County Health and Social Services — Environmental Health Division',
        'contact': 'Cochise County Environmental Health Division, 1415 Melody Lane, Building G, Bisbee, AZ 85603; septic inspection line 520-432-9441. Sewage-disposal permit applications are processed through county Health Department offices.',
        'sources': [
            ('Cochise County — Septic Systems', 'https://www.cochise.az.gov/898/Septic-Systems'),
            ('Cochise County — Accessory Dwelling Units', 'https://www.cochise.az.gov/237/Accessory-Dwelling-Units'),
            ('Cochise County — Residential Projects', 'https://www.cochise.az.gov/868/Residential-Projects'),
        ],
        'sections': [
            ('Soil and site evaluation comes before the sewage-disposal permit', 'Cochise County states that the first step is to have the property evaluated to determine septic-system size and location. The soil and site evaluation must be completed before the applicant applies for the county sewage-disposal permit.'),
            ('The county specifies at least three deep test pits', 'Cochise County requires a state-certified evaluator to excavate at least three test pits: two in the proposed primary disposal area and one in the reserve disposal-field area. The county states that the pits are excavated to a depth of 12 feet so the evaluator can determine soil absorption capacity and identify limiting conditions.'),
            ('Qualified evaluators are specifically defined', 'Cochise County identifies qualified site and soil evaluators as Arizona registered professional engineers, registered professional geologists, registered sanitarians, or individuals holding training certification from a course recognized by ADEQ.'),
            ('Alternative systems follow the limiting conditions found onsite', 'When conditions such as inadequate soil, high groundwater, or impermeable layers prevent a conventional design, Cochise County directs the evaluator to recommend an alternative design. Depending on the system selected, the alternative-system application may be reviewed by the county Health Department or ADEQ.'),
            ('County septic inspections remain required even under reduced building-inspection paths', 'Cochise County states that its rural Owner-Builder Amendment can reduce or eliminate certain Building Safety inspections, but septic, well, zoning, floodplain, and other non-building approvals and inspections still apply. Septic inspections are therefore not waived by the owner-builder building option.'),
            ('Added dwelling units can trigger septic expansion or a new permitted system', 'Cochise County warns that most existing systems are designed only for the primary residence. Adding an accessory dwelling unit will likely require expansion of the existing septic system or installation of a new permitted system, and the county directs owners to contact Environmental Health early in planning.'),
        ],
    },
    {
        'county': 'Mohave',
        'authority': 'Mohave County Development Services — Environmental Quality / Waste Disposal, On-Site Septic Wastewater Disposal Program',
        'contact': 'Mohave County Development Services Environmental Quality; EQpermits@mohave.gov; 928-757-0903. The county provides permitting offices and online resources for septic applications and inspections.',
        'sources': [
            ('Mohave County — Septic & Well Permitting', 'https://www.mohave.gov/departments/development-services/environmental-qualitywaste-disposal/septic-well-permitting/'),
            ('Mohave County — Engineering Permits', 'https://www.mohave.gov/departments/development-services/environmental-qualitywaste-disposal/engineering-permits/'),
            ('Mohave County — Environmental Quality / Waste Disposal', 'https://www.mohave.gov/departments/development-services/environmental-qualitywaste-disposal/'),
        ],
        'sections': [
            ('Development Services performs the delegated septic permit sequence', 'Mohave County states that ADEQ delegates the environmental-program authority to Development Services. The county monitors site investigations, reviews applications and installation plans, issues Construction Authorizations, inspects newly installed systems, issues Discharge Authorizations, and monitors ownership transfers.'),
            ('Construction cannot start before the Construction Authorization is signed', 'Mohave County explicitly states that septic construction may not begin until the Construction Authorization has been signed by the applicant. Licensed contractors often handle permitting for owners, while owner-builders may submit the county application themselves.'),
            ('Site investigation supports both system selection and sizing', 'The county requires percolation and soil evaluation before system installation because the site investigation provides the information needed to select and size the system. Mohave County maintains an approved site-investigator list and requires site-investigation notification before the investigation.'),
            ('Alternative systems address documented limiting conditions', 'Mohave County explains that alternative systems are used when the site investigation finds limiting conditions such as high groundwater, high rock content, or soils that drain too quickly. The county publishes additional alternative-system requirements and an adjusted soil-absorption-rate chart.'),
            ('Some parcels have an additional 50-foot property-line buffer tied to water availability', 'Mohave County states that in areas where public water is not available, the septic system must maintain a 50-foot buffer to any property line unless the property owners execute an agreement that is notarized and recorded with the deed.'),
            ('County has separate alteration, abandonment, transfer, and larger-system paths', 'Mohave County publishes separate materials and fees for adding disposal area for increased flow, tank replacement, abandonment, transfer of ownership, alternative designs, and larger 4.23 systems. Its engineering-permit page requires stamped engineering construction plans for 4.23 onsite wastewater systems.'),
        ],
    },
]

az2_urls = []
for d in AZ2_COUNTIES:
    sources = [
        ('Arizona Department of Environmental Quality — Onsite Wastewater Treatment Facilities', AZ2_STATE),
        ('ADEQ — Delegation Agreements', AZ2_DELEGATION),
        ('ADEQ — Notice of Transfer and Inspection', AZ2_TRANSFER),
    ] + d['sources']
    sections = [
        ('Arizona county-delegation framework', 'ADEQ states that it has statewide authority for onsite wastewater treatment facilities and has delegated permitting authority to each of Arizona’s 15 counties. ADEQ rules continue to apply statewide, while delegated counties may impose separate or stricter local standards. Applicants should submit through the county where the property is located unless a specific system remains under direct ADEQ jurisdiction.'),
        ('Property transfer has a statewide inspection and notice process', 'Arizona requires an onsite-system inspection in connection with a property transfer and requires the buyer to submit the applicable Notice of Transfer within 15 calendar days after transfer. ADEQ identifies county-specific filing paths for delegated counties, so owners should use the current transfer instructions for the property location.')
    ] + d['sections']
    az2_urls.append(write_county_page('Arizona', 'arizona', d['county'], d['authority'], d['contact'], sections, sources, verified='August 30, 2026'))

# Rebuild the Arizona hub so the additional verified counties are discoverable without changing the shared page template.
az_links = []
for d in AZ_COUNTIES:
    az_links.append((d['county'], d['authority']))
for d in AZ2_COUNTIES:
    az_links.append((d['county'], d['authority']))
write_hub(
    'Arizona', 'arizona', sorted(az_links),
    'Arizona DEQ has statewide onsite-wastewater authority and delegates permitting functions to all 15 counties. These county guides are limited to jurisdictions where current government sources support both the local permitting authority and substantive local requirements.',
    'This verified Arizona set covers Maricopa, Pima, Yavapai, Coconino, Pinal, Cochise, and Mohave counties. Counties without independently validated local guidance remain clearly labeled lookup pages rather than speculative guides.'
)

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/arizona/'] + az2_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-30</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sitemap.write_text(sm.replace('</urlset>', entries + '</urlset>'), encoding='utf-8')

print(f'Arizona additional expansion complete: +{len(az2_urls)} verified county guides')
