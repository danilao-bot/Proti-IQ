# Proti IQ: 5-Person Team Roles & Technical AI Architecture

---

## 1. The Three AI Systems Used in Proti IQ

When mentors or judges ask: *"What AI models are powering Proti IQ?"*, here are the three specific systems:

### AI 1: Meta ESM-2 650M Transformer (Protein Language Model)
* **Model ID:** `facebook/esm2_t33_650M_UR50D` (650 Million parameters, 33 layers, 1280-dimensional hidden states).
* **Role in App:** Converts raw amino acid sequences of 348 seed storage proteins into 1280-D vectors representing 3D evolutionary folds and biological topology without requiring expensive wet-lab crystallography.
* **Status:** Zero-shot frozen foundation model. All 348 vectors are extracted and stored locally in `model_artifacts/embeddings/`.

### AI 2: DeepMind AlphaFold 2 / AlphaFold DB (Structural Topology)
* **Model ID:** AlphaFold Monomer v2.0 pipeline (AlphaFold DB v6 predictions).
* **Role in App:** Provides atomic 3D coordinate (.pdb) models and per-residue confidence scores (pLDDT: 0–100) for key benchmark storage proteins (`A0A1S3VZW2`, `P02858`, `P11827`) to visualize solvent accessibility and binding interfaces in `ui/pages/3_Structure.py`.

### AI 3: Generative Formulation & Clinical Advisory LLM
* **Recommended Free Provider:** **Groq Cloud API** (running open-weights `llama-3.3-70b-versatile` or `llama-3.1-8b-instant`) or **xAI Grok / Google Gemini Free Tier**.
* **Role in App:** Powers the conversational formulation assistant behind the `POST /api/v1/hub/advisory/formulate` endpoint. Takes the pre-computed biophysical scores and generates:
  * Tailored 5-step home kitchen recipes for consumers.
  * Personalized swallow fortification ratios (e.g. +15% cowpea hydrolysate in Amala) and BCAA mTOR analysis for clinical nutritionists.

---

## 2. Team Role Division (The 5 Builders)

| Teammate | Official Role | Core Deliverables | Hand-Off Target |
|:---|:---|:---|:---|
| **YOU (User)** | **AI Engineering & Backend Lead** | ESM-2 scoring pipeline, dynamic weights (`jobs.yaml`), FastAPI REST API (`main.py`, `hub.py`), open CORS | Serves live REST endpoints to Edna |
| **PRECIOUS** | **Database & Cloud Engineer** | Supabase PostgreSQL schema (`docs/SUPABASE_POSTGRESQL_SCHEMA.sql`), 9 tables, RLS security policies | Gives API keys & URI to You and Edna |
| **EDNA** | **Frontend & UI/UX Engineer** | React.js web client, responsive component cards, 3-persona user flows (Consumer vs Nutritionist vs Food Co) | Consumes FastAPI endpoints & Supabase |
| **VIVIAN** | **Biochemistry & Wet-Lab Lead** | Food chemistry validation, Path B formulation levers (pH, CaCl2, heat, blanching), Pretoria dataset check | Signs off on science claims |
| **TEAMMATE 5** | **Product, QA & Pitch Lead** | Mentors checklist compliance, pitch deck, 60-second screen recording backup (`Win + Alt + R`) | Presents to mentors and judges |

---

## 3. What You & Edna Collect from Precious

Once Precious executes `docs/SUPABASE_POSTGRESQL_SCHEMA.sql` on Supabase:
1. **For Edna (React):** `Project URL` + `anon (public)` key.
2. **For You (FastAPI):** `Connection string URI` + `service_role (secret)` key.

---

## 4. Master Application Scores (Latest Run run_383377)

| Target Application | African Yam Bean | Pigeon Pea | Cowpea | Groundnut | Bambara (Wet-Lab) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Plant Meat / Suya (`meat`)** | **93.9%** | **96.0%** | 88.2% | 92.2% | Press-cake fiber |
| **Tofu / Awara Curd (`gel`)** | **88.5%** | **87.9%** | 87.8% | 87.1% | LGC: 8.0% - 10.0% |
| **Plant Egg (`egg`)** | 82.6% | **87.4%** | **85.1%** | 85.1% | Elastic scramble |
| **Mayonnaise (`mayo`)** | 77.2% | **85.9%** | **82.3%** | 79.5% | 70% oil emulsion |
| **Crayfish Umami (`crayfish`)** | 75.6% | **83.2%** | **81.4%** | 77.4% | Fermented Iru |
| **Sarcopenia Swallows (`sarcopenia`)** | 74.1% | **81.5%** | **80.3%** | 76.9% | Low viscosity 18g protein |
| **Plant Milk (`milk`)** | 70.2% | **80.6%** | **79.1%** | 76.6% | **82.27% pH 7 solubility** |
