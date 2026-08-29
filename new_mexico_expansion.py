# SepticScope New Mexico expansion — official-source county pages
# Executed after prior state expansions are built.

NM_REG = 'https://www.env.nm.gov/wp-content/uploads/sites/14/2017/08/2073NMACIntegratedapprovedAL-2014.pdf'
NM_APPLICATION = 'https://www.env.nm.gov/septic/wp-content/uploads/sites/14/2017/08/LW-Application-for-Liquid-Waste-Permit-or-Registration-Form-LW-401E-210127-1.pdf'
NM_FIELD_OFFICES = 'https://www.env.nm.gov/wp-content/uploads/2025/09/Liquid-Waste-Permit-Search-Request-20210104-Auto-Fill-Pull-Down.pdf'
NM_PERMIT_FINDER = 'https://lwop.waste.web.env.nm.gov/wwtspf/'
NM_PERMIT_FINDER_HELP = 'https://lwop.waste.web.env.nm.gov/wwtspf/instructions'

# Current NMED permit-search form identifies these county-located Environmental Health Bureau
# field offices. Bernalillo County is intentionally excluded because NMED's permit finder states
# that Bernalillo County is outside NMED jurisdiction for this program.
NM_COUNTIES = {
    'Chaves': ('Roswell', '575-624-6046', '1914 W. Second Street, Roswell, NM 88201'),
    'Cibola': ('Grants', '505-209-4042', '708 Uranium Ave., Grants, NM 87020'),
    'Colfax': ('Raton', '575-445-3621', '1277 A South Second Street, Raton, NM 87740'),
    'Curry': ('Clovis', '575-762-3728', '100 E Manana Blvd. Unit 3, Clovis, NM 88101'),
    'Doña Ana': ('Las Cruces', '575-288-2050', '2301 Entrada del Sol, Las Cruces, NM 88001'),
    'Eddy': ('Carlsbad', '575-885-9023', '406 N. Guadalupe Ste C, Carlsbad, NM 88220'),
    'Grant': ('Silver City', '575-388-1934', '3082 32nd St. Bypass, Suite D, Silver City, NM 88061'),
    'Lea': ('Hobbs', '575-397-6910', '2120 N Alto, Hobbs, NM 88240'),
    'Lincoln': ('Ruidoso', '575-258-3272', '1216 Mechem Dr., Bldg. 2, Ruidoso, NM 88345'),
    'Luna': ('Deming', '575-546-1464', '405 E. Florida, Deming, NM 88030'),
    'McKinley': ('Gallup', '505-722-4160', '911 Metro Avenue, Gallup, NM 87301'),
    'Otero': ('Alamogordo', '575-437-7115', '811 E. First St., Suite D, Alamogordo, NM 88310'),
    'Quay': ('Tucumcari', '575-461-1671', '113 West Center, Tucumcari, NM 88401'),
    'Rio Arriba': ('Española', '505-753-7256', '712 La Joya Street, Española, NM 87532'),
    'San Juan': ('Farmington', '505-566-9741', '3400 Messina Dr, Ste 5000, Farmington, NM 87402'),
    'San Miguel': ('Las Vegas', '505-454-2800', '2538 Ridge Runner Road, Las Vegas, NM 87701'),
    'Sandoval': ('Rio Rancho', '505-771-5980', '4359 Jager Dr. NE, Ste. B, Rio Rancho, NM 87144'),
    'Santa Fe': ('Santa Fe', '505-827-1840', '2540 Camino Edward Ortiz, Santa Fe, NM 87507'),
    'Taos': ('Taos', '575-758-8808', '145 Roy Road, Ste. B, Taos, NM 87571'),
    'Valencia': ('Los Lunas', '505-841-5277', '475 Courthouse Rd, SE Suite B, Los Lunas, NM 87031'),
}

nm_urls = []
nm_links = []
for county, (office, phone, address) in NM_COUNTIES.items():
    contact = (
        f'New Mexico Environment Department Environmental Health Bureau — {html.escape(office)} field office: '
        f'{html.escape(phone)}; {html.escape(address)}. NMED’s current Liquid Waste Permit Search Request form '
        f'lists this field office in {html.escape(county)} County.'
    )
    sections = [
        ('NMED is the permitting authority',
         'New Mexico’s Liquid Waste Disposal and Treatment Regulations are administered by the New Mexico Environment Department for these counties. Bernalillo County follows a separate county-administered program, and sovereign Tribal lands are not governed by the state Liquid Waste Regulations; this guide therefore should not be used for Tribal lands.'),
        ('Permit before a new system or modification',
         '20.7.3.401 NMAC states that a person must obtain a department permit before installing a new on-site liquid waste system or modifying an existing one. The rule also requires an on-site liquid waste permit before constructing or modifying a residential or commercial unit on a lot where such a system is required.'),
        ('Application requires property, water and system details',
         'NMED’s Liquid Waste Permit or Registration application requests the legal owner, physical system location, county, lot size, subdivision or legal-description information, water-supply information, existing liquid-waste permit numbers, installer information and a separate treatment/disposal design page for each proposed system on the lot.'),
        ('Site plan and design information matter',
         'The NMED application requires existing permitted systems to be identified and new, modified or unpermitted systems to be clearly shown. Its design section addresses wastewater design flow, hydrology or limiting-layer depths, soil description, treatment units and disposal-field design, so site conditions can materially change what is approvable.'),
        ('Installer and homeowner rules',
         'State regulation generally requires a valid and appropriate New Mexico Construction Industries Division contractor license for installation or modification. A homeowner exception exists for a qualified homeowner installing or modifying a permitted conventional system serving the homeowner’s personal residence; the regulations include qualification requirements for that exception.'),
        ('Final inspection and property transfers',
         'NMED’s permit application includes final-inspection approval before the system is treated as approved. State regulation also contains a property-transfer evaluation process for existing onsite systems; an approved final inspection or qualifying transfer evaluation completed within 180 days of transfer can satisfy the timing exception described in 20.7.3.902 NMAC.'),
        ('Finding an older permit',
         'NMED provides an online Wastewater Treatment System Permit Finder for older records. The agency warns that the public finder is only current through January 27, 2017; for newer records or an unsuccessful search, use the local Environmental Health Bureau field office and provide a legal description or proof of ownership when possible.')
    ]
    sources = [
        ('New Mexico Liquid Waste Disposal and Treatment Regulations — 20.7.3 NMAC', NM_REG),
        ('NMED Liquid Waste Permit or Registration application', NM_APPLICATION),
        ('NMED Liquid Waste Permit Search Request — current field-office list', NM_FIELD_OFFICES),
        ('NMED Wastewater Treatment System Permit Finder', NM_PERMIT_FINDER),
        ('NMED Permit Finder instructions and Bernalillo County jurisdiction notice', NM_PERMIT_FINDER_HELP),
    ]
    url = write_county_page(
        'New Mexico', 'new-mexico', county,
        'New Mexico Environment Department (NMED), Environmental Health Bureau, Liquid Waste Program',
        contact, sections, sources, verified='August 28, 2026'
    )
    nm_urls.append(url)
    nm_links.append((county, office))

write_hub(
    'New Mexico', 'new-mexico',
    [(c, f'NMED {o} field office') for c, o in sorted(nm_links)],
    'New Mexico generally regulates onsite septic systems through the Environment Department’s Environmental Health Bureau and Liquid Waste Program. This batch covers counties with a current NMED field office identified directly on the department’s Liquid Waste Permit Search Request form.',
    'Bernalillo County is intentionally excluded because NMED states that the county is outside NMED jurisdiction for this program. Sovereign Tribal lands are also outside the state Liquid Waste Regulations. Additional New Mexico counties will be added only when the appropriate NMED field-office routing can be supported from official sources.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    if '/counties/new-mexico/' not in text:
        promo = '<section><h2>New Mexico</h2><p><a href="/counties/new-mexico/">Browse 20 verified New Mexico county septic guides →</a></p></section>'
        text = text.replace('</main>', promo + '</main>', 1) if '</main>' in text else text.replace('</body>', promo + '</body>', 1)
        county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/new-mexico/'] + nm_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-28</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'New Mexico expansion complete: +{len(nm_urls)} verified county guides')
exec((ROOT / 'idaho_expansion.py').read_text(encoding='utf-8'), globals())
