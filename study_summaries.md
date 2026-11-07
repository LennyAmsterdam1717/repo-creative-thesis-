# Study summaries and thesis ideas per study

*Written 7 November 2026, for Frank's MSc AI thesis (Utrecht, supervisor Dr. Ioana Karnstedt-Hulpuș).*

**How to read this file.** There is one section per study. Each section has six parts:
1. the citation,
2. a summary,
3. the gaps the authors name themselves,
4. gaps I see that the authors do not mention,
5. one thesis idea,
6. a feasibility score.

I wrote it in plain language. A technical term gets a short explanation the first time it appears.

**Verification legend**
- **[FT]**: I read the full text (the PDF you uploaded).
- **[ABS]**: I opened only the abstract or record page.
- **[UNVERIFIED]**: I saw the paper only in search results and did not open it. I mention these papers but do not rely on them.

Numbers from the eight studies come from the PDFs. Check them against the PDF again before you use them in the thesis.

**Inventory**
- The GitHub repo `repo-creative-thesis-` was **empty** when I cloned it (no commits, no files). All studies therefore come from the 9 uploaded PDFs.
- Two of the uploads are the same paper (S7): `823b6566-…semantic_company_relationship_graph.pdf` and `d767a45c-…_1.pdf`. Their extracted text is byte-identical, so I treated them as one study. That leaves **8 unique studies**.
- Every file opened and parsed without errors.

| # | File | Short title | Year, venue |
|---|---|---|---|
| S1 | `51076ece-Stock_Market_Prediction_Using_Node_Transformer…pdf` | Node transformer + BERT sentiment | 2026, IEEE Access |
| S2 | `5b0641c1-3787466.pdf` | LLM + career knowledge graph for job-mobility prediction | 2026, ACM TMIS |
| S3 | `1d42c893-s40854-025-00827-3.pdf` | Portfolio management with dynamic link prediction | 2026, Financial Innovation |
| S4 | `adbead6b-out.pdf` | Systematic review: heterogeneous data for stock prediction | 2026, IJACSA |
| S5 | `ae4d6f54-mathematics-14-00289-v2.pdf` | Regime-dependent GNN for volatility | 2026, Mathematics |
| S6 | `65143c49-1-s2.0-S0957417426010559-main.pdf` | Multi-graph fusion of news events, fundamentals and relations | 2026, Expert Systems with Applications |
| S7 | `823b6566-…pdf` (= `d767a45c-…_1.pdf`) | Semantic company relationship graph from news + NIST-GNN | 2026 (online Nov 2025), Quantitative Finance |
| S8 | `6c4df246-1-s2.0-S1474034625008201-main.pdf` | Technology-convergence prediction in multilayer patent networks | 2026 (online Oct 2025), Advanced Engineering Informatics |

**Feasibility rubric.** Each criterion is scored from 1 to 5, for a total out of 35:
- **Data**: availability of the data.
- **Coding**: how hard the code is for an intermediate coder who uses AI.
- **Novelty**: novelty compared with 2025–2026 work.
- **Eval**: how clear the evaluation is.
- **Scope**: whether it fits in 30 weeks.
- **Interests**: fit with your interests (prediction, finance, XAI, politics).
- **Supervisor**: fit with your supervisor's expertise.

---

## S1. Node transformer with BERT sentiment (Al Ridhawi, Haj Ali & Al Osman, 2026)

### 1. Citation [FT]
Al Ridhawi, M., Haj Ali, M., & Al Osman, H. (2026). Stock market prediction using node transformer architecture integrated with BERT sentiment analysis. *IEEE Access*, 14, 72613–72630. https://doi.org/10.1109/ACCESS.2026.3691980 (published 12 May 2026; peer-reviewed; CC BY 4.0).

### 2. Summary
**Problem.** The authors want to forecast stock prices using two things together: links between stocks and investor mood on social media.

**Method.** They treat 20 large S&P 500 stocks as a fully connected graph. Each stock is a node, and every pair has an edge. The edge weights start from a mix of "same GICS sector" and positive return correlation. They are then *learned* during training (Eq. 12–13).

A "node transformer" applies attention across time (252 trading days of input) and across the graph at once. BERT is fine-tuned on a labelled sentiment set and then scores about 4.2 million X/Twitter posts (2007–2025, collected through the X API). The sentiment enters the model in two ways: it modulates the attention, and a gate driven by volatility decides how much weight the sentiment branch gets.

**Data.**
- Daily prices for 20 current S&P 500 members, 1982–2025.
- Split: training 1982–2010, validation 2011–2016, test 2017–March 2025.
- The labelled sentiment set is public. The 4.2 million posts are the authors' own crawl and are not released.

**Results.**
- One-day error (MAPE, mean absolute percentage error): 0.80%. ARIMA gets 1.20%, LSTM 1.00% and a naive random walk 1.35%.
- Theil's U is 0.59. A value below 1 means the model beats "tomorrow = today".
- Direction is right 65% of the time.
- Removing sentiment makes the error 10% worse; removing the graph makes it 15% worse.
- A long-short top-5/bottom-5 strategy returns 22.8% a year gross and 14.6% net of 10 basis points (0.10%) costs, against 13.9% for buy-and-hold. The net Sharpe ratio is 0.84 (§V-E).
- The learned edges look "economically meaningful". For example, ExxonMobil–Caterpillar gets 0.67, the highest cross-sector weight (Table 12, §VI-A).

**Code.** No code or repository is mentioned.

**Limitations the paper itself admits.** Survivorship bias, only 20 stocks, sentiment from one platform, and simplified trading costs (§VI-C).

### 3. Gaps the authors name (with location)
- **Survivorship bias.** The 20 stocks were picked because they are in today's S&P 500. A *point-in-time* universe, built from historical index membership, is "a priority for future work" (§VI-C, p. 72629; §VI-D).
- **Scale.** Whether the learned edges stay useful when the graph grows from 20 nodes to hundreds "remains an open question" (§VI-C, pp. 72629–72630).
- **Non-stationary correlations.** The edges are initialised from 1982–2010 correlations, and these "may weaken or reverse" later (§VI-C).
- **Sentiment.** Sentiment covers only 2007–2010 of the training period, and it is English, from one platform. Future work: multilingual sources, Reddit, news and earnings calls (§VI-C, §VI-D).
- **Other future work.** Efficient attention, regime-shift detection, and linking the forecasts to portfolio optimisation (§VI-D, p. 72630).

### 4. Gaps I see (my own analysis)
- **The forecast accuracy looks too good.** Daily price-level errors of 0.80%, against a random walk at 1.35%, mean the model removes about 40% of the day-to-day surprise in mega-cap prices. That would be extraordinary for liquid stocks. The paper gives no explanation for where such predictability comes from, and no code to check it. This calls for replication before anyone builds on it.
- **"Interpretable" edges are claimed but never tested.** The learned edge weights are said to reveal real links, such as supply chain or commodity exposure (§VI-A). They are never compared with any independent record of real company relationships.
- **The graph cannot represent opposite movements.** Weights are forced non-negative (`max(0, ρ)` in Eq. 12) and are undirected, so the model cannot represent stocks that move in opposite directions, or that lead and lag each other.
- **The test design is fragile.** There is one fixed split with an 8-year test period, and no retraining. Daily turnover of 32% also leaves a lot of room for real trading costs to eat the returns.

### 5. Thesis idea I1: "Do the stock graphs that models learn mean anything?"
**Pitch.** Many stock models learn their own graph and then claim it is interpretable. This thesis checks those learned graphs against public records of real company relationships, and asks whether a learned edge can *predict* a real link before it shows up in the records.

**Research question.** Do the edges that graph-learning stock models discover match documented company relations (industry, supplier–customer, common ownership)? And do "surprising" learned edges become documented relations later?

**Sub-questions.**
1. What share of each model's top-k learned edges is a real relation (precision@k), compared with a plain correlation graph and with random graphs that have the same number of links per node?
2. Are the learned edges stable across random seeds and time windows? An explanation that changes every time you retrain is not much of an explanation.
3. Learned edges that are *not* yet real relations in year y: do they become real relations in year y+1 (a new disclosed customer, new shared institutional owners) more often than chance?

**What gets predicted.** Mainly this is an *evaluation* thesis. The predictive part is whether a pair of companies gets a documented link in the next year, so the unit is a firm pair and the horizon is 1 year.

The audit framing is the better choice here. The S1-type papers already predict prices; what is missing is any check that their explanations are true. That fits your XAI background (faithfulness and plausibility of explanations).

**Data.** Everything is public:
- *Prices:* daily prices for about 100–500 US stocks, 2010–2025, from Stooq or `yfinance`.
- *Industry:* SIC codes from SEC EDGAR.
- *Supplier and customer links:* triples extracted from 10-K reports. Use the open FinReflectKG dataset (Arun et al., 2025 [ABS]). The earlier feasibility study in this Project found about 3.6 firm–firm edges per filer-year in a sample, which is sparse but usable.
- *Common ownership:* SEC Form 13F holdings, which show common institutional owners.

**Access risk.**
- Medium. EDGAR and price sites are blocked from my cloud session but work from a laptop.
- 13F files need cleaning.
- A point-in-time S&P 500 member list must be rebuilt from public change lists. This is risky; a fixed large universe plus a survivorship caveat is the fallback.

**Method sketch.**
1. Train three graph-learning models:
   - MTGNN or Graph WaveNet, which learn an "adaptive" adjacency matrix (code exists in PyTorch Geometric Temporal and the authors' repos);
   - an attention model over a fully connected stock graph (like S1);
   - graphical lasso (`sklearn.covariance.GraphicalLasso`) as a simple statistical graph learner.
2. Extract each model's learned edges per time window.
3. Compare them with the ground-truth relation sets, using `networkx` and `pandas`.

**Evaluation.**
- *Metrics:* precision@k, area under the precision–recall curve, and Jaccard stability across seeds.
- *Null models:* degree-preserving rewired graphs.
- *Leak-free:* edges are learned on window [t−3y, t], and the "future link" test uses only relations first recorded after t.

**What makes it creative.** It flips the usual direction. Instead of using a graph to predict prices, it uses real-world knowledge to *grade the graph a model invented*. It treats XAI faithfulness as a link-prediction problem.

**Supervisor connection.** Strong. The ground truth is a knowledge graph, the comparison is network analysis, and the predictive part is link prediction, which she named.

**Kill test.** Queries: `learned stock graph edge weights validated against supply chain customer relationships 2025`, `stock graph structure learning learned adjacency interpretability compared to industry classification faithfulness 2026`.
- Huang et al. (2026, arXiv 2604.19476 [ABS]) build a 10-K text graph and filter edges with an LLM. The abstract shows no check against an independent database of real links.
- Graph-learning papers usually only show that learned graphs roughly recover sector blocks (e.g., arXiv 2608.06618 [UNVERIFIED]).
- I found no 2025–2026 work that grades learned stock graphs against supplier or ownership data, or that uses learned edges to predict future real links.
- **Outcome: survived** (weakened only slightly: "it recovers sectors" checks are common).

### 6. Feasibility I1: 28/35
| Criterion | Score | Why |
|---|---|---|
| Data | 4 | All public. 13F cleaning and a point-in-time universe take effort. |
| Coding | 3 | Existing model code, but each model must be run and its adjacency extracted. |
| Novelty | 4 | No close 2025–2026 work found. Sector-recovery checks exist. |
| Eval | 4 | Clear metrics and null models. The ground truth itself is incomplete. |
| Scope | 4 | Doable with fallbacks (fewer models, SIC + 13F only). |
| Interests | 5 | XAI + finance + prediction. |
| Supervisor | 4 | KG ground truth, network comparison, link prediction. |

---

## S2. LLM-enhanced career knowledge graph for job-mobility prediction (Cui et al., 2026)

### 1. Citation [FT]
Cui, S., Sun, Y., Zhang, Y., Meng, Q., & Zhu, H. (2026). LLM-enhanced career knowledge graph understanding for job mobility prediction. *ACM Transactions on Management Information Systems*, 17(3), Article 15, 21 pp. https://doi.org/10.1145/3787466 (peer-reviewed; code: https://github.com/cuishuting/SCP).

### 2. Summary
**Problem.** Predict a person's next job, as a (job title, company) pair, from their CV history.

**Why an LLM plus a graph.** LLMs know a lot about jobs but can "hallucinate". Earlier models only used text similarity.

**Method ("Smart Career Predictor", SCP).**
- They build a career knowledge graph from LinkedIn trajectories. It has two node types, companies and job titles, and four edge types: has, belongs-to, company→company transition, and job→job transition (Table 1).
- For each person they retrieve a 2-hop subgraph around their past jobs.
- A heterogeneous graph attention network (MMP-GAT, 4 meta-paths) is pre-trained on link prediction.
- An "entropy-based retrieval score", inspired by TF-IDF, down-weights generic, very popular nodes such as famous companies.
- A two-way cross-attention adapter fuses BERT text embeddings with graph embeddings into "soft prompt" tokens.
- Llama-3.1-8B is then fine-tuned with QLoRA (a cheap fine-tuning method) to choose the next (job, company) from **20 candidates**: 1 true and 19 negatives from the same company type.

**Data.** Two LinkedIn sets, finance (FIN) and IT, with about 18k and 23k users and data up to 1 Dec 2019. The data are **not public**.

**Results.**
- FIN: Hit@1 is 0.61 for SCP, against 0.60 for G-Retriever, 0.54 for plain fine-tuned Llama and 0.45 for DeepSeek-V3.2 (685B).
- IT: Hit@1 is 0.73 (Table 3).
- Random guessing would score 0.05.
- In the ablations, each module helps a little.

**Limitations.** The paper has no limitations or future-work section (§6 is a conclusion only).

### 3. Gaps the authors name
- None explicitly; the paper has no limitations or future-work section (§6, p. 15:19).
- Implicitly, they flag two problems, which the paper sets out to address (§1, pp. 15:2–15:3):
  - LLM hallucination without domain knowledge;
  - "imbalanced" retrieval that favours popular entities.

### 4. Gaps I see (my own analysis)
- **Possible leakage.** The career graph is built "from these users' career trajectories" (§3.1). Nothing says test users' later jobs were removed. If not, the graph already contains the very transitions to be predicted.
- **The evaluation is not chronological.** Users are split at random. There is no "train on careers before year X, predict moves after X".
- **The task is easy.** Choosing 1 out of 20 candidates says little about real recommendation among thousands of companies.
- **The numbers do not match between tables.** Table 3 and Table 5 report different numbers for "SCP with Llama", and the FIN/IT columns appear swapped.
- **The data are private**, so nobody can replicate the results.
- **The method has only been tried on job-hopping.** Career knowledge graphs plus LLMs have never been applied to public career data, for example from politics.

### 5. Thesis idea I2: "Through the revolving door: predicting where politicians go after office"
**Pitch.** "Revolving door" means people moving between public office and private-sector jobs. This thesis transfers the career-knowledge-graph + LLM approach from private LinkedIn data to **public** Wikidata careers of European politicians, and predicts which sector, and which organisation, they move to after leaving office. The evaluation is strictly chronological.

**Research question.** Can a temporal knowledge graph of public political careers predict a politician's next post-office employer type and organisation better than simple baselines? Which relations (portfolio, committee, earlier employers, party colleagues' moves) drive the prediction?

**Sub-questions.**
1. How do simple baselines compare with the more advanced models?
   - *Simple:* most common destination; "same as colleagues from the same committee".
   - *Advanced:* a temporal-KG model in the style of CAPER, and a KG-enhanced LLM in the style of SCP.
2. Is there a measurable "portfolio → industry" pattern? For example, energy committee → energy company.
3. Can each prediction be explained by a short chain of links in the knowledge graph, for example "minister of X → regulator of Y → board of Z"?

**What gets predicted.**
- *Target:* (a) the destination sector, as a classification over about 10 classes such as lobby/consultancy, energy, finance, EU body, academia, NGO; (b) the destination organisation, ranked.
- *Unit:* one exit from office.
- *Horizon:* the first new position within 3 years of the exit.

**Data.**
- Wikidata, which is free and queried with SPARQL:
  - "position held" (P39), with start and end dates;
  - "employer" (P108);
  - "member of" (P463);
  - optionally "member of political party" (P102).
- European Parliament MEP open data.
- The EU Transparency Register / LobbyFacts, which is public.

**Access risk.** Medium. Wikidata coverage of post-office jobs is incomplete, so measure label coverage in the first two weeks (go/no-go). Wikidata itself is easy to download from a laptop.

**Method sketch.**
1. Turn the Wikidata facts into time-stamped triples (`SPARQLWrapper`, `pandas`).
2. Baselines: popularity, nearest neighbours, gradient boosting on hand-made features.
3. Temporal-KG models, using CAPER's public code and/or a temporal-KG library.
4. A KG-enhanced LLM, reusing SCP's public code with a small open model and QLoRA.
5. *Fallback:* drop the LLM and keep the TKG + boosting.

**Evaluation.**
- Chronological by exit year: train on exits up to 2016, validate on 2017–2019, test on 2020–2025.
- **For each exit, the graph contains only facts dated before that exit.** This fixes S2's leakage.
- Rank against *all* organisations, not 19 negatives.
- Metrics: macro-F1 for sector; Hits@1/5/10 and MRR for organisation.

**What makes it creative.** It moves a commercial HR method into political accountability. It replaces private data with an open knowledge graph, and it adds the leakage-free evaluation the original lacks.

**Supervisor connection.** Very strong:
- Wikidata *is* semantic-web/RDF data;
- the task is link prediction on a heterogeneous temporal knowledge graph;
- the explanation part fits her argumentation and knowledge-network interests.

There is also a finance angle: moves from office to banks or regulated firms.

**Kill test.** Queries: `revolving door prediction politicians next job machine learning Wikidata`, `career trajectory prediction politicians Wikidata positions held knowledge graph link prediction LLM`.
- Political-economy papers *explain* the effect of revolving-door laws, but do not predict individual moves with ML (Fisman, Leder-Luis, O'Donnell & Vannutelli, 2025/2026 [UNVERIFIED]).
- CAPER (Lee et al., arXiv 2408.15620, KDD 2025 [ABS]) predicts careers with a temporal KG, on a non-public job dataset.
- A 2026 paper uses graph-augmented LLMs for *ideology* prediction of Swiss MPs (Yuan et al., arXiv 2605.04643 [ABS]), a different task.
- I found no work that predicts politicians' post-office employers from a KG.
- **Outcome: survived.**

**Ethics (flag).** Politicians are named natural persons, so the GDPR applies. Party membership counts as data about *political opinions* (a special category under Art. 9). It is arguably "manifestly made public" by the persons themselves, but the topic needs an ethics check. Mitigations:
- report only aggregate patterns;
- never publish named individual predictions;
- consider leaving party out.

### 6. Feasibility I2: 27/35
| Criterion | Score | Why |
|---|---|---|
| Data | 3 | Free and public. Label coverage on Wikidata is uncertain. |
| Coding | 3 | SPARQL + existing CAPER/SCP code. The LLM part is the hardest. |
| Novelty | 4 | No close work found. |
| Eval | 4 | Clean chronological split and standard ranking metrics. |
| Scope | 3 | Data cleaning (entity matching, dates) can take weeks. A fallback exists. |
| Interests | 5 | Politics + prediction + XAI explanations. |
| Supervisor | 5 | KG, semantic web, link prediction on a heterogeneous temporal graph. |

---

## S3. Multiobjective portfolio management based on dynamic link prediction (Shi, Wang & Wu, 2026)

### 1. Citation [FT]
Shi, Y., Wang, Y., & Wu, J. (2026). Multiobjective portfolio management based on dynamic link prediction. *Financial Innovation*, 12, 17. https://doi.org/10.1186/s40854-025-00827-3 (received 20 Jul 2024, accepted 22 Oct 2025; peer-reviewed; open access).

### 2. Summary
**Problem.** Classic portfolio theory avoids holding stocks that move together. The authors argue instead that you should *predict which pairs will move together, and in which direction*:
- buy pairs that will rise together;
- avoid pairs that will fall together.

**Graph construction.** For every 10-day window they build a graph over 30 Chinese A-share stocks (6 sectors, 5 stocks each).
- A **positive edge** means the share of days both stocks rose, times their correlation, is at least 0.25.
- A **negative edge** is the same rule for days both fell (Eqs. 1–2).
- Note that "negative" here means *falling together*, not moving in opposite directions.

**Prediction model.** Graph convolutions build edge features, and an LSTM predicts each pair's label in the next window (positive, negative or none). A new resampling method ("RePre-Sampling") fixes the heavy class imbalance: 586k "no edge" labels against 45k positive and 97k negative (Table 2).

**Portfolio steps.**
- Four stock-selection rules based on the predicted links.
- A three-objective optimisation (return, value-at-risk, and a predicted "co-movement score"), solved with a particle-swarm algorithm (MOPSO).

**Data.** WIND (a paid database), 2017–2023. Training uses a 1,500-day rolling window, which leaves **170 trading days** for back-testing. Data "available on request".

**Results.**
- Link prediction is weak: AUC 0.553 (0.5 is random), micro-precision 39.9%, 68.5% when "no edge" is ignored (Table 4).
- The portfolio results are huge: the best strategy makes a cumulative return of 310% in the 170-day test, with an annual Sharpe ratio of 4.22, against 93% for equal weights (Table 5).
- No transaction costs are included.

### 3. Gaps the authors name
All of these are in the Conclusion (pp. 34–35):
- Combine the method with *market-index forecasting*, because the strategies behave very differently in bull and bear markets.
- Long-term planning, *lower turnover*, *other definitions of positive and negative links*, and finer market conditions.
- Test in *developed markets* such as the US, where synchronicity (stocks moving together) is lower.

### 4. Gaps I see (my own analysis)
- **The labels overlap with the inputs.** The label for window τ comes from graph G(τ+1), which covers days τ+1 to τ+11. The input window ends at τ+10, so the two share 9 of 10 days. A simple "next graph = current graph" baseline would probably score well. That baseline is missing.
- **Weak predictions, huge returns.** An AUC of 0.55 cannot plausibly explain 175% a year. There are no trading costs, the back-test is only 170 days long, the universe is 30 hand-picked stocks, and there is no significance test against a simple shrinkage-covariance portfolio. The paper never shows *how much* link-prediction accuracy is needed before the portfolio benefits.
- **The link predictor is trained for classification accuracy, not for the portfolio outcome.**
- **"Negative" edges are not anti-correlations.** They are "both fall together". Real opposite movement is not modelled.

### 5. Thesis idea I3: "How good does a link predictor need to be?"
**Pitch.** Measure the *portfolio value of link-prediction accuracy*. Take the true future co-movement graph, damage it step by step, and record how portfolio risk changes. That gives a curve that tells you how accurate a predictor must be before it helps. Then test whether training the predictor *on the portfolio outcome* moves it up that curve.

**Research question.** How does the out-of-sample quality of a co-movement-aware portfolio depend on the accuracy of the predicted links? And does decision-focused training (training on portfolio loss instead of classification loss) lower the accuracy needed to beat strong classic baselines?

**Sub-questions.**
1. **The oracle-degradation curve.**
   - Feed the *true* next-period graph into a fixed portfolio rule, then randomly flip 5%, 10%, … of its edges.
   - Plot portfolio volatility, drawdown and Sharpe (after costs) against edge accuracy.
2. **Where do real predictors land on the curve?**
   - Persistence ("next graph = this graph").
   - Logistic regression on pair features.
   - A GC-LSTM like S3.
   - A temporal GNN (e.g., TGN) from an existing library.
3. **Decision-focused training.** Does training with a loss equal to the realised variance of a differentiable minimum-variance portfolio beat training on cross-entropy?

**What gets predicted.**
- *Target:* the signed co-movement edge (positive, negative or none) for every stock pair.
- *Horizon:* the next 20 trading days, with no overlap with the input window. Negative edges are defined as true anti-correlation.
- *Final measure:* next-period portfolio volatility, drawdown and Sharpe after 10 basis points (0.10%) per trade.

**Data.**
- Daily prices for about 100 S&P 500 or Euro Stoxx stocks, 2005–2025, from Stooq or `yfinance` (free).
- *Optional replication of S3:* Chinese A-shares via the open Python libraries AkShare or baostock. Check their terms of use.
- *Access risk:* low from a laptop. Survivorship bias is the main caveat.

**Method sketch.**
- `pandas` for building the windows.
- Link predictors from `scikit-learn`, PyTorch Geometric Temporal, or DyGLib/TGB.
- Portfolio: `cvxpy` for the optimiser and `cvxpylayers` for the differentiable version.

**Evaluation.**
- Rolling, non-overlapping windows with a gap between input and label.
- Strong classic baselines:
  - equal weights;
  - minimum variance with Ledoit–Wolf shrinkage (`sklearn`), which is the key baseline to beat;
  - a hierarchical-risk-parity portfolio.
- For link quality: AUC and macro-F1.
- For the portfolio: realised volatility, maximum drawdown and net Sharpe. Compare Sharpe ratios with a robust Sharpe-difference test (Ledoit & Wolf, 2008, background) or a block bootstrap.

**What makes it creative.** It turns S3's puzzle (weak predictions, giant returns) into a measurement tool. Any paper on "link prediction for portfolios" can place itself on the curve. It also introduces a "value of information" view of graph learning.

**Supervisor connection.** Directly hits her strongest signals: link prediction, and signed, time-activated edges. It pairs naturally with the earlier P1 proposal (signed lead-lag edge-state forecasting): P1 predicts the edges, and I3 measures what they are worth.

**Kill test.** Queries: `decision-focused learning portfolio optimization graph neural network correlation 2025`, `end-to-end graph structure learning differentiable portfolio optimization layer stock relation graph`.
- Decision-focused portfolio learning exists:
  - Hwang et al. (2025, arXiv 2502.00828 [ABS]), with no graph component in the abstract;
  - Kim, Tae & Lee (2025, arXiv 2508.10776 [ABS]), decision-focused covariance estimation.
- Graph models trained toward portfolios exist:
  - Li & Fan (2025, arXiv 2510.20868 [ABS]), which learns a sparse graph;
  - L2GMOM (arXiv 2308.12212, 2023, background [UNVERIFIED]).
- I found no study that measures portfolio value as a function of link-prediction accuracy (the oracle-degradation curve).
- **Outcome: weakened.** The decision-focused part is not new; the curve and the link-prediction framing are.

### 6. Feasibility I3: 29/35
| Criterion | Score | Why |
|---|---|---|
| Data | 4 | Free daily prices. Survivorship caveat. |
| Coding | 4 | Mostly `pandas` / `sklearn` / `cvxpy`. The differentiable layer is the only tricky step. |
| Novelty | 3 | Decision-focused portfolios exist. The degradation curve is new. |
| Eval | 5 | Controlled experiment, strong classic baselines, no overlap. |
| Scope | 5 | Easy to cut down: drop decision-focused training and the curve alone is a thesis. |
| Interests | 4 | Prediction + finance. |
| Supervisor | 4 | Signed temporal link prediction. Little text or KG. |

---

## S4. Integrating heterogeneous data for stock market prediction: a systematic literature review (Almusned et al., 2026)

### 1. Citation [FT]
Almusned, A., Hassan, M. M., Alkhamees, B., & Al-Qurishi, M. (2026). Integrating heterogeneous data for stock market prediction: A systematic literature review. *International Journal of Advanced Computer Science and Applications (IJACSA)*, 17(3), 252–260+. (I could not find a DOI in the PDF; the journal site is www.thesai.org.)

### 2. Summary
**Aim.** A systematic review of studies that combine more than one kind of data to predict stocks. The kinds are:
- technical data (prices and indicators);
- fundamental data (company reports);
- text-based sentiment (news, social media, forums).

**Method.**
- Search five publisher libraries (IEEE, Springer, Wiley, ScienceDirect, Emerald) for journal papers from 2018–2024.
- Screening: 576 hits → 63 read in full → **44 included**.
- Each paper is quality-checked with 8 questions (QA1–QA8).

**Main findings.**
- **Data sources.** Most studies use exactly two (31 of 44), usually prices plus news or social media. Ten use three, and three use four or more (Fig. 6).
- **Markets and languages.** About 70% study the US or China. English dominates, followed by Chinese, Farsi, Portuguese, Polish and Turkish.
- **Methods.** LSTM/GRU, CNN and FinBERT-with-LSTM "two-branch" designs dominate. Some use reinforcement learning for trading.
- **Fusion.** Data are combined either early (join features) or late (combine model outputs). Hybrid gates and attention are more robust but rarely tested with ablations.
- **Evaluation.** Accuracy and RMSE dominate. Only a few papers report profit-based measures.

**Central message.** Results often depend more on *getting timestamps right and avoiding leakage* than on the model. Examples:
- after-hours news that is wrongly aligned with the trading day;
- overlapping windows;
- random splits.

**Data and code.** None; this is a review.

**Limitations.** Journals only, English only, and no meta-analysis of effect sizes.

### 3. Gaps the authors name
- **Standardised benchmarks.** These are needed so that fusion methods can be compared fairly (§VII Future work, p. 260).
- **Non-English markets.** Domain-specific NLP resources for non-English markets (§VII; also §IV-D, pp. 258–259, on Chinese, Farsi and Turkish).
- **Interpretability.** It should be a "first-class evaluation criterion" (§VII).
- **Temporal leakage.** Leakage through timestamps, overlapping windows and text aggregation needs explicit rules (§V, pp. 259–260; abstract).
- **Emerging markets.** These suffer from limited data and transparency (§IV-D).

### 4. Gaps I see (my own analysis)
- **The search is already outdated.** It stops at 2024, so the LLM era (2025–2026) is missing, and it excludes conference papers (ACL/FinNLP, KDD, AAAI), where most of this work appears.
- **Company relations are left out as a data source.** Graph-based multimodal prediction (relations + text + prices, as in S6 and S7) is barely covered, even though it is now a major strand.
- **No quantitative synthesis.** The review never measures how big the gain from adding text really is.
- **European languages beyond English are not discussed** (Dutch, German, French).

### 5. Thesis idea I4: "Does Dutch-language news tell the market something English news doesn't?"
**Pitch.** For companies listed in Amsterdam, test whether Dutch-language news, especially news with no English counterpart, predicts big next-day price moves that English coverage misses.

**Research question.** For AEX/AMX/AScX companies, does Dutch-only news coverage predict next-day abnormal volatility beyond what English-language coverage predicts?

**Sub-questions.**
1. How much firm news exists only in Dutch, with no English story within 24 hours, and for which firm sizes?
2. Does Dutch-only news improve prediction of big next-day moves, especially for small caps?
3. Do Dutch models (RobBERT, FinGEITje) beat "translate to English, then use FinBERT"?

**What gets predicted.**
- *Target:* whether firm i has a "big move" on day t+1 (absolute abnormal return above 2 standard deviations), plus the size of the absolute return.
- *Unit and horizon:* firm-day, next trading day.
- *Why:* a volatility-type target is more realistic than direction.

**Data.**
- GDELT 2.0, which monitors Dutch-language sources and offers machine translation (public). Whether the translingual stream covers enough Dutch outlets is **[UNVERIFIED]**.
- Company press releases from investor-relations pages.
- Daily prices from Stooq or Euronext (free).
- *Access risk:* high. The main Dutch financial papers are paywalled; check whether the UU library gives LexisNexis or Nexis Uni access.

**Method sketch.**
1. Link firm names in the text to companies (`spaCy` Dutch model plus a hand-made alias list).
2. Embed the text (RobBERT, multilingual-e5).
3. Predict with gradient boosting or logistic regression.
4. Add an event-study check on the result.

**Evaluation.**
- Chronological split.
- Strict publication-time rules: news after 17:30 CET counts for the next day.
- Baselines: no-text model, English-only text.
- Metrics: AUC and Brier score for big moves; MAE for absolute returns.

**What makes it creative.** It turns the review's "non-English" gap into a concrete question about how information spreads *across languages*.

**Supervisor connection.** Text analysis: yes. Graphs: weak. A co-mention network of Dutch firms could be added, but the core is NLP. **Flag: only partial fit.**

**Kill test.** Queries: `Dutch language financial news stock return prediction Euronext Amsterdam NLP`, `"Expected Returns and Large Language Models" Chen Kelly Xiu languages markets Netherlands Dutch`.
- Chen, Kelly & Xiu test news predictability in 16 markets and 13 languages [UNVERIFIED: I could not confirm whether Dutch or the Netherlands is included].
- FinGEITje (Noels et al., 2024, arXiv 2410.12835 [UNVERIFIED], background) is a Dutch financial LLM, not used for returns.
- Nobody tests a "local language beyond English" gain for Dutch stocks, as far as I found.
- **Outcome: weakened.**

### 6. Feasibility I4: 21/35
| Criterion | Score | Why |
|---|---|---|
| Data | 2 | The Dutch news archive is the bottleneck. Paywalls. |
| Coding | 3 | Standard NLP pipeline, but entity linking and time alignment are fiddly. |
| Novelty | 3 | Chen–Kelly–Xiu may already cover Dutch. |
| Eval | 3 | Clear metrics, but timestamp errors are easy to make. |
| Scope | 3 | Feasible only if data access is solved early. |
| Interests | 4 | Prediction + finance. Local relevance for an Accenture NL internship. |
| Supervisor | 3 | Text analysis yes; network/KG weak. |

---

## S5. Regime-dependent graph neural networks for volatility prediction (Kumar, Umeorah & Alochukwu, 2026)

### 1. Citation [FT]
Kumar, P. N., Umeorah, N., & Alochukwu, A. (2026). Regime-dependent graph neural networks for enhanced volatility prediction in financial markets. *Mathematics*, 14(2), 289. https://doi.org/10.3390/math14020289 (received 14 Nov 2025, published 13 Jan 2026; peer-reviewed). An earlier version is arXiv 2410.16858 (Oct 2024).

### 2. Summary
**Problem.** Forecast the volatility of 8 national stock indices (S&P 500, DAX, CAC 40, FTSE 100, Nifty 50, Nikkei 225, KOSPI, Hang Seng) at horizons of 1, 5, 15 and 21 days. Volatility is how much prices swing. The idea is that shocks spread between markets.

**Graph.** Each index is a node. Directed edges come from the **Diebold–Yilmaz spillover index**, a standard econometric measure of how much of one market's forecast uncertainty comes from shocks in another market (based on a VAR model). A correlation graph is the alternative.

**Model.** "TemporalGAT": an LSTM first encodes each index's past volatility, then two GCN layers and two GAT (graph attention) layers mix information across markets.

**Data.** Daily Yahoo Finance prices, Nov 2007–Jun 2022 (public):
- training to Aug 2014;
- validation Sep 2014–Dec 2017;
- test Jan 2018–Jun 2022.

The volatility "proxy" is squared daily returns.

**Results.**
- TemporalGAT beats GARCH, EGARCH, HAR-RV, LSTM and other GNN variants in the main tables (e.g., average MSE 0.01165, Table 3).
- The differences are tested with Diebold–Mariano tests and bootstrap intervals (§5.6).
- Spillover graphs work better than correlation graphs.

**The crucial result.** In the **strict expanding-window test** (§5.6.4, Table 11, pp. 40–41), the graph is estimated only from past data and the model is retrained as time moves forward. Under that test:
- R² becomes strongly negative (about −5.7 to −8.2), meaning the model forecasts worse than a constant;
- a dynamically re-estimated graph gives "no systematic gains" over a fixed graph (abstract).

**Code.** No code is mentioned. The data are Yahoo Finance.

### 3. Gaps the authors name
All of these are in §6 Conclusions (pp. 41–42), unless stated otherwise:
- **A noisy volatility proxy.** Squared daily returns are noisy. Use range-based estimators (Garman–Klass, Rogers–Satchell) and the QLIKE loss.
- **Static graphs.** The graph is "piecewise-static" (fixed within each period). Fully dynamic or intraday graphs are needed for rapid structural breaks; rolling graphs are "left for future work" (§4.3, Remark 1, pp. 16–17).
- **More data.** Other asset classes; macro, sentiment and microstructure inputs.

### 4. Gaps I see (my own analysis)
- **The main results are not truly out-of-sample.** The test-period graph is estimated *from the whole test period* (§4.3). The authors call this leakage-free "across phases", but within the test period it uses future information. The strict test then collapses (negative R²). The headline improvements are therefore probably optimistic.
- **Time zones are ignored.** On the same calendar day, Asian markets close before Europe and the US open. The edges should respect that order.
- **What switches spillover edges on is never explained.** The paper only says spillovers are "regime-dependent", without saying what causes a regime: crises, policy shocks, geopolitics.
- **Only 8 nodes.** The graph is tiny, so a GNN has little structure to exploit.

### 5. Thesis idea I5: "When politics flips the switch"
**Pitch.** Use news-based **country-pair geopolitical tension** (for example US–China tariff disputes, or EU–Russia sanctions) as the signal that switches volatility-spillover edges between national stock markets on, up or down. Then test whether this improves volatility forecasts under a *strict* out-of-sample design, the setting in which S5's model failed.

**Research question.** Does bilateral geopolitical tension, measured from news, tell us when volatility spillovers between two countries' stock markets strengthen? Does a graph model whose edges are "activated" by that tension forecast volatility better than strong econometric baselines?

**Sub-questions.**
1. Is the rolling spillover A→B larger in months with high A–B tension (descriptive and panel regression)?
2. Under expanding-window evaluation, does a tension-gated graph model beat:
   - HAR (the standard volatility model);
   - HAR with foreign lagged volatility;
   - a fixed-spillover GNN like S5?
3. Which country pairs and events drive the gains? This gives an analyst-friendly explanation.

**What gets predicted.**
- *Main target:* next-day and next-week realised volatility (Garman–Klass, computed from daily open/high/low/close) for each of about 20–25 national indices.
- *Edge-level target:* next month's spillover strength A→B. This is "edge-state forecasting", as in the earlier P1 proposal.

**Data.**
- *Prices:* daily index OHLC from Stooq (free).
- *Tension, monthly:* the **CEPII IntenSE** dataset (Chevalier, Crozet, Emlinger & Mirza, 2026 [FT, partial]). It gives monthly country-pair "Shade" (the share of negative-tone reports) and "Intensity", built from GDELT, for 201 countries, Mar 2015–Jul 2025. The paper says it is available on the CEPII website.
- *Tension, daily:* GDELT event data (public; BigQuery or raw files).
- *Access risk:* low to medium (monthly granularity; GDELT is noisy).

**Method sketch.**
- Rolling Diebold–Yilmaz spillovers using `statsmodels` VAR.
- HAR models (`statsmodels` OLS).
- A GNN in PyTorch Geometric with edge weight = spillover × learned function of tension.
- Session order (Asia → Europe → US) is built into the time lags.
- *Fallback:* drop the GNN and use HAR with tension-weighted foreign volatility. That is already a thesis.

**Evaluation.**
- Strict expanding window; graphs and tension use only past data.
- Losses: QLIKE and MSE.
- Tests: Diebold–Mariano and the Model Confidence Set (`arch` package).
- Report results separately for the 2018–19 and 2025 tariff periods.

**What makes it creative.** It brings your political interest *into the graph* as the reason edges switch on. That is the supervisor's "signed, time-activated edges" with an external, interpretable trigger.

**Supervisor connection.** Good: temporal graphs with time-activated edges, and text-derived (news) signals. There are no knowledge graphs.

**Kill test.**
- *Variant A (time-zone-ordered spillover graph): killed.*
  - Query: `nonsynchronous trading time zones graph neural network global volatility spillover forecasting`.
  - Zhao & Qiao (2026, arXiv 2608.25369 [ABS]) build a spillover-network transformer for *asynchronous* markets.
  - Chi, Gao & Wang (arXiv 2409.15320 [ABS]; cited elsewhere as *J. Forecasting* 2026 [UNVERIFIED]) handle all trading days.
  - Liu, Grith, Dong & Cucuringu (2026, arXiv 2603.10559 [ABS]) use time-ordered US→China session graphs.
- *Variant B (geopolitics-gated edges): survived.*
  - Query: `geopolitical events GDELT country pair edges graph neural network volatility spillover tariffs 2025 2026`.
  - Geopolitical risk spillovers are studied with classic connectedness tables (e.g., Palomba & Tedeschi, 2025 [UNVERIFIED]).
  - CEPII IntenSE is new and not linked to markets [FT, partial].
  - I found no GNN or volatility model that gates market edges with bilateral news tension.

### 6. Feasibility I5: 28/35
| Criterion | Score | Why |
|---|---|---|
| Data | 4 | Free prices + public CEPII/GDELT. Monthly tension is coarse. |
| Coding | 3 | VAR/HAR in `statsmodels` is easy. The GNN gate is moderate. |
| Novelty | 4 | No gated-edge work found. Variant A killed. |
| Eval | 4 | Standard volatility losses and tests. Strict OOS is easy to enforce. |
| Scope | 4 | The HAR-based fallback is solid. |
| Interests | 5 | Politics + finance + prediction (+ explanation). |
| Supervisor | 4 | Time-activated edges, temporal graph, text signals. No KG. |

---

## S6. A multi-graph learning framework to fuse heterogeneous market information (Li et al., 2026)

### 1. Citation [FT]
Li, Z., Xiong, J., Wang, J., Tan, J., Du Jardin, P., Deveci, M., & Zhong, K. (2026). A multi-graph learning framework to fuse heterogeneous market information for stock forecasting. *Expert Systems with Applications*, 319, 132142. https://doi.org/10.1016/j.eswa.2026.132142 (received Oct 2025, accepted 17 Mar 2026; peer-reviewed).

### 2. Summary
**Problem.** Predict tomorrow's up/down move for Chinese stocks using three kinds of information:
- numbers (prices, volume);
- text (financial news);
- company relations.

The key argument: "momentum spillovers" (through industry ties) and "media spillovers" (through news) travel along *different* graphs, so they should not be mixed in one graph.

**News processing.**
- Chinese news is parsed with a dependency parser (DDParser).
- Subject–predicate–object "event triples" are extracted, using hand-made rules suggested by analysts (§4.1).
- Each triple is embedded with FinBERT.

**Two graphs.**
- G1, an *industry* graph from the CSMAR database, carries the fundamentals.
- G2 is G1 *plus* links between firms that appear together in event triples, or have similar triple entities (cosine similarity above a threshold). It carries the news features.

**Model.** GRU encoders, two GCNs, and a two-branch "cross-attention" transformer that fuses the two graphs.

**Data.**
- 1,295 A/B-share stocks and 439k news articles from 12 Chinese sites, for **one year** (Dec 2017–Jan 2019, 243 trading days).
- Split 80/10/10 in time, so the **test is about 24 trading days**.
- The paper says the event relations are released, but the data statement says "available on request".

**Results.**
- Large universe: accuracy 0.571, AUC 0.579, against about 0.56 for strong baselines (Table 2).
- Using **Qwen3-8B (an LLM) for event extraction did *worse*** than the rule-based extractor (AUC 0.5485 vs 0.5714, Table 3).
- A Top-10 back-test reaches 56.5% annualised return with Sharpe 2.18, at zero transaction costs (Table 4).

### 3. Gaps the authors name
- No limitations section. The conclusion (§7, p. 11) only says the framework could transfer to other domains (social recommendation, derivatives, visual question answering).
- The introduction names the challenge they address: earlier work mixes all spillovers in one graph, and simple text representations lose information (§1–2).

### 4. Gaps I see (my own analysis)
- **The test period is tiny.** One year of data and about 24 test days are far too short to trust an AUC gain of 1–2 points or a Sharpe of 2.
- **Look-ahead is possible in the news graph.** It is not clear that G2's similarity edges are built only from news published *before* each prediction day.
- **Nobody knows which extracted links are real.** The LLM extractor did worse, but nobody knows *why*: did it miss real links, or add fake ones? There is no check of whether an extracted company–company link is economically real. Only end-task accuracy is reported.
- **The setting is narrow.** One market, one language, and no transaction costs.

### 5. Thesis idea I6: "Markets as annotators"
**Pitch.** Use the stock market's own reaction as an independent, automatic check on company–company relations that LLMs extract from text. Then learn to predict which extracted links the market will "confirm". That gives a filter for building better company knowledge graphs.

**Research question.** Can abnormal co-movement after a newly reported relation ("A signs a deal with B", "A sues B", "A supplies B") be used as weak supervision to separate material from spurious links in LLM-extracted company knowledge graphs?

**Sub-questions.**
1. After a relation between A and B is first reported on date d, do A and B show abnormal co-movement or spillover in the next 20 trading days, compared with matched unlinked pairs? Does this differ by relation type?
2. Which extraction settings produce links the market "confirms" more often?
   - rules vs open LLM;
   - single-pass vs reflection prompting;
   - 8-K filings vs news.
3. Can a classifier, using only the text of a relation, predict whether it will be market-confirmed, and so filter a knowledge graph before any price data exist?

**What gets predicted.**
- *Unit:* one extracted relation (edge).
- *Target:* "market-confirmed" yes/no, meaning significant abnormal return correlation or lead-lag between A and B in days d+1…d+20 compared with their pre-event baseline.
- *Horizon:* 20 trading days.

**Data.**
- *Text:* SEC 8-K filings, which are public and time-stamped; and/or GDELT GKG organisation co-mentions (public).
- *Relations:* the open FinReflectKG triples from 10-Ks (yearly).
- *Prices:* Stooq.
- *Names to tickers:* SEC `company_tickers.json`.

**Access risk.** Medium. EDGAR works from a laptop, not from my cloud session. Entity matching takes effort.

**Method sketch.**
1. Relation extraction with a small open LLM (e.g., Qwen-7B via `transformers` or `vllm`), or reuse FinReflectKG.
2. A market-model event study (`statsmodels` OLS).
3. Labels with Benjamini–Hochberg correction for many tests.
4. A classifier (logistic regression or LightGBM on sentence embeddings).
5. Optionally, a GNN on the resulting company knowledge graph.

**Evaluation.**
- Chronological.
- Placebo pairs: random pairs, and same-industry pairs.
- A hand-labelled check of 200 relations, to compare "market-confirmed" with human judgement.
- Metrics: AUC and precision@k of the filter; then the downstream gain of a filtered KG in a simple stock graph model.

**What makes it creative.** It reverses the usual direction: the market labels the knowledge graph, instead of the knowledge graph predicting the market. It also directly addresses S6's unexplained finding that LLM extraction was worse.

**Supervisor connection.** Very strong: knowledge-graph construction and quality, text analysis, and financial networks.

**Kill test.** Query: `LLM extracted company relations validated by stock price reaction knowledge graph quality 2026`.
- KG quality is judged with LLM-as-judge in FinReflectKG-EvalBench (Dimino et al., 2025/2026, arXiv 2510.05710 [ABS]).
- Web-mined, LLM-built firm networks are validated against a proprietary database and aggregate economic data (Köse et al., 2026, INET Oxford WP 2026-14 [ABS]).
- Supply-chain links found through search snippets are validated against CSMAR (Fukada & Mizuno, 2026, arXiv 2605.27845 [UNVERIFIED]).
- None of these use market reactions as the check.
- **Outcome: survived.**

### 6. Feasibility I6: 26/35
| Criterion | Score | Why |
|---|---|---|
| Data | 3 | All public, but EDGAR/GDELT processing and entity matching are work. |
| Coding | 3 | LLM extraction + event study + classifier: each is standard, but there are three parts. |
| Novelty | 5 | No market-as-validator work found. |
| Eval | 3 | No perfect ground truth. Confounding news needs care. |
| Scope | 3 | Doable if the sample is limited (e.g., S&P 500 8-Ks, 2015–2025). |
| Interests | 4 | Finance + trust/explainability of AI-built data. |
| Supervisor | 5 | KG + text + financial networks, her core area. |

---

## S7. Spatial-temporal stock prediction with a semantic company relationship graph (Luo, He, Cucuringu & Ma, 2026)

### 1. Citation [FT]
Luo, C., He, H. (H.), Cucuringu, M., & Ma, T. (2026). Spatial-temporal stock movement prediction and portfolio selection based on the semantic company relationship graph. *Quantitative Finance*, 26(1), 99–117. https://doi.org/10.1080/14697688.2025.2548897 (published online 12 Nov 2025; peer-reviewed; open access CC BY-NC-ND).

*Note: you uploaded this paper twice (the second copy has the suffix `_1`). The text is identical.*

### 2. Summary
**Problem.** Predict next-day up/down moves of S&P 500 stocks using a graph of how companies are related "in investors' minds".

**The SCRG graph.**
- They count how often company names (mapped to tickers) appear close together in **1.3 million Dow Jones Factiva news articles from 2000–2019**.
- Closer appearances count more (weight 1/word distance).
- Frequent "context words" are included as well.
- **GloVe** word embeddings are trained on these counts.
- Edges are the cosine similarity of two companies' embeddings, kept if above 0.45.

**The NIST-GNN model.**
- It extends a graph-convolutional recurrent network (GCRN).
- It uses a GCN filter instead of a Chebyshev filter.
- Importantly, each company gets **its own LSTM weights**, so stocks do not have to behave alike over time.

**Data.**
- 432 S&P 500 firms; prices from Financial Modeling Prep.
- In-sample 2007–2019; out-of-sample 2020–2022.
- Retrained every 20 days.
- Factiva is commercial and the news data are **not public**.

**Trading.**
- Portfolios hold only stocks whose model accuracy over the past 3 years exceeds a threshold.
- Daily long-short; no transaction costs.

**Results.**
- At threshold 0.53: Sharpe 1.03, against 0.42 with a correlation graph and 0.29 for the S&P 500 (Table 2).
- It holds up in each year 2020–2022 (Table 3) and across top-K variants.
- Accuracy is only about 54%.

**Main claim.** Public information "experiences a minimum one-day lag in diffusion" across linked firms, which the authors present as evidence against efficient markets (§5.6, §6).

### 3. Gaps the authors name
All in §5.6 (pp. 113–114):
- **The SCRG is static, but relationships change.** Model it dynamically.
- **The graph and the GNN are trained separately.** Train them end-to-end so the graph can be tuned with market information.
- **Predictions are binary.** Predict continuous returns (magnitude).
- They also suggest business-to-product and business-to-industry semantic networks (§5.5).

### 4. Gaps I see (my own analysis)
- **The "one-day lag" claim is not tested directly.** It is inferred from a daily model being profitable. Day t−1 data predict day t, but that is not a measurement of how fast information spreads. There are no trading costs, and accuracy is only about 54%.
- **Possible look-ahead in training.** The graph uses news up to 2019 for the whole in-sample period from 2007 onward. Early training years "see" relations that became known only later.
- **Survivorship.** The universe is S&P 500 members as of end-2019. Survivorship is handled out of sample only.
- **Not reproducible with public data.** Factiva is commercial.
- **Edges are unsigned and symmetric.** Similarity cannot express "A leads B", or "A and B move in opposite directions".

### 5. Thesis idea I7: "Does the news graph lead the price graph?"
**Pitch.** Build an open, *time-varying* version of the semantic company graph from public news (GDELT). Measure *how long* after two firms become linked in the news a price link between them appears. Then use news links in a temporal link predictor to forecast new signed price links. Along the way, test S7's "one-day lag" claim directly.

**Research question.** When two companies become newly linked in the news, does a signed price link (correlation or lead-lag) follow, after what delay? And do news-graph features improve the prediction of next month's signed price edges over price-only temporal link predictors?

**Sub-questions.**
1. What is the distribution of delays between the first strong news co-mention and the appearance of a price edge? Is a lag of one day or more typical?
2. Does adding news-graph features improve temporal link prediction of next month's signed price edges, against strong simple baselines (EdgeBank, "repeat last month")?
3. Which news contexts (deals, lawsuits, supply relations) produce price links fastest?

**What gets predicted.**
- *Target:* next-month signed price edge for each firm pair: positive, negative or none, from rolling residual correlations or lead-lag.
- *Horizon:* 1 month.

**Data.**
- GDELT GKG 2015–2025 ("organizations" field; public).
- Stooq prices for S&P 500 firms.

**Access risk.** Medium. GDELT organisation names are noisy, so build an alias table for about 500 firms.

**Method sketch.**
1. Co-mention counts per month, plus embeddings.
2. Temporal link predictors from DyGLib or TGB (TGN, GraphMixer).
3. A logistic-regression baseline.
4. An event-time analysis for the delay distribution.

**Evaluation.**
- Chronological.
- Negative sampling with historical negatives.
- Baselines: EdgeBank and persistence.
- Metrics: MRR and AUC.
- Tests split by sector and firm size.

**What makes it creative.** It answers S7's own stated limitation (a static graph) with open data, and it turns a claim about market efficiency into a measurable delay.

**Supervisor connection.** Very strong: text-derived networks plus temporal link prediction.

**Kill test.** Query: `news co-occurrence network predicts future stock return correlation network temporal link prediction`.
- Tang, Zhou & Hong (2019, *JRFM* 12(1):45 [ABS], background) already show that news co-occurrences predict return correlations up to 12 months ahead.
- Equity2Vec (2019, arXiv 1909.04497 [UNVERIFIED], background) uses dynamic co-mention graphs.
- Huang et al. (2026 [ABS]) build semantic 10-K networks for cross-stock predictability.
- **Outcome: weakened.** The core "news predicts correlation" result is known. What is new is signed lead-lag edges, delay measurement, and a modern temporal link prediction evaluation.

### 6. Feasibility I7: 26/35
| Criterion | Score | Why |
|---|---|---|
| Data | 4 | Public GDELT + prices. Name matching is noisy. |
| Coding | 3 | Existing temporal link prediction libraries. GDELT processing is moderate. |
| Novelty | 2 | The core relation has been known since 2019. |
| Eval | 4 | Clear temporal link prediction protocol with strong baselines. |
| Scope | 4 | Clear fallback (delay analysis only). |
| Interests | 4 | Finance + prediction. |
| Supervisor | 5 | Text networks + temporal link prediction. |

---

## S8. From technology hierarchies to convergence prediction: GCN link prediction in multilayer patent networks (Liu, Wang & Feng, 2026)

### 1. Citation [FT]
Liu, Z., Wang, X., & Feng, J. (2026). From technology hierarchies to convergence prediction: Integrating graph learning into multi-layer heterogeneous networks. *Advanced Engineering Informatics*, 69, 103927. https://doi.org/10.1016/j.aei.2025.103927 (received Jun 2025, online 19 Oct 2025; peer-reviewed).

### 2. Summary
**Problem.** Predict which technology topics will "converge", meaning they will start to be combined in new inventions. The case study is 3D printing.

**Data.** 70,718 3D-printing patents (1983–2023) from Derwent Innovations Index, a paid database.

**Method, step by step.**
1. A BERT classifier sorts patents into three layers (AUC above 0.9): micro (basic components, 40,340 patents), meso (integrated systems, 12,452) and macro (applications, 17,926). The source of the training labels is not described.
2. Each layer gets its own text elements:
   - micro: 300 TF-IDF keywords;
   - meso: 100 LDA topics;
   - macro: 9 BERTopic clusters.
3. A three-layer "funnel" network is built:
   - co-occurrence edges within the micro and meso layers;
   - "contains" and "shares-keywords" edges between layers.
4. A four-layer GCN predicts links between meso-layer topics.

**Results.**
- GCN AUC 0.95, against 0.76 for Node2Vec and 0.73 for random forest or SVM (Table 5).
- The top predicted convergences, e.g., medical tissue scaffolds × laser microstructure (T82–T86), are "validated" by checking whether 2024 Web of Science papers lie near them in a UMAP plot.

**Code and data.** Neither is released ("No data was used", data statement).

### 3. Gaps the authors name
All on p. 14 (§5–6):
- **Only one patent dataset.** Integrate papers and news through knowledge-graph fusion.
- **Weak validation.** Validation relies on existing literature only. Add socio-economic variables (market demand, policy incentives).
- **Unknown generalisability.** Test the method on other emerging fields.

### 4. Gaps I see (my own analysis)
- **The split is random, not chronological.** It uses a 90/10 random edge split of a network built from all 40 years at once (Table 4). "Predicting" convergence then means filling in hidden links of a known graph, not forecasting future ones. A time-split test with simple baselines (common neighbours, EdgeBank) is missing.
- **The graph is tiny.** There are only 100 topic nodes, so an AUC of 0.95 on a random hold-out is easy.
- **Firms and markets are missing.** Convergence is never connected to *which companies* are converging, or to whether the market notices.

### 5. Thesis idea I8: "Which listed companies will move into each other's technology next?"
**Pitch.** Build a firm–technology graph from free USPTO patent data. Forecast, with a proper chronological test, which listed firms will enter which technology classes. Then check whether firms predicted to converge start to move together in the stock market.

**Research question.** Can temporal link prediction on a firm–technology-class graph forecast new technology entries by listed firms better than simple baselines? Do predicted convergences between firms carry information about their future return co-movement?

**Sub-questions.**
1. Out of sample by filing year, how do TGN-type temporal link predictors compare with preferential attachment, EdgeBank and technology-relatedness baselines?
2. Do firm pairs that are predicted to become technologically close show rising return correlation in the following year?
3. Which technology paths typically lead to entry (explanation)?

**What gets predicted.**
- *Target:* new firm → CPC-group links, meaning the first patent application by the firm in that technology group.
- *Horizon:* the next 2 years.
- *Second-stage target:* next-year return correlation of firm pairs.

**Data.**
- USPTO PatentsView bulk data (free).
- Firm matching: SEC EDGAR company names plus fuzzy matching. A public patent–firm crosswalk such as DISCERN is an option, but its availability is **[UNVERIFIED]**.
- Prices: Stooq.

**Access risk.** Medium, mainly the matching of patent owners to listed firms.

**Method sketch.**
- Heterogeneous temporal graph models: PyTorch Geometric `HeteroConv`, DyGLib/TGB.
- Baselines: `networkx` link-prediction heuristics.

**Evaluation.**
- Chronological by application date: train up to 2014, validate 2015–2016, test 2017–2020.
- Patents are only *published* about 18 months after filing, so features must be dated by publication date to avoid look-ahead.
- Metrics: MRR, Hits@k, AUC with historical negatives.

**What makes it creative.** It replaces "random-split technology convergence" with real forecasting, and links patents to markets.

**Supervisor connection.** Good: heterogeneous temporal graphs and link prediction.

**Kill test.** Queries: `firm technology convergence prediction patents temporal link prediction listed companies stock returns 2025`, `temporal link prediction firm patent technology class bipartite graph neural network future technological entry`.
- Technology-convergence link prediction is a crowded topic in *Technological Forecasting and Social Change*, e.g., Park & Geum (2022) and Wang & Li (2024) [both UNVERIFIED].
- Firm-specific technology-opportunity link prediction also exists (Lee et al., 2021 [UNVERIFIED]).
- Technology-linked firms' returns predict each other (Lee, Sun, Wang & Zhang, *JFE* 2019 [UNVERIFIED], background).
- **Outcome: weakened.**

### 6. Feasibility I8: 22/35
| Criterion | Score | Why |
|---|---|---|
| Data | 3 | PatentsView is free. Matching patent owners to listed firms is the risk. |
| Coding | 3 | Heterogeneous temporal graph libraries exist. Data engineering is heavy. |
| Novelty | 2 | Crowded topic. The returns link is known. |
| Eval | 4 | Clean chronological protocol is possible. |
| Scope | 3 | Matching and cleaning could eat many weeks. |
| Interests | 3 | Prediction + some finance. |
| Supervisor | 4 | Heterogeneous temporal link prediction. |
