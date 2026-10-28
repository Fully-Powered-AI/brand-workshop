#!/usr/bin/env python3
"""The mechanical half of the fresh pass: the brand document against the owner's recorded choices.

Usage: python3 -I check_choices.py CHOICES_RECORD.md BRAND_DOCUMENT.md

For each decision block in the record (pair, purpose line, category, positioning statement, dimensions,
adjectives): at least three candidates were offered, each saying what it commits the company to; a
recommendation was named; the owner's words were recorded; and every "Chosen:" line appears, word for
word after whitespace, emphasis and quote normalisation, in the section of the reader-first document
(owner's amendment 6) that decision governs: Purpose, Category, Positioning statement, Personality.
The dimensions decision is checked for its record only: the document carries the five traits, not the
two dimensions behind them, so its "Chosen:" line is not looked for in the document. A document section
that is filled with no recorded decision fails: either the skill chose, or the record is incomplete.
When a decision has several blocks (a revision), the last block in the file is the one checked (the
record is appended to, so the last is the latest); the earlier ones are history. A section marked TBD needs no decision.

The rest of the fresh pass is reading: does the In short paragraph, the Voice section and the persona follow the
choices in spirit. This script does not do that and says so.

Exit 0: PASS (mechanical part). Exit 1: FAIL, or a file could not be read.
"""
import re
import sys
from pathlib import Path

GOVERNS = {
    "pair": "Purpose",
    "purpose line": "Purpose",
    "category": "Category",
    "positioning statement": "Positioning statement",
    "dimensions": "Personality",
    "adjectives": "Personality",
}
RECORD_ONLY = {"dimensions"}  # chosen in the working notes; the document carries the traits they produced
MIN_CANDIDATES = 3  # the protocol: several candidates that differ in substance; fewer than three is a wording choice


def norm(s):
    s = s.replace("*", "").replace("_", "")
    s = s.strip().strip('"“”\'').rstrip(".").lower()
    s = s.replace("’", "'").replace("‘", "'").replace("—", "-").replace("–", "-")
    return re.sub(r"\s+", " ", s)


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as e:
        print(f"FAIL cannot read {path}: {e}")
        print("RESULT: FAIL")
        sys.exit(1)


def blocks(lines, pattern):
    """Blocks by heading. A later block with the same heading supersedes the earlier one: the record is
    appended to, never rewritten, so a revised choice is a new block and the document carries the latest."""
    out, key = {}, None
    for line in lines:
        m = re.match(pattern, line)
        if m:
            key = m.group(1).strip()
            out[key] = []
            continue
        if key is not None:
            out[key].append(line)
    return out


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        print("RESULT: FAIL (usage)")
        sys.exit(1)
    record = blocks(read(sys.argv[1]), r"^## Decision: (.+?)\s*$")
    doc = blocks(read(sys.argv[2]), r"^## (.+?)\s*$")
    fails = []
    if not record:
        fails.append("the choices record has no '## Decision: ...' block")
    if not doc:
        fails.append("the brand document has no '## ...' sections")

    def section_text(h):
        body = doc.get(h)
        if body is None:
            return None, False
        content = [l for l in body if l.strip()]
        first = content[0].strip().upper() if content else ""
        tbd = first == "TBD" or first.startswith("**TBD")
        return norm(" ".join(content)), tbd

    checked = 0
    for key, body in record.items():
        if key not in GOVERNS:
            fails.append(f"decision '{key}' is not one of {sorted(GOVERNS)}; the record's decision names are fixed")
            continue
        text = "\n".join(body)
        if "{{" in text:
            fails.append(f"decision '{key}': unfilled placeholder in the record")
        cands = [l for l in body if re.match(r"^- [A-Z]\d*: ", l)]
        if len(cands) < MIN_CANDIDATES:
            fails.append(f"decision '{key}': {len(cands)} candidate(s) offered; at least {MIN_CANDIDATES}, differing in substance, so the owner had a real choice")
        for c in cands:
            if "commits the company to" not in c or not c.split("commits the company to", 1)[1].strip():
                fails.append(f"decision '{key}': a candidate does not say what it commits the company to: {c[:60]}")
        if not any(l.startswith("Recommendation:") and l[15:].strip() for l in body):
            fails.append(f"decision '{key}': no 'Recommendation:' line (the skill's view is given, named as the skill's)")
        if not any(l.startswith("Recorded:") and re.search(r"\d{4}-\d{2}-\d{2}", l) for l in body):
            fails.append(f"decision '{key}': no 'Recorded: YYYY-MM-DD' line")
        if not any(l.startswith("Owner's words:") and l[14:].strip() for l in body):
            fails.append(f"decision '{key}': no 'Owner's words:' line; the choice is the owner's and is recorded in the owner's words")
        chosen = [l[7:].strip() for l in body if l.startswith("Chosen:") and l[7:].strip()]
        if not chosen:
            fails.append(f"decision '{key}': no 'Chosen:' line; a decision without a recorded choice was not made by the owner")
            continue
        sect, tbd = section_text(GOVERNS[key])
        if sect is None:
            fails.append(f"decision '{key}': the document has no section '{GOVERNS[key]}'")
            continue
        if tbd:
            fails.append(f"decision '{key}' is recorded but section '{GOVERNS[key]}' is TBD; either the section was not written or the record is from another run")
            continue
        if key in RECORD_ONLY:
            continue
        for ch in chosen:
            needle = norm(re.sub(r"^(Who|That|Unlike|Differentiator|Because of|Is a|For):\s*", "", ch))
            if needle not in sect:
                fails.append(f"decision '{key}': the chosen text is not in section '{GOVERNS[key]}' word for word: \"{ch[:70]}\"")
            checked += 1

    # A filled section whose decision is missing from the record.
    for key, h in GOVERNS.items():
        sect, tbd = section_text(h)
        if sect is not None and not tbd and key not in record:
            fails.append(f"section '{h}' is filled but the record has no 'Decision: {key}' block: the skill chose, or the record is incomplete")

    for x in fails:
        print("FAIL", x)
    print(f"{len(record)} decision(s) in the record, {checked} chosen line(s) found in the document, {len(fails)} failure(s)")
    print("Not checked here, read it: whether the In short paragraph, the Voice section and the persona follow these choices in spirit; the dimensions are checked for their record only.")
    if fails:
        print("RESULT: FAIL")
        sys.exit(1)
    print("RESULT: PASS (mechanical part of the fresh pass)")
    sys.exit(0)


if __name__ == "__main__":
    main()
