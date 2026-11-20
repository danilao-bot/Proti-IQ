import sys
sys.path.insert(0, ".")
from api.db import SessionLocal, Protein, Crop, init_db

init_db()
db = SessionLocal()

for acc in ["A0A1S3VZW2", "P02858", "P11827"]:
    p = db.query(Protein).filter(Protein.accession == acc).first()
    crop = db.query(Crop).filter(Crop.id == p.crop_id).first() if p else None
    cname = crop.common_name if crop else "Unknown"
    print(f"{acc}: found={p is not None} | crop={cname} | tax={p.tax_id} | name={p.name} | len={p.length} | rev={p.reviewed}")

db.close()
