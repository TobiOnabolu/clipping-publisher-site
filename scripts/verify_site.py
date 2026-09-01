#!/usr/bin/env python3
"""Black-box checks for the static TikTok review site."""

from __future__ import annotations

import struct
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "privacy.html", "terms.html")


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            values = dict(attrs)
            if values.get("href"):
                self.hrefs.append(values["href"] or "")


for page in PAGES:
    path = ROOT / page
    text = path.read_text(encoding="utf-8")
    assert "<title>" in text, f"{page}: missing title"
    parser = Links()
    parser.feed(text)
    for href in parser.hrefs:
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        assert (ROOT / href).is_file(), f"{page}: broken local link {href}"

forbidden = "client" + "_secret"
for path in ROOT.rglob("*"):
    if path.is_file() and ".git" not in path.parts:
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert forbidden not in text.lower(), f"secret-like text in {path}"

icon = ROOT / "app-icon.png"
data = icon.read_bytes()
assert data[:8] == b"\x89PNG\r\n\x1a\n", "app icon is not PNG"
width, height = struct.unpack(">II", data[16:24])
assert (width, height) == (1024, 1024), f"app icon is {width}x{height}"
assert icon.stat().st_size <= 5 * 1024 * 1024, "app icon exceeds 5 MB"

print("site verification passed")
