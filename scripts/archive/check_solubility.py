import csv

with open("data/processed/pretoria_tidy_measurements.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if "solubility" in row["property"].lower() and "7" in row["conditions"]:
            print(f"{row['crop']} | {row['variety']} | {row['form']} | {row['value']} {row['unit']} | {row['source_file']} | {row['sheet']} | {row['cell_range']}")
