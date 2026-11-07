"""Coverage check for idea I2 using Open Draaideur (Open State Foundation).

Open Draaideur (https://www.opendraaideur.nl) lists Dutch ex-MPs and ministers and
the organisations they joined after leaving office, with a sector label.
The site's public API is api.opendraaideur.nl (found in the site's JavaScript).

This script writes AGGREGATE counts only (no names) to data/opendraaideur_summary.csv.
The raw download contains named persons (GDPR): it is kept in data/raw/ (git-ignored).

Run:  python scripts/opendraaideur_summary.py
"""
import collections
import json
import urllib.request
from pathlib import Path

import pandas as pd

API = "https://api.opendraaideur.nl/persons/search?limit=1000"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(API, headers={"User-Agent": "thesis-coverage-check/0.1"})
    data = json.load(urllib.request.urlopen(req, timeout=60))
    (RAW / "opendraaideur_persons.json").write_text(json.dumps(data, ensure_ascii=False))
    persons = [h["_source"] for h in data["hits"]["hits"]]

    # Memberships without a label are the post-office jobs; 'lid' = party, 'functie' = Tweede Kamer.
    post = [m for p in persons for m in p.get("memberships", []) if m.get("label") is None]
    with_job = {p["id"] for p in persons
                if any(m.get("label") is None for m in p.get("memberships", []))}
    sectors = collections.Counter(m["organization"].get("classification", "").strip().lower() for m in post)
    years = collections.Counter((m.get("start_date") or "")[:4] for m in post)

    rows = [("persons", len(persons)), ("persons_with_post_office_job", len(with_job)),
            ("post_office_jobs", len(post)),
            ("post_office_jobs_with_start_date", sum(1 for m in post if m.get("start_date"))),
            ("distinct_destination_orgs", len({m["organization"]["id"] for m in post}))]
    rows += [(f"sector: {k}", v) for k, v in sectors.most_common()]
    rows += [(f"start year: {k or 'missing'}", v) for k, v in sorted(years.items())]
    out = pd.DataFrame(rows, columns=["measure", "count"])
    out.to_csv(ROOT / "data" / "opendraaideur_summary.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
