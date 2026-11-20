"""Export all protein sequences as FASTA for ESM-2 inference on Google Colab."""
import sys
sys.path.insert(0, ".")
from api.db import SessionLocal, Protein, init_db

init_db()
db = SessionLocal()

proteins = db.query(Protein).all()
output_path = "data/processed/all_proteins.fasta"

with open(output_path, "w", encoding="utf-8") as f:
    for p in proteins:
        f.write(f">{p.accession}\n")
        # Write sequence in 80-char lines
        seq = p.sequence
        for i in range(0, len(seq), 80):
            f.write(seq[i:i+80] + "\n")

print(f"Exported {len(proteins)} sequences to {output_path}")
db.close()
