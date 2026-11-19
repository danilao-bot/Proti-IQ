# Proti IQ — Known Gaps & Graceful Degradation Register

This living document logs gaps in external databases, missing accessions, or hardware constraints encountered during pipeline execution, along with the implemented fallback strategy.

| ID | Crop / Target | Issue Description | Impact | Graceful Degradation / Fallback Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **GAP-01** | Bambara Groundnut (*V. subterranea*) | Sparse reviewed Swiss-Prot entries for seed storage 7S/11S; most entries are unreviewed TrEMBL or partial chloroplast/photosystem entries. | Lower confidence in exact vicilin sequence accuracy. | Query TrEMBL + NCBI taxonomy cross-references; fallback to nearest *Vigna* homologous vicilin; display visible **"Low Confidence - Sparse Data"** badge in UI. |
| **GAP-02** | African Yam Bean (*S. stenocarpa*) | Under-annotated orphan legume; limited AlphaFold models directly indexed in AlphaFold DB. | Structure preview may be unavailable for specific accessions. | Show sequence/physicochemical analysis; mark 3D structure viewer as "Structure model not indexed in AlphaFold DB"; do not fail pipeline. |
| **GAP-03** | 11S/7S Ratio Availability | Seed-level protein ratio is missing in literature for certain candidate crops (e.g., wild landraces). | Cannot directly inject measured ratio into gel model. | Model treats ratio field as `null`, falls back strictly to sequence proxies (cysteine % and legumin family share), and notifies user in the contributions breakdown. |
| **GAP-04** | Milk Application Benchmark | Pulse milk literature is fragmented; commercial pea isolates suffer from low solubility, whereas soy is highly soluble. | Milk job has higher empirical variance. | Hardcoded confidence penalty (0.85 multiplier) applied to milk job; flagged visibly as lowest-confidence application. |
