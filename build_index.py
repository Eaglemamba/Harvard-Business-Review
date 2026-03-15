#!/usr/bin/env python3
"""
build_index.py — Auto-regenerate docs/index.html article list
==============================================================
Scans all HTML files in docs/, reads dashboard_meta tags, and
replaces the AUTO-GENERATED block in docs/index.html.

Usage:
    python3 build_index.py

Run this after adding any new article HTML files to docs/.
The /hbr-single and /hbr-batch commands run this automatically.
"""

import os
import re
import json
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "docs"
INDEX_FILE = DOCS_DIR / "index.html"

# Markers in index.html that bracket the auto-generated section
START_MARKER = "// ── Article Data ─────────────────── AUTO-GENERATED START ───────"
END_MARKER   = "// ── AUTO-GENERATED END ───────────────────────────────────────────"


def extract_meta(html_path: Path):
    """Extract doc-* meta tags from an HTML file. Returns None if incomplete."""
    text = html_path.read_text(encoding="utf-8")

    def get(name):
        m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', text)
        return m.group(1).strip() if m else ""

    date    = get("doc-date")
    title   = get("doc-title")
    source  = get("doc-source")
    tags    = get("doc-tags")
    rating  = get("doc-rating")
    summary = get("doc-summary")
    file    = get("doc-file")

    # Skip if missing required fields
    if not (date and title and file):
        print(f"  [SKIP] {html_path.name} — missing required meta tags")
        return None

    return {
        "file":    file or html_path.name,
        "title":   title,
        "source":  source,
        "date":    date,
        "tags":    [t.strip() for t in tags.split(",") if t.strip()] if tags else [],
        "rating":  rating or "0.0",
        "summary": summary,
    }


def build_articles_js(articles) -> str:
    """Render articles list as a JS const articles = [...] block."""
    D = "        "   # 8-space base indent (matches script block in index.html)
    I = "    "       # 4-space relative indent

    def js(val):
        return json.dumps(val, ensure_ascii=False)

    lines = [
        f"{D}{START_MARKER}",
        f"{D}// Do not edit this block manually — run: python3 build_index.py",
        f"{D}const articles = ["
    ]
    for i, a in enumerate(articles):
        comma = "" if i == len(articles) - 1 else ","
        lines.append(f"{D}{I}{{")
        lines.append(f"{D}{I}{I}file: {js(a['file'])},")
        lines.append(f"{D}{I}{I}title: {js(a['title'])},")
        lines.append(f"{D}{I}{I}source: {js(a['source'])},")
        lines.append(f"{D}{I}{I}date: {js(a['date'])},")
        lines.append(f"{D}{I}{I}tags: {js(a['tags'])},")
        lines.append(f"{D}{I}{I}rating: {js(a['rating'])},")
        lines.append(f"{D}{I}{I}summary: {js(a['summary'])}")
        lines.append(f"{D}{I}}}{comma}")
    lines.append(f"{D}];")
    lines.append(f"{D}{END_MARKER}")
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("HBR Index Builder")
    print("=" * 60)

    # Scan docs/ for article HTML files
    html_files = sorted(
        [f for f in DOCS_DIR.glob("*.html") if f.name != "index.html"]
    )
    print(f"[INFO] Found {len(html_files)} HTML files in docs/")

    articles = []
    for f in html_files:
        meta = extract_meta(f)
        if meta:
            articles.append(meta)
            print(f"  [OK] {f.name} — {meta['date']} ★{meta['rating']}")

    # Sort newest first
    articles.sort(key=lambda a: a["date"], reverse=True)

    # Read current index.html
    index_text = INDEX_FILE.read_text(encoding="utf-8")

    # Locate and replace the auto-generated block
    start_idx = index_text.find(START_MARKER)
    end_idx   = index_text.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print("[ERROR] Could not find AUTO-GENERATED markers in index.html")
        print("        Add the following markers to docs/index.html:")
        print(f"        {START_MARKER}")
        print(f"        {END_MARKER}")
        return

    # Replace from start of START_MARKER line to end of END_MARKER line
    line_start = index_text.rfind("\n", 0, start_idx) + 1
    end_of_end_line = index_text.find("\n", end_idx + len(END_MARKER))
    if end_of_end_line == -1:
        end_of_end_line = len(index_text)
    else:
        end_of_end_line += 1  # include the newline

    new_block = build_articles_js(articles)
    new_index = index_text[:line_start] + new_block + "\n" + index_text[end_of_end_line:]

    INDEX_FILE.write_text(new_index, encoding="utf-8")

    print(f"\n[SUCCESS] docs/index.html updated with {len(articles)} articles")
    print("=" * 60)


if __name__ == "__main__":
    main()
