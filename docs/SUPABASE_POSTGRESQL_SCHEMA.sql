-- ==============================================================================
-- Proti IQ Master Production Database Schema for Supabase PostgreSQL (PostgreSQL 15 / 16)
-- Target: Supabase Cloud Database Instance
-- Architecture: Complete African Alternative-Protein Discovery Hub & Decision Engine
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. ENUM TYPES
DO $$ BEGIN
    CREATE TYPE crop_role AS ENUM ('candidate', 'benchmark', 'orphan_expansion');
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

DO $$ BEGIN
    CREATE TYPE user_persona AS ENUM ('consumer', 'nutritionist', 'food_processor');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ------------------------------------------------------------------------------
-- 2. TABLE: crops
-- Description: Master catalog of 14 Indigenous African Legumes & Commercial Benchmarks
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.crops (
    id VARCHAR(50) PRIMARY KEY, -- e.g. 'cowpea', 'bambara_groundnut', 'pigeon_pea', 'african_yam_bean'
    common_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(100) NOT NULL,
    tax_id INTEGER,
    role crop_role NOT NULL DEFAULT 'candidate',
    primary_region VARCHAR(100) NOT NULL DEFAULT 'West Africa',
    protein_content_pct VARCHAR(30), -- e.g. '23% - 26%'
    sequence_data_status VARCHAR(50) NOT NULL DEFAULT 'Available', -- 'Available', 'Orphan / Wet-Lab Only'
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ------------------------------------------------------------------------------
-- 3. TABLE: jobs
-- Description: The 7 Alternative-Protein Target Applications & Benchmark Proteins
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.jobs (
    id VARCHAR(30) PRIMARY KEY, -- 'egg', 'milk', 'gel', 'meat', 'crayfish', 'mayo', 'sarcopenia'
    name VARCHAR(120) NOT NULL,
    animal_replaced VARCHAR(100) NOT NULL,
    target_benchmark_accession VARCHAR(30) NOT NULL,
    benchmark_crop_id VARCHAR(50) NOT NULL,
    target_metric_to_beat TEXT NOT NULL,
    benchmark_citation TEXT NOT NULL,
    biochemical_mechanism TEXT NOT NULL
);

-- ------------------------------------------------------------------------------
-- 4. TABLE: meals (Traditional African Meals Layer)
-- Description: Authentic African dishes connecting crops to cultural diets & 'Plant-Based as Cooked' verification
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.meals (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    local_names VARCHAR(150), -- e.g. 'Kosai, Koose, Acaraje'
    country VARCHAR(100) NOT NULL, -- 'Nigeria', 'Ghana', 'Kenya', 'South Africa', 'Pan-African'
    primary_crop_id VARCHAR(50) REFERENCES public.crops(id) ON UPDATE CASCADE,
    meal_type VARCHAR(50) NOT NULL, -- 'Pudding', 'Fritter', 'Stew', 'Drink', 'Snack', 'Curd', 'Swallow'
    plant_based_as_cooked VARCHAR(50) NOT NULL, -- '100% Plant-Based', 'Plant-Based as Cooked'
    animal_ingredient_to_swap TEXT, -- e.g. 'Replace dried crayfish with fermented Iru for 100% plant-based'
    description TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ------------------------------------------------------------------------------
-- 5. TABLE: proteins
-- Description: Curated seed storage proteins from UniProtKB
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.proteins (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    crop_id VARCHAR(50) NOT NULL REFERENCES public.crops(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    accession VARCHAR(30) UNIQUE NOT NULL, -- e.g. 'A0A1S3VZW2', 'P02858', 'P11827'
    reviewed BOOLEAN NOT NULL DEFAULT FALSE,
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
-- Description: Calculated physicochemical features (MW, pI, net charge, GRAVY, cysteines)
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
    vector_ref VARCHAR(255) NOT NULL,
    sha256 CHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ------------------------------------------------------------------------------
-- 8. TABLE: model_runs
-- Description: Model execution run tracking for scientific reproducibility
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.model_runs (
    id VARCHAR(50) PRIMARY KEY, -- e.g. 'run_383377'
    git_sha VARCHAR(40) NOT NULL DEFAULT 'local_snapshot',
    data_snapshot_id VARCHAR(50) NOT NULL,
    config_hash VARCHAR(64) NOT NULL,
    metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ------------------------------------------------------------------------------
-- 9. TABLE: rankings
-- Description: In-silico AI screening biophysical similarity scores across all 7 jobs
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.rankings (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id VARCHAR(50) NOT NULL REFERENCES public.model_runs(id) ON DELETE CASCADE,
    job VARCHAR(30) NOT NULL REFERENCES public.jobs(id) ON UPDATE CASCADE,
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
-- 10. TABLE: measurements (University of Pretoria & Empirical Wet-Lab Data)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.measurements (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    crop_id VARCHAR(50) REFERENCES public.crops(id) ON UPDATE CASCADE,
    job VARCHAR(30),
    property VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(30) NOT NULL,
    conditions TEXT,
    study_id VARCHAR(50) NOT NULL,
    citation TEXT NOT NULL,
    verified_by VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_measurements_crop ON public.measurements(crop_id);

-- ------------------------------------------------------------------------------
-- 11. TABLE: lab_protocols (Path B Food Science Roadmaps)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.lab_protocols (
    id VARCHAR(50) PRIMARY KEY,
    job VARCHAR(30) NOT NULL REFERENCES public.jobs(id) ON UPDATE CASCADE,
    title VARCHAR(200) NOT NULL,
    target_metric_to_beat VARCHAR(255) NOT NULL,
    benchmark_citation TEXT NOT NULL,
    extraction_ph VARCHAR(100) NOT NULL,
    thermal_profile VARCHAR(100) NOT NULL,
    ionic_coagulant VARCHAR(255) NOT NULL,
    step_by_step_protocol JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ------------------------------------------------------------------------------
-- 12. TABLE: advisory_inquiries
-- Description: Stores role-based formulation requests from Edna's React frontend
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.advisory_inquiries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    persona user_persona NOT NULL,
    job VARCHAR(30) REFERENCES public.jobs(id),
    crop_id VARCHAR(50) REFERENCES public.crops(id),
    country VARCHAR(50) DEFAULT 'Nigeria',
    older_person_mode BOOLEAN DEFAULT FALSE,
    response_payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ------------------------------------------------------------------------------
-- 13. SEED DATA: All 14 African & Benchmark Crops
-- ------------------------------------------------------------------------------
INSERT INTO public.crops (id, common_name, scientific_name, tax_id, role, primary_region, protein_content_pct, sequence_data_status, description)
VALUES
-- Core Scored Nigerian Candidates
('cowpea', 'Cowpea (Black-eyed pea)', 'Vigna unguiculata', 3899, 'candidate', 'West Africa', '23% - 26%', 'Available', 'Drought-tolerant West African staple legume high in 7S beta-vignin.'),
('pigeon_pea', 'Pigeon Pea', 'Cajanus cajan', 3862, 'candidate', 'East & West Africa', '21% - 25%', 'Available', 'Nitrogen-fixing pulse with high homology to mung bean vicilin and soy legumin.'),
('african_yam_bean', 'African Yam Bean', 'Sphenostylis stenocarpa', 3886, 'candidate', 'West & Central Africa', '24% - 29%', 'Available', 'Underutilized protein-dense tuberous legume rich in 11S legumin subunits.'),
('groundnut', 'Groundnut (Peanut)', 'Arachis hypogaea', 3818, 'candidate', 'Pan-African', '25% - 28%', 'Available', 'Major oilseed legume producing arachin (11S) and conarachin (7S) globulins.'),

-- Tier 1 Wet-Lab & Expansion Crops
('bambara_groundnut', 'Bambara Groundnut', 'Vigna subterranea', 3914, 'candidate', 'Pan-African', '20% - 24%', 'Orphan / Wet-Lab Only', 'Indigenous pulse with 82.3% solubility and superior gelation (Okpa); evaluated via Pretoria wet-lab data.'),
('african_locust_bean', 'African Locust Bean (Iru/Dawadawa)', 'Parkia biglobosa', 148316, 'orphan_expansion', 'West African Savanna', '30% - 35%', 'Orphan / Traditional', 'Savanna tree legume fermented into traditional umami savory condiment to replace crayfish and MSG.'),
('kerstings_groundnut', 'Kerstings Groundnut', 'Macrotyloma geocarpum', 290479, 'orphan_expansion', 'West Africa (Benin/Nigeria/Togo)', '21% - 24%', 'Orphan / Underutilized', 'High-lysine subterranean pulse highly resilient to semi-arid drought.'),
('lablab_bean', 'Lablab (Hyacinth Bean)', 'Lablab purpureus', 3854, 'orphan_expansion', 'East & Central Africa', '22% - 26%', 'Available', 'Multi-purpose traditional pulse with robust starch-protein matrix.'),
('african_breadfruit', 'African Breadfruit (Ukwa)', 'Treculia africana', 193514, 'orphan_expansion', 'Southeastern Nigeria', '18% - 20%', 'Orphan / Underutilized', 'Protein- and fat-dense seed staple traditionally eaten as rich pottage in Igboland.'),
('marama_bean', 'Marama Bean', 'Tylosema esculentum', 162843, 'orphan_expansion', 'Southern Africa (Kalahari)', '30% - 37%', 'Orphan / Underutilized', 'Arid wild perennial legume rich in protein and unsaturated fatty acids.'),
('winged_bean', 'Winged Bean', 'Psophocarpus tetragonolobus', 3882, 'orphan_expansion', 'Tropical Africa & Asia', '30% - 40%', 'Available', 'Super-legume with protein and lipid composition comparable to soybean.'),

-- International Commercial Controls
('soybean', 'Soybean', 'Glycine max', 3847, 'benchmark', 'Global', '36% - 40%', 'Available', 'Global industrial control for tofu curd, soy milk, and TVP meat.'),
('mung_bean', 'Mung Bean', 'Vigna radiata', 3916, 'benchmark', 'Global', '24% - 26%', 'Available', 'Commercial control for heat-set liquid egg substitutes (JUST Egg).'),
('field_pea', 'Field Pea', 'Pisum sativum', 3888, 'benchmark', 'Global', '21% - 25%', 'Available', 'Commercial control for yellow pea protein burgers and plant milk.')
ON CONFLICT (id) DO UPDATE SET 
    common_name = EXCLUDED.common_name,
    protein_content_pct = EXCLUDED.protein_content_pct,
    sequence_data_status = EXCLUDED.sequence_data_status;

-- ------------------------------------------------------------------------------
-- 14. SEED DATA: All 7 Target Jobs & Commercial Benchmarks
-- ------------------------------------------------------------------------------
INSERT INTO public.jobs (id, name, animal_replaced, target_benchmark_accession, benchmark_crop_id, target_metric_to_beat, benchmark_citation, biochemical_mechanism)
VALUES
(
    'egg',
    'Heat-Set Plant-Based Egg Gel',
    'Chicken Eggs (Scrambled & Baking)',
    'A0A1S3VZW2',
    'mung_bean',
    'JUST Egg scramble texture: Rupture Force ~0.8 N, Springiness >85%',
    'Brishti et al., 2017; US Patent 10,820,612 B2',
    'Thermal unfolding of 7S vicilin trimers at 72C-80C creates an elastic, scramblable gel matrix without rubbery hardness.'
),
(
    'gel',
    'Coagulated Curd / Tofu / Awara',
    'Stew Meat Chunks & Fulani Cow Cheese (Wara / Wagashi)',
    'P02858',
    'soybean',
    'Commercial Firm Tofu: Breaking Stress 1.2 - 1.5 N, Elastic Modulus G'' > 1200 Pa',
    'Foods 2025; Poysa et al., Breeding Science 2000',
    'Divalent calcium ions (0.3% CaCl2) cross-link negatively charged Asp/Glu residues; 85C heat triggers covalent intermolecular -S-S- bonds.'
),
(
    'milk',
    'Colloidal Plant-Based Milk',
    'Cow Milk & Canned Evaporated Milk',
    'P11827',
    'soybean',
    'Soy Milk Stability: Colloidal Stability Index >90% (7 days at 4C), pH 7 Solubility >80%',
    'Tang et al., 2023; University of Pretoria Dataset 2024',
    'Strong net negative charge (-18 to -28 mV) provides electrostatic repulsion against curdling; 90C blanching deactivates lipoxygenase.'
),
(
    'meat',
    'Textured Plant-Based Meat & Suya',
    'Red Meat, Beef & Chewy Goat Meat (Asun)',
    'P02858',
    'soybean',
    'Extruded TVP Chewiness: High tensile shear modulus matching cooked beef fibers',
    'Osen et al., Food Chemistry 2014; Foods 2025',
    '11S legumin hexamers unfold under twin-screw extrusion shear (140C-160C), forming aligned, parallel meat-like fibers.'
),
(
    'crayfish',
    'Savory Umami Peptides & Crayfish Alternative',
    'Dried River Crayfish & Smoked Fish Seasoning Powder',
    'P11827',
    'soybean',
    'Savory Broth Profile: High free glutamic acid and sulfurous savory peptides',
    'Beaumont 2002; Achi 2005 (Fermented Legume Condiments)',
    'Solid-state fermentation with Bacillus subtilis hydrolyzes storage globulins into short umami peptides (<1 kDa).'
),
(
    'mayo',
    'Plant-Based Mayonnaise & Emulsions',
    'Commercial Egg-Yolk Mayonnaise & Salad Creams',
    'P11827',
    'soybean',
    'Emulsion Stability: 70% vegetable oil phase stable >12 months without separation',
    'McSweeney et al., Food Hydrocolloids 2021',
    'Amphiphilic surface-active 7S globulins wrap around microscopic oil droplets, preventing droplet coalescence.'
),
(
    'sarcopenia',
    'Clinical Sarcopenia High-Protein Swallows & Porridges',
    'Medical Whey Protein Isolate & Meat Broth Fortifiers',
    'P11827',
    'soybean',
    'Clinical Delivery: 18g protein / 100g portion with zero paste viscosity increase',
    'Bauer et al., JAMDA 2013; WHO Protein Quality Guidelines',
    'Enzymatic pre-digestion (DH 5-8%) reduces molecular weight, allowing seamless fortification into Amala, Tuwo, and Ogi.'
)
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    animal_replaced = EXCLUDED.animal_replaced,
    target_metric_to_beat = EXCLUDED.target_metric_to_beat,
    biochemical_mechanism = EXCLUDED.biochemical_mechanism;

-- ------------------------------------------------------------------------------
-- 15. SEED DATA: 16 Authentic African Meals & Dietary Flags
-- ------------------------------------------------------------------------------
INSERT INTO public.meals (id, name, local_names, country, primary_crop_id, meal_type, plant_based_as_cooked, animal_ingredient_to_swap, description)
VALUES
('moi_moi', 'Moi Moi', 'Alele, Steamed Bean Pudding', 'Nigeria', 'cowpea', 'Pudding', 'Plant-Based as Cooked', 'Replace dried crayfish or boiled eggs with ground Iru/Dawadawa for 100% plant-based umami.', 'Steamed savory pudding made of de-hulled whipped cowpea paste, red peppers, onions, and oil.'),
('akara', 'Akara', 'Kosai, Koose, Bean Fritters', 'Nigeria', 'cowpea', 'Fritter', '100% Plant-Based', 'None (inherently 100% plant-based).', 'Crisp, golden-brown deep-fried fritters made of whipped cowpea paste.'),
('okpa', 'Okpa', 'Igbirigo, Bambara Pudding', 'Nigeria', 'bambara_groundnut', 'Pudding', '100% Plant-Based', 'None (inherently 100% plant-based).', 'Dense, elastic steamed pudding made with Bambara groundnut flour, red palm oil, and habanero peppers.'),
('awara', 'Awara', 'Beske, Nigerian Tofu', 'Nigeria', 'soybean', 'Curd', '100% Plant-Based', 'None (fry in clean vegetable oil).', 'Fresh coagulated plant curd sliced and deep-fried, sold with pepper sauce across Northern Nigeria.'),
('ewa_agoyin', 'Ewa Agoyin', 'Mashed Beans', 'Nigeria', 'cowpea', 'Stew', '100% Plant-Based', 'Ensure pepper sauce uses vegetable/palm oil without fish powder.', 'Slow-cooked mashed cowpeas served with spicy dark caramelized chili-onion oil.'),
('kuli_kuli', 'Kuli-Kuli', 'Groundnut Snack Cake', 'Nigeria', 'groundnut', 'Snack', '100% Plant-Based', 'None (inherently 100% plant-based).', 'Crunchy, defatted groundnut snack sticks seasoned with ginger, pepper, and salt.'),
('kunu_aya', 'Kunu Aya', 'Tigernut Plant Milk', 'Nigeria', 'cowpea', 'Drink', '100% Plant-Based', 'None (sweetened naturally with dates).', 'Chilled creamy plant milk extraction made with tigernuts, coconut, and dates.'),
('suya_plant', 'Plant-Based Suya', 'Soya Suya, Veggie Suya', 'Nigeria', 'african_yam_bean', 'Snack', '100% Plant-Based', 'None (uses groundnut press-cake and Yaji spice blend).', 'Chewy, fibrous plant protein strips grilled with spicy northern Yaji suya pepper.'),
('egusi_soup', 'Egusi Soup', 'Melon Seed Stew', 'Nigeria', 'african_yam_bean', 'Stew', 'Plant-Based as Cooked', 'Replace stockfish and crayfish with fermented Iru and mushroom broth.', 'Rich soup made of ground melon seeds thickened into delicate curds with leafy greens.'),
('red_red', 'Red Red', 'Ghanaian Bean Stew', 'Ghana', 'cowpea', 'Stew', 'Plant-Based as Cooked', 'Omit dried smoked fish; simmer beans in red palm oil and tomato sauce.', 'Sweet, savory black-eyed pea stew served with fried ripe plantains (Kelewele).'),
('waakye', 'Waakye', 'Rice & Beans', 'Ghana', 'cowpea', 'Swallow', '100% Plant-Based', 'Serve with plant-based tomato stew and shito.', 'Classic Ghanaian rice and cowpeas cooked with red sorghum leaf sheaths for deep burgundy color.'),
('mbaazi_za_nazi', 'Mbaazi za Nazi', 'Pigeon Peas in Coconut Milk', 'Kenya', 'pigeon_pea', 'Stew', '100% Plant-Based', 'None (inherently 100% plant-based).', 'Swahili coastal breakfast dish of tender pigeon peas simmered in thick coconut cream.'),
('githeri', 'Githeri', 'Muthokoi', 'Kenya', 'cowpea', 'Stew', '100% Plant-Based', 'None (boiled corn and beans seasoned with salt and onions).', 'Hearty one-pot boiled legume and maize staple eaten across rural Kenya.'),
('samp_and_beans', 'Umngqusho', 'Samp and Beans', 'South Africa', 'cowpea', 'Swallow', '100% Plant-Based', 'Use plant oil instead of beef tallow or butter.', 'Iconic Xhosa comfort dish of cracked white maize and sugar beans simmered to creamy perfection.'),
('chakalaka', 'Chakalaka', 'Spicy Bean Relish', 'South Africa', 'cowpea', 'Stew', '100% Plant-Based', 'None (inherently 100% plant-based).', 'Spicy South African relish of baked beans, carrots, peppers, and curry powder.'),
('fortified_amala', 'Protein-Fortified Amala', 'Clinical Swallow', 'Nigeria', 'cowpea', 'Swallow', '100% Plant-Based', 'None.', 'Traditional yam flour swallow fortified with 15% soluble legume hydrolysate for sarcopenia.')
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    plant_based_as_cooked = EXCLUDED.plant_based_as_cooked,
    animal_ingredient_to_swap = EXCLUDED.animal_ingredient_to_swap;

-- ------------------------------------------------------------------------------
-- 16. SEED DATA: Path B Lab Formulation Roadmaps
-- ------------------------------------------------------------------------------
INSERT INTO public.lab_protocols (id, job, title, target_metric_to_beat, benchmark_citation, extraction_ph, thermal_profile, ionic_coagulant, step_by_step_protocol)
VALUES
(
    'proto_egg',
    'egg',
    'Heat-Set Scrambled Egg Protocol',
    'Rupture force ~0.8 N, Springiness >85%',
    'Brishti et al., 2017',
    'pH 9.5 alkaline solubilization, neutralize to pH 7.2',
    '85C for 8-10 minutes',
    '0.1% Dipotassium phosphate buffer',
    '["Extract isolate at pH 9.5 to unfold native globulin.", "Neutralize to pH 7.2; calibrate to 11% w/v dispersion.", "Emulsify with 3% vegetable oil and 0.2% lecithin.", "Pan-fry at 85C for 4 minutes to achieve scramblable curd texture."]'::jsonb
),
(
    'proto_gel',
    'gel',
    'Coagulated Tofu / Awara Curd Protocol',
    'Breaking stress 1.2 - 1.5 N',
    'Foods 2025; Breeding Science 2000',
    'pH 8.5 - 9.0 alkaline extraction',
    '85C for 15 minutes',
    '0.3% w/v food-grade CaCl2 or 0.25% CaSO4',
    '["Disperse defatted meal in water (1:10 w/v) at pH 8.5.", "Heat liquor to 85C for 15 min to unfold 11S legumin hexamers.", "Add 0.3% CaCl2 at 80C while stirring gently.", "Transfer curd to mold and press at 15 kPa for 20 minutes."]'::jsonb
),
(
    'proto_milk',
    'milk',
    'Colloidal Plant Milk Protocol',
    'Colloidal stability >90% at 7 days, pH 7 solubility >80%',
    'Tang et al., 2023; Pretoria 2024',
    'pH 6.8 - 7.2 neutral buffering',
    '90C for 3 minutes (Blanching)',
    '0.1% Dipotassium phosphate (K2HPO4)',
    '["Blanch de-hulled seeds in water at 90C for 3 min to kill lipoxygenase.", "Wet-mill at 1:8 seed-to-water ratio.", "Homogenize in two stages (50 MPa / 10 MPa).", "Buffer at pH 7.0 for 7-day refrigeration stability."]'::jsonb
)
ON CONFLICT (id) DO UPDATE SET 
    title = EXCLUDED.title,
    step_by_step_protocol = EXCLUDED.step_by_step_protocol;

-- ------------------------------------------------------------------------------
-- 17. ROW LEVEL SECURITY (RLS) POLICIES FOR SUPABASE
-- ------------------------------------------------------------------------------
ALTER TABLE public.crops ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.proteins ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.features ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.model_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rankings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.measurements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lab_protocols ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.advisory_inquiries ENABLE ROW LEVEL SECURITY;

-- Public Read-Only Access for Edna's React Frontend (using anon key)
CREATE POLICY "Public Read on crops" ON public.crops FOR SELECT USING (true);
CREATE POLICY "Public Read on jobs" ON public.jobs FOR SELECT USING (true);
CREATE POLICY "Public Read on meals" ON public.meals FOR SELECT USING (true);
CREATE POLICY "Public Read on proteins" ON public.proteins FOR SELECT USING (true);
CREATE POLICY "Public Read on features" ON public.features FOR SELECT USING (true);
CREATE POLICY "Public Read on embeddings" ON public.embeddings FOR SELECT USING (true);
CREATE POLICY "Public Read on model_runs" ON public.model_runs FOR SELECT USING (true);
CREATE POLICY "Public Read on rankings" ON public.rankings FOR SELECT USING (true);
CREATE POLICY "Public Read on measurements" ON public.measurements FOR SELECT USING (true);
CREATE POLICY "Public Read on lab_protocols" ON public.lab_protocols FOR SELECT USING (true);
CREATE POLICY "Public Read on advisory_inquiries" ON public.advisory_inquiries FOR SELECT USING (true);

-- Allow public anonymous insert for frontend user inquiries
CREATE POLICY "Public Insert on advisory_inquiries" ON public.advisory_inquiries FOR INSERT WITH CHECK (true);
