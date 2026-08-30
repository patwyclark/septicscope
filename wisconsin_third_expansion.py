# SepticScope Wisconsin third expansion — verified county POWTS guidance from official sources.
# Verified from Wisconsin DSPS and official Kenosha, Jefferson, and Sauk County sources on 2026-08-30.

WI_STATE_POWTS = 'https://dsps.wi.gov/Pages/Programs/POWTS/Default.aspx'
WI_THIRD_COUNTIES = {
    'Kenosha': {
        'authority': 'Kenosha County Department of Planning and Development — Sanitary / POWTS Program',
        'contact': 'Kenosha County Planning and Development administers sanitary permits county-wide. The county online permitting portal lists sanitary permit applications for septic systems across Kenosha County.',
        'sources': [
            ('Kenosha County — Sanitary Forms List', 'https://www.kenoshacountywi.gov/2495/Sanitary-Forms-List'),
            ('Kenosha County — Planning & Development Online Permit Portal', 'https://permitting.kenoshacountywi.gov/eTRAKiT/default.aspx'),
            ('Kenosha County — Sanitary Board of Review', 'https://www.kenoshacountywi.gov/821/Sanitary-Board-of-Review'),
        ],
        'sections': [
            ('County-wide sanitary permit administration', 'Kenosha County’s permitting portal identifies the county Planning and Development program as the sanitary-permit contact for septic systems county-wide. Applicants should use the county sanitary process even where zoning or building permits are handled by a municipality.'),
            ('A licensed master plumber applies for the sanitary permit', 'Kenosha County states that only a Wisconsin Licensed Master Plumber or Master Plumber Restricted Service may apply for a sanitary permit on the owner’s behalf. The county directs the licensed professional to submit through its Planning and Development online permitting portal.'),
            ('County publishes separate review and maintenance documents', 'The county sanitary forms page distinguishes the State Sanitary Permit application from county-only permit forms and publishes separate documents for holding-tank review, existing-POWTS evaluation, soil-test review for land divisions, POWTS abandonment, and maintenance reporting.'),
            ('Some maintenance agreements must be recorded', 'Kenosha County distinguishes non-recordable maintenance documents from recordable agreements for systems or components requiring service intervals shorter than 12 months. The county also publishes recordable notices for holding tanks, per-capita sizing, systems serving more than one building, and pretreatment-unit maintenance.'),
            ('County variance path is formalized', 'Kenosha County’s Sanitary Board of Review hears variance requests under the county Sanitary Code and Private Sewage System Ordinance. Owners with sites that cannot meet standard requirements should use that formal county process rather than assume a variance is available.'),
        ],
    },
    'Jefferson': {
        'authority': 'Jefferson County Planning and Zoning Department — POWTS / Sanitary Program',
        'contact': 'Jefferson County Planning and Zoning Department, 311 S. Center Ave., Room C1040, Jefferson, WI 53549; phone 920-674-7130; zoning@jeffersoncountywi.gov.',
        'sources': [
            ('Jefferson County — current POWTS ordinance in 2026 Planning & Zoning packet', 'https://apps.jeffersoncountywi.gov/Supplemental/2026/02232026/P%26Z%20Committee%20Packet.pdf'),
            ('Jefferson County — POWTS Ordinance', 'https://apps.jeffersoncountywi.gov/Handout/2021/01112021/POWTS%20Ordinance.pdf'),
            ('Jefferson County — Land Records / sanitary permit search', 'https://apps.jeffersoncountywi.gov/jc/'),
        ],
        'sections': [
            ('Sanitary permit before installation, replacement, or modification', 'Jefferson County’s POWTS ordinance requires a sanitary permit before a POWTS or any regulated part is installed, replaced, or modified. The ordinance identifies limited maintenance exceptions such as adding manhole risers or replacing covers, baffles, or pumps.'),
            ('New construction must identify both initial and replacement areas', 'Jefferson County requires a primary and replacement POWTS area for new construction other than holding-tank situations. The county ordinance also generally prohibits holding tanks for new construction, subject to its stated exception process.'),
            ('Soil evaluation has county-specific documentation rules', 'The county requires soil and site evaluations under Wisconsin code with at least three soil profile evaluations unless more are needed to delineate the site. County verification may be required, and the ordinance calls for county onsite verification for soils other than those supporting an in-ground or conventional soil absorption system unless waived by the county.'),
            ('Certain sewer-service and growth areas need jurisdiction approval first', 'Jefferson County’s current ordinance states that proposed POWTS in a sanitary district, city or village, a 15-year growth area, or an urban or limited urban service area require approval from that jurisdiction before the county sanitary permit is issued.'),
            ('Public sewer availability can require abandonment', 'When approved public sewer becomes available to a structure served by POWTS, Jefferson County’s ordinance requires disconnection within one year and connection to public sewer. The disconnected POWTS must then be abandoned under applicable code, with an abandonment report filed with Planning and Zoning within 30 days.'),
        ],
    },
    'Sauk': {
        'authority': 'Sauk County Land Resources and Environment Department — Planning & Zoning / Sanitary Program',
        'contact': 'Sauk County Land Resources and Environment, 505 Broadway, Baraboo, WI 53913; phone 608-355-3245. Land-use and sanitary permits are submitted through the county OpenGov portal.',
        'sources': [
            ('Sauk County — Land Resources and Environment', 'https://www.co.sauk.wi.us/cpz'),
            ('Sauk County — Permit Applications, Forms, Instructions and Affidavits', 'https://www.co.sauk.wi.us/cpz/permit-applications-forms-instructions-and-affidavits'),
            ('Sauk County — New Residence with Private Septic Permit Instructions', 'https://www.co.sauk.wi.us/planningandzoning/new-residence-private-septic-permit-instructions'),
        ],
        'sections': [
            ('County land-use and sanitary permits are online', 'Sauk County Land Resources and Environment states that land-use and sanitary permits are submitted online through its OpenGov portal. The department is the county contact for the combined land-use/sanitary permitting process.'),
            ('New residences require a full septic submittal package', 'For a new residence with private septic, Sauk County requires the permit application and plot plan plus a Septic Maintenance Agreement, a POWTS sanitary application signed by the plumber/installer, an original and copy of the soil test, and an original and copy of state-approved septic plans.'),
            ('Land-use and septic review are coordinated', 'The county’s new-residence instructions integrate the sanitary submittal with the land-use permit. Applicants should resolve the septic design and sanitary documentation before assuming the building or land-use portion can be approved independently.'),
            ('County publishes current permit activity', 'Sauk County publishes lists of issued land-use and sanitary permits that include new septic systems, reconnections, and related work. This confirms active county administration of the sanitary program and provides a public reference for recent permit activity.'),
        ],
    },
}

for county, data in WI_THIRD_COUNTIES.items():
    sections = [
        ('Wisconsin POWTS framework', 'Wisconsin Department of Safety and Professional Services states that counties have primary responsibility to inspect Private Onsite Wastewater Treatment Systems except for state-owned projects. DSPS supplies the statewide sanitary-permit, soil/site-evaluation, inspection, plan-review, and professional-licensing framework used with county administration.'),
        ('Use county requirements together with Wisconsin approvals', 'County sanitary permitting does not replace Wisconsin POWTS technical requirements or any state plan review that applies to the proposed system. System type, design flow, sewer availability, site conditions, additions, and repairs can change the required review path, so applicants should verify the current county instructions before work begins.'),
    ] + data['sections']
    sources = [('Wisconsin DSPS — Private Onsite Wastewater Treatment Systems', WI_STATE_POWTS)] + data['sources']
    write_county_page('Wisconsin', 'wisconsin', county, data['authority'], data['contact'], sections, sources, verified='August 30, 2026')

print(f'Wisconsin third expansion complete: +{len(WI_THIRD_COUNTIES)} verified county guides')
