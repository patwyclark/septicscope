#!/usr/bin/env python3
"""Keep Cloudflare Pages redirects within limits during quality recovery.

Thousands of county redirects would exceed Cloudflare Pages' 2,000 static-rule limit.
Quality-withheld county pages therefore remain 200/noindex/ad-free so crawlers can see
the noindex directive, while only true consolidation and legacy routes redirect.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
REDIRECTS = SITE / "_redirects"
STATIC_LIMIT = 2000
DYNAMIC_LIMIT = 100


def main() -> None:
    if not REDIRECTS.exists():
        raise RuntimeError("Generated _redirects file is missing")
    raw = REDIRECTS.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    output: list[str] = []
    in_recovery = False
    removed_county_redirects = 0
    consolidated_faq_redirects = 0

    for line in lines:
        stripped = line.strip()
        if stripped == "# BEGIN ADSENSE QUALITY RECOVERY":
            in_recovery = True
            output.append(line)
            continue
        if stripped == "# END ADSENSE QUALITY RECOVERY":
            in_recovery = False
            output.append(line)
            continue
        if in_recovery and stripped.startswith("/counties/"):
            removed_county_redirects += 1
            continue
        if in_recovery and re.match(r"^/faq/[^\s]+\s+/faq/\s+302$", stripped):
            output.append(re.sub(r"\s+302$", " 301", line))
            consolidated_faq_redirects += 1
            continue
        output.append(line)

    cleaned = "\n".join(output).rstrip() + "\n"
    REDIRECTS.write_text(cleaned, encoding="utf-8")

    static_rules = 0
    dynamic_rules = 0
    for line in cleaned.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        source = stripped.split()[0]
        if "*" in source or re.search(r"/[A-Za-z][A-Za-z0-9_]*:", source) or re.search(r"/:[A-Za-z]", source):
            dynamic_rules += 1
        else:
            static_rules += 1
    if static_rules > STATIC_LIMIT or dynamic_rules > DYNAMIC_LIMIT:
        raise RuntimeError(
            f"Cloudflare Pages redirect budget exceeded: {static_rules} static, {dynamic_rules} dynamic"
        )
    if any(
        line.strip().startswith("/counties/")
        for line in cleaned.splitlines()[
            cleaned.splitlines().index("# BEGIN ADSENSE QUALITY RECOVERY") + 1:
            cleaned.splitlines().index("# END ADSENSE QUALITY RECOVERY")
        ]
    ):
        raise RuntimeError("Per-county quality-recovery redirects remain")
    print(
        f"Redirect hygiene complete: removed {removed_county_redirects} county redirects; "
        f"made {consolidated_faq_redirects} FAQ consolidations permanent; "
        f"final budget {static_rules} static/{dynamic_rules} dynamic"
    )


if __name__ == "__main__":
    main()
