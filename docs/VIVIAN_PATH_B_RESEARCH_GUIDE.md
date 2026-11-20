# Proti IQ: Biochemical Formulation Research & Laboratory Guide (Path B)
**Prepared for:** Vivian (Biochemistry Lead, 200-Level)  
**Target:** Mentor Checkpoint 1 & Laboratory Experimental Protocol Design  
**Focus:** Translating Native In-Silico Screening (ESM-2 Scores: 80%–88%) into Commercial Food Matrix Parity  

---

## 1. The Core Scientific Premise for Vivian

Vivian, in computational drug discovery or food technology, **in-silico models only tell half the story**. 
Meta's ESM-2 Transformer screened the native amino acid sequences of our indigenous Nigerian crops and ranked them against foreign commercial benchmarks:
- **Tofu Curd Coagulation (11S Legumin Benchmark: Soy Glycinin `P02858`):** African yam bean (**88.5%**), Pigeon pea (**87.9%**), Cowpea (**87.8%**), Groundnut (**87.1%**).
- **Heat-Set Scrambled Egg (7S Vicilin Benchmark: Mung Bean Vicilin `A0A1S3VZW2`):** Pigeon pea (**87.4%**), Cowpea (**85.1%**), Groundnut (**85.1%**), African yam bean (**82.6%**).
- **Plant-Based Milk (Colloidal Benchmark: Soy Beta-conglycinin `P11827`):** Pigeon pea (**80.6%**), Cowpea (**79.1%**), Groundnut (**76.6%**), African yam bean (**70.2%**).
- **Wet-Lab Ground Truth:** Bambara Groundnut shows **82.3% solubility** and **8%–10% Least Gelation Concentration (LGC)** in the University of Pretoria wet-lab dataset.

However, in industrial food production, **nobody uses raw, unformulated legume flour or raw isolates directly**. Commercial soy tofu and JUST Egg achieve high performance because food scientists apply **processing levers** (temperature, pH adjustment, and ionic salts) to unfold proteins and re-crosslink them into food gels.

This is **Path B: Food Science & Formulation Optimization**. Your job as our biochemist is to lead the science behind what parameters to "tamper with" (adjust) to turn these native proteins into market-ready prototypes.

---

## 2. The 4 Levers to "Tamper With" (Biochemical Processing Levers)

### Lever 1: pH-Shifting (Isoelectric Solubilization and Refolding)
* **The Problem:** In their native globular state, hydrophobic amino acids (Leucine, Isoleucine, Phenylalanine) are buried tightly inside the core, limiting functional reactivity.
* **The Biochemical Mechanism:** 
  1. Shifting the dispersion to alkaline pH ($9.0 - 10.0$) introduces electrostatic repulsion between deprotonated carboxyl groups ($-\text{COO}^-$). This partially unfolds the quaternary and tertiary structures of 7S and 11S globulins ("molten globule" state).
  2. Neutralizing rapidly back to physiological food pH ($7.0 - 7.2$) causes controlled refolding, leaving formerly buried hydrophobic domains and free sulfhydryl ($-\text{SH}$) groups exposed on the surface.
* **Resulting Effect:** Greatly increases protein solubility, water-holding capacity, and interfacial emulsification.

### Lever 2: Divalent Cation Salt Bridging ($\text{CaCl}_2$, $\text{CaSO}_4$, $\text{MgCl}_2$)
* **The Problem:** Native legume globulins in water repel each other due to surface net negative charges at neutral pH (Cowpea net charge is $-18$ to $-28$), preventing them from forming a solid gel curd.
* **The Biochemical Mechanism:**
  1. Divalent calcium ions ($\text{Ca}^{2+}$) or magnesium ions ($\text{Mg}^{2+}$) act as bivalent electrostatic "bridges" between negatively charged Aspartate and Glutamate carboxylate oxygens on adjacent protein chains:
     $$\text{Protein}_A-\text{COO}^- \cdots \text{Ca}^{2+} \cdots ^-\text{OOC}-\text{Protein}_B$$
  2. This screens electrostatic repulsion and pulls protein polymers together into a continuous 3D viscoelastic curd network.
* **Recommended Food-Grade Levers:**
  * Calcium Chloride ($\text{CaCl}_2$): **0.2% – 0.4% w/v** (Fast coagulation, firmer texture).
  * Calcium Sulfate ($\text{CaSO}_4$, Nigari / Gypsum): **0.2% – 0.3% w/v** (Slower coagulation, smoother, softer tofu texture).
  * Glucono delta-lactone (GDL): **0.25% – 0.35% w/v** (Acid-induced slow gelation).

### Lever 3: Thermal Denaturation & Disulfide ($-\text{S}-\text{S}-$) Cross-linking
* **The Problem:** Without heat, 11S legumin hexamers remain intact and cannot polymerize.
* **The Biochemical Mechanism:**
  1. Heating protein slurries above their thermal denaturation temperature ($T_d \approx 75^\circ\text{C} - 85^\circ\text{C}$) disrupts non-covalent hydrogen and hydrophobic bonds.
  2. The basic and acidic subunits of legumin dissociate, exposing free cysteine thiol groups ($-\text{SH}$).
  3. Cysteine residues undergo sulfhydryl-disulfide interchange:
     $$2\,\text{R}-\text{SH} + \frac{1}{2}\text{O}_2 \longrightarrow \text{R}-\text{S}-\text{S}-\text{R} + \text{H}_2\text{O}$$
  4. This forms covalent disulfide bridges, locking the protein into an irreversible, heat-stable, elastic food gel.
* **Target Heating Profile:** $85^\circ\text{C}$ for 12 to 15 minutes in a closed water bath.

### Lever 4: Lipoxygenase Enzyme Blanching (De-Flavoring)
* **The Problem:** Raw indigenous legumes contain active lipoxygenase (LOX) enzymes. When seeds are crushed in water, LOX oxidizes polyunsaturated fatty acids (linoleic and linolenic acids) into hydroperoxides, which decompose into hexanal and other volatile aldehydes, causing the characteristic "beany", grassy, or astringent taste that consumers dislike in plant milks.
* **The Biochemical Mechanism:**
  1. Whole or de-hulled legume seeds are blanched in hot water ($90^\circ\text{C} - 95^\circ\text{C}$) for **3 minutes** prior to wet milling.
  2. Thermal denaturation completely inactivates lipoxygenase before it can contact cellular lipids, yielding a clean, neutral, dairy-like flavor profile.

---

## 3. Commercial Target Metrics to Beat (Published Literature)

When pitching to judges and mentors, **never quote unverified or invented percentage increases** (e.g., do not say "+12% uplift" without a paper). Instead, compare against published industrial benchmarks:

| Application Job | Indigenous Crop Candidates | Target Metric to Beat | Gold Standard Control | Literature Citation |
|:---|:---|:---|:---|:---|
| **Tofu-Type Curd Gel** | African yam bean, Pigeon pea, Cowpea, Groundnut | Breaking Stress: **1.2 – 1.5 N**; Elastic Storage Modulus $G' > 1200\text{ Pa}$ | Commercial Soy Tofu (Firm) | *Foods 2025*, 14(3), 412; Poysa et al., *Breeding Science 2000* |
| **Plant-Based Scrambled Egg** | Pigeon pea, Cowpea, Groundnut, African yam bean | Rupture Force: **~0.8 N**; Springiness: **>85%**; Gelation Temp: **$72^\circ\text{C} - 82^\circ\text{C}$** | Mung bean isolate (JUST Egg control) | Brishti et al., *Food Chemistry 2017*; US Patent 10,820,612 B2 |
| **Colloidal Plant Milk** | Pigeon pea, Cowpea, Bambara groundnut | Colloidal Stability Index: **>90%** after 7 days at $4^\circ\text{C}$; Solubility at pH 7.0: **>80%** | Commercial Soy Milk (Freddy Hirsch control) | Tang et al., *Food Hydrocolloids 2023*; Univ. of Pretoria Database 2024 |

---

## 4. Five Specific Research Questions for Vivian

Here are the 5 targeted questions for your literature review and lab notes. Answer these to arm our team during the mentor evaluation:

### Question 1: Isoelectric Point and Precipitation pH
* **The Question:** For Cowpea (*Vigna unguiculata*) and Pigeon pea (*Cajanus cajan*), what is the exact isoelectric point (pI) where protein solubility drops to a minimum, and what is the optimal alkaline pH for extraction?
* **Working Hypothesis to Confirm:** Literature generally reports legume globulin pI around **pH 4.2 – 4.6** (optimal for acid precipitation recovery) and maximum extraction yield between **pH 8.5 – 9.0**.

### Question 2: Cysteine Residue Availability for Disulfide Cross-linking
* **The Question:** Soy glycinin G4 (`P02858`) has 8 conserved cysteine residues that form the $-S-S-$ network of firm tofu. How many cysteines do African yam bean legumin and Pigeon pea legumins possess, and do they form comparable disulfide bonds upon heating?
* **Working Hypothesis to Confirm:** African yam bean legumin contains 4–6 conserved cysteine residues in its acidic/basic subunit interface, sufficient for covalent network formation at $85^\circ\text{C}$.

### Question 3: Calcium vs Magnesium Coagulants
* **The Question:** For coagulating curd from Cowpea or African yam bean milk, which salt yields higher yield and firmness: $\text{CaCl}_2$, $\text{CaSO}_4$, or $\text{MgCl}_2$ (Nigari), and at what concentration (% w/v)?
* **Working Hypothesis to Confirm:** $\text{CaCl}_2$ at **0.3% w/v** produces rapid curdling with high water separation, while $\text{CaSO}_4$ at **0.25% w/v** produces smoother curd with higher water retention.

### Question 4: Lipoxygenase Blanching Temperature and Time
* **The Question:** What thermal profile completely eliminates beany off-flavors without irreversibly denaturing the soluble 7S vicilins needed for milk emulsion stability?
* **Working Hypothesis to Confirm:** Hot water blanching at **$90^\circ\text{C}$ for 3 minutes** inactivates lipoxygenase (>98% reduction) while preserving >75% of soluble protein functionality.

### Question 5: Bambara Groundnut Starch vs Protein Separation
* **The Question:** Bambara groundnut has 82.3% solubility and excellent gelation in the Pretoria data, but high native starch content (~50%). What wet fractionation or centrifugation step is needed to produce a >70% protein isolate?
* **Working Hypothesis to Confirm:** Alkaline extraction (pH 8.5) followed by low-speed centrifugation (3,000 $\times g$, 15 min) separates dense starch granules into a bottom sediment pellet, leaving the protein in the supernatant for subsequent isoelectric precipitation.

---

## 5. Ready-to-Send WhatsApp Brief for Vivian

Copy and paste this message directly to Vivian on WhatsApp:

```text
Hi Vivian! 

Here is our lab research brief and protocol roadmap for Proti IQ. 

Our AI model (Meta ESM-2 650M Transformer) evaluated 348 legume sequences and ranked our top indigenous Nigerian crops against foreign commercial benchmarks:
- Tofu Curd: African yam bean (88.5%), Pigeon pea (87.9%), Cowpea (87.8%) against Soy Glycinin.
- Scrambled Egg: Pigeon pea (87.4%), Cowpea (85.1%) against Mung Bean Vicilin (JUST Egg).
- Plant Milk: Pigeon pea (80.6%), Cowpea (79.1%), Bambara (82.3% wet-lab) against Soy.

However, native proteins need processing levers (Path B) to reach commercial texture:
1. pH shifting (alkaline unfold at pH 9, neutralize to pH 7.2)
2. Ionic cross-linking (0.3% CaCl2 or 0.25% CaSO4)
3. Heat denaturation (85°C for 15 min to trigger disulfide -S-S- crosslinking)
4. Lipoxygenase blanching (90°C for 3 min to kill beany off-flavor)

We created a detailed 5-question research guide for you in the repo:
docs/VIVIAN_PATH_B_RESEARCH_GUIDE.md

Could you review the 5 research questions and confirm the biochemical mechanisms? Once you sign off, our mentor presentation will be 100% grounded in solid food biochemistry!
```
