# Proti IQ — Limitations & Scope Boundaries

## 1. Computational Nature vs. Food Matrix Reality
- **Not a Taste, Sensory, or Rheology Guarantee:** Proti IQ predicts similarity and biochemical suitability, not final product texture, flavor, or palatability.
- **Processing and Extraction Effects:** In food chemistry, extraction conditions (pH-shifting, temperature, ionic strength, defatting, salt-washing) dramatically alter functional properties (e.g. Least Gelation Concentration of mung bean swings from 22% native to 15% after pH 12 treatment). A computational tool evaluates intrinsic protein properties, not industrial process variations.

## 2. In-Silico Structural Predictions
- AlphaFold structures downloaded from AlphaFold DB are high-quality computational predictions, not experimentally resolved X-ray crystallographic or cryo-EM models. Regions with low pLDDT (<70) indicate disordered loops or mobile domains.

## 3. Data Scarcity for Indigenous Crops
- While benchmark crops (soy, mung bean, pea) and major crops (cowpea, groundnut) have rich sequence and structural annotation, underutilised indigenous African legumes (such as Bambara groundnut and African yam bean) suffer from sparse entries in Swiss-Prot/UniProtKB.
- Where direct seed storage sequences are limited, Proti IQ applies transparent homology proxies and explicitly displays a **"Low Confidence"** badge.

## 4. Screening Flags vs Safety Clearances
- Allergen flags and anti-nutritional factor screenings (e.g., protease inhibitors, lectins) are retrieved directly from UniProt annotations and keywords.
- These flags are **preliminary screening indicators**, never toxicological clearances or clinical allergenicity guarantees.

## 5. Sample Size of Back-Test Answer Key
- Back-test benchmarks derive from a curated set of single-study comparative literature and the open University of Pretoria dataset ($n \approx 10\text{--}15$ protein lines).
- Rank comparisons demonstrate directional consistency and algorithmic sanity, but do not constitute high-power statistical proof on small cohorts. Pairwise agreement is reported rather than asserting unpowered Spearman $\rho$ values.

## 6. Intra-Crop Variety Variance Exceeds Inter-Crop Variance
- In the empirical Pretoria dataset, Cowpea variety *Dr Saunders* gels at 5.0% w/v, whereas Cowpea variety *Bechuana White* requires 10.0% w/v. This 5.0% variety gap spans the difference between species.
- Public sequence databases (UniProtKB) index species (*Vigna unguiculata*), not landraces. Sequence similarity models cannot distinguish cultivars without transcriptomic/genomic cultivar data. This variety spread represents the natural experimental noise floor.

## 7. Like-for-Like Extraction Parity
- Commercial soy isolate scores 88.1% solubility, whereas laboratory-extracted soy isolate scores 75.3% at pH 7. Under identical laboratory extraction, both Bambara isolates (79.2–82.3%) and Cowpea isolates (82.6%) outperform lab soy.
- Comparing raw indigenous extracts against commercial ultra-processed controls conflates industrial processing with intrinsic biology. Proti IQ explicitly benchmarks against laboratory-extracted controls.

## 8. The Bambara Groundnut Sequence Gap
- UniProtKB contains 0 reviewed or unreviewed 7S vicilin or 11S legumin storage globulins for *Vigna subterranea* (Taxon 115715).
- Sequence models cannot rank Bambara. Bambara is evaluated exclusively via Tier 1 empirical wet-lab measurements.
