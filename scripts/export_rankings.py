import sys, os
sys.path.append(os.path.abspath("."))
from api.db import SessionLocal, Ranking, Crop, Protein, ModelRun
import pandas as pd

db = SessionLocal()
latest_run = db.query(ModelRun).order_by(ModelRun.created_at.desc()).first()
run_id = latest_run.id if latest_run else None
print(f"Exporting rankings for latest run: {run_id}")

ranks = db.query(Ranking).filter(Ranking.run_id == run_id).all()
rows = []
for r in ranks:
    crop = db.query(Crop).filter(Crop.id == r.crop_id).first()
    prot = db.query(Protein).filter(Protein.id == r.protein_id).first()
    rows.append({
        'job': r.job,
        'crop_id': r.crop_id,
        'crop_name': crop.common_name if crop else r.crop_id,
        'protein_accession': prot.accession if prot else '',
        'score': r.score,
        'confidence': r.confidence
    })

df = pd.DataFrame(rows)
df.to_csv('data/processed/latest_rankings.csv', index=False)
print(f"Exported {len(df)} rankings across jobs: {df['job'].unique().tolist()}")
db.close()
