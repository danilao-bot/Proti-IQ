"""
AlphaFold Model Downloader.
Downloads AlphaFold v6 PDB structures for target benchmark proteins.
"""
import urllib.request
import os

TARGETS = {
    "A0A1S3VZW2": "https://alphafold.ebi.ac.uk/files/AF-A0A1S3VZW2-F1-model_v6.pdb",
    "P02858": "https://alphafold.ebi.ac.uk/files/AF-P02858-F1-model_v6.pdb",
    "P11827": "https://alphafold.ebi.ac.uk/files/AF-P11827-F1-model_v6.pdb"
}

os.makedirs("data/raw/structures", exist_ok=True)
for acc, url in TARGETS.items():
    out = f"data/raw/structures/{acc}.pdb"
    if not os.path.exists(out):
        print(f"Downloading {acc}...")
        urllib.request.urlretrieve(url, out)
        print(f"  Saved {out}")
    else:
        print(f"  {acc}.pdb already exists.")
print("AlphaFold model verification complete.")
