"""Build SepticScope's national homepage, search, and local-service experience."""
from __future__ import annotations

from septicscope_experience_common import *  # noqa: F401,F403
from septicscope_experience_home import write_county_directory, write_homepage
from septicscope_experience_services import (
    inject_provider_sections,
    patch_privacy,
    write_provider_directory,
)

def assert_full_output(providers: list[dict[str, Any]]) -> None:
    home = (SITE / "index.html").read_text(encoding="utf-8", errors="replace")
    if "ZIP code, city and state, or county" not in home:
        raise RuntimeError("Homepage location search was not generated")
    if "indiana/index.html" in home.lower() or ">Indiana rules<" in home:
        raise RuntimeError("Legacy Indiana homepage promotion remains")
    if len(providers) < 7:
        raise RuntimeError("Initial provider pilot unexpectedly regressed")
    for path in (SITE / "assets" / "septicscope-home.css", SITE / "assets" / "septicscope-home-components.css", SITE / "assets" / "location-search.js", SITE / "assets" / "local-services.css", SITE / "data" / "county-search.json"):
        if not path.exists() or path.stat().st_size < 500:
            raise RuntimeError(f"Required experience asset is missing or empty: {path}")
    for relative, business in (
        ("counties/texas/denton/index.html", "Howdeshell Site Services"),
        ("counties/texas/collin/index.html", "Collin County Septic Design &amp; Evaluation"),
    ):
        page = SITE / relative
        if not page.exists() or business not in page.read_text(encoding="utf-8", errors="replace"):
            raise RuntimeError(f"Local service pilot was not injected into {relative}")

def assert_directory_output(providers: list[dict[str, Any]]) -> None:
    page = (SITE / "providers" / "index.html").read_text(encoding="utf-8", errors="replace")
    for provider in providers:
        if html.escape(provider["business_name"]) not in page:
            raise RuntimeError(f"Provider directory is missing {provider['business_name']}")
    if "noindex" in page.lower():
        raise RuntimeError("Populated provider directory must be indexable")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory-only", action="store_true")
    args = parser.parse_args()
    if not SITE.is_dir():
        raise RuntimeError("site/ does not exist; run the core build first")
    records = county_records()
    providers = load_providers()
    if args.directory_only:
        write_provider_directory(records, providers)
        patch_privacy()
        assert_directory_output(providers)
        print(f"Local service directory finalized: {len(providers)} provider listings")
        return

    copy_assets()
    write_county_search_data(records)
    write_homepage(records, providers)
    write_county_directory(records)
    injected = inject_provider_sections(records, providers)
    write_provider_directory(records, providers)
    patch_privacy()
    assert_full_output(providers)
    assert_directory_output(providers)
    print(
        "National homepage and local-service experience complete: "
        f"ZIP/city/county search enabled; {len(providers)} providers across {injected} county pages"
    )


if __name__ == "__main__":
    main()
