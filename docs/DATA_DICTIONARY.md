# Data Dictionary: University of Pretoria Pulse Protein Ingredient Dataset

**Dataset Title:** Quantitative analysis of pulse (Bambara groundnut, cowpea, and soybeans) protein ingredients
**Source Institution:** University of Pretoria Department of Consumer and Food Sciences
**Repository Identifier:** researchdata.up.ac.za / DOI: 10.25403/UPresearchdata.27677994
**Crops Investigated:** Bambara groundnut (*Vigna subterranea*), Cowpea (*Vigna unguiculata*), Soybean (*Glycine max*)
**Ingredient Processing Forms:** Defatted Flour, Protein Concentrate (wet milled), Protein Isolate (isoelectric precipitate, commercial control)

---

## Summary of Workbook Inventory

| File Name | Primary Functional Domain | Analyzed Sheets | Measured Properties |
| :--- | :--- | :--- | :--- |
| `FINALsds band intensities.xlsx` | Subunit Composition (11S/7S) | Non-reducing, Reducing | SDS-PAGE band intensities (%), MW (kDa) |
| `FUNCTIONAL PROPERTIES DATABASE.xlsx` | Food Functionality | Protein Solubility, WAC, OAC, WSI, Foam C n S, Emulsion A n S, Gelling | LGC (%), Solubility (%), WAC (g/g), OAC (g/g), FC (%), FS (%), EC (%), ES (%) |
| `PROTEIN SOLUBILITY.xlsx` | Protein Solubility Curves | Rep 1, Rep 2, PS, Average N%, Solubility (2) | Solubility (%) across pH 3, 4, 7, 8 |
| `PROXIMATE COMPOSITION DATABASE.xlsx` | Proximate & Electrokinetics | Moisture, Ash, pH of extracts, Total Starch, Zeta Potential, Salt | Moisture %, Ash %, Starch %, Zeta Potential (mV), Salt (mg/g) |
| `PHENOLIC CONTENT AND AMINO ACID DATABASE .xlsx` | Bioactives & Amino Acids | Total phenolics, Flavonoids, Tannin, TAA - SAGL | Amino acid profiles (g/100g protein), phenolics (mg GAE/g) |
| `Protein content - extracts.xlsx` | Protein Purity | Sheet1 | Dumas nitrogen protein content (%) |
| `SECONDARY STRUCTURES.xlsx` | Protein Conformation | SOYA, SOYB, RBGN, CBGN, DRS, BW | FTIR deconvolution: alpha-helix, beta-sheet, beta-turns (%) |
| `VISCOSITY DATABASE.xlsx` | Rheological Flow Behavior | Viscosity-Solid, Viscosity-Salt, Viscosity-pH | Apparent viscosity (Pa.s), shear stress vs shear rate |

---

## Detailed File and Sheet Specifications

### File: `FINALsds band intensities.xlsx`
#### Sheet: `Non-reducing`
- **Dimensions:** 63 rows x 33 columns (Approx. 23 data rows)
- **Target Crops Identified:** Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Lab Extracted (Local), Red
- **Sample Headers / Columns:** `SDS-PAGE; labelling can be found in old dissertation book - date 08/03/2022; Report on the most intense bands; The bolded ones are the ones that are intensified on the gel, according to my eyes`

#### Sheet: `Reducing `
- **Dimensions:** 55 rows x 33 columns (Approx. 21 data rows)
- **Target Crops Identified:** Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Lab Extracted (Local)
- **Sample Headers / Columns:** `SDS-PAGE; labelling can be found in old dissertation book - date 08/03/2022; isolates; concentrate; soy; soy le; soy wm; Cream bambara groundnut`

---
### File: `FUNCTIONAL PROPERTIES DATABASE.xlsx`
#### Sheet: `Protein Solubility `
- **Dimensions:** 52 rows x 27 columns (Approx. 44 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Soybean
- **Ingredient Forms Identified:** concentrate, defatted flour, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `Isolates; pH Range; PH 3; PH 4; PH 7; 3; 4; 8`

#### Sheet: `WAC`
- **Dimensions:** 87 rows x 18 columns (Approx. 75 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Lab Extracted (Local), Red, Unspecified Variety, Wet Milled
- **Sample Headers / Columns:** `Water Absorption capacity; Legume; Treatement; weight of tube (g); weight of dry food (g); weight of tube and dry sample; weight of tube + sediment (g); WAC`

#### Sheet: `OAC`
- **Dimensions:** 87 rows x 17 columns (Approx. 74 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Lab Extracted (Local), Red, Unspecified Variety, Wet Milled
- **Sample Headers / Columns:** `Oil Absorption capacity; OAC , (g oil /g dry protein concentrate or isolate) = ((weight of tube + sediment) - (Weight of tube + dry sample)) / (weight of protein); dry weight basis (d.w.b); dwb--WAC/ (100-MC) *100; Legume; Treatement; weight of tube (g); weight of dry food (g)`

#### Sheet: `WSI`
- **Dimensions:** 78 rows x 16 columns (Approx. 65 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** concentrate, defatted flour, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Red, Unspecified Variety, Wet Milled
- **Sample Headers / Columns:** `Sample; replicates; weight of empty aluminium pan (g); Weight of supernatant (g); mass of sample; Weight of aluminium pan and dried supernatant (g); WSI (%); MC`

#### Sheet: `Foam C n S`
- **Dimensions:** 151 rows x 38 columns (Approx. 150 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `FOAM CAPACITY; SAMPLES; V 0; V1; FC; MEAN; STD; V t`

#### Sheet: `Emulsion A n S`
- **Dimensions:** 151 rows x 29 columns (Approx. 151 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `Emulion Capacity = Emulsion Stability; Emulsion Capacity = Emulsion stability; V initial; V 1; V 2; EC and ES; MEAN; STD`

#### Sheet: `Gelling`
- **Dimensions:** 36 rows x 20 columns (Approx. 28 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `Samples; concentration  (%); Key; weak gel (- or *); isolates; 2.5; 3; 5`

---
### File: `PHENOLIC CONTENT AND AMINO ACID DATABASE .xlsx`
#### Sheet: `Total phenolic content`
- **Dimensions:** 70 rows x 29 columns (Approx. 41 data rows)
- **Target Crops Identified:** Bambara groundnut, Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Cream, Lab Extracted (Local), Red
- **Sample Headers / Columns:** `User: ADMIN; Path: C:\Program Files (x86)\BMG\Omega\Admin\Data\; Test ID: 53`

#### Sheet: `Flavonoid content`
- **Dimensions:** 84 rows x 32 columns (Approx. 56 data rows)
- **Target Crops Identified:** Bambara groundnut, Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Cream, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `User: ADMIN; Path: C:\Program Files (x86)\BMG\Omega\Admin\Data\; Test ID: 46`

#### Sheet: `Tannin content`
- **Dimensions:** 32 rows x 38 columns (Approx. 11 data rows)
- **Target Crops Identified:** Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Freddy Hirsch Commercial Control, Lab Extracted (Local)
- **Sample Headers / Columns:** `Colour blank; Catechin Blank; Catechin std; SFH (Blank); SFH (sample); SE (blank); SE (sample); SC (blank)`

#### Sheet: `TAA - SAGL`
- **Dimensions:** 52 rows x 30 columns (Approx. 41 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `Sample; number (codes); Replications; Amino acid profile (g/100g) (dry basis - db); Histidine; Serine; Arginine; Glycine`

---
### File: `PROTEIN SOLUBILITY.xlsx`
#### Sheet: `Rep 1`
- **Dimensions:** 131 rows x 23 columns (Approx. 52 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `Isolates; Sample; pH (obtained); Mass sample (mg); Volume (ul) supernatant used; % N mass in 100 ul supernatant (mg); Mass of Absorbant (mg); volume of supernatant post centrifuge (ul)`

#### Sheet: `Rep 2`
- **Dimensions:** 74 rows x 24 columns (Approx. 52 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety, Wet Milled
- **Sample Headers / Columns:** `ISOLATES; Sample; pH (obtained); Mass sample (mg); Volume (ul) supernatant used; % N mass in 100 ul supernatant (mg); Mass of Absorbant (mg); volume of supernatant post centrifuge (ul)`

#### Sheet: `PS`
- **Dimensions:** 21 rows x 10 columns (Approx. 15 data rows)
- **Target Crops Identified:** Bambara groundnut
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Red
- **Sample Headers / Columns:** `% N absorbant; % N (mg); 1; 0.0537; 51.52; 51.235; 2; 0.0673`

#### Sheet: `Average N% content `
- **Dimensions:** 67 rows x 5 columns (Approx. 49 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `Isolates; =AVERAGE('C:\Users\SKand\Documents\Career POSTGRADUATE\MSC  2020 - 2021\2021\NEW RESULTS\[Protein content - extracts.xlsx]Sheet1'!$AA$14:$AB$16); Sample; pH (obtained); Average N % in sample; soy Fh; 3.18; 13.372097621266475`

#### Sheet: `Protein Solubility  (2)`
- **Dimensions:** 48 rows x 28 columns (Approx. 35 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `Isolates; pH Range; PH 3; PH 4; 3; 4; 7; 8`

#### Sheet: `Protein Solubility `
- **Dimensions:** 52 rows x 27 columns (Approx. 44 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Soybean
- **Ingredient Forms Identified:** concentrate, defatted flour, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `Isolates; pH Range; PH 3; PH 4; PH 7; 3; 4; 8`

#### Sheet: `Residual Solubility `
- **Dimensions:** 116 rows x 26 columns (Approx. 113 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Red, Unspecified Variety
- **Sample Headers / Columns:** `Extract; Mass plastic pan (g); Mass upernatant (g); Mass pan + dried supernatant (g); Total solid of supernatant (g); mass supernatant (mg); weight of absorbant (mg); Solid of sampled supernatant (mg)`

---
### File: `PROXIMATE COMPOSITION DATABASE.xlsx`
#### Sheet: `Moisture`
- **Dimensions:** 144 rows x 15 columns (Approx. 79 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** concentrate, defatted flour, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Lab Extracted (Local), Red, Unspecified Variety, Wet Milled
- **Sample Headers / Columns:** `Legume; Extracts; weight of tin (g) A; weight of dry food (g) B; weight of food + tin (g) C; % Moisture; MEAN; STD`

#### Sheet: `Ash`
- **Dimensions:** 135 rows x 17 columns (Approx. 53 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Cream, Dr Saunders, Lab Extracted (Local), Red, Unspecified Variety, Wet Milled
- **Sample Headers / Columns:** `Legume; Treatement; weight of crucible (g); weight of dry food (g); weight of ash + crucible (g); % Ash; mean; std`

#### Sheet: `pH of all extracts`
- **Dimensions:** 37 rows x 8 columns (Approx. 37 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** concentrate, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `Extract description; Replicate #; Mass (g); Total mass; pH (of extract); average pH; STD; Letters`

#### Sheet: `Total Starch Content  `
- **Dimensions:** 53 rows x 16 columns (Approx. 34 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Bechuana White, Cream, Lab Extracted (Local), Red, Unspecified Variety
- **Sample Headers / Columns:** `EXPERIMENT NO.; TOTAL STARCH ASSAY; Date; 2. Starch % determination using the megazyme total starch assay, Abs reading at 510nm`

#### Sheet: `Zeta Potential for all isolates`
- **Dimensions:** 19 rows x 191 columns (Approx. 19 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Red, Unspecified Variety
- **Sample Headers / Columns:** `Measurement Date and Time; Sample Name; Zeta Potential (mV); Conductivity (mS/cm); Intensities[1]; Intensities[2]; Intensities[3]; Intensities[4]`

#### Sheet: `Salt content`
- **Dimensions:** 26 rows x 12 columns (Approx. 25 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Unspecified Variety
- **Sample Headers / Columns:** `Sample; mass(g); V0; V1; Mass(mg); V(ml); mg salt/g sample; Average`

---
### File: `Protein content - extracts.xlsx`
#### Sheet: `Sheet1`
- **Dimensions:** 100 rows x 45 columns (Approx. 88 data rows)
- **Target Crops Identified:** Bambara groundnut, Cowpea, Maize (Control), Soybean
- **Ingredient Forms Identified:** concentrate, defatted flour, isolate
- **Varieties / Landraces:** Bechuana White, Cream, Dr Saunders, Freddy Hirsch Commercial Control, Lab Extracted (Local), Red, Unspecified Variety, Wet Milled
- **Sample Headers / Columns:** `Dumatherm  Nitrogen / Protein  Analyser`

---
### File: `SECONDARY STRUCTURES.xlsx`
#### Sheet: `SOYA`
- **Dimensions:** 39 rows x 17 columns (Approx. 38 data rows)
- **Target Crops Identified:** General / Calibration standards
- **Ingredient Forms Identified:** Unspecified
- **Varieties / Landraces:** Unspecified
- **Sample Headers / Columns:** `1; 2; 3; Peaks; Areas; Peaks; Areas; Peaks`

#### Sheet: `SOYB`
- **Dimensions:** 47 rows x 16 columns (Approx. 45 data rows)
- **Target Crops Identified:** General / Calibration standards
- **Ingredient Forms Identified:** Unspecified
- **Varieties / Landraces:** Unspecified
- **Sample Headers / Columns:** `1; 2; 3; Peaks; Areas; Peaks; Areas; Peaks`

#### Sheet: `RBGN`
- **Dimensions:** 31 rows x 16 columns (Approx. 28 data rows)
- **Target Crops Identified:** General / Calibration standards
- **Ingredient Forms Identified:** Unspecified
- **Varieties / Landraces:** Unspecified
- **Sample Headers / Columns:** `1; 2; 3; alpha helix; Beta sheets; beta turns; unordered/ random coils; Peaks`

#### Sheet: `CBGN`
- **Dimensions:** 38 rows x 15 columns (Approx. 31 data rows)
- **Target Crops Identified:** General / Calibration standards
- **Ingredient Forms Identified:** Unspecified
- **Varieties / Landraces:** Unspecified
- **Sample Headers / Columns:** `1; 2; 3; Peaks; Areas; Peaks; Areas; Peaks`

#### Sheet: `DRS`
- **Dimensions:** 40 rows x 16 columns (Approx. 35 data rows)
- **Target Crops Identified:** General / Calibration standards
- **Ingredient Forms Identified:** Unspecified
- **Varieties / Landraces:** Unspecified
- **Sample Headers / Columns:** `1; 2; 3; Peaks; Areas; Peaks; Areas; Peaks`

#### Sheet: `BW`
- **Dimensions:** 41 rows x 15 columns (Approx. 40 data rows)
- **Target Crops Identified:** General / Calibration standards
- **Ingredient Forms Identified:** Unspecified
- **Varieties / Landraces:** Unspecified
- **Sample Headers / Columns:** `1; 2; 3; Peaks; Areas; Peaks; Areas; Peaks`

---
### File: `VISCOSITY DATABASE.xlsx`
#### Sheet: `Viscosity-Solid Concentration`
- **Dimensions:** 79 rows x 132 columns (Approx. 76 data rows)
- **Target Crops Identified:** Bambara groundnut, Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Cream, Lab Extracted (Local)
- **Sample Headers / Columns:** `Data Series Information; Data Series Information; Data Series Information; Data Series Information; Name:; CB-2%; Name:; CB-6%`

#### Sheet: `Viscosity-Salt Concentration`
- **Dimensions:** 79 rows x 134 columns (Approx. 76 data rows)
- **Target Crops Identified:** Bambara groundnut, Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Cream, Lab Extracted (Local)
- **Sample Headers / Columns:** `Data Series Information; Data Series Information; Data Series Information; Data Series Information; Name:; CB-10%-0; Name:; CB-10%-50`

#### Sheet: `Viscosity-pH`
- **Dimensions:** 81 rows x 113 columns (Approx. 76 data rows)
- **Target Crops Identified:** Soybean
- **Ingredient Forms Identified:** isolate
- **Varieties / Landraces:** Lab Extracted (Local)
- **Sample Headers / Columns:** `Data Series Information; Data Series Information; Data Series Information; Data Series Information; Name:; SI-10%-pH4; Name:; SI-10%-pH5.5`

---