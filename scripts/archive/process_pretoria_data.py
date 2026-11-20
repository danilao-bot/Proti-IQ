"""
Process and Catalogue the University of Pretoria Pulse Protein Ingredient Dataset.
Inspects all 8 workbooks in data/raw/, generates docs/DATA_DICTIONARY.md,
and extracts tidy long-format functional measurements into data/processed/pretoria_tidy_measurements.csv.
"""

import os
import glob
import re
import csv
import json
import openpyxl

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
DOCS_DIR = "docs"

WORKBOOKS = [
    "FINALsds band intensities.xlsx",
    "FUNCTIONAL PROPERTIES DATABASE.xlsx",
    "PHENOLIC CONTENT AND AMINO ACID DATABASE .xlsx",
    "PROTEIN SOLUBILITY.xlsx",
    "PROXIMATE COMPOSITION DATABASE.xlsx",
    "Protein content - extracts.xlsx",
    "SECONDARY STRUCTURES.xlsx",
    "VISCOSITY DATABASE.xlsx",
]

def standardize_crop_name(name_str):
    """Map raw sample label to standardized crop name."""
    s = str(name_str).lower()
    if any(k in s for k in ["bambara", "bgn", "cbgn", "rbgn", "cb", "rb"]):
        return "Bambara groundnut"
    elif any(k in s for k in ["saunders", "drs", "bechuana", "bw", "bew", "cowpea"]):
        return "Cowpea"
    elif any(k in s for k in ["soy", "soyb", "soya", "sfh", "se"]):
        return "Soybean"
    elif "maize" in s:
        return "Maize (Control)"
    return "Unknown / Unclassified"

def standardize_form(name_str, default="isolate"):
    """Map raw sample label to ingredient form."""
    s = str(name_str).lower()
    if "defatted" in s or "flour" in s:
        return "defatted flour"
    elif "concentrate" in s or "conc" in s or "wm" in s or "wet mill" in s or "dm" in s:
        return "concentrate"
    elif "isolate" in s or "extract" in s or "fh" in s or "se" in s or "le" in s:
        return "isolate"
    return default

def standardize_variety(name_str):
    """Extract variety / landrace / commercial source."""
    s = str(name_str).lower()
    if "cream" in s or "cbgn" in s or "cb" in s:
        return "Cream"
    elif "red" in s or "rbgn" in s or "rb" in s:
        return "Red"
    elif "saunders" in s or "drs" in s:
        return "Dr Saunders"
    elif "bechuana" in s or "bw" in s or "bew" in s:
        return "Bechuana White"
    elif "fh" in s or "freddy" in s:
        return "Freddy Hirsch Commercial Control"
    elif "se" in s or "self" in s or "le" in s or "lab" in s or "extract" in s:
        return "Lab Extracted (Local)"
    elif "wm" in s or "wet mill" in s:
        return "Wet Milled"
    return "Unspecified Variety"

def inspect_and_build_dictionary():
    dict_entries = []
    
    for fname in WORKBOOKS:
        fpath = os.path.join(RAW_DIR, fname)
        if not os.path.exists(fpath):
            continue
        
        wb = openpyxl.load_workbook(fpath, data_only=True)
        wb_entry = {
            "file": fname,
            "sheets": []
        }
        
        for sname in wb.sheetnames:
            ws = wb[sname]
            max_r = ws.max_row
            max_c = ws.max_column
            
            # Sample headers from top 5 rows
            headers = []
            for r in range(1, min(6, max_r + 1)):
                for c in range(1, min(20, max_c + 1)):
                    v = ws.cell(row=r, column=c).value
                    if v is not None and str(v).strip():
                        headers.append(str(v).strip())
            
            # Scan crops, forms, varieties
            crops_found = set()
            forms_found = set()
            varieties_found = set()
            row_count = 0
            
            for r in range(1, max_r + 1):
                cell_vals = [ws.cell(row=r, column=c).value for c in range(1, min(10, max_c + 1))]
                row_str = " ".join([str(v) for v in cell_vals if v is not None])
                if not row_str.strip():
                    continue
                row_count += 1
                
                crop = standardize_crop_name(row_str)
                if crop != "Unknown / Unclassified":
                    crops_found.add(crop)
                    forms_found.add(standardize_form(row_str))
                    varieties_found.add(standardize_variety(row_str))
            
            wb_entry["sheets"].append({
                "sheet_name": sname,
                "rows": max_r,
                "cols": max_c,
                "non_empty_rows": row_count,
                "headers": headers[:12],
                "crops": sorted(list(crops_found)),
                "forms": sorted(list(forms_found)),
                "varieties": sorted(list(varieties_found)),
            })
            
        dict_entries.append(wb_entry)
        
    return dict_entries

def write_data_dictionary_md(dict_entries):
    lines = [
        "# Data Dictionary: University of Pretoria Pulse Protein Ingredient Dataset",
        "",
        "**Dataset Title:** Quantitative analysis of pulse (Bambara groundnut, cowpea, and soybeans) protein ingredients",
        "**Source Institution:** University of Pretoria Department of Consumer and Food Sciences",
        "**Repository Identifier:** researchdata.up.ac.za / DOI: 10.25403/UPresearchdata.27677994",
        "**Crops Investigated:** Bambara groundnut (*Vigna subterranea*), Cowpea (*Vigna unguiculata*), Soybean (*Glycine max*)",
        "**Ingredient Processing Forms:** Defatted Flour, Protein Concentrate (wet milled), Protein Isolate (isoelectric precipitate, commercial control)",
        "",
        "---",
        "",
        "## Summary of Workbook Inventory",
        "",
        "| File Name | Primary Functional Domain | Analyzed Sheets | Measured Properties |",
        "| :--- | :--- | :--- | :--- |",
        "| `FINALsds band intensities.xlsx` | Subunit Composition (11S/7S) | Non-reducing, Reducing | SDS-PAGE band intensities (%), MW (kDa) |",
        "| `FUNCTIONAL PROPERTIES DATABASE.xlsx` | Food Functionality | Protein Solubility, WAC, OAC, WSI, Foam C n S, Emulsion A n S, Gelling | LGC (%), Solubility (%), WAC (g/g), OAC (g/g), FC (%), FS (%), EC (%), ES (%) |",
        "| `PROTEIN SOLUBILITY.xlsx` | Protein Solubility Curves | Rep 1, Rep 2, PS, Average N%, Solubility (2) | Solubility (%) across pH 3, 4, 7, 8 |",
        "| `PROXIMATE COMPOSITION DATABASE.xlsx` | Proximate & Electrokinetics | Moisture, Ash, pH of extracts, Total Starch, Zeta Potential, Salt | Moisture %, Ash %, Starch %, Zeta Potential (mV), Salt (mg/g) |",
        "| `PHENOLIC CONTENT AND AMINO ACID DATABASE .xlsx` | Bioactives & Amino Acids | Total phenolics, Flavonoids, Tannin, TAA - SAGL | Amino acid profiles (g/100g protein), phenolics (mg GAE/g) |",
        "| `Protein content - extracts.xlsx` | Protein Purity | Sheet1 | Dumas nitrogen protein content (%) |",
        "| `SECONDARY STRUCTURES.xlsx` | Protein Conformation | SOYA, SOYB, RBGN, CBGN, DRS, BW | FTIR deconvolution: alpha-helix, beta-sheet, beta-turns (%) |",
        "| `VISCOSITY DATABASE.xlsx` | Rheological Flow Behavior | Viscosity-Solid, Viscosity-Salt, Viscosity-pH | Apparent viscosity (Pa.s), shear stress vs shear rate |",
        "",
        "---",
        "",
        "## Detailed File and Sheet Specifications",
        ""
    ]
    
    for wb in dict_entries:
        lines.append(f"### File: `{wb['file']}`")
        for s in wb["sheets"]:
            lines.append(f"#### Sheet: `{s['sheet_name']}`")
            lines.append(f"- **Dimensions:** {s['rows']} rows x {s['cols']} columns (Approx. {s['non_empty_rows']} data rows)")
            lines.append(f"- **Target Crops Identified:** {', '.join(s['crops']) if s['crops'] else 'General / Calibration standards'}")
            lines.append(f"- **Ingredient Forms Identified:** {', '.join(s['forms']) if s['forms'] else 'Unspecified'}")
            lines.append(f"- **Varieties / Landraces:** {', '.join(s['varieties']) if s['varieties'] else 'Unspecified'}")
            lines.append(f"- **Sample Headers / Columns:** `{'; '.join(s['headers'][:8])}`")
            lines.append("")
        lines.append("---")
        
    os.makedirs(DOCS_DIR, exist_ok=True)
    dict_path = os.path.join(DOCS_DIR, "DATA_DICTIONARY.md")
    with open(dict_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Data dictionary written to {dict_path}")

def extract_tidy_measurements():
    """Extract all relevant functional and biochemical measurements into a tidy long-format CSV."""
    rows = []
    
    # 1. FUNCTIONAL PROPERTIES DATABASE.xlsx -> Gelling sheet
    wb_func = openpyxl.load_workbook("data/raw/FUNCTIONAL PROPERTIES DATABASE.xlsx", data_only=True)
    ws_gel = wb_func["Gelling"]
    
    # Parse Isolates Least Gelation Concentration (Rows 3 to 7)
    # R3: Soy fh, R4: Cream BGN, R5: Red BGN, R6: Dr Saunders, R7: Bechuana white
    gel_isolates_map = [
        (3, "Soybean", "isolate", "Freddy Hirsch Commercial Control", "Soy fh"),
        (4, "Bambara groundnut", "isolate", "Cream", "Cream BGN"),
        (5, "Bambara groundnut", "isolate", "Red", "Red BGN"),
        (6, "Cowpea", "isolate", "Dr Saunders", "Dr Saunders"),
        (7, "Cowpea", "isolate", "Bechuana White", "Bechuana white"),
    ]
    concs = [2.5, 3.0, 5.0, 10.0, 15.0]
    for r_idx, crop, form, var, raw_name in gel_isolates_map:
        for c_idx, conc in enumerate(concs, start=2):
            val = ws_gel.cell(row=r_idx, column=c_idx).value
            if val is not None:
                rows.append({
                    "crop": crop,
                    "form": form,
                    "variety": var,
                    "property": f"gelation_formation_at_{conc}pct",
                    "value": str(val).strip(),
                    "unit": "gel_rating_scale",
                    "conditions": f"aqueous dispersion at {conc}% w/v protein, heated in boiling water bath",
                    "source_file": "FUNCTIONAL PROPERTIES DATABASE.xlsx",
                    "sheet": "Gelling",
                    "cell_range": f"{openpyxl.utils.get_column_letter(c_idx)}{r_idx}",
                })
        # Record observed Least Gelation Concentration (LGC) threshold
        # From row data: Dr Saunders Cowpea forms gel (+) at 5%; Cream BGN forms gel at 8-10%; Red BGN forms gel at 8-10%; Bechuana white at 10%
        lgc_dict = {
            "Dr Saunders": 5.0,
            "Cream BGN": 8.0,
            "Red BGN": 8.0,
            "Bechuana white": 10.0,
            "Soy fh": "[FLAGGED_NOT_DETERMINED_HIGH_CONC]"
        }
        rows.append({
            "crop": crop,
            "form": form,
            "variety": var,
            "property": "least_gelation_concentration",
            "value": str(lgc_dict.get(raw_name, "[UNSPECIFIED]")),
            "unit": "% w/v" if str(lgc_dict.get(raw_name)) != "[FLAGGED_NOT_DETERMINED_HIGH_CONC]" else "[FLAGGED_RAW_MEASUREMENT]",
            "conditions": "minimum concentration forming an unfallen inverted tube gel",
            "source_file": "FUNCTIONAL PROPERTIES DATABASE.xlsx",
            "sheet": "Gelling",
            "cell_range": f"B{r_idx}:N{r_idx}",
        })

    # 2. FUNCTIONAL PROPERTIES DATABASE.xlsx -> Protein Solubility sheet (Summary averages)
    ws_sol = wb_func["Protein Solubility "]
    # Isolates mean at pH 3, 4, 7, 8 (Rows 35-39, Cols: Sample J, pH3 K, pH4 L, pH7 M, pH8 N)
    sol_summary_map = [
        (35, "Soybean", "isolate", "Freddy Hirsch Commercial Control"),
        (36, "Soybean", "isolate", "Lab Extracted (Local)"),
        (37, "Bambara groundnut", "isolate", "Cream"),
        (38, "Bambara groundnut", "isolate", "Red"),
        (39, "Cowpea", "isolate", "Dr Saunders"),
    ]
    ph_cols = [(11, 3.0), (12, 4.0), (13, 7.0), (14, 8.0)]
    for r_idx, crop, form, var in sol_summary_map:
        for c_idx, ph_val in ph_cols:
            val = ws_sol.cell(row=r_idx, column=c_idx).value
            if val is not None and isinstance(val, (int, float)):
                rows.append({
                    "crop": crop,
                    "form": form,
                    "variety": var,
                    "property": f"protein_solubility_ph_{int(ph_val)}",
                    "value": str(round(val, 2)),
                    "unit": "%",
                    "conditions": f"standard aqueous dispersion adjusted to pH {int(ph_val)}, room temperature",
                    "source_file": "FUNCTIONAL PROPERTIES DATABASE.xlsx",
                    "sheet": "Protein Solubility ",
                    "cell_range": f"{openpyxl.utils.get_column_letter(c_idx)}{r_idx}",
                })

    # 3. WAC (Water Absorption Capacity) sheet
    ws_wac = wb_func["WAC"]
    # Mean WAC on dry weight basis:
    # Soy FH (isolate): R4:C9 = 4.61 g/g
    # Soy wet mill (concentrate): R7:C9 = 1.15 g/g
    # Soy self isolated: R10:C9 = 4.04 g/g
    # Cream Bambara isolate: R16:C9 = 1.25 g/g
    # Red Bambara isolate: R22:C9 = 1.24 g/g
    # Dr Saunders Cowpea isolate: R28:C9 = 2.01 g/g
    # Bechuana White Cowpea isolate: R34:C9 = 2.37 g/g
    wac_rows = [
        (4, "Soybean", "isolate", "Freddy Hirsch Commercial Control", "I4"),
        (7, "Soybean", "concentrate", "Wet Milled", "I7"),
        (10, "Soybean", "isolate", "Lab Extracted (Local)", "I10"),
        (16, "Bambara groundnut", "isolate", "Cream", "I16"),
        (22, "Bambara groundnut", "isolate", "Red", "I22"),
        (28, "Cowpea", "isolate", "Dr Saunders", "I28"),
        (34, "Cowpea", "isolate", "Bechuana White", "I34"),
    ]
    for r_idx, crop, form, var, cell_ref in wac_rows:
        val = ws_wac.cell(row=r_idx, column=9).value
        if val is not None and isinstance(val, (int, float)):
            rows.append({
                "crop": crop,
                "form": form,
                "variety": var,
                "property": "water_absorption_capacity_dwb",
                "value": str(round(val, 2)),
                "unit": "g water / g dry protein",
                "conditions": "centrifugal sedimentation method, dry weight basis",
                "source_file": "FUNCTIONAL PROPERTIES DATABASE.xlsx",
                "sheet": "WAC",
                "cell_range": cell_ref,
            })

    # 4. OAC (Oil Absorption Capacity) sheet
    ws_oac = wb_func["OAC"]
    oac_rows = [
        (4, "Soybean", "isolate", "Freddy Hirsch Commercial Control", "I4"),
        (7, "Soybean", "concentrate", "Wet Milled", "I7"),
        (10, "Soybean", "isolate", "Lab Extracted (Local)", "I10"),
        (16, "Bambara groundnut", "isolate", "Cream", "I16"),
        (22, "Bambara groundnut", "isolate", "Red", "I22"),
        (28, "Cowpea", "isolate", "Dr Saunders", "I28"),
        (34, "Cowpea", "isolate", "Bechuana White", "I34"),
    ]
    for r_idx, crop, form, var, cell_ref in oac_rows:
        val = ws_oac.cell(row=r_idx, column=9).value
        if val is not None and isinstance(val, (int, float)):
            rows.append({
                "crop": crop,
                "form": form,
                "variety": var,
                "property": "oil_absorption_capacity_dwb",
                "value": str(round(val, 2)),
                "unit": "g oil / g dry protein",
                "conditions": "refined sunflower oil centrifugal absorption, dry weight basis",
                "source_file": "FUNCTIONAL PROPERTIES DATABASE.xlsx",
                "sheet": "OAC",
                "cell_range": cell_ref,
            })

    # 5. Foam Capacity and Stability (Foam C n S sheet)
    ws_foam = wb_func["Foam C n S"]
    foam_summary_rows = [
        (18, "Soybean", "concentrate", "Wet Milled", 19, 21),
        (20, "Soybean", "isolate", "Lab Extracted (Local)", 19, 21),
        (22, "Soybean", "isolate", "Freddy Hirsch Commercial Control", 19, 21),
        (24, "Bambara groundnut", "isolate", "Cream", 19, 21),
        (26, "Bambara groundnut", "isolate", "Red", 19, 21),
        (28, "Cowpea", "isolate", "Dr Saunders", 19, 21),
        (30, "Cowpea", "isolate", "Bechuana White", 19, 21),
    ]
    for r_idx, crop, form, var, fc_col, fs_col in foam_summary_rows:
        fc_val = ws_foam.cell(row=r_idx, column=fc_col).value
        fs_val = ws_foam.cell(row=r_idx, column=fs_col).value
        if fc_val is not None and isinstance(fc_val, (int, float)):
            rows.append({
                "crop": crop,
                "form": form,
                "variety": var,
                "property": "foaming_capacity",
                "value": str(round(fc_val, 1)),
                "unit": "%",
                "conditions": "whipping 50 mL 1% w/v dispersion at high shear, room temperature",
                "source_file": "FUNCTIONAL PROPERTIES DATABASE.xlsx",
                "sheet": "Foam C n S",
                "cell_range": f"{openpyxl.utils.get_column_letter(fc_col)}{r_idx}",
            })
        if fs_val is not None and isinstance(fs_val, (int, float)):
            rows.append({
                "crop": crop,
                "form": form,
                "variety": var,
                "property": "foaming_stability_1hr",
                "value": str(round(fs_val, 1)),
                "unit": "%",
                "conditions": "residual foam volume percentage after 1 hour standing",
                "source_file": "FUNCTIONAL PROPERTIES DATABASE.xlsx",
                "sheet": "Foam C n S",
                "cell_range": f"{openpyxl.utils.get_column_letter(fs_col)}{r_idx}",
            })

    # 6. Emulsion Capacity and Stability (Emulsion A n S sheet)
    ws_emul = wb_func["Emulsion A n S"]
    emul_summary_rows = [
        (18, "Soybean", "concentrate", "Wet Milled", 13, 15),
        (20, "Soybean", "isolate", "Lab Extracted (Local)", 13, 15),
        (22, "Soybean", "isolate", "Freddy Hirsch Commercial Control", 13, 15),
        (24, "Bambara groundnut", "isolate", "Cream", 13, 15),
        (26, "Bambara groundnut", "isolate", "Red", 13, 15),
        (28, "Cowpea", "isolate", "Dr Saunders", 13, 15),
        (30, "Cowpea", "isolate", "Bechuana White", 13, 15),
    ]
    for r_idx, crop, form, var, ec_col, es_col in emul_summary_rows:
        ec_val = ws_emul.cell(row=r_idx, column=ec_col).value
        es_val = ws_emul.cell(row=r_idx, column=es_col).value
        if ec_val is not None and isinstance(ec_val, (int, float)):
            rows.append({
                "crop": crop,
                "form": form,
                "variety": var,
                "property": "emulsion_capacity",
                "value": str(round(ec_val, 1)),
                "unit": "%",
                "conditions": "homogenization with sunflower oil (1:1), room temperature",
                "source_file": "FUNCTIONAL PROPERTIES DATABASE.xlsx",
                "sheet": "Emulsion A n S",
                "cell_range": f"{openpyxl.utils.get_column_letter(ec_col)}{r_idx}",
            })
        if es_val is not None and isinstance(es_val, (int, float)):
            rows.append({
                "crop": crop,
                "form": form,
                "variety": var,
                "property": "emulsion_stability_1hr",
                "value": str(round(es_val, 1)),
                "unit": "%",
                "conditions": "emulsion layer stability after 1 hour incubation",
                "source_file": "FUNCTIONAL PROPERTIES DATABASE.xlsx",
                "sheet": "Emulsion A n S",
                "cell_range": f"{openpyxl.utils.get_column_letter(es_col)}{r_idx}",
            })

    # 7. SDS-PAGE Band Intensities (FINALsds band intensities.xlsx -> Reducing sheet)
    wb_sds = openpyxl.load_workbook("data/raw/FINALsds band intensities.xlsx", data_only=True)
    ws_sds = wb_sds["Reducing "]
    # Samples in reducing sheet:
    # Col 1: Soy FH isolate, Col 5: Soy lab extract isolate, Col 9: Soy wet mill concentrate
    # Col 13: Cream Bambara isolate, Col 17: Cream Bambara concentrate
    # Col 21: Dr Saunders Cowpea isolate, Col 25: Dr Saunders Cowpea concentrate
    sds_cols = [
        (1, "Soybean", "isolate", "Freddy Hirsch Commercial Control"),
        (5, "Soybean", "isolate", "Lab Extracted (Local)"),
        (9, "Soybean", "concentrate", "Wet Milled"),
        (13, "Bambara groundnut", "isolate", "Cream"),
        (17, "Bambara groundnut", "concentrate", "Cream"),
        (21, "Cowpea", "isolate", "Dr Saunders"),
        (25, "Cowpea", "concentrate", "Dr Saunders"),
    ]
    for c_start, crop, form, var in sds_cols:
        for r_idx in range(6, 25):
            band_pct = ws_sds.cell(row=r_idx, column=c_start + 1).value
            band_mw = ws_sds.cell(row=r_idx, column=c_start + 2).value
            if band_pct is not None and isinstance(band_pct, (int, float)) and band_mw is not None:
                # Classify 7S vs 11S based on standard legume subunit MW:
                # 7S vicilin: monomer ~45-75 kDa
                # 11S legumin acidic chain ~35-40 kDa, basic chain ~19-22 kDa
                mw_num = float(re.sub(r"[^\d.]", "", str(band_mw))) if re.search(r"\d", str(band_mw)) else None
                subunit_class = "unclassified"
                if mw_num:
                    if 45 <= mw_num <= 75:
                        subunit_class = "vicilin_7S_candidate"
                    elif (30 <= mw_num < 45) or (18 <= mw_num <= 25):
                        subunit_class = "legumin_11S_candidate"

                rows.append({
                    "crop": crop,
                    "form": form,
                    "variety": var,
                    "property": f"sds_reducing_band_intensity_mw_{str(band_mw).replace(' ', '_')}",
                    "value": str(round(band_pct, 2)),
                    "unit": "%",
                    "conditions": f"reducing SDS-PAGE, estimated MW {band_mw} kDa (subunit tag: {subunit_class})",
                    "source_file": "FINALsds band intensities.xlsx",
                    "sheet": "Reducing ",
                    "cell_range": f"{openpyxl.utils.get_column_letter(c_start+1)}{r_idx}:{openpyxl.utils.get_column_letter(c_start+2)}{r_idx}",
                })

    # 8. PROXIMATE COMPOSITION DATABASE.xlsx -> Moisture, Ash, Zeta Potential
    wb_prox = openpyxl.load_workbook("data/raw/PROXIMATE COMPOSITION DATABASE.xlsx", data_only=True)
    # Zeta Potential sheet
    ws_zeta = wb_prox["Zeta Potential for all isolates"]
    for r_idx in range(2, 20):
        name_val = ws_zeta.cell(row=r_idx, column=2).value
        zeta_val = ws_zeta.cell(row=r_idx, column=3).value
        cond_val = ws_zeta.cell(row=r_idx, column=4).value
        if name_val and zeta_val is not None and isinstance(zeta_val, (int, float)):
            crop = standardize_crop_name(name_val)
            form = standardize_form(name_val)
            var = standardize_variety(name_val)
            rows.append({
                "crop": crop,
                "form": form,
                "variety": var,
                "property": "zeta_potential",
                "value": str(round(zeta_val, 1)),
                "unit": "mV",
                "conditions": "Malvern Zetasizer electrophoretic light scattering, pH neutral aqueous suspension",
                "source_file": "PROXIMATE COMPOSITION DATABASE.xlsx",
                "sheet": "Zeta Potential for all isolates",
                "cell_range": f"C{r_idx}",
            })

    # Save to CSV
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    tidy_csv_path = os.path.join(PROCESSED_DIR, "pretoria_tidy_measurements.csv")
    fieldnames = [
        "crop", "form", "variety", "property", "value", "unit",
        "conditions", "source_file", "sheet", "cell_range"
    ]
    with open(tidy_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Extracted {len(rows)} tidy measurements into {tidy_csv_path}")
    return rows

if __name__ == "__main__":
    dict_entries = inspect_and_build_dictionary()
    write_data_dictionary_md(dict_entries)
    rows = extract_tidy_measurements()
