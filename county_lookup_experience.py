#!/usr/bin/env python3
"""Build the public county/ZIP/city lookup used by the homepage and county hub."""
from __future__ import annotations

from collections import defaultdict
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
MANIFEST = SITE / "data" / "national-coverage-manifest.json"
DOMAIN = "https://septicscope.com"
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
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}

LOOKUP_CSS = r'''
.lookup-shell{max-width:1200px;margin:auto;padding:60px 22px}.lookup-intro{max-width:780px}.lookup-intro h1{font-size:clamp(2.35rem,5vw,4.25rem);line-height:1.04;letter-spacing:-.04em;color:var(--forest);margin:.15em 0}.lookup-intro p{font-size:1.08rem;color:var(--muted)}.county-lookup{margin-top:28px}.county-lookup-box{background:#fff;border:1px solid var(--line);border-radius:20px;padding:16px;box-shadow:var(--shadow)}.county-lookup-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px}.county-lookup-row input{width:100%;border:1px solid var(--line);border-radius:12px;padding:14px;font:650 1rem inherit}.county-lookup-row button{border:0;border-radius:12px;background:var(--forest);color:#fff;padding:14px 20px;font:850 1rem inherit;cursor:pointer}.county-lookup-tools{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;margin-top:10px;color:var(--muted);font-size:.88rem}.county-lookup-tools button{border:0;background:transparent;color:var(--forest2);padding:0;text-decoration:underline;font:800 .88rem inherit;cursor:pointer}.county-lookup-status{margin:14px 0 0;color:var(--muted)}.county-lookup-results{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:16px}.county-result{display:block;border:1px solid var(--line);border-radius:15px;padding:16px;background:#fff;text-decoration:none;color:var(--ink)}.county-result:hover{border-color:#9cb8ae;box-shadow:0 8px 24px rgba(18,61,53,.08)}.county-result-head{display:flex;align-items:flex-start;justify-content:space-between;gap:14px}.county-result h3{margin:0;color:var(--forest);font-size:1.1rem}.county-result-badge{flex:none;border-radius:999px;padding:4px 8px;background:var(--mint);color:var(--forest2);font-size:.73rem;font-weight:900}.county-result-badge.is-progress{background:#f3f0e8;color:#6f5c34}.county-result-meta{display:flex;flex-wrap:wrap;gap:8px 14px;color:var(--muted);font-size:.84rem;margin-top:8px}.county-result-authority{margin:10px 0 0;color:#44524e;font-size:.9rem}.county-result-action{display:block;margin-top:11px;font-weight:850;color:var(--forest2)}.lookup-note{border:1px solid #ead9b8;background:#fff8ed;border-radius:15px;padding:16px;margin-top:18px}.state-browse{margin-top:58px}.state-browse h2{font-size:clamp(1.8rem,3vw,2.6rem);color:var(--forest)}.state-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:11px}.state-card{border:1px solid var(--line);border-radius:13px;padding:14px;background:#fff;text-decoration:none;color:var(--ink)}.state-card strong{display:block;color:var(--forest)}.state-card span{display:block;color:var(--muted);font-size:.82rem;margin-top:4px}@media(max-width:900px){.state-grid{grid-template-columns:repeat(3,1fr)}}@media(max-width:700px){.county-lookup-results{grid-template-columns:1fr}.state-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:520px){.county-lookup-row{grid-template-columns:1fr}.state-grid{grid-template-columns:1fr}.county-result-head{display:block}.county-result-badge{display:inline-block;margin-top:8px}}
'''

COUNTY_LOOKUP_JS = r'''(function(){"use strict";let payload=null;const stateNames={AL:"Alabama",AK:"Alaska",AZ:"Arizona",AR:"Arkansas",CA:"California",CO:"Colorado",CT:"Connecticut",DE:"Delaware",DC:"District of Columbia",FL:"Florida",GA:"Georgia",HI:"Hawaii",ID:"Idaho",IL:"Illinois",IN:"Indiana",IA:"Iowa",KS:"Kansas",KY:"Kentucky",LA:"Louisiana",ME:"Maine",MD:"Maryland",MA:"Massachusetts",MI:"Michigan",MN:"Minnesota",MS:"Mississippi",MO:"Missouri",MT:"Montana",NE:"Nebraska",NV:"Nevada",NH:"New Hampshire",NJ:"New Jersey",NM:"New Mexico",NY:"New York",NC:"North Carolina",ND:"North Dakota",OH:"Ohio",OK:"Oklahoma",OR:"Oregon",PA:"Pennsylvania",RI:"Rhode Island",SC:"South Carolina",SD:"South Dakota",TN:"Tennessee",TX:"Texas",UT:"Utah",VT:"Vermont",VA:"Virginia",WA:"Washington",WV:"West Virginia",WI:"Wisconsin",WY:"Wyoming"};const stateAbbr=Object.fromEntries(Object.entries(stateNames).map(([abbr,name])=>[normalize(name),abbr]));function normalize(value){return String(value||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase().replace(/[^a-z0-9]+/g," ").trim()}function track(name,params){if(typeof window.gtag==="function")window.gtag("event",name,params||{})}async function fetchJson(url,timeout){const controller=new AbortController,timer=setTimeout(()=>controller.abort(),timeout||9000);try{const response=await fetch(url,{headers:{Accept:"application/json"},signal:controller.signal});if(!response.ok)throw new Error("HTTP "+response.status);return await response.json()}finally{clearTimeout(timer)}}async function loadPayload(){if(payload)return payload;payload=await fetchJson("/data/county-lookup.json",10000);return payload}function parseCityState(query){const raw=String(query||"").trim(),parts=raw.split(",").map(x=>x.trim()).filter(Boolean);let city="",state="";if(parts.length>1){city=parts.slice(0,-1).join(" ");state=parts.at(-1)}else{const words=raw.split(/\s+/),last=words.at(-1)||"",abbr=last.toUpperCase();if(stateNames[abbr]||stateAbbr[normalize(last)]){state=words.pop();city=words.join(" ")}}const abbreviation=stateNames[state.toUpperCase()]?state.toUpperCase():stateAbbr[normalize(state)];return city&&abbreviation?{city,state:abbreviation}:null}async function fipsForCoordinates(lat,lon){const fcc="https://geo.fcc.gov/api/census/block/find?latitude="+encodeURIComponent(lat)+"&longitude="+encodeURIComponent(lon)+"&format=json";try{const data=await fetchJson(fcc,8000),fips=data&&data.County&&String(data.County.FIPS||"").padStart(5,"0");if(fips)return fips}catch(error){}const census="https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x="+encodeURIComponent(lon)+"&y="+encodeURIComponent(lat)+"&benchmark=Public_AR_Current&vintage=Current_Current&format=json",data=await fetchJson(census,9000),rows=data&&data.result&&data.result.geographies&&data.result.geographies.Counties,county=Array.isArray(rows)?rows[0]:null;if(county)return String(county.STATE||"").padStart(2,"0")+String(county.COUNTY||"").padStart(3,"0");throw new Error("County could not be resolved")}async function remoteFips(query){const zip=String(query||"").trim().match(/^\d{5}$/);let places=[],label="";if(zip){const data=await fetchJson("https://api.zippopotam.us/us/"+zip[0],8000);places=Array.isArray(data.places)?data.places:[];label="ZIP "+zip[0]}else{const parsed=parseCityState(query);if(!parsed)return{fips:[],label:""};const data=await fetchJson("https://api.zippopotam.us/us/"+parsed.state.toLowerCase()+"/"+encodeURIComponent(parsed.city),8000);places=Array.isArray(data.places)?data.places:[];label=parsed.city+", "+parsed.state}const coordinates=[],seen=new Set;for(const place of places){if(place.latitude==null||place.longitude==null)continue;const key=Number(place.latitude).toFixed(4)+","+Number(place.longitude).toFixed(4);if(seen.has(key))continue;seen.add(key);coordinates.push(place);if(coordinates.length>=12)break}const settled=await Promise.allSettled(coordinates.map(place=>fipsForCoordinates(place.latitude,place.longitude)));return{fips:[...new Set(settled.filter(item=>item.status==="fulfilled").map(item=>item.value))],label}}function localMatches(query){const normalized=normalize(query),fipsMatch=normalized.match(/^(?:fips|county code|county fips)\s*(\d{5})$/);if(fipsMatch){const row=payload.counties.find(item=>item.f===fipsMatch[1]);return row?[row]:[]}if(normalized.length<2)return[];const tokens=normalized.split(" ");return payload.counties.filter(item=>{const haystack=normalize(item.n+" "+item.s+" "+item.a+" "+item.f);return tokens.every(token=>haystack.includes(token))}).sort((a,b)=>Number(b.v)-Number(a.v)||a.s.localeCompare(b.s)||a.n.localeCompare(b.n)).slice(0,50)}function escapeText(value){return String(value||"")}function resultCard(row){const link=document.createElement("a");link.className="county-result";link.href=row.u;const head=document.createElement("div");head.className="county-result-head";const title=document.createElement("h3");title.textContent=row.n+", "+row.s;const badge=document.createElement("span");badge.className="county-result-badge"+(row.v?"":" is-progress");badge.textContent=row.v?"Verified guide":"Official help page";head.append(title,badge);const meta=document.createElement("div");meta.className="county-result-meta";const code=document.createElement("span");code.textContent="County FIPS code: "+row.f;const status=document.createElement("span");status.textContent=row.v?(row.r?"Sources reviewed "+row.r:"Source checked"):("County-specific research in progress");meta.append(code,status);link.append(head,meta);if(row.o){const authority=document.createElement("p");authority.className="county-result-authority";authority.textContent="Permitting authority: "+row.o;link.append(authority)}const action=document.createElement("span");action.className="county-result-action";action.textContent=row.v?"Open county septic information →":"Open official starting points →";link.append(action);return link}function render(root,rows,message){const results=root.querySelector("[data-county-results]"),status=root.querySelector("[data-county-status]");results.innerHTML="";rows.forEach(row=>results.append(resultCard(row)));status.textContent=message;status.hidden=false}async function runSearch(root){await loadPayload();const input=root.querySelector("[data-county-input]"),query=input.value.trim();if(!query){render(root,[],"Enter a ZIP code, city and state, county and state, or FIPS county code.");return}const local=localMatches(query),isZip=/^\d{5}$/.test(query),cityState=parseCityState(query);if(isZip||cityState){root.querySelector("[data-county-status]").textContent="Resolving the location to its county or counties…";try{const resolved=await remoteFips(query),rows=payload.counties.filter(row=>resolved.fips.includes(row.f));if(rows.length){render(root,rows,rows.length===1?"Found the county associated with "+resolved.label+". ZIP and city boundaries can cross county lines, so confirm the property address.":"Found "+rows.length+" possible counties for "+resolved.label+". Confirm the property's legal county before relying on permit information.");track("county_lookup_search",{search_type:isZip?"zip":"city_state",result_count:rows.length});return}render(root,local,"The live location resolver did not return a county. Try the county and state, or browse by state below.");return}catch(error){render(root,local,"The live ZIP/city resolver is temporarily unavailable. Search the county and state instead, or browse by state below.");return}}render(root,local,local.length?"Showing "+local.length+" matching county"+(local.length===1?"":" results")+".":"No county matched that search. Try the county name plus state, or type a county code as FIPS 48121.");track("county_lookup_search",{search_type:normalize(query).startsWith("fips")?"fips":"county_text",result_count:local.length})}function useLocation(root){const status=root.querySelector("[data-county-status]");if(!navigator.geolocation){status.textContent="Location access is not supported by this browser.";return}status.hidden=false;status.textContent="Requesting your location…";navigator.geolocation.getCurrentPosition(async position=>{try{await loadPayload();const fips=await fipsForCoordinates(position.coords.latitude,position.coords.longitude),row=payload.counties.find(item=>item.f===fips);if(!row)throw new Error("not found");root.querySelector("[data-county-input]").value=row.n+", "+row.a;render(root,[row],"Found your likely county. Confirm the legal county shown in the property record before relying on permit information.");track("county_lookup_search",{search_type:"geolocation",result_count:1})}catch(error){status.textContent="Your county could not be resolved. Enter a ZIP code, city and state, or county and state."}},()=>{status.textContent="Location permission was not granted. Enter a ZIP code, city and state, or county and state."},{timeout:10000,maximumAge:300000})}function initRoot(root){const form=root.querySelector("[data-county-form]");if(!form)return;form.addEventListener("submit",event=>{event.preventDefault();runSearch(root)});const locate=root.querySelector("[data-use-location]");if(locate)locate.addEventListener("click",()=>useLocation(root));const params=new URLSearchParams(location.search),query=params.get("q");if(query){root.querySelector("[data-county-input]").value=query;loadPayload().then(()=>runSearch(root)).catch(()=>{})}}document.addEventListener("DOMContentLoaded",()=>{document.querySelectorAll("[data-county-lookup-root]").forEach(initRoot);loadPayload().catch(()=>{})})})();'''


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def load_records() -> list[dict]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = data.get("records", [])
    if len(records) != 3144:
        raise RuntimeError(f"County lookup requires 3,144 records; found {len(records)}")
    return records


def compact_records(records: list[dict]) -> list[dict]:
    compact = []
    for record in records:
        state = clean(record.get("state"))
        url = clean(record.get("page_url"))
        fips = clean(record.get("fips"))
        if not re.fullmatch(r"\d{5}", fips) or not url.startswith(DOMAIN + "/"):
            continue
        compact.append({
            "f": fips,
            "n": clean(record.get("county_or_equivalent_name")),
            "s": state,
            "a": clean(record.get("state_abbreviation")) or STATE_ABBR.get(state, ""),
            "u": url.removeprefix(DOMAIN),
            "v": record.get("verification_status") == "verified",
            "o": clean(record.get("official_regulating_authority")),
            "r": clean(record.get("date_last_reviewed")),
        })
    if len(compact) != 3144 or len({row["f"] for row in compact}) != 3144:
        raise RuntimeError("County lookup payload does not contain 3,144 unique FIPS records")
    compact.sort(key=lambda row: (row["s"], row["n"]))
    return compact


def state_cards(records: list[dict]) -> str:
    states: dict[str, dict] = defaultdict(lambda: {"total": 0, "verified": 0})
    for record in records:
        state = clean(record.get("state"))
        states[state]["total"] += 1
        states[state]["verified"] += int(record.get("verification_status") == "verified")
    return "".join(
        f'<a class="state-card" href="/counties/{escape(slugify(state))}/"><strong>{escape(state)}</strong>'
        f'<span>{values["verified"]} verified guides · {values["total"]} counties/equivalents</span></a>'
        for state, values in sorted(states.items())
    )


def lookup_form() -> str:
    return '''<div class="county-lookup" data-county-lookup-root><div class="county-lookup-box"><form data-county-form><div class="county-lookup-row"><label><span class="ssn-skip">Property location or county code</span><input data-county-input name="q" type="search" autocomplete="postal-code" placeholder="ZIP, City + State, County + State, or FIPS 48121"></label><button type="submit">Find county information</button></div><div class="county-lookup-tools"><span>Examples: <strong>75068</strong>, <strong>Oak Point, TX</strong>, <strong>Denton County, Texas</strong>, or <strong>FIPS 48121</strong></span><button data-use-location type="button">Use my current location</button></div></form><p class="county-lookup-status" data-county-status aria-live="polite">Search all 3,144 U.S. counties and county-equivalents.</p><div class="county-lookup-results" data-county-results></div></div></div>'''


def write_directory(records: list[dict]) -> None:
    verified = sum(record.get("verification_status") == "verified" for record in records)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>County Septic Permit, FIPS Code & Official Information Lookup</title><meta name="description" content="Search by ZIP, city and state, county and state, or county FIPS code to find the correct SepticScope permit guide, official authority, records starting points, and local septic information."><link rel="canonical" href="{DOMAIN}/counties/"><meta property="og:type" content="website"><meta property="og:title" content="U.S. County Septic Information Lookup | SepticScope"><meta property="og:description" content="Find county septic permit guidance, official contacts, source status, and county FIPS codes by ZIP, city, county, or code."><meta property="og:url" content="{DOMAIN}/counties/"><link rel="stylesheet" href="/assets/septic-services-near-me.css"><style>{LOOKUP_CSS}</style><script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}');</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script><script defer src="/assets/county-lookup.js"></script></head><body><a class="ssn-skip" href="#main">Skip to content</a><header class="ssn-header"><nav class="ssn-nav" aria-label="Primary"><a class="ssn-brand" href="/"><span class="ssn-mark">SS</span><span>SepticScope</span></a><div class="ssn-links"><a class="ssn-nav-cta" href="/counties/">County lookup</a><a href="/guides/">Homeowner guides</a><a href="/faq/">FAQs</a><a href="/about/">Research standards</a></div></nav></header><main id="main"><section class="lookup-shell"><div class="lookup-intro"><p class="ssn-eyebrow">County permits, records, codes, and official contacts</p><h1>Find county septic information</h1><p>Search the property location or a county FIPS code. SepticScope will take you to a source-checked county guide when one is complete, or a clearly labeled official-help page while local research is still in progress.</p></div>{lookup_form()}<div class="lookup-note"><strong>Why the county matters:</strong> septic permitting may be handled by a county, health district, municipality, state agency, or delegated office. ZIP and city boundaries can cross county lines. Confirm the legal county in the property record before filing, buying, designing, or starting work.</div><section class="state-browse"><p class="ssn-eyebrow">Browse without searching</p><h2>All states and the District of Columbia</h2><p><strong>{verified:,}</strong> county guides are currently source-verified. Every remaining county page provides official government starting points without pretending its local rules are already complete.</p><div class="state-grid">{state_cards(records)}</div></section></section></main><footer class="ssn-footer"><div class="ssn-footer-inner"><div class="ssn-footer-links"><a href="/">Home</a><a href="/counties/">County lookup</a><a href="/guides/">Homeowner guides</a><a href="/faq/">FAQs</a><a href="/about/">About our research</a><a href="/privacy/">Privacy</a><a href="/contact/">Corrections & feedback</a></div><small>© 2026 SepticScope. Independent informational resource; not a government agency. Current agency instructions control.</small></div></footer></body></html>'''
    out = SITE / "counties"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")


def main() -> None:
    if not SITE.is_dir() or not MANIFEST.exists():
        raise RuntimeError("Run the first site inventory before county lookup generation")
    records = load_records()
    compact = compact_records(records)
    assets = SITE / "assets"
    data_dir = SITE / "data"
    assets.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    (assets / "county-lookup.js").write_text(COUNTY_LOOKUP_JS.strip() + "\n", encoding="utf-8")
    (data_dir / "county-lookup.json").write_text(
        json.dumps({"schema_version": 1, "record_count": len(compact), "counties": compact}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    write_directory(records)
    if "data-county-lookup-root" not in (SITE / "counties" / "index.html").read_text(encoding="utf-8"):
        raise RuntimeError("County lookup interface was not generated")
    print(f"County lookup experience complete: {len(compact):,} searchable counties and county-equivalents")


if __name__ == "__main__":
    main()
