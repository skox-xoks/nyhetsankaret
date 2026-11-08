#!/usr/bin/env python3
"""Lägg till eller ersätt en dagsrapport.

Användning: python3 scripts/add_report.py sökväg/till/rapport.json

Kontrollerar strukturen, sparar som reports/ÅÅÅÅ-MM-DD.json och
uppdaterar reports/index.json (nyast först).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
BEATS = {"teknik", "hallbarhet", "inrikes", "utrikes"}
REL = {"hog", "medel", "lag"}


def fail(msg):
    sys.exit(f"Fel i rapporten: {msg}")


def validate(r):
    if not isinstance(r, dict):
        fail("toppnivån måste vara ett objekt")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r.get("date", ""))):
        fail("'date' måste vara ÅÅÅÅ-MM-DD")
    secs = r.get("sections")
    if not isinstance(secs, list) or not secs:
        fail("'sections' saknas eller är tom")
    for s in secs:
        if s.get("id") not in BEATS:
            fail(f"okänt område: {s.get('id')!r}")
        for it in s.get("items", []):
            for f in ("title", "summary"):
                if not str(it.get(f, "")).strip():
                    fail(f"en nyhet i {s['id']} saknar '{f}'")
            if it.get("reliability") not in REL:
                fail(f"'{it.get('title')}': reliability måste vara hog, medel eller lag")
            for src in it.get("sources", []):
                if not str(src.get("url", "")).startswith(("https://", "http://")):
                    fail(f"'{it.get('title')}': ogiltig källänk {src.get('url')!r}")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    validate(report)
    REPORTS.mkdir(exist_ok=True)
    date = report["date"]
    (REPORTS / f"{date}.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    dates = sorted({p.stem for p in REPORTS.glob("????-??-??.json")}, reverse=True)
    (REPORTS / "index.json").write_text(
        json.dumps({"dates": dates}, indent=1) + "\n", encoding="utf-8")
    print(f"Sparade {date}. Arkivet har {len(dates)} {'dag' if len(dates) == 1 else 'dagar'}.")


if __name__ == "__main__":
    main()
