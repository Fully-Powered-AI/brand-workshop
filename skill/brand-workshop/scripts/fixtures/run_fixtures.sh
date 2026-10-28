#!/bin/sh
# Fixtures for the two scripts: a green case, a must-fail case and a partial case for check_brand_document.py,
# and the green document against its choices record for check_choices.py. Run from anywhere; exit 0 when every
# expectation holds. The company in the fixtures is invented for this purpose and is not one from the course.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
scripts="$(dirname "$here")"
fails=0
expect() {  # expect <exit code> <label> <command...>
  want="$1"; label="$2"; shift 2
  out="$("$@" 2>&1)"; got=$?
  if [ "$got" -ne "$want" ]; then
    echo "FAIL $label: expected exit $want, got $got"; echo "$out" | tail -3; fails=$((fails+1))
  else
    echo "ok   $label (exit $got): $(echo "$out" | tail -1)"
  fi
}
must_say() {  # must_say <label> <needle> <command...>
  label="$1"; needle="$2"; shift 2
  out="$("$@" 2>&1)"
  if echo "$out" | grep -q -- "$needle"; then echo "ok   $label names: $needle"; else echo "FAIL $label does not name: $needle"; fails=$((fails+1)); fi
}
expect 0 "green document" python3 -I "$scripts/check_brand_document.py" "$here/brand-document-pass.md"
expect 2 "partial document" python3 -I "$scripts/check_brand_document.py" "$here/brand-document-partial.md"
must_say "partial document" "RESULT: PARTIAL" python3 -I "$scripts/check_brand_document.py" "$here/brand-document-partial.md"
expect 1 "must-fail document" python3 -I "$scripts/check_brand_document.py" "$here/brand-document-fail.md"
for needle in "title must read" "is numbered" "a table" "banned word 'leverages'" "one bold sentence" "must be one sentence" "Because of" "expected five numbered traits" "line 40: the prose opens in the 'X, but not Y' form" "line 41: the trait name is" "line 42: the prose opens" "line 43: the trait name is" "line 44: the prose opens" "line 45: the prose opens" "no 'Not:'" "About-page header" "names the bar test" "Earlier versions" "Date must be YYYY-MM-DD" "one line per version"; do
  must_say "must-fail document" "$needle" python3 -I "$scripts/check_brand_document.py" "$here/brand-document-fail.md"
done
expect 1 "unfilled template" python3 -I "$scripts/check_brand_document.py" "$scripts/../assets/brand-document-template.md"
expect 0 "choices record against the green document" python3 -I "$scripts/check_choices.py" "$here/choices-record-pass.md" "$here/brand-document-pass.md"
expect 1 "choices record against the partial document" python3 -I "$scripts/check_choices.py" "$here/choices-record-pass.md" "$here/brand-document-partial.md"
echo "$fails failure(s)"
[ "$fails" -eq 0 ]
