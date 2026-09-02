#!/usr/bin/env python3
'''Build the crawlable, location-aware Septic Services Near Me experience.'''
from __future__ import annotations

from datetime import date
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from provider_curated_experience import curated_provider_data

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
MANIFEST = SITE / "data" / "national-coverage-manifest.json"
DOMAIN = "https://septicscope.com"
PAGE_PATH = "/septic-services-near-me/"
TODAY = date.today().isoformat()
GA_MEASUREMENT_ID = "G-F6RB8YERCM"
ADSENSE_CLIENT = "ca-pub-8782868222380999"

STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}

SERVICE_LABELS = {
    "pumping": "Septic pumping", "septic_pumping": "Septic pumping",
    "cleaning": "Tank cleaning", "septic_cleaning": "Tank cleaning",
    "inspection": "Septic inspection", "inspections": "Septic inspection",
    "septic_inspection": "Septic inspection",
    "property_transfer": "Property-transfer inspection",
    "certification": "Inspection / certification",
    "installation": "System installation", "installations": "System installation",
    "septic_installation": "System installation", "design": "System design",
    "septic_design": "System design", "site_evaluation": "Site evaluation",
    "soil_testing": "Soil testing", "permit_assistance": "Permit assistance",
    "repair": "System repair", "repairs": "System repair",
    "septic_repair": "System repair", "replacement": "System replacement",
    "system_replacement": "System replacement", "drainfield": "Drainfield service",
    "drainfield_service": "Drainfield service", "locating": "Tank locating",
    "root_removal": "Root removal", "maintenance": "Maintenance",
    "maintenance_contracts": "Maintenance contracts",
    "aerobic": "Aerobic-system service", "aerobic_maintenance": "Aerobic maintenance",
    "alternative_systems": "Alternative systems", "engineered_systems": "Engineered systems",
    "mound_systems": "Mound systems", "holding_tank": "Holding tanks",
    "risers": "Risers / access", "filter_service": "Effluent-filter service",
    "pump_service": "Pump service", "sump_pump": "Sump / pump service",
    "lift_station": "Lift stations", "grease_trap": "Grease traps",
    "commercial": "Commercial service", "septage_disposal": "Septage disposal",
    "portable_sanitation": "Portable sanitation", "excavation": "Excavation",
    "land_clearing": "Land clearing", "drain_cleaning": "Drain cleaning",
    "line_clearing": "Line clearing", "jetting": "Hydro jetting",
    "hydrojetting": "Hydro jetting", "camera_inspection": "Camera inspection",
    "treatment": "Treatment service", "utility": "Utility / site work",
    "sewer": "Sewer service", "sewer_pump": "Sewer-pump service",
    "sand_trap": "Sand traps", "emergency": "Emergency service",
}

FILTER_GROUPS = {
    "pumping": {"pumping", "septic_pumping", "cleaning", "septic_cleaning", "holding_tank"},
    "inspection": {"inspection", "inspections", "septic_inspection", "property_transfer", "certification", "camera_inspection"},
    "installation": {"installation", "installations", "septic_installation", "design", "septic_design", "site_evaluation", "soil_testing", "permit_assistance"},
    "repair": {"repair", "repairs", "septic_repair", "replacement", "system_replacement", "drainfield", "drainfield_service", "locating", "root_removal", "drain_cleaning", "line_clearing", "jetting", "hydrojetting", "excavation", "emergency"},
    "maintenance": {"maintenance", "maintenance_contracts", "aerobic", "aerobic_maintenance", "alternative_systems", "engineered_systems", "mound_systems", "risers", "filter_service", "pump_service", "sump_pump"},
    "commercial": {"commercial", "grease_trap", "lift_station", "septage_disposal", "portable_sanitation", "utility", "sewer", "sewer_pump", "sand_trap"},
}


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def active_providers() -> list[dict]:
    data = curated_provider_data()
    rows = [
        provider for provider in data.get("providers", [])
        if isinstance(provider, dict)
        and str(provider.get("status", "active")).lower() in {"active", "verified"}
        and clean(provider.get("business_name"))
        and clean(provider.get("public_phone"))
        and provider.get("source_urls")
    ]
    rows.sort(key=lambda item: (clean(item.get("business_name")).casefold(), clean(item.get("id"))))
    return rows


def county_fips(provider: dict) -> list[str]:
    values: list[str] = []
    for item in provider.get("counties_served", []):
        value = item.get("fips", "") if isinstance(item, dict) else item
        fips = clean(value)
        if re.fullmatch(r"\d{5}", fips) and fips not in values:
            values.append(fips)
    return values


def service_keys(provider: dict) -> list[str]:
    result: list[str] = []
    for raw in provider.get("service_categories", []):
        key = re.sub(r"[^a-z0-9]+", "_", clean(raw).lower()).strip("_")
        if key and key not in result:
            result.append(key)
    return result


def display_services(provider: dict) -> list[str]:
    labels: list[str] = []
    for key in service_keys(provider):
        label = SERVICE_LABELS.get(key, key.replace("_", " ").title())
        if label not in labels:
            labels.append(label)
    return labels or ["Septic services"]


def filter_tokens(provider: dict) -> list[str]:
    keys = service_keys(provider)
    tokens = list(keys)
    for group, members in FILTER_GROUPS.items():
        if set(keys).intersection(members):
            tokens.append(group)
    return sorted(set(tokens))


def safe_url(value: object) -> str:
    value = clean(value)
    return value if value.startswith(("https://", "http://")) else ""


def load_counties() -> tuple[dict[str, dict], list[dict]]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = data.get("records", [])
    if len(records) != 3144:
        raise RuntimeError(f"Expected 3,144 county records; found {len(records)}")
    by_fips: dict[str, dict] = {}
    compact: list[dict] = []
    for record in records:
        fips = clean(record.get("fips"))
        state = clean(record.get("state"))
        name = clean(record.get("county_or_equivalent_name"))
        url = clean(record.get("page_url"))
        if not re.fullmatch(r"\d{5}", fips) or not url.startswith(DOMAIN + "/"):
            continue
        item = {
            "f": fips, "n": name, "s": state, "a": STATE_ABBR.get(state, ""),
            "u": url.removeprefix(DOMAIN),
            "v": record.get("verification_status") == "verified" or record.get("indexability_status") == "indexable",
        }
        by_fips[fips] = item
        compact.append(item)
    if len(by_fips) != 3144:
        raise RuntimeError(f"County map is incomplete: {len(by_fips)}")
    compact.sort(key=lambda item: (item["s"], item["n"]))
    return by_fips, compact


def provider_payload(provider: dict, counties: dict[str, dict]) -> dict:
    fips_values = county_fips(provider)
    county_values = [counties[fips] for fips in fips_values if fips in counties]
    source_urls = [safe_url(value) for value in provider.get("source_urls", [])]
    source_urls = [url for url in source_urls if url]
    return {
        "id": clean(provider.get("id")),
        "name": clean(provider.get("business_name")),
        "website": safe_url(provider.get("website")),
        "phone": clean(provider.get("public_phone")),
        "email": clean(provider.get("public_email")),
        "address": clean(provider.get("address")),
        "city": clean(provider.get("city")),
        "state": clean(provider.get("state")),
        "zip": clean(provider.get("zip_code")),
        "fips": fips_values,
        "counties": county_values,
        "services": service_keys(provider),
        "service_labels": display_services(provider),
        "filter_tokens": filter_tokens(provider),
        "license": clean(provider.get("license_information") or provider.get("license_or_registration")),
        "coverage": clean(provider.get("coverage_notes") or provider.get("coverage_basis")),
        "hours": clean(provider.get("hours_note")),
        "verified": clean(provider.get("date_last_verified")),
        "source": source_urls[0] if source_urls else safe_url(provider.get("website")),
        "sponsored": bool(provider.get("sponsored")),
        "affiliate": bool(provider.get("affiliate")),
    }


def tel_href(phone: str) -> str:
    return re.sub(r"[^0-9+]", "", phone)


def provider_card(item: dict) -> str:
    search_parts = [
        item["name"], item["address"], item["city"], item["state"], item["zip"],
        " ".join(county["n"] + " " + county["s"] for county in item["counties"]),
        " ".join(item["service_labels"]),
    ]
    search = clean(" ".join(search_parts)).lower()
    location = ", ".join(part for part in (item["address"], item["city"], item["state"]) if part)
    if item["zip"]:
        location = f"{location} {item['zip']}".strip()
    if not location:
        location = "Public street address was not listed in the reviewed source."
    elif not item["address"]:
        location = "Service base: " + location + ". Public street address was not listed in the reviewed source."
    chips = "".join(f'<span class="ssn-chip">{escape(label)}</span>' for label in item["service_labels"])
    county_links = "".join(
        f'<a href="{escape(county["u"])}">{escape(county["n"])}, {escape(county["a"] or county["s"])}</a>'
        for county in item["counties"]
    )
    actions = []
    if item["website"]:
        actions.append(f'<a class="ssn-button ssn-button-primary" href="{escape(item["website"])}" rel="nofollow external noopener">Company website</a>')
    if item["phone"]:
        actions.append(f'<a class="ssn-button" href="tel:{escape(tel_href(item["phone"]))}">{escape(item["phone"])}</a>')
    if item["email"]:
        actions.append(f'<a class="ssn-button" href="mailto:{escape(item["email"])}">Email</a>')
    source_html = (
        f'<a href="{escape(item["source"])}" rel="nofollow external noopener">View verification source</a>'
        if item["source"] else "Verification source is retained in the catalog."
    )
    license_html = f'<p><strong>Credential note:</strong> {escape(item["license"])}</p>' if item["license"] else ""
    hours_html = f'<p><strong>Published availability:</strong> {escape(item["hours"])}</p>' if item["hours"] else ""
    commercial = '<span class="ssn-commercial">Sponsored / commercial relationship disclosed</span>' if item["sponsored"] or item["affiliate"] else ""
    return f'''<article class="ssn-provider" data-provider-card data-fips="{escape(" ".join(item["fips"]))}" data-state="{escape(item["state"])}" data-services="{escape(" ".join(item["filter_tokens"]))}" data-search="{escape(search)}">
<div class="ssn-provider-head"><div><h2>{escape(item["name"])}</h2><p class="ssn-address">{escape(location)}</p></div><span class="ssn-source-badge">Source reviewed</span></div>
<div class="ssn-chips">{chips}</div><div class="ssn-county-links"><strong>Published coverage:</strong>{county_links}</div>
<p>{escape(item["coverage"])}</p>{license_html}{hours_html}{commercial}<div class="ssn-actions">{"".join(actions)}</div>
<details><summary>Source and review details</summary><p>{source_html}</p><p>Public information last reviewed: <strong>{escape(item["verified"] or "date not published")}</strong>.</p><p>Confirm the exact address, job scope, current credentials, insurance, availability, and written price directly with the business and the local permitting authority.</p></details></article>'''


CSS = r''':root{--forest:#123d35;--forest2:#1e6253;--mint:#eaf4ef;--cream:#f8f4e9;--paper:#fffdfa;--ink:#17221f;--muted:#5d6965;--line:#d9e2dc;--gold:#d99a35;--shadow:0 16px 48px rgba(18,61,53,.11);--max:1200px}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.62}a{color:var(--forest2);text-underline-offset:3px}.ssn-skip{position:absolute;left:-9999px}.ssn-skip:focus{left:16px;top:12px;background:#fff;padding:10px;z-index:99}.ssn-header{position:sticky;top:0;z-index:40;background:rgba(255,253,250,.96);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}.ssn-nav{max-width:var(--max);margin:auto;padding:14px 22px;display:flex;align-items:center;justify-content:space-between;gap:18px}.ssn-brand{display:flex;align-items:center;gap:9px;font-weight:900;color:var(--forest);text-decoration:none}.ssn-mark{display:grid;place-items:center;width:36px;height:36px;border-radius:11px;background:var(--forest);color:#fff}.ssn-links{display:flex;align-items:center;gap:19px}.ssn-links a{text-decoration:none;font-weight:700;color:var(--ink)}.ssn-links .ssn-nav-cta{background:var(--forest);color:#fff;padding:9px 14px;border-radius:999px}.ssn-hero{background:var(--cream);border-bottom:1px solid var(--line)}.ssn-hero-inner{max-width:var(--max);margin:auto;padding:66px 22px 62px;display:grid;grid-template-columns:minmax(0,1.2fr) minmax(310px,.8fr);gap:48px;align-items:center}.ssn-eyebrow{margin:0 0 13px;color:var(--forest2);font-size:.78rem;font-weight:900;letter-spacing:.13em;text-transform:uppercase}.ssn-hero h1{font-size:clamp(2.6rem,6vw,5rem);line-height:1.02;letter-spacing:-.045em;margin:.05em 0 .25em;color:var(--forest)}.ssn-lede{font-size:clamp(1.05rem,2vw,1.25rem);color:#46534f;max-width:760px}.ssn-search{background:#fff;border:1px solid rgba(18,61,53,.17);border-radius:20px;padding:12px;box-shadow:var(--shadow);margin-top:26px}.ssn-search-row{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(180px,.55fr) auto;gap:9px}.ssn-search input,.ssn-search select{width:100%;border:1px solid var(--line);border-radius:12px;padding:13px 12px;font:650 1rem inherit;background:#fff;color:var(--ink)}.ssn-search button{border:0;border-radius:12px;background:var(--forest);color:#fff;padding:13px 18px;font:850 .96rem inherit;cursor:pointer}.ssn-search button:disabled{opacity:.6}.ssn-search-tools{display:flex;justify-content:space-between;gap:16px;align-items:center;margin-top:10px;color:var(--muted);font-size:.86rem}.ssn-use-location{border:0!important;background:transparent!important;color:var(--forest2)!important;padding:2px!important;text-decoration:underline;font:800 .86rem inherit!important}.ssn-status{margin:12px 0 0;color:var(--muted)}.ssn-status[hidden]{display:none}.ssn-hero-card{background:var(--forest);color:#fff;border-radius:26px;padding:28px;box-shadow:0 26px 66px rgba(18,61,53,.23)}.ssn-hero-card h2{margin:0 0 12px;color:#fff}.ssn-hero-card p{color:#d5e6e0}.ssn-checks{display:grid;gap:10px;margin-top:18px}.ssn-check{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.13);border-radius:13px;padding:12px}.ssn-check strong{display:block}.ssn-metrics{max-width:var(--max);margin:-25px auto 0;padding:0 22px;position:relative}.ssn-metric-grid{display:grid;grid-template-columns:repeat(4,1fr);background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow);overflow:hidden}.ssn-metric{padding:20px 22px;border-right:1px solid var(--line)}.ssn-metric:last-child{border-right:0}.ssn-metric strong{display:block;font-size:1.7rem;color:var(--forest)}.ssn-metric span{font-size:.86rem;color:var(--muted);font-weight:700}.ssn-section{max-width:var(--max);margin:auto;padding:72px 22px}.ssn-section h2,.ssn-section h3{color:var(--forest);line-height:1.12}.ssn-section-title{display:flex;justify-content:space-between;align-items:end;gap:24px;margin-bottom:27px}.ssn-section-title h2{font-size:clamp(2rem,4vw,3.1rem);margin:0}.ssn-section-title p{max-width:620px;color:var(--muted);margin:0}.ssn-filters{display:grid;grid-template-columns:1fr 230px 160px;gap:10px;margin-bottom:16px}.ssn-filters input,.ssn-filters select{border:1px solid var(--line);border-radius:11px;padding:12px;font:650 1rem inherit;background:#fff}.ssn-results-meta{display:flex;justify-content:space-between;gap:16px;color:var(--muted);font-size:.92rem;margin-bottom:18px}.ssn-provider-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.ssn-provider{border:1px solid var(--line);border-radius:19px;padding:21px;background:#fff;box-shadow:0 8px 28px rgba(18,61,53,.055)}.ssn-provider[hidden]{display:none}.ssn-provider-head{display:flex;justify-content:space-between;gap:16px;align-items:start}.ssn-provider h2{font-size:1.32rem;margin:0 0 5px}.ssn-address{margin:0;color:var(--muted);font-size:.9rem}.ssn-source-badge{flex:none;background:var(--mint);color:var(--forest2);border-radius:999px;padding:5px 9px;font-size:.74rem;font-weight:900}.ssn-chips{display:flex;flex-wrap:wrap;gap:6px;margin:15px 0}.ssn-chip{background:var(--mint);color:#164e43;border-radius:999px;padding:4px 8px;font-size:.76rem;font-weight:800}.ssn-county-links{display:flex;flex-wrap:wrap;gap:7px;align-items:center;font-size:.9rem}.ssn-county-links a{background:var(--cream);border:1px solid #e9dfcc;border-radius:8px;padding:4px 7px;text-decoration:none}.ssn-actions{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}.ssn-button{display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:10px;padding:9px 12px;text-decoration:none;font-weight:850}.ssn-button-primary{background:var(--forest);color:#fff;border-color:var(--forest)}.ssn-provider details{border-top:1px solid var(--line);padding-top:12px;margin-top:10px}.ssn-provider summary{cursor:pointer;color:var(--forest2);font-weight:800}.ssn-commercial{display:inline-block;background:#fff3d7;border:1px solid #ead39e;padding:5px 8px;border-radius:8px;font-size:.8rem}.ssn-empty{border:1px dashed #9eb5ad;border-radius:16px;background:var(--mint);padding:22px;margin-top:18px}.ssn-empty[hidden]{display:none}.ssn-county-suggestions{display:grid;gap:8px;margin-top:12px}.ssn-county-suggestions a{display:block;background:#fff;border:1px solid var(--line);border-radius:10px;padding:10px;text-decoration:none;font-weight:800}.ssn-how{background:var(--mint);border-block:1px solid var(--line)}.ssn-how-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.ssn-how article{background:#fff;border:1px solid var(--line);border-radius:17px;padding:20px}.ssn-how h3{margin-top:0}.ssn-quick-links{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.ssn-quick-links a{border:1px solid var(--line);border-radius:15px;padding:17px;background:#fff;text-decoration:none;font-weight:850}.ssn-faq{display:grid;gap:9px}.ssn-faq details{border:1px solid var(--line);border-radius:13px;background:#fff;padding:0 16px}.ssn-faq summary{padding:15px 0;cursor:pointer;font-weight:850;color:var(--forest)}.ssn-footer{background:#102e29;color:#d9e6e1}.ssn-footer-inner{max-width:var(--max);margin:auto;padding:40px 22px}.ssn-footer a{color:#fff}.ssn-footer-links{display:flex;flex-wrap:wrap;gap:18px}.ssn-footer small{display:block;margin-top:18px;color:#aac3ba}@media(max-width:930px){.ssn-hero-inner{grid-template-columns:1fr}.ssn-provider-grid{grid-template-columns:1fr}.ssn-how-grid,.ssn-quick-links{grid-template-columns:1fr 1fr}.ssn-metric-grid{grid-template-columns:1fr 1fr}.ssn-metric:nth-child(2){border-right:0}.ssn-metric:nth-child(-n+2){border-bottom:1px solid var(--line)}}@media(max-width:760px){.ssn-links a:not(.ssn-nav-cta){display:none}.ssn-search-row,.ssn-filters{grid-template-columns:1fr}.ssn-section-title{display:block}.ssn-section-title p{margin-top:10px}.ssn-results-meta{display:block}.ssn-how-grid,.ssn-quick-links{grid-template-columns:1fr}}@media(max-width:520px){.ssn-metric-grid{grid-template-columns:1fr}.ssn-metric{border-right:0;border-bottom:1px solid var(--line)}.ssn-provider-head{display:block}.ssn-source-badge{display:inline-block;margin-top:9px}.ssn-actions{display:grid}.ssn-button{width:100%}.ssn-search-tools{display:block}}'''

JS = r'''(function(){"use strict";let data=null;const stateNames={AL:"Alabama",AK:"Alaska",AZ:"Arizona",AR:"Arkansas",CA:"California",CO:"Colorado",CT:"Connecticut",DE:"Delaware",DC:"District of Columbia",FL:"Florida",GA:"Georgia",HI:"Hawaii",ID:"Idaho",IL:"Illinois",IN:"Indiana",IA:"Iowa",KS:"Kansas",KY:"Kentucky",LA:"Louisiana",ME:"Maine",MD:"Maryland",MA:"Massachusetts",MI:"Michigan",MN:"Minnesota",MS:"Mississippi",MO:"Missouri",MT:"Montana",NE:"Nebraska",NV:"Nevada",NH:"New Hampshire",NJ:"New Jersey",NM:"New Mexico",NY:"New York",NC:"North Carolina",ND:"North Dakota",OH:"Ohio",OK:"Oklahoma",OR:"Oregon",PA:"Pennsylvania",RI:"Rhode Island",SC:"South Carolina",SD:"South Dakota",TN:"Tennessee",TX:"Texas",UT:"Utah",VT:"Vermont",VA:"Virginia",WA:"Washington",WV:"West Virginia",WI:"Wisconsin",WY:"Wyoming"},stateAbbr=Object.fromEntries(Object.entries(stateNames).map(([k,v])=>[normalize(v),k]));function normalize(v){return String(v||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase().replace(/[^a-z0-9]+/g," ").trim()}function track(n,p){if(typeof window.gtag==="function")window.gtag("event",n,p||{})}async function fetchJson(u,m){const c=new AbortController,t=setTimeout(()=>c.abort(),m||9000);try{const r=await fetch(u,{headers:{Accept:"application/json"},signal:c.signal});if(!r.ok)throw new Error("HTTP "+r.status);return await r.json()}finally{clearTimeout(t)}}async function loadData(){if(data)return data;data=await fetchJson("/data/septic-services-near-me.json",1e4);return data}function parseCityState(q){const raw=String(q||"").trim(),parts=raw.split(",").map(x=>x.trim()).filter(Boolean);let city="",state="";if(parts.length>1){city=parts.slice(0,-1).join(" ");state=parts.at(-1)}else{const words=raw.split(/\s+/),last=words.at(-1)||"",abbr=last.toUpperCase();if(stateNames[abbr]||stateAbbr[normalize(last)]){state=words.pop();city=words.join(" ")}}const a=stateNames[state.toUpperCase()]?state.toUpperCase():stateAbbr[normalize(state)];return city&&a?{city,state:a}:null}async function fipsForCoordinates(lat,lon){const fcc="https://geo.fcc.gov/api/census/block/find?latitude="+encodeURIComponent(lat)+"&longitude="+encodeURIComponent(lon)+"&format=json";try{const d=await fetchJson(fcc,8e3),f=d&&d.County&&String(d.County.FIPS||"").padStart(5,"0");if(f)return f}catch(e){}const u="https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x="+encodeURIComponent(lon)+"&y="+encodeURIComponent(lat)+"&benchmark=Public_AR_Current&vintage=Current_Current&format=json",d=await fetchJson(u,9e3),rows=d&&d.result&&d.result.geographies&&d.result.geographies.Counties,c=Array.isArray(rows)?rows[0]:null;if(c)return String(c.STATE||"").padStart(2,"0")+String(c.COUNTY||"").padStart(3,"0");throw new Error("county unresolved")}async function remoteFips(q){const zip=String(q||"").trim().match(/^\d{5}$/);let places=[],label="";if(zip){const d=await fetchJson("https://api.zippopotam.us/us/"+zip[0],8e3);places=Array.isArray(d.places)?d.places:[];label="ZIP "+zip[0]}else{const p=parseCityState(q);if(!p)return{fips:[],label:""};const d=await fetchJson("https://api.zippopotam.us/us/"+p.state.toLowerCase()+"/"+encodeURIComponent(p.city),8e3);places=Array.isArray(d.places)?d.places:[];label=p.city+", "+p.state}const coords=[],seen=new Set;for(const p of places){if(p.latitude==null||p.longitude==null)continue;const key=Number(p.latitude).toFixed(4)+","+Number(p.longitude).toFixed(4);if(seen.has(key))continue;seen.add(key);coords.push(p);if(coords.length>=10)break}const settled=await Promise.allSettled(coords.map(p=>fipsForCoordinates(p.latitude,p.longitude)));return{fips:[...new Set(settled.filter(x=>x.status==="fulfilled").map(x=>x.value))],label}}function countyMatches(q){const n=normalize(q);if(n.length<2)return[];const tokens=n.split(" ");return data.counties.filter(c=>{const h=normalize(c.n+" "+c.s+" "+c.a);return tokens.every(t=>h.includes(t))}).sort((a,b)=>Number(b.v)-Number(a.v)||a.n.localeCompare(b.n)).slice(0,10)}function applyCards({query="",service="",state="",fips=[],countyRows=[]}){const cards=[...document.querySelectorAll("[data-provider-card]")];let shown=0;cards.forEach(card=>{const ok=(!service||card.dataset.services.split(/\s+/).includes(service))&&(!state||card.dataset.state===state)&&(!fips.length||fips.some(x=>card.dataset.fips.split(/\s+/).includes(x)))&&(fips.length||!query||normalize(query).split(" ").every(t=>normalize(card.dataset.search).includes(t)));card.hidden=!ok;if(ok)shown++});document.querySelector("[data-result-count]").textContent=shown+" source-reviewed provider"+(shown===1?"":"s")+" shown";const empty=document.querySelector("[data-empty]"),wrap=document.querySelector("[data-county-suggestions]");empty.hidden=shown>0;wrap.innerHTML="";if(!shown)countyRows.forEach(c=>{const a=document.createElement("a");a.href=c.u;a.textContent=(c.n+", "+c.s)+(c.v?" — open verified county guide":" — open county help page");wrap.appendChild(a)});return shown}async function search(){await loadData();const q=document.querySelector("[data-location-input]").value.trim(),service=document.querySelector("[data-service-filter]").value,state=document.querySelector("[data-state-filter]").value,status=document.querySelector("[data-search-status]");document.querySelector("[data-directory-text]").value=q;status.hidden=false;status.textContent="Checking county and service coverage…";let fips=[],label="",rows=[];const local=countyMatches(q),zip=/^\d{5}$/.test(q),city=parseCityState(q);if(q&&(zip||city)){try{const r=await remoteFips(q);fips=r.fips;label=r.label;rows=data.counties.filter(c=>fips.includes(c.f))}catch(e){status.textContent="The live city/ZIP resolver is unavailable. Try the county and state, or filter by state.";rows=local}}else if(q&&local.length){const exact=local.filter(c=>{const n=normalize(q);return[normalize(c.n),normalize(c.n+" "+c.s),normalize(c.n+" "+c.a)].includes(n)});rows=exact.length?exact:local;if(exact.length===1)fips=[exact[0].f]}const shown=applyCards({query:q,service,state,fips,countyRows:rows});if(fips.length)status.textContent=shown+" listing"+(shown===1?"":"s")+" with published coverage for "+(label||rows.map(c=>c.n+", "+c.a).join("; "))+". Confirm the exact property address before hiring.";else if(q&&local.length&&!shown)status.textContent="No current provider record matched that search. Open the county guide below and check back as coverage expands.";else status.textContent=shown+" source-reviewed listing"+(shown===1?"":"s")+" matched your filters.";const params=new URLSearchParams;if(q)params.set("q",q);if(service)params.set("service",service);if(state)params.set("state",state);history.replaceState(null,"",location.pathname+(params.toString()?"?"+params:""));track("septic_services_search",{result_count:shown,service:service||"all",location_type:zip?"zip":city?"city_state":q?"county_or_text":"none"})}function useLocation(){const status=document.querySelector("[data-search-status]");if(!navigator.geolocation){status.textContent="Location access is not supported in this browser.";return}status.textContent="Requesting your location…";navigator.geolocation.getCurrentPosition(async pos=>{try{await loadData();const f=await fipsForCoordinates(pos.coords.latitude,pos.coords.longitude),c=data.counties.find(x=>x.f===f);if(!c)throw new Error;document.querySelector("[data-location-input]").value=c.n+", "+c.a;await search()}catch(e){status.textContent="Your county could not be resolved. Enter a ZIP code, city and state, or county."}},()=>{status.textContent="Location permission was not granted. Enter a ZIP code, city and state, or county."},{timeout:1e4,maximumAge:3e5})}function init(){const form=document.querySelector("[data-service-search]");if(!form)return;form.addEventListener("submit",e=>{e.preventDefault();search()});document.querySelector("[data-use-location]").addEventListener("click",useLocation);document.querySelector("[data-directory-text]").addEventListener("change",e=>{document.querySelector("[data-location-input]").value=e.target.value;search()});document.querySelector("[data-state-filter]").addEventListener("change",search);const p=new URLSearchParams(location.search);document.querySelector("[data-location-input]").value=p.get("q")||"";document.querySelector("[data-directory-text]").value=p.get("q")||"";document.querySelector("[data-service-filter]").value=p.get("service")||"";document.querySelector("[data-state-filter]").value=p.get("state")||"";loadData().then(search).catch(()=>{document.querySelector("[data-search-status]").textContent="Directory filters are temporarily unavailable; all source-reviewed listings remain visible."})}document.addEventListener("DOMContentLoaded",init)})();'''


def build_html(provider_items: list[dict]) -> str:
    states = sorted({item["state"] for item in provider_items if item["state"]})
    state_options = "".join(f'<option value="{escape(state)}">{escape(state)}</option>' for state in states)
    cards = "".join(provider_card(item) for item in provider_items)
    county_count = len({fips for item in provider_items for fips in item["fips"]})
    service_count = len({label for item in provider_items for label in item["service_labels"]})
    schema = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": "Septic Services Near Me",
        "description": "Source-reviewed septic pumping, inspection, repair, installation and maintenance businesses with documented county coverage.",
        "numberOfItems": len(provider_items),
        "itemListElement": [
            {"@type": "ListItem", "position": index, "name": item["name"],
             "url": item["website"] or item["source"] or f"{DOMAIN}{PAGE_PATH}"}
            for index, item in enumerate(provider_items, 1)
        ],
    }
    faq = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "How does SepticScope decide which septic businesses appear?", "acceptedAnswer": {"@type": "Answer", "text": "A listing needs public business contact information, septic-service evidence, and a documented relationship to the county or service area shown. Search snippets and copied reviews are not publication evidence."}},
            {"@type": "Question", "name": "Are the businesses ranked or endorsed?", "acceptedAnswer": {"@type": "Answer", "text": "No. Ordinary listings use neutral ordering and are not recommendations. Property owners should confirm current service area, credentials, insurance, availability, job scope, and price."}},
            {"@type": "Question", "name": "Can a ZIP code cross county lines?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. ZIP and city searches use representative coordinates and may return more than one likely county. Confirm the property's legal county before relying on permit information or provider coverage."}},
        ],
    }
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Septic Services Near Me: Pumping, Inspection, Repair & Installation</title><meta name="description" content="Find source-reviewed septic services near you. Search by ZIP, city, county, state, or service for pumping, inspections, repair, installation, maintenance, drainfield work and more."><link rel="canonical" href="{DOMAIN}{PAGE_PATH}"><meta property="og:type" content="website"><meta property="og:title" content="Septic Services Near Me | SepticScope"><meta property="og:description" content="Search source-reviewed local septic pumping, inspection, repair, installation and maintenance businesses by location and service."><meta property="og:url" content="{DOMAIN}{PAGE_PATH}"><link rel="stylesheet" href="/assets/septic-services-near-me.css"><script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c")}</script><script type="application/ld+json">{json.dumps(faq, ensure_ascii=False).replace("<", "\\u003c")}</script></head><body>
<a class="ssn-skip" href="#main">Skip to content</a><header class="ssn-header"><nav class="ssn-nav" aria-label="Primary"><a class="ssn-brand" href="/"><span class="ssn-mark">SS</span><span>SepticScope</span></a><div class="ssn-links"><a href="/counties/">County guides</a><a href="/guides/">Homeowner guides</a><a href="/providers/">Provider directory</a><a class="ssn-nav-cta" href="{PAGE_PATH}">Septic Services Near Me</a></div></nav></header>
<main id="main"><section class="ssn-hero"><div class="ssn-hero-inner"><div><p class="ssn-eyebrow">Local support without fake rankings</p><h1>Septic Services Near Me</h1><p class="ssn-lede">Search publicly documented septic pumping, inspection, repair, installation, maintenance, drainfield, aerobic-system, and specialty providers by ZIP code, city, county, state, or service.</p><form class="ssn-search" data-service-search><div class="ssn-search-row"><label><span class="ssn-skip">Location</span><input data-location-input type="search" name="q" placeholder="ZIP, City + State, County, or business name" autocomplete="postal-code"></label><label><span class="ssn-skip">Service</span><select data-service-filter name="service"><option value="">All septic services</option><option value="pumping">Pumping & cleaning</option><option value="inspection">Inspections & home sales</option><option value="installation">Design & installation</option><option value="repair">Repair & drainfield work</option><option value="maintenance">Aerobic & routine maintenance</option><option value="commercial">Commercial & specialty</option></select></label><button type="submit">Find local service</button></div><div class="ssn-search-tools"><span>Try: <strong>85022</strong>, <strong>Knoxville, TN</strong>, or <strong>Horry County</strong></span><button class="ssn-use-location" type="button" data-use-location>Use my current location</button></div><p class="ssn-status" data-search-status aria-live="polite">Loading source-reviewed listings…</p></form></div><aside class="ssn-hero-card"><h2>What “source reviewed” means</h2><p>We open the company-owned website or an official public directory before publishing contact, service, and coverage information.</p><div class="ssn-checks"><div class="ssn-check"><strong>Documented geography</strong>County coverage is published by the business or an official source.</div><div class="ssn-check"><strong>Useful service detail</strong>Pumping, inspection, repair, installation, maintenance, and specialty work are labeled separately.</div><div class="ssn-check"><strong>No copied ratings</strong>Ordinary listings are neutral and not endorsements or “best company” rankings.</div></div></aside></div></section>
<div class="ssn-metrics"><div class="ssn-metric-grid"><div class="ssn-metric"><strong>{len(provider_items):,}</strong><span>source-reviewed businesses</span></div><div class="ssn-metric"><strong>{county_count:,}</strong><span>counties with provider coverage</span></div><div class="ssn-metric"><strong>{len(states):,}</strong><span>states represented</span></div><div class="ssn-metric"><strong>{service_count:,}</strong><span>service labels documented</span></div></div></div>
<section class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Browse and filter</p><h2>Local septic provider directory</h2></div><p>Search results reflect public service-area evidence—not distance, price, availability, review score, or a paid rank. Call before relying on a listing.</p></div><div class="ssn-filters"><input data-directory-text type="search" placeholder="Filter business, county, city, or service" aria-label="Filter directory text"><select data-state-filter aria-label="Filter by state"><option value="">All represented states</option>{state_options}</select><a class="ssn-button" href="/contact/">Suggest a business</a></div><div class="ssn-results-meta"><strong data-result-count>{len(provider_items):,} source-reviewed providers shown</strong><span>Last catalog review: {TODAY}</span></div><div class="ssn-provider-grid">{cards}</div><div class="ssn-empty" data-empty hidden><h3>No source-reviewed listing matched yet</h3><p>Directory coverage is expanding. Open the likely county page below for permit contacts and official local starting points, then independently verify any company you find.</p><div class="ssn-county-suggestions" data-county-suggestions></div><p><a href="/counties/">Browse every county and county-equivalent</a> · <a href="/contact/">Suggest a provider for review</a></p></div></section>
<section class="ssn-how"><div class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Choose the right professional</p><h2>Match the job to the service</h2></div><p>A pumper, inspector, installer, maintenance provider, site evaluator, designer, and repair contractor may have different credentials and scopes.</p></div><div class="ssn-how-grid"><article><h3>Routine pumping or cleaning</h3><p>Ask whether locating lids, exposing access, disposal, filters, and inspection observations are included. Pumping alone does not repair a failed drainfield.</p><a href="/guides/septic-tank-pumping-cost/">Understand pumping quotes →</a></article><article><h3>Inspection or home sale</h3><p>Confirm the inspection type, accessible components, pumping requirements, written report, and any local transfer rules before scheduling.</p><a href="/guides/septic-inspection-checklist/">Use the inspection checklist →</a></article><article><h3>Repair, design, or installation</h3><p>Start with the permitting authority. Soil, groundwater, setbacks, design flow, reserve area, and system type can determine which professional and permit are required.</p><a href="/counties/">Find county requirements →</a></article></div></div></section>
<section class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Practical homeowner help</p><h2>Know what to do before you call</h2></div></div><div class="ssn-quick-links"><a href="/guides/septic-system-failure-signs/">Warning signs and urgent next steps →</a><a href="/guides/septic-maintenance-checklist/">Maintenance checklist →</a><a href="/guides/types-of-septic-systems/">Identify the system type →</a><a href="/guides/septic-drainfield-repair-replacement/">Drainfield repair versus replacement →</a><a href="/guides/septic-tank-size-calculator/">Tank-size planning tool →</a><a href="/guides/septic-system-winter-care/">Frozen-system and winter guidance →</a></div></section>
<section class="ssn-section"><div class="ssn-section-title"><div><p class="ssn-eyebrow">Directory questions</p><h2>How to use these listings safely</h2></div></div><div class="ssn-faq"><details><summary>Are these businesses recommended or ranked?</summary><p>No. Ordinary listings use neutral ordering. Inclusion means we found publishable public contact, service, and geographic evidence; it is not a quality guarantee or endorsement.</p></details><details><summary>Does a county listing guarantee service to my address?</summary><p>No. Some businesses serve only part of a county or limit travel by job type. Confirm the exact property address and requested work directly with the business.</p></details><details><summary>How should I verify a septic contractor?</summary><p>Ask the local permitting authority which license, registration, certification, maintenance-provider authorization, insurance, or permit responsibility applies. Then confirm the business and individual performing the work.</p></details><details><summary>Why are some street addresses missing?</summary><p>Mobile service businesses do not always publish a customer-facing office. We show a street or mailing address only when a reviewed public source supports it; otherwise the card identifies the published service base.</p></details></div></section></main>
<footer class="ssn-footer"><div class="ssn-footer-inner"><div class="ssn-footer-links"><a href="/">Home</a><a href="/counties/">County septic guides</a><a href="/providers/">Provider directory</a><a href="/guides/">Homeowner guides</a><a href="/about/">Research standards</a><a href="/privacy/">Privacy</a><a href="/contact/">Corrections & feedback</a></div><small>© 2026 SepticScope. Independent informational resource; not a government agency. Current local agency instructions and current contractor credentials control.</small></div></footer><script src="/assets/septic-services-near-me.js" defer></script></body></html>'''


def ensure_sitemap() -> None:
    sitemap = SITE / "sitemap.xml"
    if not sitemap.exists():
        raise RuntimeError("sitemap.xml is missing")
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    tree = ET.parse(sitemap)
    root = tree.getroot()
    target = f"{DOMAIN}{PAGE_PATH}"
    matching = []
    for node in root.findall(f"{{{ns}}}url"):
        loc = node.find(f"{{{ns}}}loc")
        if loc is not None and clean(loc.text) == target:
            matching.append(node)
    for duplicate in matching[1:]:
        root.remove(duplicate)
    node = matching[0] if matching else ET.SubElement(root, f"{{{ns}}}url")
    loc = node.find(f"{{{ns}}}loc")
    if loc is None:
        loc = ET.SubElement(node, f"{{{ns}}}loc")
    loc.text = target
    lastmod = node.find(f"{{{ns}}}lastmod")
    if lastmod is None:
        lastmod = ET.SubElement(node, f"{{{ns}}}lastmod")
    lastmod.text = TODAY
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)


def build() -> None:
    if not SITE.is_dir() or not MANIFEST.exists():
        raise RuntimeError("Run the first production inventory before building the service locator")
    counties, county_items = load_counties()
    provider_items = [provider_payload(provider, counties) for provider in active_providers()]
    if not provider_items:
        raise RuntimeError("Septic Services Near Me requires at least one active source-reviewed provider")
    assets = SITE / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "septic-services-near-me.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (assets / "septic-services-near-me.js").write_text(JS.strip() + "\n", encoding="utf-8")
    data_dir = SITE / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1, "generated_at": TODAY,
        "method_note": "ZIP and city lookups use representative postal coordinates and public county geocoding. Provider cards use source-reviewed county relationships; confirm the exact address and current service area directly.",
        "providers": provider_items, "counties": county_items,
    }
    (data_dir / "septic-services-near-me.json").write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    out = SITE / PAGE_PATH.strip("/")
    out.mkdir(parents=True, exist_ok=True)
    html = build_html(provider_items)
    (out / "index.html").write_text(html, encoding="utf-8")
    ensure_sitemap()
    if html.lower().count("<h1") != 1 or ">Septic Services Near Me<" not in html:
        raise RuntimeError("Service locator heading integrity failure")
    if "noindex" in html.lower():
        raise RuntimeError("Populated service locator must be indexable")
    if len(county_items) != 3144:
        raise RuntimeError("Service locator county index is incomplete")
    if not all(item["phone"] and item["source"] and item["fips"] for item in provider_items):
        raise RuntimeError("Every service locator record needs a phone, source, and county")
    print(f"Septic Services Near Me complete: {len(provider_items):,} providers; {len({f for item in provider_items for f in item['fips']}):,} counties; {len({item['state'] for item in provider_items if item['state']}):,} states")


if __name__ == "__main__":
    build()
