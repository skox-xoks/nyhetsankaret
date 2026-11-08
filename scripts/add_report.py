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
KINDS = {"public", "kommersiell", "nyhetsbyra", "myndighet", "ovrigt"}


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
            check_item(it, s["id"])
    bs = r.get("backside")
    if bs is not None:
        if not isinstance(bs, dict):
            fail("'backside' måste vara ett objekt")
        for it in bs.get("mustKnow", []):
            check_item(it, "Inte att missa")
        unk = bs.get("unknown")
        if unk is not None:
            if not str(unk.get("theme", "")).strip():
                fail("'backside.unknown' saknar 'theme'")
            check_item(unk.get("item") or {}, "Okänd mark")


def check_item(it, where):
    for f in ("title", "summary"):
        if not str(it.get(f, "")).strip():
            fail(f"en nyhet i {where} saknar '{f}'")
    if it.get("reliability") not in REL:
        fail(f"'{it.get('title')}': reliability måste vara hog, medel eller lag")
    for src in it.get("sources", []):
        if not str(src.get("url", "")).startswith(("https://", "http://")):
            fail(f"'{it.get('title')}': ogiltig källänk {src.get('url')!r}")
        if "kind" in src and src["kind"] not in KINDS:
            fail(f"'{it.get('title')}': kind måste vara en av {sorted(KINDS)}")
        if "country" in src and not re.fullmatch(r"[A-Z]{2}", str(src["country"])):
            fail(f"'{it.get('title')}': country ska vara en landskod med två versaler, t.ex. SE")


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
