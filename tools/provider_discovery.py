#!/usr/bin/env python3
"""Load the checksum-verified free official-source provider discovery implementation."""
from __future__ import annotations

import base64
import gzip
import hashlib
from pathlib import Path

PARTS = Path(__file__).with_name("provider_discovery_parts")
PART_COUNT = 4
SOURCE_SHA256 = "24ec64a4855709036d1f78cf8ac4a0e46f46697595c48ad1ee0e4fb74f89e098"

encoded = "".join(
    (PARTS / f"part{index:02d}.txt").read_text(encoding="utf-8").strip()
    for index in range(PART_COUNT)
)
source_bytes = gzip.decompress(base64.b64decode(encoded, validate=True))
actual = hashlib.sha256(source_bytes).hexdigest()
if actual != SOURCE_SHA256:
    raise RuntimeError(f"Provider discovery source checksum mismatch: {actual}")

# The preserved implementation originally had an optional paid-search branch. SepticScope
# now operates this job entirely from free official public sources. Rename the old secret
# lookup before compilation so a forgotten repository secret can never turn paid search on,
# and replace the obsolete warning with an accurate operating message.
source_text = source_bytes.decode("utf-8")
source_text = source_text.replace(
    "BRAVE_SEARCH_API_KEY",
    "SEPTICSCOPE_PAID_SEARCH_PERMANENTLY_DISABLED",
)
source_text = source_text.replace(
    "BRAVE_SEARCH_API_KEY is not configured; this run used official-source discovery only.",
    "This run used free official-source discovery; no paid search API is configured or required.",
)

exec(
    compile(
        source_text,
        str(Path(__file__).with_name("provider_discovery_impl.py")),
        "exec",
    ),
    globals(),
)
