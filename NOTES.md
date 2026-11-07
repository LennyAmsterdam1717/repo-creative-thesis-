# NOTES: decision log

## 2026-11-07: creative-ideas run on the uploaded studies

### Inputs and access
- **The GitHub repo `LennyAmsterdam1717/repo-creative-thesis-` was empty** when I cloned it (no commits, no files). All studies came from the 9 PDFs uploaded in chat.
- **Duplicate upload.** `823b6566-…semantic_company_relationship_graph.pdf` and `d767a45c-…_1.pdf` are the same paper (S7). Their extracted text is identical; only the file bytes differ, probably a download watermark. I processed it once, so there are **8 unique studies**.
- **All 8 PDFs parsed** with `pdftotext`. Nothing was skipped. I read each body in full, without the reference lists. S5 (45 pages) was read section by section, including the appendix on how the spillover index is derived.
- **Web access.**
  - WebSearch and WebFetch worked.
  - I did not try Google Scholar this run. Earlier runs logged it as blocked, so I did not retry.
  - The shell was not used for web downloads.
  - The page `cepii.fr/PDF_PUB/wp/2026/wp2026-02.pdf` was read only partly (the first 100k of 183k characters).
- **Mid-run requests from Frank.**
  1. Write the proposals so they are simple to understand. Done: plain language, with jargon explained.
  2. He asked why I was researching online. Answer: the brief asks for 1–2 kill-test searches per idea, to check that 2025–2026 work has not already done it.

### Kill-test search queries (all WebSearch, standard mode)
| Idea | Query | Outcome |
|---|---|---|
| I1 | `learned stock graph edge weights validated against supply chain customer relationships 2025` | No ground-truth audit of learned graphs; LLM-filtered 10-K graphs exist (arXiv 2604.19476) |
| I1 | `stock graph structure learning learned adjacency interpretability compared to industry classification faithfulness 2026` | Only "recovers sectors" checks → survived |
| I2 | `revolving door prediction politicians next job machine learning Wikidata` | Only political-economy studies of revolving-door laws |
| I2 | `career trajectory prediction politicians Wikidata positions held knowledge graph link prediction LLM` | CAPER (career TKG, non-public data), PG-RAG (MP ideology) → survived |
| I3 | `decision-focused learning portfolio optimization graph neural network correlation 2025` | Decision-focused portfolio papers exist (2502.00828, 2508.10776) |
| I3 | `end-to-end graph structure learning differentiable portfolio optimization layer stock relation graph` | CRISP 2510.20868, L2GMOM 2308.12212, GAPNet 2602.00888 → weakened |
| I4 | `Dutch language financial news stock return prediction Euronext Amsterdam NLP` | FinGEITje (Dutch financial LLM); no Dutch return study found |
| I4 | `"Expected Returns and Large Language Models" Chen Kelly Xiu languages markets Netherlands Dutch` | 16 markets / 13 languages; Dutch inclusion unverified → weakened |
| I5 | `nonsynchronous trading time zones graph neural network global volatility spillover forecasting` | 2608.25369, 2409.15320, 2603.10559 → **variant A killed** |
| I5 | `geopolitical events GDELT country pair edges graph neural network volatility spillover tariffs 2025 2026` | CEPII IntenSE dataset (2026); no gated-edge GNN found → variant B survived |
| I6 | `LLM extracted company relations validated by stock price reaction knowledge graph quality 2026` | KG quality judged by LLM-as-judge or proprietary databases, never by the market → survived |
| I7 | `news co-occurrence network predicts future stock return correlation network temporal link prediction` | Tang, Zhou & Hong 2019; Equity2Vec 2019 → weakened |
| I8 | `firm technology convergence prediction patents temporal link prediction listed companies stock returns 2025` | Lee et al. JFE tech links (background) |
| I8 | `temporal link prediction firm patent technology class bipartite graph neural network future technological entry` | Crowded technology-convergence literature in TFSC → weakened |

**Abstract pages opened with WebFetch:** 2608.25369, 2604.19476, 2510.20868, 2408.15620, 2603.10559, 2510.05710, 2502.00828, 2409.15320, 2605.04643, 2508.10776, 2508.17906, the JRFM 12(1):45 page, the INET Oxford WP 2026-14 page, and the CEPII WP 2026-02 PDF (partly).

### Decisions
- **One idea per study** (8 in total), as the brief asked. All studies had at least one usable gap.
- **I5 time-zone variant dropped (killed).** It was replaced by the geopolitics-gated variant.
- **Ranking tie at 26 (I6 vs I7).** Broken by novelty, so I6 ranks higher.
- **Search-snippet-only papers are marked [UNVERIFIED]** and not relied on. Papers whose arXiv or record page I opened are marked [ABS].
- **Scores are my judgement** using the rubric in the brief. Each has a one-line reason in `study_summaries.md`.

### Red flags noticed in the studies (worth remembering for the literature review)
- **S1.** A daily price MAPE of 0.80% against a random walk at 1.35% (Theil's U 0.59) is implausibly strong for mega-caps. There is no code. Survivorship bias.
- **S2.** Possible leakage: the career KG may include test transitions. Users are split at random. Table 3 and Table 5 disagree.
- **S3.** Label windows overlap the input window by 9 of 10 days. AUC 0.55, yet 310% cumulative return in 170 days, with no costs.
- **S5.** The test-period graph is estimated from the whole test period. The strict expanding-window R² is about −5.7 to −8.2.
- **S6.** One year of data and about 24 test days. The LLM extractor did worse than rules.
- **S7.** Static news graph built from 2000–2019 news but used from 2007 onward. Factiva is not public. No costs.
- **S8.** Random 90/10 edge split on a 100-node topic graph. No temporal test.

### Open questions and unverified leads
- Does Chen, Kelly & Xiu's 13-language sample include Dutch? [UNVERIFIED]
- CEPII IntenSE download link: the paper says it is on cepii.fr, but I did not find a direct link.
- Where FinReflectKG is released (Hugging Face?): the arXiv page does not say. The 6 Nov feasibility study did use a sample of 103 shards.
- The *J. Forecasting* 2026 publication of Chi, Gao & Wang is only cited by another paper [UNVERIFIED].
- Whether Wikidata has enough post-office employer (P108) data for European politicians: check first if I2 is chosen.
