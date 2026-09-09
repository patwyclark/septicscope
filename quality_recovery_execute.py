#!/usr/bin/env python3
"""Execute quality_recovery with correct nested skip-section handling.

Provider and automated-related-link modules are excluded from county originality and
word-count scoring. The original parser increments its skip depth for those marked
sections but cannot see their attributes on the closing tag. This runner tracks the
exact marked element depth so content after the module—especially Official sources—is
still evaluated.
"""
from __future__ import annotations

from collections import Counter
import sys

import quality_recovery as recovery


class FixedParser(recovery.Parser):
    def __init__(self) -> None:
        super().__init__()
        self._element_depths: Counter[str] = Counter()
        self._marked_skip_stack: list[tuple[str, int]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self._element_depths[tag] += 1
        attr = {str(key).lower(): str(value or "") for key, value in attrs}
        marked = (
            attr.get("data-septicscope-provider-section") == "1"
            or attr.get("data-septicscope-growth-links") == "1"
        )
        super().handle_starttag(tag, attrs)
        if marked:
            self._marked_skip_stack.append((tag, self._element_depths[tag]))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        depth = self._element_depths.get(tag, 0)
        super().handle_endtag(tag)
        if self._marked_skip_stack and self._marked_skip_stack[-1] == (tag, depth):
            self._marked_skip_stack.pop()
            if self._skip_depth:
                self._skip_depth -= 1
        if depth > 1:
            self._element_depths[tag] -= 1
        else:
            self._element_depths.pop(tag, None)


recovery.Parser = FixedParser


if __name__ == "__main__":
    raise SystemExit(recovery.main())
