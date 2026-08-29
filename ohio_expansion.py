# SepticScope Ohio expansion — counties with current, substantive local health-district guidance.
# Sources are limited to Ohio law and official county/local public-health sources.

OH_RULES='https://codes.ohio.gov/ohio-administrative-code/chapter-3701-29'
OH_PERMIT='https://codes.ohio.gov/ohio-administrative-code/rule-3701-29-06'

OH_COUNTIES={
    'Franklin': {
        'authority':'Franklin County Public Health — Water Quality program (for properties within FCPH jurisdiction)',
        'contact':'Franklin County Public Health: 280 East Broad Street, Columbus, OH 43215; main phone 614-525-3160; Water Quality email waterquality@franklincountyohio.gov; failing HSTS line 614-525-4787.',
        'sources':[
            ('Franklin County Public Health — Water Quality','https://myfcph.org/water-quality/'),
            ('Franklin County Public Health — Forms & Permits','https://myfcph.org/forms-permits/'),
            ('Franklin County Public Health — Jurisdictions','https://myfcph.org/about/'),
            ('Franklin County Public Health — Regulations','https://myfcph.org/fcph-regulations/'),
        ],
        'sections':[
            ('County permitting and site-review workflow','Franklin County Public Health says its Water Quality program reviews, inspects, and regulates household, small-flow, and semi-public sewage treatment systems. For household systems, the department directs owners installing, repairing, or replacing an HSTS to its permit forms and offers site reviews, building-plan reviews, lot-split reviews, and real-estate septic inspections.'),
            ('Operation and maintenance oversight','FCPH states that it makes annual observations of aeration systems, evapotranspiration mounds, commercial septic systems, and household systems installed since 2015. It also investigates failing household systems and can require repair or replacement when a system is failing.'),
            ('Important jurisdiction boundary','Franklin County Public Health is a general health district serving the county townships and villages plus contracting cities. Its current jurisdiction information identifies the City of Columbus and Worthington as outside FCPH jurisdiction. Properties inside a separate municipal health jurisdiction should confirm the responsible agency before filing.'),
            ('Local sewage regulation','FCPH publishes local Regulation 106 for sewage treatment systems in addition to the statewide Ohio sewage-treatment rules. Applicants should use the current county forms and local requirements together with Ohio Administrative Code Chapter 3701-29.'),
        ],
    },
    'Delaware': {
        'authority':'Delaware Public Health District — Environmental Health / Sewage program',
        'contact':'Delaware Public Health District: 470 S. Sandusky Street, Delaware, OH 43015; phone 740-368-1700.',
        'sources':[
            ('Delaware Public Health District — Sewage','https://www.delawarehealth.org/sewage/'),
            ('Delaware Public Health District — About / Jurisdiction','https://www.delawarehealth.org/about-us/'),
        ],
        'sections':[
            ('Household sewage permitting authority','The Delaware Public Health District states that its sewage program inspects potential new parcels for adequate HSTS area, reviews designs for new household sewage treatment systems, inspects installations, and issues operational permits for continued HSTS use.'),
            ('Current applications and contractor registrations','The district publishes current household sewage forms for site-plan/permit applications, installation or alteration permits, addition/remodel reviews, lot feasibility, variances, and contractor registrations for septic installers, service providers, septage haulers, and septage land application.'),
            ('Semi-public systems','Under contracts with Ohio EPA, the district says it issues installation permits for semi-public sewage treatment systems sized at 1,000 gallons per day or less and performs inspections and annual operation permitting for semi-public systems sized at 25,000 gallons per day or less.'),
            ('District jurisdiction caveat','The Delaware Public Health District describes itself as a combined health district serving Delaware County, Delaware City, and Powell, except portions annexed into Westerville, Columbus, and Dublin. Owners in annexed areas should confirm which health authority has jurisdiction before applying.'),
        ],
    },
    'Fairfield': {
        'authority':'Fairfield County Health Department — Environmental Health, Sewage Treatment Systems program',
        'contact':'Fairfield County Health Department: 1550 Sheridan Drive, Suite 100, Lancaster, OH 43130; Environmental Health 740-652-2800, Option 3.',
        'sources':[
            ('Fairfield County Health Department — Sewage Treatment Systems','https://www.fairfieldhealth.org/Environmental-Division/FDH-Household-Sewage-Treatment-Systems.html'),
            ('Fairfield County Health Department — Land Lot Inspections & Subdivision','https://www.fairfieldhealth.org/Environmental-Division/FDH-Subdivision-of-Land-Lot-Inspection.html'),
            ('Fairfield County Health Department — Fee Schedule','https://www.fairfieldhealth.org/Fee-Schedule.html'),
        ],
        'sections':[
            ('Permit required for installation or alteration','Fairfield County states that its sewage program issues permits for new installations, replacements, and alterations and registers installers, service providers, and pumpers operating in the county. The county explicitly states that any installation or alteration work requires a permit.'),
            ('Soil report and design sequence','For a new system, Fairfield County requires a soil report with every new-system application regardless of lot size or creation date. The county reviews the soil information, returns a calculation worksheet identifying potential HSTS options, and then requires a design proposal, soil reports, permit application, and fee. The county directs applicants to use a registered installer.'),
            ('Lot splits and development suitability','Fairfield County requires health-department approval for all new lots, including the remainder, regardless of size. The county requires an Order One Soil Evaluation for each proposed lot and states that the proposed lot must contain a usable, contiguous area with soils suitable for a sewage treatment system.'),
            ('Current county fee schedule','Fairfield County publishes a current sewage-program fee schedule, including separate categories for new/replacement HSTS, small-flow systems, alterations, operation and maintenance, lot inspections, installer registration, service-provider registration, and septage hauling. Because the county warns that fees can change, SepticScope links to the live schedule rather than hard-coding a filing cost.'),
        ],
    },
    'Licking': {
        'authority':'Licking County Health Department — Sewage Treatment Program',
        'contact':'Licking County Health Department: 675 Price Road, Newark, OH 43055; phone 740-349-6535. Pataskala branch: 621 W. Broad Street, Pataskala, OH 43062; phone 740-755-4520.',
        'sources':[
            ('Licking County Health Department — Sewage Treatment Program','https://lickingcohealth.org/sewage/'),
            ('Licking County Health Department — Contact Us','https://lickingcohealth.org/contact-us/'),
            ('Licking County Health Department — Pataskala Branch Office','https://lickingcohealth.org/pataskala-branch-office/'),
        ],
        'sections':[
            ('County program and site evaluation','Licking County Health Department states that its Sewage Treatment Program regulates household and small-flow sewage treatment systems through inspections, sewage-rule enforcement, and homeowner education. The county recommends evaluating a site early because system design is based on site-specific soil characteristics.'),
            ('Lot splits and subdivisions','For new lots in areas not served by public water and sewer, Licking County performs a preliminary evaluation to determine whether a household sewage treatment system can be placed on the lot. The county states that a separate, more detailed evaluation is then required so the HSTS can be designed for the specific home, and it also reviews subdivisions in areas without public water and sewer.'),
            ('Operation and maintenance program','Licking County states that sewage treatment systems are required to be entered into an operation and maintenance program under the Ohio sewage rules effective January 1, 2015, with inspection used to confirm proper operation.'),
            ('Local access to environmental-health permits','The county provides Environmental Health Services and Permits at its Pataskala branch as well as its Newark office, giving western Licking County applicants a second official location for permit services.'),
        ],
    },
}

for county,data in OH_COUNTIES.items():
    sections=[
        ('Ohio permit framework','Ohio Administrative Code Chapter 3701-29 governs sewage treatment systems statewide. Rule 3701-29-06 provides that a sewage treatment system may not be installed, altered, or operated without an approved permit from the board of health, and owners must comply with permit conditions and maintain the system in proper working condition.'),
        ('Local rules can be more stringent','Ohio law allows a board of health to adopt more stringent sewage-treatment standards when local conditions support them and the required state approval is obtained. County or health-district instructions therefore matter in addition to the statewide minimum rules.'),
    ] + data['sections']
    sources=[
        ('Ohio Administrative Code Chapter 3701-29 — Sewage Treatment Systems',OH_RULES),
        ('Ohio Administrative Code Rule 3701-29-06 — General Provisions and Permits',OH_PERMIT),
    ] + data['sources']
    write_county_page('Ohio','ohio',county,data['authority'],data['contact'],sections,sources,verified='August 29, 2026')

print(f'Ohio expansion complete: +{len(OH_COUNTIES)} verified county guides')
