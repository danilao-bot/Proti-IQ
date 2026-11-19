# Proti IQ — Master Specification & Hackathon Prep Pack

**Event:** Hack the Fork Nigeria 2026 (20–21 Nov 2026, Veritas University, Abuja)  
**Challenge:** Challenge 1 — AI for alternative-protein ingredient discovery and functional optimisation  
**Target User:** Nigerian food developer or startup deciding which legume crops to send to the lab first  
**Status:** Ready for Phase 0 Kickoff

---

## 1. Executive Summary & Critical Ground Rules

### Three Foundational Corrections & Reality Checks
1. **Cowpea is already published as an egg substitute (Dec 2024, *Food Chemistry: X*):**  
   - **Never say:** *"Nobody has checked local Nigerian legumes."*  
   - **The honest pitch:** Published evidence is fragmented, measured under non-standard extraction conditions, and absent for most indigenous crops. Proti IQ synthesizes sequence, structural, and biochemical data into a single, ranked, explainable screening platform.  
   - **Validation check:** Cowpea is evaluated against external literature benchmarks. When the model ranks cowpea in the top tier alongside pigeon pea and groundnut, that provides directional alignment with wet-lab reality without claiming independent statistical proof.
2. **11S / 7S Ratio is a seed-level measurement, not sequence-computable:**  
   - In tofu-type gels, 11S (glycinin) to 7S ($\beta$-conglycinin) ratio correlates strongly with firmness ($R = 0.92$) and elasticity ($R = 0.98$) (*Foods 2025*).  
   - In Proti IQ, 11S/7S is an optional literature/crop-level input (null if unmeasured). Sequence-only gel scoring uses proxies (cysteine fraction for disulfide bridges, legumin-family membership) and explicitly states this proxy assumption on-screen.
3. **Cross-study numbers are not directly comparable:**  
   - Mung bean least gelation concentration (LGC) varies drastically by extraction protocol (e.g., 12% in Brishti 2017 vs 22% native / 15% pH-shifted in another).  
   - Model back-testing compares **within-study rank order** (Spearman rank correlation), never absolute numbers across different literature protocols.
4. **Machine Learning vs Analytical Scoring:**  
   - With 5–15 benchmark proteins, training a complex Random Forest produces overfitted noise.  
   - Core model: deterministic, explainable feature & embedding similarity with biochemist-reviewed transparent weights, evaluated via leave-one-out rank correlation. Supervised ML only triggers if verified labelled rows exceed ~30.

---

## 2. Target Crops & Candidate Data Strategy

### Benchmarks (Low Risk)
- **Mung bean (*Vigna radiata*):** Proven commercial plant egg benchmark (e.g. JUST Egg).
- **Soy (*Glycine max*):** Established milk and tofu gel benchmark.
- **Pea (*Pisum sativum*):** Secondary comparative benchmark (note: poor solubility in milk contexts).

### Candidates (Nigerian Legumes)
1. **Cowpea (*Vigna unguiculata*):** Storage proteins characterized; vicilin-like globulin validated in 2024 egg substitute literature. Low risk.
2. **Bambara groundnut (*Vigna subterranea*):** Vicilin characterized biochemically (*Diedericks et al. 2019*), but sequence coverage in UniProt may be thin. High priority UniProt check. *Plan B:* Use closest *Vigna* vicilin and flag visibly as "Low Confidence - Homology Proxy".
3. **Pigeon pea (*Cajanus cajan*):** Check 7S/11S sequence counts on UniProt.
4. **African yam bean (*Sphenostylis stenocarpa*):** Indigenous orphan crop; sequence coverage to be assessed via API.
5. **Groundnut (*Arachis hypogaea*):** Well sequenced; allergen screening flags are vital.

### Keep / Drop Rule
A candidate crop is ranked only if it possesses at least one valid 7S (vicilin-like) or 11S (legumin-like) storage protein sequence in UniProt. Otherwise, it is rendered with a "No Data / Unranked" badge—never fabricated.

---

## 3. Strict Wording & Compliance Guide (No Overclaiming)

| Approved Phrasing ("Say") | Prohibited Phrasing ("Never Say") |
| :--- | :--- |
| "Ranks which crops to lab-test first" | "Finds the best crop for plant egg" |
| "Similarity-based likelihood, not a measurement" | "Predicts egg-like performance" |
| "Matches the published order in X of Y comparisons" | "Accurate", "Validated", "Proven" |
| "This crop has few sequences, so its ranking is low confidence" | Hiding thin data / claiming false precision |
| "Screening flag, not a safety clearance" | "Safe", "Non-toxic", "Cleared" |
| "Lab validation is the required next step" | "Guarantees", "Proves" |

### Non-Negotiable Limitations to State Out Loud
- Published extraction methods vary widely; answer key data is small and indicative.
- Sequence and predicted structure similarity do not equal processing behaviour (heating, shear, ionic strength change function).
- AlphaFold models are in-silico predictions (pLDDT reported), not crystal structures.
- No wet-lab functional assays or sensory tasting were performed by this computational tool.

---

## 4. System Architecture & Tech Stack

```
[UniProt REST API]   [AlphaFold DB API]   [answer_key.csv]   [Resource Pack CSV]
        \                   |                    |                   /
         v                  v                    v                  v
   +----------------- OFFLINE PIPELINE (CLI / Precomputed) -----------------+
   | Ingest -> Validate -> Features -> ESM-2 8M Embed -> Scoring -> Backtest |
   +------------------------------------+-----------------------------------+
                                        v
                 SQLite (Local Dev) / PostgreSQL 16 (Docker)
                     + Hash-Pinned model_artifacts/
                                        ^
                                        | Read-Only Role
                          FastAPI Backend (/api/v1)
                                        ^
                                        | JSON
                         Streamlit Interactive UI
```

### Core Technologies
- **Runtime:** Python 3.11+
- **Backend:** FastAPI, Pydantic v2 (`extra="forbid"`), SQLAlchemy 2.0, Alembic, slowapi rate-limiting.
- **Biocomputing:** Biopython (`ProteinAnalysis`, `PairwiseAligner` with BLOSUM62), ESM-2 8M (`facebook/esm2_t6_8M_UR50D`) on CPU for offline embeddings, NumPy, SciPy, Scikit-learn.
- **Frontend:** Streamlit, Plotly, `stmol` / `py3Dmol` for AlphaFold 3D structure visualization.
- **Security:** Read-only DB connection for API, SHA-256 artifact manifest, CSV formula injection neutralization (`=`, `+`, `-`, `@`), rate limiting, no dynamic pickle loading.

---

## 5. Answer Key (Back-Test Benchmarks)

| Job | Protein / System | Measured Property | Reported Value | Source | Verified |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Egg** | Mung bean isolate | Least Gelation Conc. (LGC) | 12% (Soy: 14%) | Brishti et al. 2017 | [ ] |
| **Egg** | Mung bean isolate | Foaming capacity | 89.66% (Soy: 68.66%) | Brishti et al. 2017 | [ ] |
| **Egg** | Mung bean native vs pH 12 | LGC; Water holding | 22% (native) vs 15% (pH 12); 1.56 vs 4.81 g/g | pH-shifting literature | [ ] |
| **Egg** | Mung bean Albumin vs Globulin | LGC; Water retention @ 8% | 4% vs 8%; 80.3% vs 96.2% | Lalagüe, Food Colloids | [ ] |
| **Egg** | Cowpea vs Soy isolate | Heat gel @ 70°C; Foaming | Cowpea 12%, Soy 10%; Foaming 58.6-60.2 vs 31.9-33.0 mL | Horax et al. 2004 | [ ] |
| **Egg** | Cowpea vs Mung, Soy, Pea | Gel resemblance to egg | Cowpea gel closely resembled egg gel (qualitative) | Food Chemistry: X, 2024 | [ ] |
| **Egg/Gel**| Bambara vicilin | pI; Denaturation T; Solubility | 5.3; 92°C; 86% @ >200mM NaCl | Diedericks et al. 2019 | [ ] |
| **Tofu Gel**| Soy (7 varieties) | 11S/7S; Firmness; Solubility | 1.14–4.10; 1520–1889 gf; 57.5–69.7% | Foods 2025, 14(23):4029 | [ ] |
| **Tofu Gel**| Soy lines | 11S/7S: 3.76 vs 0.12 | Breaking stress ~4x higher at 3.76 | Breeding Science 50(2), 2000 | [ ] |
| **Milk** | Soy, Pea, Lentil, Chickpea | Solubility, Emulsifying, WHC | Comprehensive pH 3, 5, 7, 9 profiles | Tang et al. 2023, Foods 12(2) | [ ] |

---

## 6. Phase Execution Roadmap

- **Phase 0 (Setup & Foundations):** Directory structure, dependencies, config YAMLs, DB models & SQLite schema, Alembic setup, FastAPI skeleton with `/health`.
- **Phase 1 (Data Ingestion & Coverage):** UniProt REST ingest for crops + benchmarks, AlphaFold metadata fetch, answer key CSV import, coverage report generator.
- **Phase 2 (Feature Pipeline & Egg Model):** Biopython features (MW, pI, GRAVY, cysteine %, secondary structure), ESM-2 8M offline embeddings, scoring engine, back-test engine (pairwise agreement + cowpea literature check).
- **Phase 3 (Egg Vertical Slice End-to-End):** FastAPI endpoints (`/rank`, `/evidence`, `/structure`), Streamlit UI with 3-click flow, contributions panel, 3D AlphaFold viewer, and explicit limitations.
- **Phase 4 (Security Hardening):** Input bounds, CSP/CORS, CSV sanitization, SHA-256 artifact verification, `SECURITY.md`.
- **Phase 5 (Gel Job):** 11S/7S weighting, cysteine cross-linking proxy, back-test vs soy 7-variety dataset.
- **Phase 6 (Milk Job):** Solubility proxies (pI distance from neutral, GRAVY hydropathy), visible low-confidence badge.
- **Phase 7 (Hackathon Readiness):** Offline demo packaging, resource pack importer, pitch script matching the 7 deliverables.
