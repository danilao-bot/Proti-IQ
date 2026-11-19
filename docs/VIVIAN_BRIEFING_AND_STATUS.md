# Proti IQ - Project Status Report
**Hack the Fork Nigeria 2026 | Challenge 1: AI for Alternative-Protein Ingredient Discovery**
**Date:** 19 November 2026

---

## FOR VIVIAN (Biochemistry Team Member)

### What Vivian Needs to Know and Verify

**Your role is to be the biochemist who spot-checks the data before we present it. Here is what needs your eyes:**

---

### 1. Spot-Check the Pretoria Dataset (15 random rows)

We extracted 206 measurements from 8 University of Pretoria Excel files into:
`data/processed/pretoria_tidy_measurements.csv`

**What to do:** Open that CSV, randomly pick 15 rows, and trace each one back to its source spreadsheet using the `source_file` and `cell_range` columns. Confirm:
- The numeric value is correct
- The unit is correct (g/g vs %, % w/v etc.)
- The crop and variety names match the original sheet label

**Files to check against:**
- `data/raw/FUNCTIONAL PROPERTIES DATABASE.xlsx` (gelling, solubility, WAC, OAC)
- `data/raw/PROTEIN SOLUBILITY.xlsx`
- `data/raw/FINALsds band intensities.xlsx` (SDS-PAGE legumin/vicilin bands)
- `data/raw/SECONDARY STRUCTURES.xlsx` (FTIR alpha-helix, beta-sheet)

---

### 2. Confirm These Specific Numbers From the Spreadsheet

The following numbers appear in our reports and need to be verified against raw cells before anyone presents them:

| Claim | Source Sheet | Need Vivian To |
|:---|:---|:---|
| Cowpea Dr Saunders LGC = **5.0% w/v** | FUNCTIONAL PROPERTIES DATABASE.xlsx > Gelling | Confirm exact cell value |
| Cowpea Bechuana White LGC = **10.0% w/v** | FUNCTIONAL PROPERTIES DATABASE.xlsx > Gelling | Confirm exact cell value |
| Bambara Cream LGC = **8.0% w/v** | FUNCTIONAL PROPERTIES DATABASE.xlsx > Gelling | Confirm and check if Red Bambara is 8% or 10% |
| Lab-extracted Soy isolate LGC | FUNCTIONAL PROPERTIES DATABASE.xlsx > Gelling | The spreadsheet shows asterisks (*) not numbers - what does * mean exactly? |
| Lab-extracted Soy solubility pH 7 = **75.32%** | PROTEIN SOLUBILITY.xlsx | Confirm exact cell |
| Commercial Soy FH solubility pH 7 = **88.11%** | PROTEIN SOLUBILITY.xlsx | Confirm this is the Freddy Hirsch commercial control |
| Cowpea Dr Saunders solubility pH 7 = **82.64%** | PROTEIN SOLUBILITY.xlsx | Confirm exact cell |
| Bambara Cream solubility pH 7 = **79.23%** | PROTEIN SOLUBILITY.xlsx | Confirm |
| Bambara Red solubility pH 7 = **82.27%** | PROTEIN SOLUBILITY.xlsx | Confirm |

**Critical flag:** In the Gelling sheet, Soy FH shows `*` at all concentrations tested (2.5% to 15%). We interpreted this as "gelled at all concentrations tested" = did not find a minimum gelation concentration = LGC is above test range. Is that the correct interpretation of `*` and `ND` in the lab protocol?

---

### 3. Confirm the SDS-PAGE Band Interpretation

From `FINALsds band intensities.xlsx`:
- We are using legumin band intensity as a proxy for 11S globulin
- We are using vicilin band intensity as a proxy for 7S globulin

**Question for Vivian:** Is the legumin-to-vicilin ratio in that sheet reliable enough to use as an empirical 11S/7S ratio? Or were the bands run under conditions that make comparison between crops unreliable?

---

### 4. Scientific Sign-Off Language

Before the pitch, we need Vivian to confirm:
- "The 206 extracted measurements from the University of Pretoria open dataset have been reviewed by [Vivian's name], BSc/MSc Biochemistry, on [date]."

Until this sign-off, all reports label the rows as **"extracted, not independently verified."**

---

### 5. Files to Send Vivian Right Now

Send these three files to Vivian:

1. **`data/processed/pretoria_tidy_measurements.csv`** — the full extracted dataset with cell references
2. **`docs/DATA_DICTIONARY.md`** — description of every sheet, column, and unit
3. **`data/processed/pretoria_empirical_test_results.json`** — the disagreements we found (especially the soy solubility disagreement)

---

## WHAT WE HAVE DONE (Complete Build Log)

### Layer 1: Configuration & Documentation
- `config/crops.yaml` — All 8 crops with verified taxonomy IDs (confirmed today against UniProtKB REST API)
- `config/jobs.yaml` — Three food jobs (egg, gel, milk) with weights and benchmarks
- `config/confidence.yaml` — Confidence tier definitions
- `docs/PREP_PACK_AND_SPEC.md`, `docs/METHODS.md`, `docs/LIMITATIONS.md`, `docs/DATA_SOURCES.md`, `docs/DEMO_SCRIPT.md`, `docs/KNOWN_GAPS.md`, `docs/DATA_DICTIONARY.md`
- `docs/MENTOR_CHECKPOINT_1_PITCH.md` — One-page pitch (numbers need update, see below)
- `data/answer_key/answer_key.csv` — 17 curated literature measurements

### Layer 2: Data Ingestion & Database
- UniProt ingestion re-run with verified taxonomy IDs (UniProtKB 2026_04, snapshot_2026_04_20261118)
- 348 verified storage globulin proteins across 8 crops
- 81 stale legacy proteins with wrong taxonomy IDs purged
- African Yam Bean: Corrected to Taxon ID 92480 (*Sphenostylis stenocarpa*)
- Bambara: Confirmed at Taxon ID 115715, only 4 proteins total, 0 verified storage globulins
- Coverage report: `data/processed/coverage_report.csv`
- University of Pretoria dataset: 206 measurements extracted into `data/processed/pretoria_tidy_measurements.csv`
- Resource Pack importer: `pipeline/import_resource_pack.py` (ready for Feb 20 drop)

### Layer 3: Feature Extraction
- 4,524 biophysical features extracted across 348 proteins
- Features: MW, isoelectric point, GRAVY hydropathy, net charge at pH 5 and 7, cysteine %, secondary structure fractions, aromaticity, instability index

### Layer 4: Protein Representations
- 348 480-dimensional vectors generated and SHA-256 hash-pinned in `model_artifacts/manifest.json`
- **HONEST LABEL:** These are deterministic biocomputational vectors (amino acid frequencies + dipeptide frequencies + hash projection), NOT live ESM-2 transformer inference. ESM-2 weights are not in local cache. This is clearly logged as `deterministic_biocomputational_480d` in the manifest.

### Layer 5: Scoring & Validation
- 270 candidate-benchmark rankings scored under `run_744893` (tagged `model-v1-frozen-2`)
- Bambara correctly excluded from sequence ranking (0 storage globulins)
- Pretoria empirical validation run: 1 agreement, 2 disagreements, 2 ties
- Validation results saved: `data/processed/pretoria_empirical_test_results.json`
- Bambara alignment against Cowpea/Mung bean 7S/11S sequences: 0 hits above 40% identity confirmed

### Layer 6: FastAPI Backend
- `api/main.py`, `api/db.py`, `api/security.py`, routers, schemas
- Tested live: `GET /health` returns HTTP 200
- Tested live: `POST /api/v1/rank` returns HTTP 200 in milliseconds
- 6/6 automated tests passing

### Layer 7: Streamlit UI
- `ui/Home.py`, `ui/pages/1_Results.py` through `5_Sources.py`
- Evidence page updated: Measured vs Predicted separation, Pretoria pairwise results table, removed "held-out" / "independently confirmed" language
- Zero emojis anywhere

### Documentation Sanitization
- Removed all "held-out", "independently confirmed", "Spearman rho on n=3" overclaims
- pH ranges corrected: Tang 2023 is pH 3, 5, 7, 9; Pretoria is pH 3, 4, 7, 8
- Tofu gel rho = 0.92 relabeled as a feature sanity check on 11S/7S input ratios, not an autonomous model result

---

## WHAT REMAINS (Priority Order)

### URGENT: Before Any Mentor Presentation

**A. Fix the pitch numbers** (30 minutes)
The pitch was written with old scores. Current clean-run scores (run_744893):

| Job | Top Candidate | Max Score | 2nd | 3rd |
|:---|:---|:---|:---|:---|
| **Egg** | Pigeon pea | 65.7 | Groundnut 63.7 | Cowpea 62.4 |
| **Gel** | Groundnut | 70.7 | Pigeon pea 68.9 | Cowpea 67.3 |
| **Milk** | Groundnut | 48.5 | Cowpea 47.4 | Bambara 47.6 (Tier 1 only) |

Update `docs/MENTOR_CHECKPOINT_1_PITCH.md` with these exact numbers.

**B. Settle the embeddings claim** (1 hour or use Colab)
Two options:
1. Run true ESM-2 on Google Colab (export sequences as FASTA, run inference, save `.npy` files, copy back)
2. Keep current vectors but label everywhere as "sequence composition similarity" not "ESM-2 protein language model"

**C. Add confidence tiers with intervals to the UI** (2-3 hours)
The scoring engine returns scalar scores. We need:
- **Tier 1 (Measured):** Bambara, Cowpea, Soy (direct Pretoria wet-lab data)
- **Tier 2 (Predicted):** Pigeon pea, African yam bean, Groundnut (sequence similarity only)
- Bootstrap confidence intervals on scores

**D. Add the Lab-First Brief** (1 hour)
For the top 2 candidates per job, generate:
- The 3 specific lab assays to run first
- The benchmark value to beat
- The variety warning (must specify cultivar, not just species)

**E. Confirm event date and pack** (tonight)
- Confirm the hackathon date and venue
- Pack: laptop, charger, ID, printed one-pager

---

### MEDIUM PRIORITY: Before Final Submission

- Get Vivian's spot-check sign-off on 15 Pretoria rows
- Resolve Soy LGC value: the spreadsheet shows `*` and `ND` not a numeric LGC. The correct statement is "Soy FH did not reach LGC under test conditions (gelled strongly at 2.5%)" — not "Soy LGC = 12%"
- Resolve Bambara LGC: Cream = 8%, Red = 10% confirmed from spreadsheet. Report as range 8-10%, not a single number
- Add processing-sensitivity flag (mung bean failure case at pH treatment: 22% to 15%)
- Add "needs lab" badge where sequence prediction and wet-lab data contradict each other

---

### LOWER PRIORITY: Polish

- Migrate Streamlit UI to show Measured vs Predicted tabs properly
- Add downloadable PDF report from the UI
- Push to GitHub: `git push origin main --tags`
