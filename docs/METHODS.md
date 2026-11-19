# Proti IQ — Methodology & Scoring Pipeline

## 1. Scientific Framework
Proti IQ is an in-silico decision-support engine engineered to rank indigenous Nigerian and regional legume seed storage proteins by functional suitability against proven benchmark crops (*Vigna radiata* / mung bean, *Glycine max* / soy, *Pisum sativum* / pea) for three key food product applications:
1. **Plant-Based Egg Gel:** Thermal coagulation and heat-set network formation driven by 7S vicilin-like globulins.
2. **Tofu-Type Coagulated Gel:** Salt/calcium-induced firm curd network dominated by 11S legumin-like (glycinin) hexamers and intermolecular disulfide bridges.
3. **Plant-Based Milk Dispersion:** Neutral-pH colloidal solubility, low sedimentation, and emulsification stability.

---

## 2. Protein Feature Extraction (Biopython & Structural Metrics)
From each verified protein amino acid sequence, the offline pipeline extracts:
- **Molecular Weight ($M_w$) & Sequence Length ($L$)**
- **Theoretical Isoelectric Point ($pI$):** Calculated via standard pKa scales.
- **Net Charge at pH 7.0 & pH 5.0:** Crucial for electrostatic repulsion and colloidal stability.
- **GRAVY (Grand Average of Hydropathicity):** Kyte-Doolittle scale measure of overall hydrophobicity/hydrophilicity.
- **Aromaticity:** Relative frequency of Phe, Tyr, and Trp residues.
- **Instability Index:** Guruprasad method for in vitro protein stability estimation.
- **Secondary Structure Fractions:** Predicted fractions of Helix, Turn, and Sheet.
- **Cysteine Residue Content:**
  $$\text{Cysteine Fraction} = \frac{N_{\text{Cys}}}{L}$$
  Serves as the sequence-level proxy for capacity to form heat/chemical-induced covalent disulfide cross-links.
- **AlphaFold Structural Confidence ($p\text{LDDT}$):** Residue-wise and mean predicted Local Distance Difference Test score from AlphaFold DB.

---

## 3. Deep Protein Language Model Embeddings (ESM-2)
- We employ **ESM-2 8M (`facebook/esm2_t6_8M_UR50D`)** executed on CPU offline.
- Per-protein representation is extracted by mean-pooling the final hidden representations across residues.
- Longer sequences are processed with standard overlapping chunking.
- Stored as hash-verified safetensors/NumPy arrays, accompanied by SHA-256 digests in `model_artifacts/manifest.json`.

---

## 4. Homology & Family Classification
- **Family Assignment:** UniProt keywords and InterPro/Pfam annotations classify sequences into **7S (Vicilin-like)**, **11S (Legumin-like)**, or **Other Storage Globulin/Albumin**.
- **Pairwise Alignment:** Biopython `PairwiseAligner` with the **BLOSUM62** substitution matrix computes global/semi-global sequence identity (%) against target benchmark proteins strictly within matching protein families (7S vs 7S, 11S vs 11S).

---

## 5. Multi-Criteria Similarity Scoring
The suitability score $S \in [0, 100]$ is computed as:
$$S = 100 \times \left( w_{\text{emb}} \cdot \text{Sim}_{\text{cos}}(\mathbf{e}_c, \mathbf{e}_b) + w_{\text{fam}} \cdot \mathbb{I}_{\text{fam}} + w_{\text{bio}} \cdot (1 - D_{\text{phys}}) + w_{\text{id}} \cdot \text{Ident} + w_{\text{spec}} \cdot F_{\text{specific}} \right)$$

Where:
- $\text{Sim}_{\text{cos}}(\mathbf{e}_c, \mathbf{e}_b)$ is the cosine similarity between candidate embedding $\mathbf{e}_c$ and benchmark embedding $\mathbf{e}_b$.
- $\mathbb{I}_{\text{fam}}$ is 1.0 for exact family match (e.g. 7S to 7S for egg), 0.5 for related globulin, and 0.0 otherwise.
- $D_{\text{phys}}$ is the normalized Euclidean distance in standardized physicochemical space.
- $\text{Ident}$ is the normalized pairwise sequence identity.
- $F_{\text{specific}}$ is application-specific:
  - **Egg:** Vicilin structural alignment & thermal stability proxy.
  - **Gel:** Cysteine fraction & optional literature 11S/7S seed ratio input.
  - **Milk:** Solubility proxy ($|pI - 7.0|$ penalty and hydrophilic GRAVY bonus).

---

## 6. Validation Strategy & Empirical Reality Checks
1. **Empirical Pairwise Agreement (Single-Laboratory Controls):**  
   Because extraction methods alter functional measurements (e.g., LGC 12% vs 22%), Proti IQ validates relative candidate order within single experimental studies using **pairwise agreement** rather than calculating rank correlation on small cohorts ($n=3$ or $n=4$, where Spearman rho is statistically unpowered).
2. **Experimental Noise Floor (Intra-Crop Variety Spread):**  
   In single-lab empirical benchmarks (University of Pretoria, 2024), Cowpea variety *Dr Saunders* gels at 5.0% w/v, whereas Cowpea variety *Bechuana White* requires 10.0% w/v. This 5.0% variety gap spans the difference between crops. Sequence models evaluate species, not cultivars, so this variety spread serves as the documented experimental noise floor.
3. **External Cowpea Benchmark Check:**  
   *Vigna unguiculata* egg gel performance reported in food literature was compared against our top-tier candidate picks. Cowpea scores in the top tier alongside pigeon pea and groundnut (which are in a statistical tie, rather than an absolute sequence rank).
4. **Tofu Gel Sanity Check (Not an Autonomous Model Validation):**  
   The correlation ($\rho = 0.92$) observed on soybean curd gels reflects the direct relationship between measured seed 11S/7S ratios and gel firmness reported in Xia et al. (*Foods* 2025, 14, 4029). It serves as a feature sanity check on globulin ratio sensitivity, not an autonomous sequence prediction.
5. **Solubility & Extraction Parity (Tang 2023 & Pretoria 2024):**  
   Solubility is benchmarked against Tang et al. (*Foods* 2023, 12, 368) across pH 3.0 to 9.0 and the Pretoria dataset across pH 3.0, 4.0, 7.0, and 8.0. Under lab-extracted parity, Cowpea (82.6%) and Bambara (80.8%) outperform lab-extracted soy (75.3%), whereas commercial soy (88.1%) reflects industrial jet-cooking and lecithination rather than intrinsic seed biology.
