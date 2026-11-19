# Proti IQ — Complete Master Build Bible
## *Single Source of Truth: Architecture, Security, Data, & Codebase Execution*

**Hack the Fork Nigeria 2026** — *Challenge 1: AI for Alternative-Protein Ingredient Discovery*  
**Date:** 18 November 2026  
**Status:** Layer 1 Complete. Layers 2–7 Execution Phase.

---

## 1. Core Mission & Executive Summary
Proti IQ is an in-silico decision-support engine engineered to rank indigenous Nigerian and regional legume seed storage proteins by functional suitability against proven benchmark crops (*Vigna radiata* / mung bean, *Glycine max* / soy, *Pisum sativum* / pea) for three key food product applications:
1. **Plant-Based Egg Gel:** Thermal coagulation and heat-set network formation driven by 7S vicilin-like globulins.
2. **Tofu-Type Coagulated Gel:** Salt/calcium-induced firm curd network dominated by 11S legumin-like (glycinin) hexamers and intermolecular disulfide bridges.
3. **Plant-Based Milk Dispersion:** Neutral-pH colloidal solubility, low sedimentation, and emulsification stability.

---

## 2. The Strict Wording Guide (Non-Negotiable)

| Approved Phrasing ("Say") | Prohibited Phrasing ("Never Say") |
| :--- | :--- |
| "Ranks which crops to lab-test first" | "Finds the best crop for plant egg" |
| "Similarity-based likelihood, not a measurement" | "Predicts egg-like performance" |
| "Matches the published order in X of Y comparisons" | "Accurate", "Validated", "Proven" |
| "This crop has few sequences, so its ranking is low confidence" | Hiding thin data / claiming false precision |
| "Screening flag, not a safety clearance" | "Safe", "Non-toxic", "Cleared" |
| "Lab validation is the required next step" | "Guarantees", "Proves" |

---

## 3. The 7 Layers Build Progress

- **Layer 1 (Foundations & Config):** ✅ Done (`crops.yaml`, `jobs.yaml`, `confidence.yaml`, `answer_key.csv`, docs, `.env.example`, `SECURITY.md`, `README.md`)
- **Layer 2 (Data Ingestion & DB):** Ingest UniProt REST, AlphaFold DB, answer key import, coverage reporting.
- **Layer 3 (Feature Engineering):** Biopython `ProteinAnalysis` (pI, MW, GRAVY, charge pH 7, Cys %, secondary structure).
- **Layer 4 (AI Embeddings):** ESM-2 8M offline embeddings + SHA-256 artifact manifest.
- **Layer 5 (Scoring & Back-Test):** Multi-criteria similarity scoring, component breakdown, pairwise agreement, cowpea literature benchmark check.
- **Layer 6 (FastAPI Backend):** `/api/v1/rank`, `/api/v1/evidence`, `/api/v1/structure`, rate limiting, read-only DB role.
- **Layer 7 (Streamlit UI):** 3-click workflow, results table, component contributions, AlphaFold 3D structure viewer, evidence & back-test tab.
