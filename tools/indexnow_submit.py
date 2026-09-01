#!/usr/bin/env python3
"""Submit changed SepticScope URLs to IndexNow after production deploys."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "septicscope.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
KEY_FILE = ROOT / "data" / "indexnow-key.txt"


def load_urls(path: Path) -> list[str]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    if isinstance(data, dict):
        data = data.get("changed_urls", [])
    if not isinstance(data, list):
        raise ValueError("URL input must be a JSON list, report object with changed_urls, or text file")
    urls = []
    for item in data:
        url = str(item).strip()
        if url.startswith(f"https://{DOMAIN}/") and url not in urls:
            urls.append(url)
    return urls[:10_000]


def submit(urls: list[str]) -> int:
    if not urls:
        print("IndexNow: no changed URLs to submit")
        return 0
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    payload = json.dumps({
        "host": DOMAIN,
        "key": key,
        "keyLocation": f"https://{DOMAIN}/{key}.txt",
        "urlList": urls,
    }).encode("utf-8")
    request = Request(
        ENDPOINT,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "SepticScopeIndexNow/1.0"},
    )
    try:
        with urlopen(request, timeout=30) as response:
            status = response.status
    except HTTPError as exc:
        if exc.code in {200, 202}:
            status = exc.code
        else:
            print(f"IndexNow submission failed with HTTP {exc.code}", file=sys.stderr)
            return 1
    except (URLError, TimeoutError, OSError) as exc:
        print(f"IndexNow submission failed: {type(exc).__name__}", file=sys.stderr)
        return 1
    if status not in {200, 202}:
        print(f"IndexNow returned unexpected status {status}", file=sys.stderr)
        return 1
    print(f"IndexNow accepted {len(urls)} changed URLs (HTTP {status})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url_file")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        assert len(KEY_FILE.read_text().strip()) >= 8
        print("PASS: IndexNow submitter self-test")
        return 0
    urls = load_urls(Path(args.url_file))
    if args.dry_run:
        print(json.dumps(urls, indent=2))
        return 0
    return submit(urls)


if __name__ == "__main__":
    raise SystemExit(main())
