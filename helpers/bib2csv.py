#!/usr/bin/env python3
"""
Extract citekey, title, doi from a BibTeX file and write to CSV.

Usage:
  python bib_extract.py final-dataset.bib out.csv
"""

from __future__ import annotations
import csv
import re
import sys
from pathlib import Path

ENTRY_START_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)
FIELD_RE = re.compile(
    r"(?P<name>\w+)\s*=\s*"
    r"(?P<value>"
    r"\{(?:[^{}]|\{[^{}]*\})*\}"   # {...} with one-level nested braces tolerated
    r"|\"(?:\\.|[^\"])*\""        # "..."
    r"|[^,\n]+)"                  # bare value
    r"\s*,?",
    re.IGNORECASE,
)

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)

def strip_wrapping(value: str) -> str:
    value = value.strip()
    if value.startswith("{") and value.endswith("}"):
        value = value[1:-1].strip()
    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1].strip()
    return value

def normalize_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def parse_entries(text: str) -> list[tuple[str, str]]:
    """
    Return list of (citekey, entry_text) blocks.
    Splits on lines starting with '@', keeping simple robustness.
    """
    parts = re.split(r"(?=^\s*@)", text, flags=re.MULTILINE)
    out = []
    for part in parts:
        part = part.strip()
        if not part.startswith("@"):
            continue
        m = ENTRY_START_RE.search(part)
        if not m:
            continue
        citekey = m.group(1).strip()
        out.append((citekey, part))
    return out

def extract_field(entry_text: str, field_name: str) -> str:
    # Find all fields; last one wins if duplicates
    fields = {}
    for m in FIELD_RE.finditer(entry_text):
        name = m.group("name").lower()
        val = strip_wrapping(m.group("value"))
        fields[name] = val
    return fields.get(field_name.lower(), "")

def extract_doi(entry_text: str) -> str:
    doi = extract_field(entry_text, "doi")
    if doi:
        doi = normalize_whitespace(doi)
        # Sometimes doi is wrapped like {https://doi.org/...}
        m = DOI_RE.search(doi)
        return m.group(0) if m else doi
    # Fallback: search anywhere
    m = DOI_RE.search(entry_text)
    return m.group(0) if m else ""

def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python bib_extract.py final-dataset.bib out.csv", file=sys.stderr)
        return 2

    bib_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    text = bib_path.read_text(encoding="utf-8", errors="replace")

    rows = []
    for citekey, entry in parse_entries(text):
        title = extract_field(entry, "title")
        title = normalize_whitespace(title)
        doi = extract_doi(entry)
        doi = normalize_whitespace(doi)
        rows.append({"citekey": citekey, "title": title, "doi": doi})

    # Optional: keep only rows with at least one of title/doi
    # rows = [r for r in rows if r["title"] or r["doi"]]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["citekey", "title", "doi"])
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {len(rows)} rows to {out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
