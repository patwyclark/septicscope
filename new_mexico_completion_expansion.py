# SepticScope New Mexico completion — all remaining counties.
# Official sources reviewed September 1, 2026.
#
# New Mexico generally administers onsite liquid-waste systems through NMED.
# NMED's own permit finder identifies Bernalillo County as outside NMED
# jurisdiction, so Bernalillo receives a separately scoped county page.
import html

NM_CURRENT_RULE = 'https://www.srca.nm.gov/parts/title20/20.007.0003.html'
NM_CONTACT = 'https://www.env.nm.gov/contact-us/'
NM_ONLINE_PERMITS = 'https://lwop.waste.web.env.nm.gov/'
NM_LIQUID_WASTE_GIS = 'https://mercator.env.nm.gov/server/rest/services/ehb/onsite_wastewater_compliance/MapServer/0'
BERNCO_PORTAL = 'https://aca-prod.accela.com/BERNCO/Welcome.aspx'
BERNCO_PERMIT_MAP = 'https://pdsgismaps.bernco.gov/server/rest/services/BERNCO/Accela_Permits/MapServer'

# These counties were not included in the first NMED field-office batch. The
# official sources reviewed for this completion batch did not identify separate
# county-run septic programs for them. Their pages therefore use NMED's verified
# statewide requirements and clearly disclose that the specific field-office
# routing must be confirmed with the department before filing.
NM_NMED_COMPLETION_COUNTIES = (
    'Catron',
    'De Baca',
    'Guadalupe',
    'Harding',
    'Hidalgo',
    'Los Alamos',
    'Mora',
    'Roosevelt',
    'Sierra',
    'Socorro',
    'Torrance',
    'Union',
)

completion_urls = []
completion_links = []

for county in NM_NMED_COMPLETION_COUNTIES:
    safe_county = html.escape(county)
    contact = (
        'New Mexico Environment Department main office — 505-827-2855 or '
        '800-219-6157; Harold Runnels Building, 1190 St. Francis Drive, '
        f'Suite N4050, Santa Fe, NM 87505. Ask for the Environmental Health Bureau '
        f'Liquid Waste field office serving {safe_county} County. SepticScope did not '
        'find a current public NMED source assigning this county to a named field '
        'office, so confirm the correct office before submitting an application or '
        'requesting an inspection.'
    )
    sections = [
        (
            'NMED administers the onsite liquid-waste program',
            f'New Mexico rule 20.7.3 NMAC applies to onsite liquid-waste systems receiving 5,000 gallons or less per day. NMED’s official permit-finder instructions identify Bernalillo County as outside NMED jurisdiction; the official sources reviewed for this page did not identify a separate county-administered program for {safe_county} County. Start with NMED and have the department confirm the field office serving the parcel. Sovereign Tribal lands can follow a different authority and should be confirmed separately.'
        ),
        (
            'Permit before installation or modification',
            '20.7.3 NMAC requires a department permit before installing a new onsite liquid-waste system or modifying an existing one. The rule also requires the applicable liquid-waste permit before constructing or modifying a residential or commercial unit on a lot that will rely on an onsite system. Do not begin regulated work based only on an application submission.'
        ),
        (
            'Application and site information',
            'NMED’s Liquid Waste Permit or Registration application requests the owner and property location, county and legal-description information, water supply, existing permit numbers, installer information, design flow, treatment components, disposal-field information, soil conditions and a site plan. Site limitations can change the permitted design, so use the current form and follow any field-office instructions for test holes, soil documentation or engineered design.'
        ),
        (
            'Installer and homeowner requirements',
            'New Mexico generally requires installation or modification by a contractor holding the appropriate Construction Industries Division license. The regulation contains a limited homeowner exception for a qualified owner working on a permitted conventional system serving the owner’s personal residence. Confirm eligibility and permit conditions with NMED before relying on that exception.'
        ),
        (
            'Inspection and final approval',
            'The permit process can require construction inspections at specified stages. The person performing the work must coordinate inspection timing with the department and must not treat an uninspected or unapproved installation as complete. Keep the final approval, design, photographs when accepted by the department, and any operating or maintenance documents with the property records.'
        ),
        (
            'Maintenance and property transfers',
            'System owners are responsible for operating and maintaining the system under the permit, manufacturer or designer instructions, and applicable rule. New Mexico also has evaluation requirements at the time of certain property transfers. Confirm the current transfer documentation, timing and evaluator requirements before a sale rather than assuming that ordinary pumping is the required evaluation.'
        ),
        (
            'Permit records and field-office routing',
            'NMED provides a public Wastewater Treatment System Permit Finder, but the agency states that its online information is only current through January 27, 2017. For newer records, unsuccessful searches or project-specific questions, contact the Environmental Health Bureau field office serving the property and have the legal description or proof of ownership available. The NMED GIS layer is another planning aid, but it is not a substitute for the official permit file.'
        ),
        (
            'County-specific information not confirmed',
            f'SepticScope did not locate a current official {safe_county} County page publishing separate septic fees, forms, setbacks or a county-level office assignment. The statewide NMED requirements above are therefore presented with a direct routing warning. Confirm the responsible office, current fees, site-evaluation requirements, inspection stages and any locally applicable land-use conditions before proceeding.'
        ),
    ]
    sources = [
        ('New Mexico Administrative Code — 20.7.3 Liquid Waste Disposal and Treatment', NM_CURRENT_RULE),
        ('NMED Liquid Waste Permit or Registration application', NM_APPLICATION),
        ('NMED Liquid Waste Online Permits', NM_ONLINE_PERMITS),
        ('NMED Wastewater Treatment System Permit Finder', NM_PERMIT_FINDER),
        ('NMED Permit Finder instructions and jurisdiction notice', NM_PERMIT_FINDER_HELP),
        ('NMED contact and field-office routing', NM_CONTACT),
        ('NMED Onsite Wastewater Bureau — Liquid Waste Permits GIS layer', NM_LIQUID_WASTE_GIS),
    ]
    url = write_county_page(
        'New Mexico',
        'new-mexico',
        county,
        'New Mexico Environment Department (NMED), Environmental Health Bureau, Liquid Waste Program — field office assignment must be confirmed',
        contact,
        sections,
        sources,
        verified='September 1, 2026',
    )
    completion_urls.append(url)
    completion_links.append((county, 'NMED field-office routing must be confirmed'))

# Bernalillo County is deliberately separate because the NMED permit finder says
# the county is outside NMED jurisdiction and directs users to the county Health
# Department. The county portal also tells applicants to verify parcel jurisdiction.
bern_contact = (
    'NMED’s official Wastewater Treatment System Permit Finder directs Bernalillo '
    'County users to the Bernalillo County Health Department at 505-314-0310. '
    'Bernalillo County’s Accela portal provides permit and inspection assistance at '
    '505-314-0351 or permits@bernco.gov and states that its online county services '
    'apply to the unincorporated area. Verify the parcel’s jurisdiction in the county '
    'portal before filing.'
)
bern_sections = [
    (
        'Bernalillo County is outside the NMED liquid-waste program',
        'NMED’s official permit-finder instructions expressly state that Bernalillo County is outside New Mexico Environment Department jurisdiction for this program and that NMED’s county data are incomplete. The instructions direct users to the Bernalillo County Health Department for more complete information. Do not route a Bernalillo County septic project through an NMED field office without first confirming jurisdiction.'
    ),
    (
        'Confirm the parcel is within county jurisdiction',
        'Bernalillo County’s Accela portal states that its permit, inspection and code-enforcement information is for the unincorporated area of Bernalillo County and directs applicants to verify county jurisdiction before applying. Confirm the property location and responsible government before paying a fee or selecting a permit type.'
    ),
    (
        'Use the county portal for current applications and records',
        'The Accela portal includes Health searches and applications, inspection scheduling and public record lookup. Use the portal and county permit staff to identify the correct septic or environmental-health process, current application materials, inspections, fees and records available for the property.'
    ),
    (
        'County-issued permit data are available as a mapping aid',
        'Bernalillo County publishes an official Accela permit map service describing county-issued permits in the unincorporated area. The map can help with preliminary research, but it is not a substitute for the complete permit file or a written determination from county staff.'
    ),
    (
        'Rules, forms and technical requirements require county confirmation',
        'The current public sources reviewed for this page did not provide a single county webpage that fully states new-system, repair, replacement, soil-evaluation, setback, inspection and fee requirements. Ask county staff to confirm each requirement for the parcel and proposed work. Do not apply NMED field-office instructions to the project merely because they apply elsewhere in New Mexico.'
    ),
    (
        'Existing records and property transfers',
        'Because NMED says its Bernalillo County permit data are incomplete, use the county Health Department and Accela record-search functions for existing permits and inspections. Before a property transfer, ask the county which inspection or evaluation documentation is required and whether the property is served by an onsite system, public sewer or another jurisdiction.'
    ),
]
bern_sources = [
    ('NMED Permit Finder instructions — Bernalillo County jurisdiction notice', NM_PERMIT_FINDER_HELP),
    ('Bernalillo County Accela Citizen Access — permits, inspections and Health records', BERNCO_PORTAL),
    ('Bernalillo County Accela permits map service', BERNCO_PERMIT_MAP),
    ('New Mexico Administrative Code — 20.7.3 Liquid Waste Disposal and Treatment', NM_CURRENT_RULE),
]
bern_url = write_county_page(
    'New Mexico',
    'new-mexico',
    'Bernalillo',
    'Bernalillo County Health Department / county environmental-health permitting program — confirm parcel jurisdiction',
    bern_contact,
    bern_sections,
    bern_sources,
    verified='September 1, 2026',
)
completion_urls.append(bern_url)
completion_links.append(('Bernalillo', 'Bernalillo County Health Department; verify parcel jurisdiction'))

all_nm_links = list(nm_links) + completion_links
write_hub(
    'New Mexico',
    'new-mexico',
    sorted(all_nm_links),
    'All 33 New Mexico counties now have source-checked SepticScope guides. NMED administers the statewide liquid-waste program in most counties, while NMED directs Bernalillo County users to the county Health Department.',
    'The completed county set distinguishes NMED-administered counties from Bernalillo County and clearly flags counties where a current public NMED source did not identify the named field office. These guides do not determine jurisdiction on sovereign Tribal lands; confirm the responsible Tribal authority for those properties.',
)

sitemap = OUTPUT / 'sitemap.xml'
new_urls = completion_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(
    f'<url><loc>{url}</loc><lastmod>2026-09-01</lastmod></url>'
    for url in new_urls
    if url not in sm
)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(
    'New Mexico county completion: '
    f'+{len(completion_urls)} verified county guides; all 33 counties covered'
)
exec((ROOT / 'idaho_expansion.py').read_text(encoding='utf-8'), globals())
