#!/usr/bin/env python3
"""Build a substantive, source-based homebuyer septic due-diligence guide."""
from __future__ import annotations

from datetime import date
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
OUT = SITE / "guides" / "buying-a-house-with-septic" / "index.html"
DOMAIN = "https://septicscope.com"
GA_MEASUREMENT_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"
TODAY = date.today().isoformat()

STYLE = r''':root{--ink:#17221f;--muted:#5d6965;--forest:#123d35;--forest2:#1e6253;--line:#d9e2dc;--mint:#eaf4ef;--cream:#faf6ec;--paper:#fffdfa;--danger:#fff1ec;--max:980px}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);line-height:1.72}a{color:var(--forest2);text-underline-offset:3px}header,footer{border-block:1px solid var(--line);background:#fff}.nav,.foot,main{max-width:var(--max);margin:auto;padding:18px 24px}.brand{font-weight:950;color:var(--forest);text-decoration:none}.nav{display:flex;justify-content:space-between;gap:18px;align-items:center}.nav-links{display:flex;flex-wrap:wrap;gap:16px}.nav-links a{text-decoration:none;font-weight:780;color:var(--ink)}main{padding-top:56px;padding-bottom:80px}h1{font-size:clamp(2.45rem,6vw,4.7rem);line-height:1.02;letter-spacing:-.045em;color:var(--forest);margin:.22em 0}h2{font-size:clamp(1.55rem,3vw,2.2rem);line-height:1.15;color:var(--forest);margin-top:1.65em}h3{color:var(--forest);margin-top:1.45em}.eyebrow{font-size:.77rem;font-weight:950;letter-spacing:.13em;text-transform:uppercase;color:var(--forest2)}.lead{font-size:1.17rem;color:#46534f;max-width:850px}.summary{background:var(--cream);border:1px solid #eadcbc;border-radius:17px;padding:20px;margin:26px 0}.summary strong{color:var(--forest)}.toc{background:var(--mint);border:1px solid var(--line);border-radius:17px;padding:20px;margin:28px 0}.toc ul{columns:2;gap:30px}.checklist{display:grid;gap:10px}.check{border:1px solid var(--line);border-radius:13px;padding:14px 16px;background:#fff}.check strong{color:var(--forest)}.table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:15px}table{width:100%;border-collapse:collapse;min-width:700px;background:#fff}th,td{text-align:left;vertical-align:top;padding:13px 14px;border-bottom:1px solid var(--line)}th{background:var(--mint);color:var(--forest)}tr:last-child td{border-bottom:0}.warning{background:var(--danger);border:1px solid #e7b9a8;border-radius:16px;padding:18px;margin:25px 0}.questions{display:grid;grid-template-columns:1fr 1fr;gap:12px}.questions article{border:1px solid var(--line);border-radius:14px;padding:16px;background:#fff}.questions h3{margin-top:0}.sources{background:var(--mint);border-radius:18px;padding:22px;margin-top:38px}.sources li{margin:.55em 0}.faq details{border:1px solid var(--line);border-radius:13px;background:#fff;padding:0 16px;margin:9px 0}.faq summary{padding:15px 0;cursor:pointer;font-weight:850;color:var(--forest)}.foot{color:var(--muted)}@media(max-width:720px){.nav-links a:nth-child(n+3){display:none}.toc ul{columns:1}.questions{grid-template-columns:1fr}}@media print{header,footer,.toc{display:none}body{background:#fff}main{max-width:none;padding:0}a{color:#000;text-decoration:none}.check,.summary,.warning,.sources{break-inside:avoid}}'''

SECTIONS = [
    ("before-offer", "Before making an offer: identify what the property actually has", [
        "Do not rely only on a listing description that says “septic,” “private sewer,” or “new system.” Start with the legal property record and the permitting authority for the parcel. The mailing city and ZIP code can cross jurisdictional lines, and the office that holds septic files may be a county, municipality, health district, state field office, or delegated environmental program. SepticScope’s county lookup is designed to help identify that starting point, but the agency’s current records control.",
        "Ask whether the home is fully served by an onsite wastewater system, connected to public sewer, using a shared or community system, or subject to a future sewer-connection requirement. A property can have an abandoned tank, a private pump station, a holding tank, an advanced treatment unit, or another arrangement that is not obvious from the yard. Utility bills, the deed, building permits, approved plans, and local records can help confirm the arrangement.",
        "Compare the approved design capacity with the house as it exists today. Bedrooms, finished basements, accessory dwelling units, additions, converted garages, short-term rental use, or a large regular occupancy can matter because many jurisdictions use design flow or bedroom count rather than the number of current residents. A larger house does not automatically mean the system is undersized, but an undocumented addition is a reason to investigate before closing."
    ]),
    ("records", "Request the septic file—not just the seller’s pumping receipt", [
        "A pumping receipt proves that a service occurred on a date; it does not prove that the system was legally permitted, matches the approved design, or has a functioning drainfield. Ask the local authority for the original permit, soil or site evaluation, approved design, as-built drawing, installation approval, final inspection, repair permits, operating permits, and any enforcement or complaint records that are publicly available.",
        "Ask the seller for inspection reports, pumping invoices, maintenance-contract records, alarm or pump repairs, effluent-filter service, component replacements, and information about backups, odors, surfacing wastewater, or seasonal problems. Records are more useful when they identify the tank size, number of compartments, system type, access locations, pump and control equipment, drainfield layout, reserve area, and date of work.",
        "If the records cannot be found, treat that as an unresolved due-diligence item rather than proof that the system is illegal or acceptable. Older systems may predate modern recordkeeping, and local archives vary. The next step may be a records search under a former owner’s name, parcel number, previous street address, or building permit, followed by physical locating and a property-specific professional evaluation."
    ]),
    ("inspection", "Order the right inspection for the transaction", [
        "EPA recommends having a septic system inspected before buying a home. The exact inspection scope varies by jurisdiction, system type, site access, weather, and contract. Ask the inspector to explain what will be opened, observed, tested, measured, and excluded. A visual walkover, a routine pump-out, a real-estate inspection, an operational evaluation, and a regulatory compliance inspection are not interchangeable.",
        "A useful inspection generally starts with the permit, design, age, pumping history, maintenance history, and known repairs. Depending on the system and local practice, the inspector may evaluate tank access and condition, liquid levels, sludge and scum, inlet and outlet components, effluent filters, pumps, floats, alarms, controls, distribution components, visible piping, and the drainfield area. Some components may be inaccessible or unsafe to enter; septic tanks are confined spaces and should never be entered by a homeowner.",
        "Ask whether pumping is required before, during, or after the inspection and whether pumping could hide or reveal important conditions. Pumping can allow inspection of accessible tank components, but an empty tank does not establish that the drainfield accepts wastewater correctly. Conversely, loading a system aggressively for a test can be inappropriate or prohibited. The inspector should follow applicable local requirements and describe the limitations in writing.",
        "If the property also uses a private well, consider the well and septic relationship rather than treating them as unrelated systems. Verify required separation distances, well records, recent water-quality testing, surface drainage, and any known contamination concerns with the appropriate local authority and qualified professionals."
    ]),
    ("site", "Walk the property with the records in hand", [
        "Locate the tank, access risers, pump tank, control panel, cleanouts, distribution components, primary drainfield, and designated replacement or reserve area when the records identify them. Look for driveways, parking, decks, sheds, pools, additions, fences, retaining walls, grading, drainage swales, irrigation, large trees, or heavy equipment over those areas. Encroachment does not automatically prove failure, but it can affect access, soil treatment, future repair options, and compliance.",
        "Watch for sewage odors, damp or spongy soil, standing water, unusually lush grass in dry weather, plumbing backups, slow drains affecting multiple fixtures, gurgling, alarm conditions, bypass piping, or visible discharge. These are warning signs, not a remote diagnosis. Recent rain, frozen soil, high groundwater, plumbing blockages, pump failure, excessive water use, or a drainfield problem can produce overlapping symptoms.",
        "Ask where roof runoff, sump discharge, foundation drainage, driveway runoff, and irrigation water go. Excess water should not be intentionally directed onto the tank or drainfield. Also note steep slopes, erosion, flood-prone areas, shorelines, wetlands, nearby wells, and limited open area. These site constraints can affect both current performance and the feasibility or cost of future replacement."
    ]),
    ("report", "Read the report as a decision document, not a pass/fail sticker", [
        "A strong report separates observed facts, records reviewed, tests performed, inaccessible components, assumptions, applicable standards, limitations, maintenance recommendations, repair recommendations, and urgent health or safety concerns. It should identify the system type and major components as accurately as the available evidence permits. Vague language such as “appears serviceable” is less useful when the report does not state what was actually inspected.",
        "Ask the inspector to distinguish routine maintenance from a defect, a defect from a regulatory violation, and a current failure from a future risk. An older working system may need planning and monitoring rather than immediate replacement. A broken lid, missing riser, clogged filter, failed pump, damaged baffle, distribution problem, hydraulic overload, or local piping defect can have a different remedy from a failed soil treatment area.",
        "When replacement is recommended, ask what evidence supports that conclusion and whether the tank, conveyance, pump equipment, distribution, and drainfield were evaluated separately. Obtain the applicable agency’s permit requirements and qualified written estimates. The approved replacement may depend on soil, groundwater, setbacks, design flow, reserve area, technology approval, and current rules—not merely the size or type of the old system."
    ]),
    ("contract", "Protect the transaction with enough time and the right contingencies", [
        "Real-estate contracts and disclosure laws vary, so use a qualified local real-estate professional or attorney for contract language. Practical due diligence often requires enough time to obtain public records, locate buried components, schedule qualified inspection, receive laboratory or specialist results when needed, obtain agency clarification, and price repairs or replacement. A short generic home-inspection window may not accommodate all of those steps.",
        "Clarify who authorizes access, who pays for locating or excavation, whether the tank must be pumped, who receives the report, and what happens if components cannot be found or inspected. Define how an unsatisfactory result affects the contract and whether the buyer can request repair, credit, escrow, price adjustment, additional investigation, or termination. Do not assume a seller-funded pump-out is equivalent to buyer-controlled due diligence.",
        "If a repair is negotiated, identify who obtains the permit, who chooses the qualified professional, what approved scope must be completed, what inspections and final approvals are required, and what documentation must be delivered before closing. A receipt that says “repair completed” is weaker than a permit, approved plan when required, itemized invoice, inspection result, and agency completion record."
    ]),
    ("red-flags", "Issues that deserve more investigation before closing", [
        "Missing records, an unknown tank location, an unpermitted bedroom addition, a drainfield under vehicle traffic, a disabled alarm, recurring pump replacements, seller reports of seasonal backup, recent unexplained pumping, visible wastewater, direct discharge, an inaccessible tank, or no apparent replacement area are reasons to pause and gather evidence. None of these items should be evaluated from a checklist alone.",
        "A seller’s statement that the system has “never had a problem” is not a substitute for records and inspection. Low occupancy can mask capacity or loading concerns, and a vacant home may not demonstrate normal performance. On the other hand, age alone does not prove failure. The goal is to understand the system, current condition, legal status, maintenance burden, and credible future risk well enough to make a property decision.",
        "Be especially careful when the transaction involves waterfront property, high groundwater, shallow bedrock, very small lots, shared systems, commercial or mixed use, accessory dwellings, advanced treatment, pumps, disinfection, spray or drip dispersal, holding tanks, easements, or off-lot components. These situations can involve operating permits, maintenance contracts, monitoring, access rights, or technology-specific requirements."
    ]),
    ("after-closing", "What to do after closing", [
        "Keep the permit, as-built drawing, inspection, pumping history, maintenance contract, equipment manuals, repair records, and agency correspondence together. Mark tank and component locations on a durable property plan without creating unsafe openings. Record the next inspection, filter service, pump-out, sampling, operating-permit, or maintenance-contract date that applies to the system.",
        "Learn which fixtures, appliances, alarms, pumps, and controls affect the system. Spread out laundry and other high-water uses, repair leaks, flush only human waste and toilet paper, keep inappropriate chemicals and solids out, protect the drainfield from traffic and excess water, and preserve access for inspection and pumping. Alternative systems may require more frequent professional attention than a conventional gravity tank and drainfield.",
        "Contact the permitting authority before an addition, bedroom conversion, pool, deck, driveway, well, grading project, landscaping change, system repair, or replacement that could affect the approved design or setbacks. The cheapest time to find a conflict is before construction begins."
    ]),
]

FAQS = [
    ("Is a septic system a reason not to buy a house?", "No. Many homes use septic systems successfully. The decision depends on the property-specific permit, design, condition, maintenance history, site constraints, inspection findings, and future risk—not the word “septic” alone."),
    ("Is a pumping receipt the same as a septic inspection?", "No. Pumping removes accumulated solids and may permit observation of accessible tank components. An inspection has a defined evaluation scope and should explain records, observations, limitations, and findings. The two services can occur together but are not interchangeable."),
    ("Who should inspect a septic system for a home purchase?", "Use a professional who is qualified for the inspection type required or customary in that jurisdiction and who can explain independence, credentials, scope, exclusions, and reporting. The local permitting authority can explain applicable licensing or transfer requirements."),
    ("What if the county has no septic records?", "Continue due diligence using parcel and building records, former owner names or addresses, physical locating, seller documentation, and qualified evaluation. Missing records do not by themselves prove that the system is acceptable or illegal."),
    ("Should the seller replace an old septic system?", "Age alone is not enough to answer that question. Evaluate current condition, permit status, component-specific findings, site and replacement feasibility, and the transaction terms with qualified local professionals."),
]


def paragraphs(values: list[str]) -> str:
    return "".join(f"<p>{escape(value)}</p>" for value in values)


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    article_sections = "".join(
        f'<section id="{escape(anchor)}"><h2>{escape(title)}</h2>{paragraphs(body)}</section>'
        for anchor, title, body in SECTIONS
    )
    toc = "".join(f'<li><a href="#{escape(anchor)}">{escape(title)}</a></li>' for anchor, title, _body in SECTIONS)
    checklist = [
        "Confirm the legal county and permitting authority for the parcel.",
        "Determine whether the property is septic, sewer, shared, community, or another arrangement.",
        "Obtain the permit, approved design, as-built, soil/site evaluation, and final approval when available.",
        "Compare permitted design flow or bedrooms with the current house and intended use.",
        "Collect pumping, inspection, maintenance, alarm, pump, filter, and repair records.",
        "Hire the appropriate independent inspector and define the scope before the appointment.",
        "Locate the tank, treatment equipment, drainfield, reserve area, and access points.",
        "Review encroachments, drainage, wells, waterways, slopes, flooding, and replacement constraints.",
        "Require a written report that separates observations, limitations, maintenance, defects, and recommendations.",
        "Obtain agency guidance and qualified estimates before accepting a major repair or replacement conclusion.",
        "Use transaction contingencies and timelines suited to septic records and inspection—not only a generic home inspection.",
        "Keep all final records and establish the next inspection and maintenance dates after closing.",
    ]
    checklist_html = "".join(f'<div class="check">☐ {escape(item)}</div>' for item in checklist)
    faq_html = "".join(f'<details><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>' for question, answer in FAQS)
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Buying a House With a Septic System: Due-Diligence Guide",
        "description": "A source-based homebuyer checklist for septic permits, records, inspection scope, site review, reports, contingencies, repair decisions, and post-closing maintenance.",
        "mainEntityOfPage": f"{DOMAIN}/guides/buying-a-house-with-septic/",
        "dateModified": TODAY,
        "publisher": {"@type": "Organization", "name": "SepticScope", "url": f"{DOMAIN}/"},
    }
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
            for question, answer in FAQS
        ],
    }
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Buying a House With a Septic System: Inspection & Records Checklist</title><meta name="description" content="Use this detailed homebuyer checklist to review septic permits, as-built plans, inspections, maintenance history, drainfield conditions, repair risk, contingencies, and post-closing care."><link rel="canonical" href="{DOMAIN}/guides/buying-a-house-with-septic/"><style>{STYLE}</style><script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c")}</script><script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False).replace("<", "\\u003c")}</script></head><body><header><nav class="nav" aria-label="Primary"><a class="brand" href="/">SepticScope</a><div class="nav-links"><a href="/counties/">County lookup</a><a href="/guides/">Homeowner guides</a><a href="/faq/">Septic FAQ</a><a href="/about/">Research standards</a></div></nav></header><main><p><a href="/">Home</a> / <a href="/guides/">Guides</a> / Buying a house with septic</p><p class="eyebrow">Homebuyer due diligence</p><h1>Buying a house with a septic system</h1><p class="lead">A septic system is not automatically a reason to avoid a property. The risk comes from buying without understanding the permit, approved capacity, system type, maintenance history, current condition, site constraints, and realistic repair or replacement path.</p><div class="summary"><strong>Use this guide before the inspection deadline:</strong> identify the legal jurisdiction, obtain the septic file, order the right inspection, walk the site with the records, understand the report, and protect enough time in the transaction to investigate unresolved findings.</div><nav class="toc" aria-label="Guide contents"><strong>On this page</strong><ul>{toc}</ul></nav>{article_sections}<section><h2>Printable homebuyer septic checklist</h2><div class="checklist">{checklist_html}</div></section><section><h2>Questions to ask before choosing an inspector</h2><div class="questions"><article><h3>Scope and qualifications</h3><p>What credential or authorization applies here? What system types do you inspect? Are you independent from the seller, repair contractor, or real-estate referral? What records will you review?</p></article><article><h3>Access and testing</h3><p>Which tanks and components will be opened? Is pumping required? Will sludge and scum be measured? How are pumps, alarms, controls, distribution, and the drainfield evaluated?</p></article><article><h3>Limitations</h3><p>What weather, occupancy, access, landscaping, groundwater, safety, or local-rule limits could prevent a conclusion? How will inaccessible components be reported?</p></article><article><h3>Report and follow-up</h3><p>Will the report identify observed facts, photos, records reviewed, excluded work, maintenance needs, defects, regulatory questions, and recommended follow-up without collapsing everything into “pass” or “fail”?</p></article></div></section><section class="warning"><h2>Health and safety warning</h2><p>Keep people and pets away from sewage backing up indoors or surfacing outdoors. Reduce water use and contact a qualified local professional or public-health authority. Do not enter a septic tank; tanks are dangerous confined spaces with toxic gases and structural hazards.</p></section><section class="faq"><h2>Homebuyer septic questions</h2>{faq_html}</section><section class="sources"><h2>Primary public sources</h2><ul><li><a href="https://www.epa.gov/septic/new-homebuyers-brochure-and-guide-septic-systems" rel="nofollow">U.S. EPA — New Homebuyer’s Brochure and Guide to Septic Systems</a></li><li><a href="https://www.epa.gov/septic/frequent-questions-septic-systems" rel="nofollow">U.S. EPA — Frequent Questions on Septic Systems</a></li><li><a href="https://www.epa.gov/septic/how-care-your-septic-system" rel="nofollow">U.S. EPA — How to Care for Your Septic System</a></li><li><a href="https://www.epa.gov/septic/types-septic-systems" rel="nofollow">U.S. EPA — Types of Septic Systems</a></li></ul><p>Editorial review: {TODAY}. General guidance does not replace local transfer rules, a property-specific permit, inspection, engineering opinion, legal advice, or current agency instructions.</p></section></main><footer><div class="foot">© 2026 SepticScope · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a> · <a href="/contact/">Corrections & feedback</a></div></footer></body></html>'''
    OUT.write_text(html, encoding="utf-8")
    if html.lower().count("<h1") != 1:
        raise RuntimeError("Homebuyer guide must contain exactly one H1")
    if html.count("https://www.epa.gov/") < 4:
        raise RuntimeError("Homebuyer guide lost its primary public sources")
    print("Substantive homebuyer septic due-diligence guide built")


if __name__ == "__main__":
    build()
