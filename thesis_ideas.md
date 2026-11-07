# Thesis ideas from the collected studies (7 Nov 2026)

There is one idea per study. Full details (research question, data, method, kill test, score justifications) are in `study_summaries.md`. This file does three things:
- ranks the ideas;
- works out the top 5 a bit further;
- shows how they fit together.

Scores use the 7-criterion rubric (1–5 each, so 35 is the maximum):
- **Data**: availability of the data.
- **Code**: how hard the code is for an intermediate coder who uses AI.
- **Nov.**: novelty against 2025–2026 work.
- **Eval**: how clear the evaluation is.
- **Scope**: whether it fits in 30 weeks.
- **Int.**: fit with your interests.
- **Sup.**: fit with the supervisor.

## Ranked table of all ideas

| Rank | Idea | Source study | Score /35 | One-line pitch | Kill test |
|---|---|---|---|---|---|
| 1 | **I3** How good does a link predictor need to be? | S3 Shi et al. 2026 | **29** | Measure how much portfolio benefit you get per unit of link-prediction accuracy, by damaging the true future co-movement graph step by step. | Weakened (decision-focused portfolios exist; the curve is new) |
| 2 | **I1** Do learned stock graphs mean anything? | S1 Al Ridhawi et al. 2026 | **28** | Grade the graphs that stock models "learn" against real company relations (industry, supplier, common owners), and test whether learned edges foresee new real links. | Survived |
| 3 | **I5** When politics flips the switch | S5 Kumar et al. 2026 | **28** | Use news-based country-pair geopolitical tension to switch volatility-spillover edges between stock markets on or off, under strict out-of-sample tests. | Survived (time-zone variant killed) |
| 4 | **I2** Through the revolving door | S2 Cui et al. 2026 | **27** | Predict where European politicians go after office from a Wikidata career knowledge graph, with a leakage-free time split. | Survived |
| 5 | **I6** Markets as annotators | S6 Li et al. 2026 | **26** | Use stock-price reactions to check, and learn to filter, company links that LLMs extract from text. | Survived |
| 6 | I7 Does the news graph lead the price graph? | S7 Luo et al. 2026 | 26 | Measure how long after a new news link a price link appears; use news links to forecast signed price edges. | Weakened (news → correlation known since 2019) |
| 7 | I8 Which companies will move into each other's technology next? | S8 Liu et al. 2026 | 22 | Chronological firm–technology link prediction from USPTO patents, linked to stock co-movement. | Weakened (crowded field) |
| 8 | I4 Dutch-language news vs English news | S4 Almusned et al. 2026 | 21 | Does Dutch-only news predict big moves of Amsterdam-listed firms that English news misses? | Weakened; only partial supervisor fit |

Ideas that were killed outright:
- **I5-A, a time-zone-ordered spillover graph.** It is already done in Zhao & Qiao (2026), Chi, Gao & Wang (2024/2026) and Liu et al. (2026).

The table orders I6 above I7 despite the same total, because I6 is clearly more novel (5 vs 2).

---

## The top 5 in more detail

### 1. I3: How good does a link predictor need to be? (29/35)

**In one paragraph.** Several 2025–2026 papers predict which stocks will move together and then build portfolios on those predictions. S3 reports a weak predictor (AUC 0.55, where 0.5 is random) together with enormous returns. Something does not add up, and nobody has measured how much a better link predictor is actually worth.

This thesis builds that measurement:
1. Take the *real* future co-movement graph, the perfect "oracle".
2. Feed it into a fixed portfolio rule.
3. Damage the graph step by step by flipping a growing share of its edges, and record how portfolio risk and Sharpe ratio change.
4. Place real predictors on that curve: "nothing changes", logistic regression, an S3-style GNN, and a temporal GNN.
5. Last, test whether training a predictor directly on portfolio outcome (decision-focused learning) moves it up the curve.

**Why it is creative.** It is a reusable ruler: every "link prediction for portfolios" paper can be placed on it.

**Plan (30 weeks).**
| Weeks | Work |
|---|---|
| 1–6 | Literature review and proposal (phase 1) |
| 7–10 | Data and leak-free windows |
| 11–14 | Oracle-degradation curve |
| 15–20 | Real predictors |
| 21–24 | Decision-focused variant |
| 25–30 | Writing |

**Main risks.**
- The curve may show that *no* realistic predictor helps. That is still a clear, publishable negative result.
- The decision-focused layer is the hardest code.

**Fallback.** Drop decision-focused training; the curve plus three predictors is a full thesis.

**First two weeks.**
- Download about 100 US stocks from Stooq.
- Define signed edges on non-overlapping 20-day windows.
- Reproduce a Ledoit–Wolf minimum-variance baseline.

### 2. I1: Do learned stock graphs mean anything? (28/35)

**In one paragraph.** Many models (S1, S5, S7 and others) let a neural network "learn" which stocks are connected, and then show the learned graph as an explanation. For example, S1 highlights ExxonMobil–Caterpillar. Nobody checks these explanations against reality.

This thesis:
1. Trains three graph-learning models: MTGNN/Graph WaveNet, an attention model, and graphical lasso.
2. Compares their learned edges with public records of real relations: SIC industry, supplier and customer links from 10-K reports (the open FinReflectKG dataset), and common institutional owners from SEC 13F filings.
3. Tests whether the "surprising" learned edges turn into documented relations a year later.

**Why it fits you.** It is an XAI thesis (are the explanations faithful and plausible?) in a finance setting, built on knowledge graphs.

**Plan.**
| Weeks | Work |
|---|---|
| 1–6 | Review and proposal |
| 7–11 | Ground-truth graphs (SIC, FinReflectKG, 13F) |
| 12–17 | Train the models and extract their edges |
| 18–22 | Overlap, stability, future-link tests |
| 23–25 | A small "explanation audit" dashboard |
| 26–30 | Writing |

**Main risks.**
- Real-relation data are sparse (FinReflectKG has about 3.6 firm–firm edges per firm-year in the earlier sample).
- 13F cleaning takes effort.

**Fallback.** Use SIC + 13F only, with two models.

**First two weeks.**
- Download FinReflectKG and count firm–firm relations for S&P 500 firms.
- Run MTGNN from PyTorch Geometric Temporal on 100 stocks and export its adjacency matrix.

### 3. I5: When politics flips the switch (28/35)

**In one paragraph.** S5's graph model looked good until it was tested strictly out-of-sample, where it failed (negative R², meaning it forecasts worse than a constant). One reason may be that the graph has no idea *why* spillovers between markets switch on and off.

This thesis gives it a reason: geopolitical tension between two countries, measured from news.
- The new CEPII IntenSE dataset (2026, built from GDELT) gives a monthly "negative tone" score for every country pair. GDELT gives a daily version.
- A volatility-forecasting graph lets the edge US→China, for example, grow stronger when US–China tension rises.

It is tested against strong classic models (HAR) under the strict design, with special attention to the 2018–19 and 2025 tariff periods.

**Plan.**
| Weeks | Work |
|---|---|
| 1–6 | Review and proposal |
| 7–10 | Index prices, volatility estimates, rolling spillovers |
| 11–13 | Tension–spillover descriptive analysis |
| 14–20 | Gated graph model vs HAR family |
| 21–24 | Robustness, explanation per country pair |
| 25–30 | Writing |

**Main risks.**
- The monthly tension measure may be too coarse; switch to daily GDELT counts.
- The effect may simply be small.

**Fallback.** HAR with tension-weighted foreign volatility (no GNN), which is simple and still answers the question.

**First two weeks.**
- Get the CEPII IntenSE file.
- Download about 20 national indices from Stooq.
- Plot US–China tension against S&P 500 → Hang Seng spillover.

### 4. I2: Through the revolving door (27/35)

**In one paragraph.** S2 predicts people's next job from private LinkedIn data, using a knowledge graph plus an LLM. This thesis moves that idea to **public** data and a **political** question:
- From Wikidata (positions held, employers, committees, all with dates), build a temporal knowledge graph of European politicians' careers.
- Predict the sector, and then the organisation, they join after leaving office.
- Fix S2's weaknesses:
  - a strict time split;
  - for each exit, only facts known before that exit;
  - ranking against *all* organisations, not 19 negatives.
- The explanation part asks which chain of facts (minister of energy → regulator → board seat) supports a prediction.

**Plan.**
| Weeks | Work |
|---|---|
| 1–6 | Review and proposal |
| 7–11 | Wikidata extraction and cleaning |
| 12–16 | Baselines + temporal-KG model (CAPER code) |
| 17–21 | KG + LLM variant (SCP code) |
| 22–24 | Explanations |
| 25–30 | Writing |

**Main risks.**
- Wikidata may record too few post-office jobs. Measure this in weeks 1–2; it is the go/no-go point.
- Ethics. The people are named, and party membership is special-category data under the GDPR. Report aggregates only.

**Fallback.** Predict only the destination *sector* with a temporal KG + gradient boosting; no LLM.

**First two weeks.**
- Write a SPARQL query for all MEPs and Dutch/German ministers since 1999 with P39 end dates.
- Count how many have a later P108 (employer).

### 5. I6: Markets as annotators (26/35)

**In one paragraph.** LLMs are increasingly used to build company knowledge graphs from filings and news. Nobody has a cheap way to tell which extracted links are real and material. S6 even found that its LLM extractor made predictions worse, without knowing why.

This thesis uses the market as the judge:
1. When a filing or news item first reports "A signs a deal with B", "A supplies B" or "A sues B", check whether A and B start moving together abnormally in the next 20 trading days, compared with matched pairs.
2. Learn to predict, from the text alone, which extracted links the market will "confirm". This gives a filter for building better knowledge graphs.
3. Check the market-based labels against a hand-labelled sample.

**Plan.**
| Weeks | Work |
|---|---|
| 1–6 | Review and proposal |
| 7–11 | 8-K/GDELT relation extraction (or reuse FinReflectKG) + entity matching |
| 12–16 | Event study and labels |
| 17–21 | Text-only "materiality" classifier |
| 22–24 | Downstream test: does a filtered KG help a simple stock graph model? |
| 25–30 | Writing |

**Main risks.**
- Other news on the same day (confounding).
- Name-to-ticker matching.

**Fallback.** Run only the event study by relation type and extraction method. That is already a strong descriptive contribution.

**First two weeks.**
- Pull S&P 500 8-K filings for 2018–2020.
- Run an open 7B model to extract company–company relations from 200 filings.
- Hand-check 50 of them.

---

## What the top 5 have in common

- **They test claims instead of adding another model.** I1 tests explanations, I3 tests portfolio claims, I6 tests extracted knowledge, and I5 and I2 test predictions under strict time splits. This matches the supervisor's advice that plain prediction with GNNs and transformers is "done". It also matches the weak spots I found in all eight studies: leakage, random splits, no transaction costs, and untested "interpretability".
- **They use public data only.** That suits the Accenture internship rule.
- **Most are about edges, not nodes.** Link prediction, edge validity, edge switching, and signed or time-activated edges are exactly the supervisor's stated niches.
- **Strict chronological evaluation is the shared method backbone.** It is also an easy story for the "relevance to AI" section of the thesis: trustworthy evaluation of graph learning.

## Which ideas combine well

1. **I1 + I6: a "two-way audit" between text graphs and market graphs.**
   - I6 checks *text-derived* company links against market reactions.
   - I1 checks *market-learned* links against text and filing records.
   - Together: "Do text-based and market-based company graphs agree, and who is right when they disagree?"
   - This is the **best supervisor fit** (knowledge graphs + text + networks) and very creative.
   - It is too big for 30 weeks if done in full. Do I6 fully and I1 on one model only.
2. **I3 + the earlier P1 (signed lead-lag edge-state forecasting, from the 6 Nov feasibility study).** P1 predicts signed edges, and I3 measures what those predictions are worth. This is the **safest** combination and it reuses earlier work.
3. **I5 + I2: a "politics" pairing.** The two share little code, so this is not a single thesis. I5 can, however, reuse the GDELT pipeline of I6 or I7.
4. **I7 as a chapter inside I6.** The delay between a news link and a price link (I7) is the same event-study machinery as I6.

## My recommendation

- **Most creative, with the best supervisor fit:** I6, with a light version of I1 as a second chapter.
- **Safest, with the clearest evaluation:** I3, combined with the earlier P1.
- **Best fit with your politics interest:** I5.

Bring all three to the supervisor. Let her reaction to "is an audit or evaluation thesis creative enough?" decide.

## Questions to ask the supervisor

1. Is a thesis whose main contribution is a **careful test of existing claims** (I1, I3, I6), rather than a new model, acceptable as the "creative niche" she asked for?
2. **I6 / I1:** does her group have experience with, or preferences for, building company knowledge graphs with LLMs? Is there GPU access at UU for running a 7B model over a few thousand filings?
3. **I2:** would she supervise a topic with named politicians (GDPR special-category data such as party membership)? Does the faculty ethics committee need to see it early?
4. **I5:** is a monthly geopolitical signal (CEPII IntenSE) acceptable, or does she expect daily GDELT-based edges?
5. Does she consider GDELT reliable enough as a research data source? Has her group used it?
6. Would she like the thesis to also produce a small analyst view or dashboard (e.g., "which learned edges are real?" for I1; "which extracted links did the market confirm?" for I6)?
7. Practical: does UU give MSc students access to WRDS or LexisNexis? Not needed for the top 3, but it would strengthen I1 (point-in-time S&P 500 membership) and I4.
