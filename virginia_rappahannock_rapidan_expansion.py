# SepticScope Virginia expansion — Rappahannock-Rapidan Health District
# Official-source county pages validated against current VDH district guidance and Virginia Administrative Code.

VA_RR_ONSITE = 'https://www.vdh.virginia.gov/rappahannock-rapidan/onsite-wastewater2/'
VA_RR_LOCATIONS = 'https://www.vdh.virginia.gov/rappahannock-rapidan/office-locations/'
VA_RR_SERVICES = 'https://www.vdh.virginia.gov/rappahannock-rapidan/private-well-and-onsite-septic-services/'
VA_PRIVATE = 'https://www.vdh.virginia.gov/environmental-health/onsite-sewage-water-services-updated/have-you-considered-using-the-private-sector/'
VA_PERMIT = 'https://law.lis.virginia.gov/admincode/title12/agency5/chapter610/section240/'
VA_APPLY = 'https://law.lis.virginia.gov/admincode/title12/agency5/chapter610/section250/'
VA_SITE = 'https://law.lis.virginia.gov/admincode/title12/agency5/chapter610/section460/'
VA_EXPIRY = 'https://law.lis.virginia.gov/admincode/title12/agency5/chapter610/section300/'

RR_COUNTIES = {
    'Culpeper': ('540-829-7466', '640 Laurel Street, Culpeper, VA 22701-3993', 'CulpeperEH@vdh.virginia.gov'),
    'Fauquier': ('540-347-6363', '330 Hospital Drive, Warrenton, VA 20186', 'FauquierEH@vdh.virginia.gov'),
    'Madison': ('540-948-5481', '1480 N. Main Street, Suite A, Madison, VA 22727', 'MadisonEH@vdh.virginia.gov'),
    'Orange': ('540-672-1291', '450 N. Madison Rd., Orange, VA 22960', 'OrangeEH@vdh.virginia.gov'),
    'Rappahannock': ('540-675-3516', '338-A Gay Street, Washington, VA 22747', 'RappahannockCoEH@vdh.virginia.gov'),
}

va_urls = []
va_links = []
for county, (phone, address, email) in RR_COUNTIES.items():
    contact = (
        f'Virginia Department of Health, Rappahannock-Rapidan Health District — {html.escape(county)} County Environmental Health. '
        f'Phone {html.escape(phone)}; {html.escape(address)}; email {html.escape(email)}. '
        'VDH lists this county office for Environmental Health and onsite sewage records and permitting assistance.'
    )
    sections = [
        ('Construction permit before septic work',
         'Virginia regulation 12VAC5-610-240 prohibits construction, expansion, or modification of a sewage disposal system without a written construction permit. Under 12VAC5-610-250, requests for a sewage-disposal construction permit are directed initially to the district or local health department.'),
        ('Licensed private-sector supporting work is required',
         'Rappahannock-Rapidan Health District states that applications for onsite sewage systems must be accompanied by supporting work from a private-sector consultant properly licensed through Virginia DPOR. VDH may provide evaluation and design services only for owners who submit the applicable petition and meet the published means-testing or hardship criteria.'),
        ('Application package and site sketch',
         'The district instructs applicants to submit the completed application, applicable fee, property plat, and a site sketch to the local health department after obtaining the required licensed-consultant supporting work. The sketch should identify property lines, existing or proposed buildings, and the desired sewage-system and well locations. State regulation also calls for site information showing relevant structures, utilities, nearby sewage systems, water bodies, drainage features, wells, cisterns, and springs needed for evaluation.'),
        ('Permit expiration and revalidation',
         'Under 12VAC5-610-300, a sewage-disposal construction permit becomes null and void when site or permit conditions materially change or more than 18 months pass from issuance. The regulation provides a revalidation process when construction has not commenced and the qualifying site conditions remain the same.'),
        ('Existing septic permit records',
         'The district maintains onsite sewage records through its county health departments. Its current onsite-wastewater page directs property-record requests through the district FOIA portal and asks requesters to provide details such as the property address, establishment name, permit number, or approximate dates so records can be located.'),
    ]
    if county == 'Fauquier':
        sections.append(('Fauquier contractor licensing note',
                         'Rappahannock-Rapidan Health District specifically notes that contractors working in Fauquier County are required to hold both a Virginia state license and the applicable local Fauquier license. Verify both credentials before contracting regulated onsite work.'))
    sources = [
        ('Rappahannock-Rapidan Health District — Onsite Wastewater', VA_RR_ONSITE),
        ('Rappahannock-Rapidan Health District — office locations and Environmental Health contacts', VA_RR_LOCATIONS),
        ('Rappahannock-Rapidan Health District — private well and onsite septic services', VA_RR_SERVICES),
        ('Virginia Department of Health — private-sector onsite sewage application requirements', VA_PRIVATE),
        ('Virginia Administrative Code 12VAC5-610-240 — permits', VA_PERMIT),
        ('Virginia Administrative Code 12VAC5-610-250 — permit application procedure', VA_APPLY),
        ('Virginia Administrative Code 12VAC5-610-460 — site and structure identification', VA_SITE),
        ('Virginia Administrative Code 12VAC5-610-300 — permit voidance and revalidation', VA_EXPIRY),
    ]
    url = write_county_page(
        'Virginia', 'virginia', county,
        'Virginia Department of Health (VDH), Rappahannock-Rapidan Health District Environmental Health',
        contact, sections, sources, verified='August 29, 2026'
    )
    va_urls.append(url)
    va_links.append((county, 'Rappahannock-Rapidan Health District Environmental Health'))

write_hub(
    'Virginia', 'virginia', sorted(va_links),
    'Virginia onsite sewage construction permits are administered through VDH district and local health departments under the Commonwealth’s Sewage Handling and Disposal Regulations. This batch covers the five counties served by the Rappahannock-Rapidan Health District.',
    'Included counties: Culpeper, Fauquier, Madison, Orange, and Rappahannock. The district publishes county-specific Environmental Health contacts, a current onsite permit workflow, and septic-record request guidance. Additional Virginia counties will be added only after their local VDH authority and procedures are independently validated.'
)

county_index = OUTPUT / 'counties' / 'index.html'
if county_index.exists():
    text = county_index.read_text(encoding='utf-8')
    if '/counties/virginia/' not in text:
        promo = '<section><h2>Virginia</h2><p><a href="/counties/virginia/">Browse 5 verified Virginia county septic guides →</a></p></section>'
        text = text.replace('</main>', promo + '</main>', 1) if '</main>' in text else text.replace('</body>', promo + '</body>', 1)
        county_index.write_text(text, encoding='utf-8')

sitemap = OUTPUT / 'sitemap.xml'
new_urls = ['https://septicscope.com/counties/virginia/'] + va_urls
if sitemap.exists():
    sm = sitemap.read_text(encoding='utf-8')
else:
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
entries = ''.join(f'<url><loc>{u}</loc><lastmod>2026-08-29</lastmod></url>' for u in new_urls if u not in sm)
if entries:
    sm = sm.replace('</urlset>', entries + '</urlset>')
    sitemap.write_text(sm, encoding='utf-8')

print(f'Virginia Rappahannock-Rapidan expansion complete: +{len(va_urls)} verified county guides')
exec((ROOT / 'arkansas_expansion.py').read_text(encoding='utf-8'), globals())
