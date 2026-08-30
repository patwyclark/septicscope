# SepticScope Missouri expansion — verified OWTS guidance from official state and county sources.
# Verified from Missouri DHSS and official St. Charles, Greene, Clay, and Platte County sources on 2026-08-30.

MO_STATE_OWTS = 'https://health.mo.gov/business-professionals/onsite-wastewater-treatment/'
MO_STATE_PERMITS = 'https://health.mo.gov/business-professionals/onsite-wastewater-treatment/owts-construction-permit-process'

MO_COUNTIES = {
    'St. Charles': {
        'authority': 'St. Charles County Division of Building and Code Enforcement — Onsite Wastewater Treatment Systems',
        'contact': 'St. Charles County Building and Code Enforcement, 201 N. Second St., Suite 412, St. Charles, MO 63301; phone 636-949-7345. County OWTS permitting applies in unincorporated St. Charles County and municipalities that contract with the county; use the county Permit Lookup Tool to confirm jurisdiction.',
        'sources': [
            ('St. Charles County — Onsite Wastewater Treatment Systems', 'https://sccmo.org/2172/Onsite-Wastewater-Treatment-Systems-OWTS'),
            ('St. Charles County — OWTS Permitting and Inspection', 'https://www.sccmo.org/2175/OWTS-Permitting-and-Inspection'),
            ('St. Charles County — Building Division Fees', 'https://www.sccmo.org/DocumentCenter/View/4836'),
        ],
        'sections': [
            ('Confirm county jurisdiction before applying', 'St. Charles County regulates onsite wastewater systems in unincorporated St. Charles County and in municipalities that contract with the county. Because incorporated areas can have a different permitting authority, the county directs applicants to its Permit Lookup Tool before starting the process.'),
            ('Permits cover installation, alteration, expansion, and repair', 'The county states that an OWTS permit is required for installation, alteration, expansion, or repair. It lists limited exceptions for changing or cleaning filters, adjusting head pressures, and replacing pumps, aerators, or blowers with like equipment.'),
            ('County applies its own private sewage disposal code', 'St. Charles County Building and Code Enforcement enforces the county Private Sewage Disposal Code for onsite wastewater systems, along with the county residential code provisions that apply to associated residential plumbing.'),
            ('County publishes dedicated septic permit fees', 'St. Charles County publishes separate residential and commercial onsite-wastewater permit fees in its Building Division fee schedule. Applicants should verify the current schedule when applying because local fees can change independently of Missouri state program fees.'),
        ],
    },
    'Greene': {
        'authority': 'Greene County Resource Management — Environmental Division / Building Regulations',
        'contact': 'Greene County Environmental Division, 940 N. Boonville Ave., Room 315, Springfield, MO 65802; phone 417-868-4147. Building Regulations in Room 305 issues the permit for projects within county jurisdiction.',
        'sources': [
            ('Greene County — Environmental Division / On-Site Wastewater Systems', 'https://greenecountymo.gov/resource_management/environmental/'),
            ('Greene County — Building Regulations', 'https://greenecountymo.gov/resource_management/building_regulations/'),
            ('Greene County — Building Applications', 'https://greenecountymo.gov/resource_management/building_regulations/application.php'),
        ],
        'sections': [
            ('County permit required for new systems and repairs', 'Greene County states that a permit is required to install a new onsite wastewater system and to repair or replace an existing system. Permits are obtained through Building Regulations, while the Environmental Division administers the county onsite-wastewater regulations and performs environmental review and field inspections.'),
            ('New and replacement permits require a soil-based site evaluation', 'For construction, repair, or replacement, Greene County requires a site-evaluation form and county soils report prepared by a qualified soil scientist, together with a site plan and system design prepared by an eligible qualified professional.'),
            ('Commercial and mechanical systems require a professional engineer', 'Greene County specifically states that all commercial, non-residential, or mechanical onsite wastewater systems must be designed by a Professional Engineer.'),
            ('Installers need both county and Missouri credentials', 'Greene County requires onsite wastewater installers to be currently certified with Greene County and registered with the Missouri Department of Health and Senior Services. The county maintains contact information for county-certified installers.'),
            ('Permit continuity matters during construction', 'Greene County Building Regulations states that permits generally become invalid if authorized work is not started within six months or if an inspection is not conducted every six months. Applicants should confirm how that rule applies to the specific wastewater permit before relying on an older approval.'),
        ],
    },
    'Clay': {
        'authority': 'Clay County Public Health Center — Environmental Health Protection / Onsite Sewage Program',
        'contact': 'Clay County Public Health Center, 800 Haines Drive, Liberty, MO 64068; Environmental Health phone 816-595-4350.',
        'sources': [
            ('Clay County Public Health Center — Onsite Sewage', 'https://clayhealth.com/154/Onsite-Sewage'),
            ('Clay County Public Health Center — Environmental Health', 'https://www.clayhealth.com/148/Environmental-Health'),
            ('Clay County Public Health Center — Contact Us', 'https://www.clayhealth.com/313/Contact-Us'),
        ],
        'sections': [
            ('Environmental Health permits and inspects onsite sewage systems', 'Clay County Public Health Center states that its Environmental Health program permits and inspects onsite sewage treatment and disposal systems under the program threshold published by the county.'),
            ('County review includes more than issuing a permit', 'The Clay County program issues construction and repair permits, conducts construction inspections, performs site approvals, reviews plans, and investigates complaints. Those steps make the county program the appropriate starting point for both new systems and regulated repairs.'),
            ('Use the county construction application and site-approval process', 'Clay County publishes separate links for a septic construction application and a site-approval application, along with county individual sewage-disposal rules and a list of Missouri registered onsite professionals. Applicants should resolve site approval and required professional involvement before construction.'),
            ('Existing-system information is available through Environmental Health', 'Clay County directs owners seeking information about an existing onsite system to Environmental Health. That record check can be useful before additions, repairs, replacement planning, or property due diligence.'),
        ],
    },
    'Platte': {
        'authority': 'Platte County Health Department — Environmental Health Sewage Program',
        'contact': 'Platte County Health Department Environmental Health administers the sewage program for unincorporated Platte County. Applicants should use the department permit or permit-exemption process before installation.',
        'sources': [
            ('Platte County Health Department — Sewage Program', 'https://www.plattecountyhealthdept.com/environmental-health/page/sewage-program'),
        ],
        'sections': [
            ('Permit required before installation in unincorporated Platte County', 'Platte County states that before an onsite wastewater treatment system is installed in unincorporated Platte County, the homeowner is responsible for obtaining a permit from the Health Department.'),
            ('County also determines permit exemptions', 'Environmental Health issues both sewage permits and permit exemptions. Owners should obtain an exemption determination from the county rather than assuming that a property or project qualifies under a Missouri state exemption.'),
            ('New, repaired, and existing systems are inspected', 'The Platte County program inspects new systems, repaired systems, and existing onsite wastewater systems. The department also investigates sewage complaints.'),
            ('Subdivision feasibility is reviewed with Planning and Zoning', 'Environmental Health evaluates proposed subdivisions to determine whether onsite wastewater treatment is feasible and coordinates that review with Platte County Planning and Zoning, helping identify unsuitable onsite disposal conditions before lots are developed.'),
        ],
    },
}

for county, data in MO_COUNTIES.items():
    sections = [
        ('Missouri onsite wastewater framework', 'Missouri Department of Health and Senior Services states that onsite wastewater permitting authority varies by county. In most counties a local health department issues construction permits, while other jurisdictions use a building department, planning and zoning office, sewer district, or DHSS itself. Local ordinances may be more restrictive than Missouri minimum construction standards.'),
        ('Confirm the permitting authority before work begins', 'Missouri DHSS states that a construction permit is required before installing or repairing most onsite wastewater treatment systems, subject to limited exemptions, and directs applicants to determine the agency with jurisdiction before work begins. Incorporated municipalities can sometimes fall outside a county authority even when the surrounding county has a local program.'),
    ] + data['sections']
    sources = [
        ('Missouri DHSS — Onsite Wastewater Treatment', MO_STATE_OWTS),
        ('Missouri DHSS — OWTS Construction Permit Process', MO_STATE_PERMITS),
    ] + data['sources']
    write_county_page('Missouri', 'missouri', county, data['authority'], data['contact'], sections, sources, verified='August 30, 2026')

print(f'Missouri expansion complete: +{len(MO_COUNTIES)} verified county guides')
exec((ROOT / 'utah_expansion.py').read_text(encoding='utf-8'), globals())