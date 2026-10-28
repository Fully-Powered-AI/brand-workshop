#!/usr/bin/env python3
"""Step-30 check of a brand document written from assets/brand-document-template.md (the reader-first layout,
owner's amendment 6, 2026-10-15).

Usage: python3 -I check_brand_document.py BRAND_DOCUMENT.md

Deterministic checks only; the judgment stays with the owner. What it checks:
  the title '# Brand strategy: <company>'; one sentence saying what the document is; an '**In short.**'
  paragraph before the first section, carrying the purpose; the eight named sections in the template's
  order, unnumbered, each opened by its answer in one bold sentence and followed by bullets or a numbered
  list; no tables anywhere; the Purpose opening 'We exist to ...'; the positioning statement as one bold
  sentence followed by its parts (For, Who, <company> is, That, Unlike, Because of); five numbered bold
  traits each followed by plain prose, none 'human', none in the 'We are X, but not Y' form; a voice entry
  per trait with what is avoided and what is written; the lines in use (About-page header, introduction,
  homepage headline); the validation section naming the bar test; the Record at the bottom with its fields,
  and a change log with one line per version; the banned words (enable, empower, leverage) in brand text;
  every placeholder filled.

Exit 0: PASS, nothing left to check by eye. Exit 2: PARTIAL, no failure but warnings or sections not run (TBD),
so the document is partial and says so. Exit 1: FAIL, or the file could not be read.
A partial result never prints as PASS.
"""
import re
import sys
from datetime import date
from pathlib import Path

SECTIONS = ["Purpose", "Who it is for", "Category", "Positioning statement", "Personality", "Voice",
            "Lines in use", "What is not yet validated"]
RECORD = "Record"
RECORD_FIELDS = ["Version", "Date", "Produced by", "Inputs", "Customers' words", "Could not judge", "Earlier versions"]
RECORD_OPTIONAL = ["Instructions found in inputs"]
PART_LABELS = ["For", "Who", "That", "Unlike", "Because of"]
# The course's no-jargon rule names these three words (ledger W-061); inflections included.
BANNED = re.compile(r"\b(enabl(?:e|es|ed|ing)|empower\w*|leverag\w*)\b", re.I)
HUMAN = re.compile(r"\bhuman\b", re.I)
BOLD_OPEN = re.compile(r"^\*\*([^*]+?[.!?][\"”)]*)\*\*")
LIST_LINE = re.compile(r"^\s*(?:-|\d+\.)\s+\S")
BULLET_LABEL = re.compile(r"^\s*-\s+\*\*(.+?)\*\*\s*(.*)$")
TRAIT_LINE = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*)$")
# The superseded form, with or without its "We are": a short phrase, then "but not" (owner's amendment 6).
XY = re.compile(r"^(?:we are\s+|we(?:'|’)re\s+)?[^.;!?]{1,60}?,?\s+but not\b", re.I)
MIN_TRAIT_WORDS = 6  # the engine's floor for "a short sentence or two"; a bare label is not a trait with its edge
CHANGE_LINE = re.compile(r"^- v\d+ \(\d{4}-\d{2}-\d{2}\): \S")

fails, warns = [], []


def fail(msg):
    fails.append(msg)


def warn(msg):
    warns.append(msg)


def norm(s):
    s = s.replace("*", "").replace("_", "")
    s = s.strip().strip('"“”\'').rstrip(".").lower()
    s = s.replace("’", "'").replace("‘", "'").replace("—", "-").replace("–", "-")
    return re.sub(r"\s+", " ", s)


def label_key(s):
    return norm(re.sub(r"[.:]\s*$", "", s.strip()))


def split_sections(lines):
    """Return (front, ordered [(heading, heading line number, [(line number, line)])])."""
    front, secs, current = [], [], None
    for ln, line in enumerate(lines, 1):
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            current = (m.group(1), ln, [])
            secs.append(current)
            continue
        if current is None:
            front.append((ln, line))
        else:
            current[2].append((ln, line))
    return front, secs


def content_lines(body):
    return [(ln, l) for ln, l in body if l.strip()]


def is_tbd(body):
    c = content_lines(body)
    return bool(c) and (c[0][1].strip().upper() == "TBD" or c[0][1].strip().upper().startswith("**TBD"))


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        print("RESULT: FAIL (usage)")
        sys.exit(1)
    path = Path(sys.argv[1])
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"FAIL cannot read {path}: {e}")
        print("RESULT: FAIL")
        sys.exit(1)
    lines = text.splitlines()
    if not lines:
        print("FAIL empty file")
        print("RESULT: FAIL")
        sys.exit(1)

    for ln, line in enumerate(lines, 1):
        if "{{" in line or "}}" in line:
            fail(f"line {ln}: unfilled placeholder: {line.strip()[:70]}")
        if line.lstrip().startswith("|"):
            fail(f"line {ln}: a table; the document uses lists, never tables (owner's amendment 6)")

    # Title, the one sentence, In short.
    if not re.match(r"^# Brand strategy: \S", lines[0]):
        fail("line 1: title must read '# Brand strategy: <company>'")
    front, secs = split_sections(lines)
    front_content = [(ln, l) for ln, l in front if l.strip() and ln != 1]
    inshort_idx = next((i for i, (ln, l) in enumerate(front_content) if re.match(r"^\*\*In short[.:]?\*\*", l)), None)
    inshort = ""
    if inshort_idx is None:
        fail("no '**In short.**' paragraph before the first section")
    else:
        if inshort_idx == 0:
            fail("no sentence saying what the document is between the title and '**In short.**'")
        elif any(l.startswith("#") for _, l in front_content[:inshort_idx]):
            fail("the lines between the title and '**In short.**' must be a sentence, not a heading")
        ln0 = front_content[inshort_idx][0]
        para = []
        for ln, l in front:
            if ln >= ln0:
                if not l.strip():
                    break
                para.append(l)
        inshort = " ".join(para)
        if "we exist to" not in inshort.lower():
            fail("'**In short.**' must carry the purpose ('We exist to ...')")

    # Sections: the eight, in order, unnumbered, then Record last.
    heads = [h for h, _, _ in secs]
    for h in heads:
        if re.match(r"^\d+\.\s", h):
            fail(f"section '## {h}' is numbered; the sections are named, not numbered")
    expected = SECTIONS + [RECORD]
    for h in expected:
        if h not in heads:
            fail(f"missing section '## {h}'")
    extra = [h for h in heads if h not in expected]
    if extra:
        fail(f"sections not in the template: {extra}; the document has the eight named sections, then Record")
    present = [h for h in expected if h in heads]
    if [h for h in heads if h in expected] != present:
        fail("sections are out of the template's order")
    if heads and heads[-1] != RECORD:
        fail("'## Record' must be the last section")

    body_of = {h: b for h, _, b in secs}
    not_run = []
    bold_of = {}
    for h in SECTIONS:
        if h not in body_of:
            continue
        body = body_of[h]
        c = content_lines(body)
        if not c:
            fail(f"{h}: empty section; write it, or 'TBD'")
            continue
        if is_tbd(body):
            not_run.append(h)
            continue
        m = BOLD_OPEN.match(c[0][1].strip())
        if not m:
            fail(f"{h}: line {c[0][0]}: the section must open with its answer in one bold sentence ('**...**')")
        else:
            bold_of[h] = m.group(1)
        if not any(LIST_LINE.match(l) for _, l in c[1:]):
            fail(f"{h}: after the bold opening line come short bullets or a numbered list; none found")
        check_section(h, c, bold_of.get(h, ""))

    # Cross-checks.
    if "Purpose" in bold_of and inshort and norm(bold_of["Purpose"]) not in norm(inshort):
        fail("'**In short.**' does not carry the Purpose section's bold line word for word; the purpose is stated once")
    if "Personality" in body_of and "Voice" in body_of and "Personality" not in not_run and "Voice" not in not_run:
        traits = [label_key(t) for t in trait_labels(content_lines(body_of["Personality"]))]
        voices = [label_key(t) for t, _ in bullet_labels(content_lines(body_of["Voice"]))]
        if traits and voices and set(traits) != set(voices):
            fail(f"Voice: its entries {voices} are not the five Personality traits {traits}")

    # Record.
    version = None
    customers_words = None
    if RECORD in body_of:
        rec = content_lines(body_of[RECORD])
        fields = {}
        for ln, l in rec:
            m = BULLET_LABEL.match(l)
            if m:
                fields[label_key(m.group(1))] = (ln, m.group(2).strip())
        for f in RECORD_FIELDS:
            v = fields.get(label_key(f))
            if v is None:
                fail(f"Record: no '- **{f}:**' line")
            elif not v[1]:
                fail(f"Record: line {v[0]}: '{f}' is empty")
        unknown = [k for k in fields if k not in {label_key(f) for f in RECORD_FIELDS + RECORD_OPTIONAL}]
        if unknown:
            warn(f"Record: lines not in the template: {unknown}; check by eye")
        v = fields.get(label_key("Version"))
        if v and v[1]:
            if re.fullmatch(r"\d+", v[1]) and int(v[1]) >= 1:
                version = int(v[1])
            else:
                fail(f"Record: Version must be a whole number from 1, got '{v[1]}'")
        d = fields.get(label_key("Date"))
        if d and d[1]:
            try:
                date.fromisoformat(d[1])
            except ValueError:
                fail(f"Record: Date must be YYYY-MM-DD, got '{d[1]}'")
        cw = fields.get(label_key("Customers' words"))
        if cw:
            customers_words = cw[1]
        cl = [i for i, (ln, l) in enumerate(rec) if re.match(r"^### Change log\s*$", l)]
        if not cl:
            fail("Record: no '### Change log' heading")
        elif version is not None:
            entries = [l for _, l in rec[cl[0] + 1:] if CHANGE_LINE.match(l)]
            if len(entries) != version:
                fail(f"Change log has {len(entries)} line(s) of the form '- vN (YYYY-MM-DD): ...' but Version is {version}; one line per version")
    if customers_words is not None:
        cw = customers_words.lower()
        if not (re.match(r"(none|no\b|not\b)", cw) or re.search(r"\d", cw)):
            fail("Record: Customers' words must say none (or not supplied) or give a count of what was supplied")
    no_words = customers_words is not None and not re.search(r"\d", customers_words) and re.match(r"(none|no\b|not\b)", customers_words.lower())
    if no_words and "What is not yet validated" in body_of and "What is not yet validated" not in not_run:
        t = " ".join(l for _, l in body_of["What is not yet validated"]).lower()
        for needle in ("bar test", "interview"):
            if needle not in t:
                fail(f"What is not yet validated: customers' words were not supplied, so the section must name the {needle}s that gather them" if needle == "interview" else
                     "What is not yet validated: customers' words were not supplied, so the bar test is unvalidated and the section must say so")

    # Banned words in brand text (everything above the Record); "human" in personality or voice.
    record_start = next((ln for h, ln, _ in secs if h == RECORD), len(lines) + 1)
    in_personality = set()
    for h in ("Personality", "Voice"):
        if h in body_of:
            in_personality.update(ln for ln, _ in body_of[h])
    for ln, line in enumerate(lines, 1):
        if ln >= record_start:
            continue
        m = BANNED.search(line)
        if m:
            fail(f"line {ln}: banned word '{m.group(0)}' (the course's no-jargon rule): {line.strip()[:70]}")
        if HUMAN.search(line):
            if ln in in_personality:
                fail(f"line {ln}: 'human' is not a personality attribute: {line.strip()[:70]}")
            else:
                warn(f"line {ln}: 'human' appears; check by eye that it is not describing the brand: {line.strip()[:70]}")

    for x in fails:
        print("FAIL", x)
    for x in warns:
        print("WARN", x)
    print(f"{len(SECTIONS) - len(not_run)} of {len(SECTIONS)} sections written, {len(not_run)} not run (TBD)"
          + (": " + "; ".join(not_run) if not_run else "") + f"; {len(fails)} failure(s), {len(warns)} warning(s)")
    if fails:
        print("RESULT: FAIL")
        sys.exit(1)
    if warns or not_run:
        print("RESULT: PARTIAL, not a pass; checks by eye remain or TBD sections are not run")
        sys.exit(2)
    print("RESULT: PASS")
    sys.exit(0)


def bullet_labels(content):
    out = []
    for ln, l in content:
        m = BULLET_LABEL.match(l)
        if m and not l.startswith("  "):
            out.append((m.group(1), m.group(2)))
    return out


def trait_labels(content):
    return [m.group(2) for _, l in content for m in [TRAIT_LINE.match(l)] if m]


def check_section(h, content, bold):
    txt = [l for _, l in content]
    joined = " ".join(txt).lower()
    if h == "Purpose":
        if not bold.startswith("We exist to "):
            fail(f"{h}: the bold opening line must be the purpose, 'We exist to ...'")
        if "tension" not in joined:
            fail(f"{h}: the section carries the tension the purpose comes from; no line names it")
    elif h == "Positioning statement":
        if re.search(r"[.!?]\s+\S", bold):
            fail(f"{h}: the bold opening line must be one sentence, the whole statement")
        labels = [label_key(t) for t, _ in bullet_labels(content)]
        for p in PART_LABELS:
            if label_key(p) not in labels:
                fail(f"{h}: no part '- **{p}** ...' under the statement")
        if not any(k == "is a" or k.endswith(" is") for k in labels):
            fail(f"{h}: no part '- **<company> is** <category>' under the statement")
        who = next((rest for t, rest in bullet_labels(content) if label_key(t) == "who"), "")
        if re.match(r"\s*(want|wish|would like|are looking for)\b", who, re.I):
            warn(f"{h}: the Who part reads as a wish for the product ('{who[:50]}'); the rule is the customer's situation; check by eye")
    elif h == "Personality":
        traits = [(ln, m) for ln, l in content for m in [TRAIT_LINE.match(l)] if m]
        if len(traits) != 5:
            fail(f"{h}: expected five numbered traits '1. **Trait.** prose'; found {len(traits)}")
        if [int(m.group(1)) for _, m in traits] != list(range(1, len(traits) + 1)):
            fail(f"{h}: the traits are numbered 1 to 5 in order")
        for ln, m in traits:
            name, prose = m.group(2).strip(), m.group(3).strip()
            if HUMAN.fullmatch(name.rstrip(".")):
                fail(f"{h}: line {ln}: 'human' is not a personality attribute")
            if re.search(r"\bbut not\b", name, re.I):
                fail(f"{h}: line {ln}: the trait name is '{name}'; a trait is one plain word or phrase, its edge goes in the prose (owner's amendment 6)")
            if not prose or len(prose.split()) < MIN_TRAIT_WORDS or not re.search(r"[.!?]", prose):
                fail(f"{h}: line {ln}: trait '{name}' needs a short sentence or two of plain prose with its edge built in")
            if XY.match(prose):
                fail(f"{h}: line {ln}: the prose opens in the 'X, but not Y' form; write the trait as plain prose with its edge built in (owner's amendment 6)")
    elif h == "Voice":
        entries = bullet_labels(content)
        if len(entries) != 5:
            fail(f"{h}: expected five entries '- **Trait.** Not: ... We write: ...', one per trait; found {len(entries)}")
        for t, rest in entries:
            if not re.search(r"\bNot:", rest):
                fail(f"{h}: entry '{t}' has no 'Not:' (what the company avoids)")
            if not re.search(r"\bWe write", rest):
                fail(f"{h}: entry '{t}' has no 'We write' (what it writes instead)")
    elif h == "Lines in use":
        labels = [label_key(t) for t, _ in bullet_labels(content)]
        for word, what in (("about-page header", "the About-page header"), ("introduction", "the introduction line"), ("headline", "the homepage headline")):
            if not any(word in k for k in labels):
                fail(f"{h}: no bullet labelled for {what}")
    elif h == "What is not yet validated":
        if "bar test" not in joined:
            fail(f"{h}: the section names the bar test, spoken aloud with people in circle 4, as the test that validates the positioning")


if __name__ == "__main__":
    main()
