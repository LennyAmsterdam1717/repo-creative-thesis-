"""Coverage check for idea I2 (revolving door).

Question: for politicians who left office, how often does Wikidata record
what they did next (a new employer or position) within 3 years?

Run:  python scripts/wikidata_coverage.py
Output: data/wikidata_coverage_summary.csv, data/wikidata_destinations.csv
Needs only the Python standard library + pandas.
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

ENDPOINT = "https://query.wikidata.org/sparql"
UA = "thesis-coverage-check/0.1 (MSc AI research script; contact via GitHub)"
OUT = Path(__file__).resolve().parent.parent / "data"
EXIT_FROM, EXIT_TO = 1999, 2022  # exits late enough to observe a 3-year window
WINDOW_YEARS = 3

# Dutch minister positions: subclasses of "minister" (Q83307) with jurisdiction/country NL
NL_MINISTER_VALUES = """
  { SELECT DISTINCT ?pos WHERE { ?pos wdt:P279+ wd:Q83307 .
    { ?pos wdt:P1001 wd:Q55 } UNION { ?pos wdt:P17 wd:Q55 } } }
"""
GROUPS = {
    "MEP": "VALUES ?pos { wd:Q27169 }",
    "NL House of Representatives": "VALUES ?pos { wd:Q18887908 }",
    "NL minister": NL_MINISTER_VALUES,
    "German Bundestag": "VALUES ?pos { wd:Q1939555 }",
}


def sparql(query: str):
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": query, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)["results"]["bindings"]
        except Exception as e:  # rate limit / timeout: wait and retry
            print("  retry after error:", e)
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("query failed 3 times")


def val(row, key):
    return row[key]["value"] if key in row else None


def qid(uri):
    return uri.rsplit("/", 1)[-1] if uri else None


def exits(group_values: str) -> pd.DataFrame:
    """Each person's last end date in this group of positions."""
    rows = sparql(f"""
    SELECT ?p (MAX(?end) AS ?lastEnd) WHERE {{
      {group_values}
      ?p p:P39 ?st . ?st ps:P39 ?pos ; pq:P582 ?end .
    }} GROUP BY ?p""")
    df = pd.DataFrame({"person": [qid(val(r, "p")) for r in rows],
                       "last_end": [val(r, "lastEnd") for r in rows]})
    df["last_end"] = pd.to_datetime(df["last_end"].str[:10], errors="coerce")
    return df.dropna()


def later_facts(persons, batch=250) -> pd.DataFrame:
    """All employer (P108) and position (P39) statements of these people (batched)."""
    frames = []
    persons = list(persons)
    for i in range(0, len(persons), batch):
        vals = " ".join(f"wd:{p}" for p in persons[i:i + batch])
        for prop, kind in [("P108", "employer"), ("P39", "position")]:
            rows = sparql(f"""
            SELECT ?p ?obj ?start WHERE {{
              VALUES ?p {{ {vals} }}
              ?p p:{prop} ?s . ?s ps:{prop} ?obj .
              OPTIONAL {{ ?s pq:P580 ?start }}
            }}""")
            frames.append(pd.DataFrame({
                "person": [qid(val(r, "p")) for r in rows],
                "obj": [qid(val(r, "obj")) for r in rows],
                "start": [val(r, "start") for r in rows],
                "kind": kind,
            }))
            time.sleep(1)
    df = pd.concat(frames, ignore_index=True)
    df["start"] = pd.to_datetime(df["start"].str[:10], errors="coerce")
    return df


def group_positions(group_values: str) -> set:
    rows = sparql(f"SELECT DISTINCT ?pos WHERE {{ {group_values} }}")
    return {qid(val(r, "pos")) for r in rows}


def label_and_type(qids):
    """English label and first 'instance of' label for destination items."""
    out = []
    qids = list(qids)
    for i in range(0, len(qids), 200):
        vals = " ".join(f"wd:{q}" for q in qids[i:i + 200])
        rows = sparql(f"""
        SELECT ?x ?xLabel (SAMPLE(?tLabel) AS ?type) WHERE {{
          VALUES ?x {{ {vals} }}
          OPTIONAL {{ ?x wdt:P31 ?t . ?t rdfs:label ?tLabel FILTER(lang(?tLabel)='en') }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,nl,de". }}
        }} GROUP BY ?x ?xLabel""")
        out += [{"obj": qid(val(r, "x")), "label": val(r, "xLabel"), "type": val(r, "type")} for r in rows]
        time.sleep(1)
    return pd.DataFrame(out)


def resolve_nl_ministers():
    """Turn the slow subclass pattern into a fixed VALUES list (one query)."""
    rows = sparql(f"SELECT DISTINCT ?pos WHERE {{ {NL_MINISTER_VALUES} }}")
    ids = " ".join(f"wd:{qid(val(r, 'pos'))}" for r in rows)
    print(f"  {len(rows)} Dutch minister positions")
    return f"VALUES ?pos {{ {ids} }}"


def main():
    OUT.mkdir(exist_ok=True)
    GROUPS["NL minister"] = resolve_nl_ministers()
    summary, dest_rows = [], []
    for name, values in GROUPS.items():
        print(name)
        ex = exits(values)
        ex = ex[(ex.last_end.dt.year >= EXIT_FROM) & (ex.last_end.dt.year <= EXIT_TO)]
        facts = later_facts(ex.person.unique())
        own = group_positions(values)
        facts = facts[~((facts.kind == "position") & facts.obj.isin(own))]
        m = facts.merge(ex, on="person")
        undated_emp = m[(m.kind == "employer") & m.start.isna()].person.nunique()
        win = m[(m.start > m.last_end) &
                (m.start <= m.last_end + pd.DateOffset(years=WINDOW_YEARS))]
        any_emp = m[m.kind == "employer"].person.nunique()
        emp_after = win[win.kind == "employer"].person.nunique()
        pos_after = win[win.kind == "position"].person.nunique()
        anything_after = win.person.nunique()
        n = ex.person.nunique()
        summary.append({
            "group": name, "exits_1999_2022": n,
            "has_any_employer": any_emp,
            "has_employer_without_start_date": undated_emp,
            "new_employer_within_3y": emp_after,
            "new_position_within_3y": pos_after,
            "anything_new_within_3y": anything_after,
            "share_employer_within_3y": round(emp_after / n, 3) if n else None,
            "share_anything_within_3y": round(anything_after / n, 3) if n else None,
        })
        w = win.copy()
        w["group"] = name
        dest_rows.append(w)
        print(summary[-1])
        time.sleep(2)
    summ = pd.DataFrame(summary)
    summ.to_csv(OUT / "wikidata_coverage_summary.csv", index=False)
    dest = pd.concat(dest_rows, ignore_index=True)
    lab = label_and_type(dest.obj.dropna().unique())
    dest = dest.merge(lab, on="obj", how="left")
    dest.to_csv(OUT / "wikidata_destinations.csv", index=False)
    print(summ.to_string(index=False))
    for name in GROUPS:
        for kind in ["employer", "position"]:
            d = dest[(dest.group == name) & (dest.kind == kind)]
            print(f"\n{name}: top {kind} labels after exit (people)")
            print(d.groupby("label").person.nunique().sort_values(ascending=False).head(12).to_string())


if __name__ == "__main__":
    main()
