# Data check for idea I2 (revolving door), 7 Nov 2026

**Question:** is there enough public data on where politicians go after they leave office to build a prediction thesis?

**Short answer:**
- **Wikidata alone: no.** It records almost no dated private-sector moves.
- **Usable alternatives exist, mainly for the Netherlands.** But they are small, so the idea has to change shape (see the end of this file).

## 1. Wikidata: tested, too thin
Script: `scripts/wikidata_coverage.py`. Output: `data/wikidata_coverage_summary.csv`.

Method:
- For everyone whose last term in a group ended between 1999 and 2022, I checked whether Wikidata records a *new* employer (P108) or position (P39) with a start date within 3 years after leaving.
- Other posts from the same group were excluded.

| Group | Exits 1999–2022 | Have any employer recorded | …of which undated | New employer ≤3 y | Anything new ≤3 y |
|---|---|---|---|---|---|
| MEPs | 2,516 | 397 | 342 | **5 (0.2%)** | 456 (18%) |
| NL House of Representatives | 566 | 87 | 71 | **5 (0.9%)** | 84 (15%) |
| NL ministers | 113 | 44 | 38 | **4 (3.5%)** | 25 (22%) |
| German Bundestag | 1,746 | 177 | 129 | **6 (0.3%)** | 85 (5%) |

How to read the table:
- **Only about 20 dated post-office employers** across about 4,900 exits.
- Most "new positions" are **other political offices**: Senate, Council of Europe, national parliament, mayor. Those are political careers, not revolving-door moves.
- Employers usually have **no start date**, so you cannot tell whether a job came before or after office.
- **Conclusion:** Wikidata is fine for career *features* (positions, committees, dates in office), but useless as the *label* (where people went).

## 2. Open Draaideur (Open State Foundation): usable, small
Script: `scripts/opendraaideur_summary.py`. Output: `data/opendraaideur_summary.csv` (aggregates only).

Site: https://www.opendraaideur.nl. Built with de Volkskrant. The public API at `api.opendraaideur.nl` was found in the site's code.

Size:
- **311 Dutch ex-MPs and ministers.**
- **182 of them have at least one post-office job:** 285 jobs, 280 with a start date, mostly 2017–2021.

**Sector labels already assigned:**

| Sector | Jobs |
|---|---|
| Public domain | 111 |
| Industry associations | 39 |
| Business | 36 |
| Other | 36 |
| Independent adviser | 34 |
| Public-affairs (lobby) firm | 15 |
| NGO | 10 |

Limitations:
- **259 distinct organisations** for 285 jobs. Predicting the *exact organisation* is impossible; predicting the *sector* is realistic.
- **Exit dates are not stored.** Only the start year in the Tweede Kamer is. Exit dates have to come from Wikidata, the Tweede Kamer open-data portal, or Parliaments Day-by-Day.
- **No new data after 2021**, as far as I can see. The licence is not stated on the site [UNVERIFIED]; ask Open State Foundation before use.

## 3. Other sources found (not downloaded)
- **Transparency International EU, "Access all areas" (2017).** Career paths of 485 former MEPs and 27 former Commissioners. About 30% of the MEPs who left politics work for an organisation on the EU lobby register. The old Integrity Watch page is now 404 and the data page returns 403, so ask TI EU. [ABS, search results]
- **Corporate Europe Observatory, RevolvingDoorWatch.** A list of selected cases, not systematic, plus a spreadsheet of former Commissioners' new roles (last updated 2017). [ABS]
- **Academic datasets (not public, as far as I found):**
  - Claessen, Bailer & Turner-Zwinkels (2021, *EJPR*): their own dataset of German and Dutch MPs.
  - Van der Vlist (2023, *Acta Politica*): 970 Dutch post-parliamentary careers, 1967–2017.
  - A Leiden project (Mickler, grant 2023) that is collecting Dutch ex-MPs' later careers *with sector*.

  These would be ideal; ask the authors. [ABS]
- **Parliaments Day-by-Day** (Turner-Zwinkels et al., 2022, *LSQ*, open, CC BY-NC). Exact daily membership data for the Dutch, German and Swiss parliaments, 1947–2017. Gives clean entry and exit dates (the features), not later careers. [ABS]
- **Parlement.com (PDC) biographical archive.** Detailed Dutch careers since 1796, including later jobs. Researchers can get access; terms are unknown. [ABS]

## 4. What this means for I2
- **Original plan (dead):** predict the exact organisation, Europe-wide, from Wikidata.
- **Realistic plan:** a Dutch case study.
  - Labels: sector of the first post-office job, from Open Draaideur (about 180 people), or more if the Leiden or PDC data can be obtained.
  - Features: career facts from Wikidata, the Tweede Kamer open data and Parliaments Day-by-Day (committees, portfolios, terms, seniority).
  - Model: knowledge-graph and link-prediction methods.
  - With about 180 labelled people, the thesis is mainly about **explainable prediction on a small graph**. Expect wide error bars; a large deep-learning model is not appropriate.

**Feasibility update:** Data falls from 3 to 2. The total drops from 27 to about 26/35, unless the Leiden or PDC data can be obtained.

**Ethics:** named persons. Raw downloads stay in `data/raw/` (git-ignored); only aggregate counts are committed.
