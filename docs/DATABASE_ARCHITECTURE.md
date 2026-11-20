# Proti IQ Database Architecture & Supabase Integration Guide
**Target Audience:** Precious (Backend & Database Engineer)  
**Database Engine:** PostgreSQL 15 / 16 (Hosted on Supabase Cloud)  
**Schema File:** [SUPABASE_POSTGRESQL_SCHEMA.sql](file:///c:/Users/Hp/Downloads/Proti%20IQ/docs/SUPABASE_POSTGRESQL_SCHEMA.sql)  

---

## 1. Executive Summary & Purpose

The Proti IQ database stores and manages the data foundation for discovering alternative protein candidates from indigenous Nigerian crops. It bridges:
1. **Bioinformatics & Structural Proteomics:** UniProtKB sequences, ESM-2 Transformer embeddings (1280-D), physicochemical properties, and AlphaFold pLDDT scores.
2. **AI Screening Engine:** Versioned ranking runs (`model_runs` and `rankings`), explainability component scores, and confidence flags.
3. **Empirical Wet-Lab Benchmarks:** University of Pretoria functional property dataset (solubility, least gelation concentration, foaming capacity) and published literature benchmarks.
4. **Path B Processing Protocols:** Formulation guidelines for food technicians and biochemists (pH shifting, divalent salt cross-linking, heat induction).

---

## 2. Entity-Relationship Overview

```mermaid
erDiagram
    CROPS ||--o{ PROTEINS : "expresses"
    CROPS ||--o{ MEASUREMENTS : "tested_in"
    CROPS ||--o{ RANKINGS : "ranked_for"
    JOBS ||--o{ RANKINGS : "evaluates"
    JOBS ||--o{ MEASUREMENTS : "benchmarked_by"
    JOBS ||--o{ LAB_PROTOCOLS : "optimized_by"
    MODEL_RUNS ||--o{ RANKINGS : "generates"
    PROTEINS ||--o{ FEATURES : "characterized_by"
    PROTEINS ||--o| EMBEDDINGS : "represented_by"
    PROTEINS ||--o{ RANKINGS : "scored_as_representative"

    CROPS {
        varchar id PK
        varchar common_name
        varchar scientific_name
        crop_role role
        varchar primary_job
    }

    JOBS {
        varchar id PK
        varchar name
        varchar target_benchmark_accession
        text target_metric_to_beat
        text benchmark_citation
    }

    PROTEINS {
        bigint id PK
        varchar crop_id FK
        varchar accession UK
        boolean reviewed
        varchar name
        protein_family family
        integer length
        text sequence
        jsonb keywords
        float plddt_mean
    }

    FEATURES {
        bigint id PK
        bigint protein_id FK
        varchar feature_name
        float value
        varchar feature_set_version
    }

    EMBEDDINGS {
        bigint id PK
        bigint protein_id FK
        varchar model_name
        integer dim
        varchar vector_ref
        char sha256
    }

    MODEL_RUNS {
        varchar id PK
        varchar git_sha
        varchar data_snapshot_id
        varchar config_hash
        jsonb metrics
    }

    RANKINGS {
        bigint id PK
        varchar run_id FK
        varchar job FK
        varchar crop_id FK
        bigint protein_id FK
        float score
        confidence_level confidence
        jsonb contributions
        jsonb flags
    }

    MEASUREMENTS {
        bigint id PK
        varchar crop_id FK
        varchar property
        float value
        varchar unit
        varchar study_id
        text citation
    }

    LAB_PROTOCOLS {
        varchar id PK
        varchar job FK
        varchar title
        varchar target_metric_to_beat
        jsonb step_by_step_protocol
    }
```

---

## 3. Data Dictionary & Key Tables

### 3.1 `crops`
Stores both indigenous African candidate crops (`cowpea`, `bambara`, `pigeon_pea`, `african_yam_bean`, `groundnut`) and foreign benchmark crops (`soybean`, `mung_bean`).
- `role`: `'candidate'` or `'benchmark'`.
- `primary_job`: Suggested starting target (`'egg'`, `'gel'`, or `'milk'`).

### 3.2 `proteins`
The 348 curated seed storage proteins from UniProtKB.
- `accession`: The official UniProt accession ID (e.g. `A0A1S3VZW2` for Mung Bean 8S Vicilin, `P02858` for Soy Glycinin G4, `P11827` for Soy Beta-conglycinin).
- `family`: Storage family classification (`'7S'`, `'11S'`, or `'other'`).
- `reviewed`: `TRUE` if Swiss-Prot (experimentally verified), `FALSE` if TrEMBL (computationally translated).
- `plddt_mean`: AlphaFold confidence metric (0–100).

### 3.3 `embeddings`
Tracks the Meta ESM-2 650M Transformer embeddings (`facebook/esm2_t33_650M_UR50D`).
- `dim`: 1280.
- `vector_ref`: Path to the local or cloud `.npy` file.
- `sha256`: Cryptographic integrity hash matching `model_artifacts/manifest.json`.
- *Note on pgvector:* If Precious activates the `pgvector` extension in Supabase, an `embedding_vector vector(1280)` column can be added to run cosine distance queries directly inside Postgres.

### 3.4 `rankings`
Contains the calculated biophysical similarity scores comparing candidate proteins against benchmark controls for each food job.
- `score`: Scaled biophysical similarity score (0–100%).
- `confidence`: `'High'`, `'Medium'`, or `'Low'` based on sequence review status and presence of full storage domains.
- `contributions`: Detailed breakdown (ESM-2 embedding similarity, family match, sequence alignment identity, charge, cysteine fraction).

### 3.5 `measurements`
Stores the ground-truth empirical wet-lab measurements from the University of Pretoria dataset:
- Cowpea Dr Saunders isolate pH 7 solubility: **82.64%** (Cell M39).
- Lab-extracted Soy isolate pH 7 solubility: **75.32%** (Cell M36).
- Bambara Cream isolate pH 7 solubility: **79.23%** (Cell M37).
- Bambara Red isolate pH 7 solubility: **82.27%** (Cell M38).
- Least Gelation Concentration (LGC): Soy (<2.5% w/v), Cowpea (5.0% w/v), Bambara (8.0% w/v).

### 3.6 `lab_protocols`
The Path B Food Science formulations detailing the exact physicochemical interventions:
- pH shift (alkaline solubilization at pH 8.5–10.0, neutralization to pH 7.2).
- Divalent salt cross-linking (0.3% $\text{CaCl}_2$ or 0.25% $\text{CaSO}_4$).
- Thermal denaturation (heating at $80^\circ\text{C} - 85^\circ\text{C}$).
- Lipoxygenase enzyme inactivation ($90^\circ\text{C}$ blanching for 3 minutes).

---

## 4. Setup Instructions for Precious on Supabase

1. **Log in to Supabase:** Go to [supabase.com](https://supabase.com) and open or create the `proti-iq` project.
2. **Run the Migration Script:**
   - In the Supabase Dashboard, navigate to the **SQL Editor** (left navigation).
   - Click **New Query**.
   - Copy the entire contents of [SUPABASE_POSTGRESQL_SCHEMA.sql](file:///c:/Users/Hp/Downloads/Proti%20IQ/docs/SUPABASE_POSTGRESQL_SCHEMA.sql) and paste into the editor.
   - Click **Run**.
3. **Verify Tables & Seed Data:**
   - Go to the **Table Editor** tab.
   - Confirm that all 9 tables (`crops`, `jobs`, `proteins`, `features`, `embeddings`, `model_runs`, `rankings`, `measurements`, `lab_protocols`) are created.
   - Verify that `jobs` and `crops` are populated with initial seed records.
4. **Obtain API Keys & Connection Strings:**
   - Navigate to **Project Settings** -> **Database**.
   - Copy the **Connection string (URI)** (starts with `postgresql://postgres.[project-ref]:[password]@...`).
   - Under **Project Settings** -> **API**, copy:
     * `Project URL`
     * `anon public` key (for frontend React client read requests)
     * `service_role secret` key (for FastAPI backend pipeline writes)
5. **Configure FastAPI Environment:**
   - In `.env` on your server/local environment, set:
     ```bash
     DATABASE_URL="postgresql://postgres.[ref]:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require"
     SUPABASE_URL="https://[ref].supabase.co"
     SUPABASE_KEY="eyJhbGciOi..."
     ```
   - SQLAlchemy in `api/db.py` will automatically connect to Supabase PostgreSQL when `DATABASE_URL` starts with `postgresql://`.

---

## 5. Security & Access Rules (Row Level Security)
- **Frontend / React App:** Can query all tables using the public `anon` key. All tables have `SELECT` policies enabled for `true`.
- **Backend Scoring Pipeline & Data Ingestion:** Uses the private `service_role` key, which bypasses RLS to insert/update protein features, rankings, and embeddings.
- No public user can tamper with, overwrite, or delete scientific protein records.
