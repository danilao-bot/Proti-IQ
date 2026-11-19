# Proti IQ 🧬🇳🇬
**AI-Guided Decision-Support for Nigerian Legume Protein Functional Screening**

> **Hack the Fork Nigeria 2026** — *Challenge 1: AI for Alternative-Protein Ingredient Discovery and Functional Optimisation*  
> *Veritas University, Abuja | November 20–21, 2026*

---

## 🎯 What Proti IQ Does
Nigerian food innovators and startups face high R&D costs when exploring local crops (such as cowpea, Bambara groundnut, pigeon pea, and African yam bean) for plant-based egg, milk, or curd/tofu applications. 

**Proti IQ** evaluates and ranks indigenous Nigerian legume storage proteins against proven industrial benchmarks (**Mung bean** for egg, **Soy** for tofu gel & milk, and **Pea** for secondary comparison). 

> **Important Scientific Principle:**  
> Proti IQ **ranks which crops to lab-test first**. Scores represent **similarity-based likelihoods**, not empirical lab measurements. Proti IQ replaces blind trial-and-error with structured, explainable biocomputational screening.

---

## 🔬 Core Method & Architecture
1. **Biochemical Feature Profiling:** Isoelectric point ($pI$), molecular weight ($M_w$), hydropathicity (GRAVY), net charge at pH 7, and cysteine fractions (covalent cross-linking potential).
2. **Deep Protein Language Embeddings:** ESM-2 8M (`facebook/esm2_t6_8M_UR50D`) representations precomputed offline.
3. **AlphaFold 3D Confidence:** Integration of per-residue $p\text{LDDT}$ scores and coordinate models from AlphaFold DB.
4. **Transparent Explainability:** Every candidate displays exact biological contribution weights (family match, fold similarity, charge distribution).
5. **Back-Tested Evidence:** Directionally verified against peer-reviewed food literature (Brishti 2017, Horax 2004, Food Chemistry: X 2024, Foods 2025).

---

## 🚀 Quickstart (Local Development)

### 1. Requirements
- Python 3.11+
- Virtual environment (`venv` or `uv`)

### 2. Setup
```powershell
# Clone or navigate to repo
cd "c:\Users\Hp\Downloads\Proti IQ"

# Create virtual environment with uv or python
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the System
```powershell
# Run Offline Ingestion & Scoring Pipeline (Phase 1 & 2)
python -m pipeline.cli run-all

# Start FastAPI Backend (/api/v1)
uvicorn api.main:app --reload --port 8000

# Start Streamlit UI
streamlit run ui/Home.py
```

---

## 📂 Repository Structure
```
proti-iq/
├── config/             # crops.yaml, jobs.yaml, confidence.yaml
├── data/
│   ├── answer_key/     # answer_key.csv (Verified empirical benchmarks)
│   ├── raw/            # Cached UniProt & AlphaFold API responses
│   └── processed/      # Ingested datasets and coverage reports
├── docs/               # Scientific methods, limitations, pitch script
├── pipeline/           # Ingestion, ESM-2 embeddings, feature extraction, scoring
├── api/                # FastAPI backend endpoints (/api/v1)
├── ui/                 # Streamlit web application & 3D AlphaFold viewer
├── model_artifacts/    # Pinned embeddings, weights, and SHA-256 manifest
└── tests/              # Unit, back-test, security, and API contract tests
```

---

## 📜 Documentation Index
- [**Full Build Specification & Prep Pack**](file:///c:/Users/Hp/Downloads/Proti%20IQ/docs/PREP_PACK_AND_SPEC.md)
- [**Scientific Methodology**](file:///c:/Users/Hp/Downloads/Proti%20IQ/docs/METHODS.md)
- [**Limitations & Scope Boundaries**](file:///c:/Users/Hp/Downloads/Proti%20IQ/docs/LIMITATIONS.md)
- [**Data Sources & Attributions**](file:///c:/Users/Hp/Downloads/Proti%20IQ/docs/DATA_SOURCES.md)
- [**Pitch Script (7 Deliverables)**](file:///c:/Users/Hp/Downloads/Proti%20IQ/docs/DEMO_SCRIPT.md)
- [**Security & Threat Model**](file:///c:/Users/Hp/Downloads/Proti%20IQ/SECURITY.md)
