-- ==============================================================================
-- Proti IQ Database Schema for Supabase PostgreSQL (PostgreSQL 15 / 16)
-- Author: Proti IQ Architecture Team
-- Target: Supabase Cloud Database Instance
-- Description: Production schema supporting indigenous African legume protein
--              discovery, ESM-2 transformer vector metrics, and food formulation lab protocols.
-- ==============================================================================

-- 1. EXTENSIONS (Optional pgvector for direct vector similarity searches)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Uncomment if using Supabase pgvector extension:
-- CREATE EXTENSION IF NOT EXISTS vector;

-- 2. ENUM TYPES
DO $$ BEGIN
    CREATE TYPE crop_role AS ENUM ('candidate', 'benchmark');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE protein_family AS ENUM ('7S', '11S', 'other');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE confidence_level AS ENUM ('High', 'Medium', 'Low');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ------------------------------------------------------------------------------
-- 3. TABLE: crops
-- Description: Legume species evaluated (Indigenous Candidates vs Commercial Benchmarks)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.crops (
    id VARCHAR(50) PRIMARY KEY, -- e.g. 'cowpea', 'bambara', 'pigeon_pea', 'african_yam_bean', 'groundnut', 'soybean', 'mung_bean'
    common_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(100) NOT NULL,
    tax_id INTEGER,
    role crop_role NOT NULL DEFAULT 'candidate',
    primary_job VARCHAR(20), -- 'egg', 'gel', 'milk', or null
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ------------------------------------------------------------------------------
-- 4. TABLE: jobs
-- Description: Target food formulation jobs and target industrial benchmark proteins
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.jobs (
    id VARCHAR(20) PRIMARY KEY, -- 'egg', 'gel', 'milk'
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    target_benchmark_accession VARCHAR(30), -- 'A0A1S3VZW2' for egg, 'P02858' for gel, 'P11827' for milk
    target_metric_to_beat TEXT NOT NULL,
    benchmark_citation TEXT NOT NULL,
    config_version VARCHAR(20) NOT NULL DEFAULT '1.0'
);

-- ------------------------------------------------------------------------------
-- 5. TABLE: proteins
-- Description: Curated legume seed storage protein sequences (UniProtKB Swiss-Prot / TrEMBL)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.proteins (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    crop_id VARCHAR(50) NOT NULL REFERENCES public.crops(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    accession VARCHAR(30) UNIQUE NOT NULL, -- UniProt Accession, e.g. 'A0A1S3VZW2'
    reviewed BOOLEAN NOT NULL DEFAULT FALSE, -- TRUE = Swiss-Prot (Golden), FALSE = TrEMBL
    name VARCHAR(255) NOT NULL,
    family protein_family NOT NULL DEFAULT 'other',
    length INTEGER NOT NULL CHECK (length > 0),
    sequence TEXT NOT NULL,
    keywords JSONB NOT NULL DEFAULT '[]'::jsonb,
    alphafold_available BOOLEAN NOT NULL DEFAULT FALSE,
    plddt_mean DOUBLE PRECISION CHECK (plddt_mean >= 0 AND plddt_mean <= 100),
    tax_id INTEGER,
    organism_name VARCHAR(150),
    source_release VARCHAR(100) NOT NULL DEFAULT 'UniProtKB 2026_04',
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_proteins_crop_id ON public.proteins(crop_id);
CREATE INDEX IF NOT EXISTS idx_proteins_family ON public.proteins(family);
CREATE INDEX IF NOT EXISTS idx_proteins_accession ON public.proteins(accession);

-- ------------------------------------------------------------------------------
-- 6. TABLE: features
-- Description: Calculated physicochemical and sequence features (charge, pI, hydrophobicity, cysteines)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.features (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    protein_id BIGINT NOT NULL REFERENCES public.proteins(id) ON DELETE CASCADE,
    feature_name VARCHAR(50) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    feature_set_version VARCHAR(20) NOT NULL DEFAULT 'v1.0',
    calculated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT uq_protein_feature UNIQUE (protein_id, feature_name, feature_set_version)
);

CREATE INDEX IF NOT EXISTS idx_features_protein_name ON public.features(protein_id, feature_name);

-- ------------------------------------------------------------------------------
-- 7. TABLE: embeddings
-- Description: Meta ESM-2 650M Transformer embeddings metadata and vector storage
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.embeddings (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    protein_id BIGINT UNIQUE NOT NULL REFERENCES public.proteins(id) ON DELETE CASCADE,
    model_name VARCHAR(120) NOT NULL DEFAULT 'facebook/esm2_t33_650M_UR50D',
    dim INTEGER NOT NULL DEFAULT 1280,
    vector_ref VARCHAR(255) NOT NULL, -- Relative path to .npy file in object storage or S3/Supabase Storage
    sha256 CHAR(64) NOT NULL,
    -- Optional: If pgvector is enabled in Supabase, uncomment the column below:
    -- embedding_vector vector(1280),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_embeddings_protein ON public.embeddings(protein_id);

-- ------------------------------------------------------------------------------
-- 8. TABLE: model_runs
-- Description: Versioned scoring pipeline executions for reproducibility
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.model_runs (
    id VARCHAR(50) PRIMARY KEY, -- e.g. 'run_294078'
    git_sha VARCHAR(40) NOT NULL DEFAULT 'local_snapshot',
    data_snapshot_id VARCHAR(50) NOT NULL,
    config_hash VARCHAR(64) NOT NULL,
    metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ------------------------------------------------------------------------------
-- 9. TABLE: rankings
-- Description: AI screening scores comparing candidate proteins against job benchmarks
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.rankings (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id VARCHAR(50) NOT NULL REFERENCES public.model_runs(id) ON DELETE CASCADE,
    job VARCHAR(20) NOT NULL REFERENCES public.jobs(id) ON UPDATE CASCADE,
    benchmark_id VARCHAR(50) NOT NULL,
    crop_id VARCHAR(50) NOT NULL REFERENCES public.crops(id) ON UPDATE CASCADE,
    protein_id BIGINT NOT NULL REFERENCES public.proteins(id) ON DELETE RESTRICT,
    score DOUBLE PRECISION NOT NULL CHECK (score >= 0 AND score <= 100),
    confidence confidence_level NOT NULL DEFAULT 'Medium',
    contributions JSONB NOT NULL DEFAULT '{}'::jsonb,
    flags JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_rankings_lookup ON public.rankings(job, benchmark_id, run_id, score DESC);
CREATE INDEX IF NOT EXISTS idx_rankings_crop ON public.rankings(crop_id);

-- ------------------------------------------------------------------------------
-- 10. TABLE: measurements (Pretoria Functional Properties Database & Published Literature)
-- Description: Ground-truth empirical wet-lab measurements (solubility, gelation, foaming)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.measurements (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    crop_id VARCHAR(50) REFERENCES public.crops(id) ON UPDATE CASCADE,
    protein_id BIGINT REFERENCES public.proteins(id) ON DELETE SET NULL,
    job VARCHAR(20) REFERENCES public.jobs(id),
    property VARCHAR(100) NOT NULL, -- e.g. 'Solubility', 'LGC', 'Foam Capacity', 'Rupture Force'
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(30) NOT NULL, -- '%', '% w/v', 'N', 'Pa'
    conditions TEXT, -- e.g. 'pH 7.0, ambient 25C, 1% dispersion'
    extraction_method VARCHAR(255), -- e.g. 'Isoelectric precipitation (pH 4.5)'
    study_id VARCHAR(50) NOT NULL, -- e.g. 'PRETORIA_2024', 'BRISHTI_2017'
    citation TEXT NOT NULL,
    verified_by VARCHAR(100), -- Biochemist verification signature
    verified_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_measurements_crop ON public.measurements(crop_id);
CREATE INDEX IF NOT EXISTS idx_measurements_property ON public.measurements(property);

-- ------------------------------------------------------------------------------
-- 11. TABLE: lab_protocols (Path B Formulation Roadmaps)
-- Description: Evidence-based wet-lab processing levers for food scientists & biochemists
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.lab_protocols (
    id VARCHAR(50) PRIMARY KEY, -- 'protocol_egg_vicilin', 'protocol_gel_legumin', 'protocol_milk_colloid'
    job VARCHAR(20) NOT NULL REFERENCES public.jobs(id) ON UPDATE CASCADE,
    title VARCHAR(200) NOT NULL,
    biochemical_mechanism TEXT NOT NULL,
    target_metric_to_beat VARCHAR(255) NOT NULL,
    benchmark_citation TEXT NOT NULL,
    ph_regime VARCHAR(100) NOT NULL,
    thermal_profile VARCHAR(100) NOT NULL,
    ionic_additives VARCHAR(255) NOT NULL,
    step_by_step_protocol JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ------------------------------------------------------------------------------
-- 12. SEED INITIAL REFERENCE DATA (Jobs and Baseline Protocols)
-- ------------------------------------------------------------------------------
INSERT INTO public.jobs (id, name, description, target_benchmark_accession, target_metric_to_beat, benchmark_citation)
VALUES 
(
    'egg',
    'Heat-Set Plant-Based Egg Gel',
    'Evaluation of 7S vicilin trimeric globulins for heat-set scramblable egg alternative.',
    'A0A1S3VZW2',
    'JUST Egg scramble texture: Rupture Force ~0.8 N, Springiness >85%',
    'Brishti et al., 2017; US Patent 10,820,612 B2'
),
(
    'gel',
    'Coagulated Curd Gel (Tofu Type)',
    'Evaluation of 11S legumin hexameric globulins for divalent ion-mediated curd formation.',
    'P02858',
    'Commercial Firm Tofu: Breaking Stress 1.2 - 1.5 N, Elastic Modulus G'' > 1200 Pa',
    'Foods 2025; Poysa et al., Breeding Science 2000'
),
(
    'milk',
    'Colloidal Plant-Based Milk',
    'Evaluation of high-solubility globulins for stable neutral-pH emulsion suspension.',
    'P11827',
    'Soy Milk Stability: Colloidal Stability Index >90% (7 days at 4C), pH 7 Solubility >80%',
    'Tang et al., 2023; University of Pretoria Dataset 2024'
)
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    target_benchmark_accession = EXCLUDED.target_benchmark_accession,
    target_metric_to_beat = EXCLUDED.target_metric_to_beat,
    benchmark_citation = EXCLUDED.benchmark_citation;

-- Seed Candidate and Benchmark Crops
INSERT INTO public.crops (id, common_name, scientific_name, tax_id, role, primary_job, description)
VALUES
('cowpea', 'Cowpea', 'Vigna unguiculata', 3899, 'candidate', 'milk', 'Drought-tolerant West African staple legume high in 7S/11S storage proteins.'),
('bambara', 'Bambara Groundnut', 'Vigna subterranea', 3914, 'candidate', 'gel', 'Indigenous semi-arid legume with superior gelation (LGC 8-10%) and 82.3% solubility.'),
('pigeon_pea', 'Pigeon Pea', 'Cajanus cajan', 3862, 'candidate', 'egg', 'Widely cultivated nitrogen-fixing legume with high homology to mung bean vicilin.'),
('african_yam_bean', 'African Yam Bean', 'Sphenostylis stenocarpa', 3886, 'candidate', 'gel', 'Underutilized protein-dense tuberous legume rich in 11S legumin subunits.'),
('groundnut', 'Groundnut (Peanut)', 'Arachis hypogaea', 3818, 'candidate', 'gel', 'Oilseed legume producing arachin (11S) and conarachin (7S) globulins.'),
('soybean', 'Soybean', 'Glycine max', 3847, 'benchmark', 'gel', 'Industrial gold standard control for coagulated curd and plant milk.'),
('mung_bean', 'Mung Bean', 'Vigna radiata', 3916, 'benchmark', 'egg', 'Commercial gold standard control for heat-set egg substitute (JUST Egg).')
ON CONFLICT (id) DO UPDATE SET 
    common_name = EXCLUDED.common_name,
    scientific_name = EXCLUDED.scientific_name,
    role = EXCLUDED.role;

-- ------------------------------------------------------------------------------
-- 13. ROW LEVEL SECURITY (RLS) POLICIES FOR SUPABASE
-- ------------------------------------------------------------------------------
ALTER TABLE public.crops ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.proteins ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.features ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.model_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rankings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.measurements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lab_protocols ENABLE ROW LEVEL SECURITY;

-- Anonymous and authenticated read-only access for Frontend (React / Streamlit / Mobile)
CREATE POLICY "Public Read Access on crops" ON public.crops FOR SELECT USING (true);
CREATE POLICY "Public Read Access on jobs" ON public.jobs FOR SELECT USING (true);
CREATE POLICY "Public Read Access on proteins" ON public.proteins FOR SELECT USING (true);
CREATE POLICY "Public Read Access on features" ON public.features FOR SELECT USING (true);
CREATE POLICY "Public Read Access on embeddings" ON public.embeddings FOR SELECT USING (true);
CREATE POLICY "Public Read Access on model_runs" ON public.model_runs FOR SELECT USING (true);
CREATE POLICY "Public Read Access on rankings" ON public.rankings FOR SELECT USING (true);
CREATE POLICY "Public Read Access on measurements" ON public.measurements FOR SELECT USING (true);
CREATE POLICY "Public Read Access on lab_protocols" ON public.lab_protocols FOR SELECT USING (true);

-- Backend API Service Role write access
-- By default in Supabase, the `service_role` secret bypasses RLS and has full write permissions.
