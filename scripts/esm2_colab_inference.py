"""
Proti IQ — ESM-2 Embedding Inference for Google Colab
=====================================================

HOW TO USE:
1. Go to https://colab.research.google.com
2. Create a new notebook (File > New notebook)
3. Copy ALL of this code into a single cell
4. Click the play button to run
5. When prompted, upload the file: data/processed/all_proteins.fasta
6. Wait ~20-30 minutes for inference to complete
7. The file embeddings.zip will auto-download when done
8. Bring embeddings.zip back to your local machine

After downloading embeddings.zip:
1. Extract it into: model_artifacts/embeddings/ (overwrite all .npy files)
2. Run locally: python scripts/import_esm2_embeddings.py
3. Run locally: python -m pipeline.scoring
4. Run locally: python -m pipeline.export
"""

# ============================================================
# STEP 1: Install dependencies
# ============================================================
import subprocess
subprocess.check_call(["pip", "install", "-q", "transformers", "torch", "sentencepiece"])

# ============================================================
# STEP 2: Upload the FASTA file
# ============================================================
print("Please upload all_proteins.fasta when the dialog appears...")
from google.colab import files
uploaded = files.upload()

fasta_filename = list(uploaded.keys())[0]
print(f"Uploaded: {fasta_filename}")

# ============================================================
# STEP 3: Load ESM-2 model
# ============================================================
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import os
import time

MODEL_NAME = "facebook/esm2_t33_650M_UR50D"
print(f"Loading {MODEL_NAME}...")
print("This downloads ~2.5 GB of model weights on first run.")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
print(f"Model loaded on {device}")

# ============================================================
# STEP 4: Parse FASTA
# ============================================================
sequences = {}
current_id = None

with open(fasta_filename, "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            current_id = line[1:].split()[0]
            sequences[current_id] = ""
        elif current_id:
            sequences[current_id] += line

print(f"Parsed {len(sequences)} protein sequences")

# ============================================================
# STEP 5: Generate embeddings
# ============================================================
os.makedirs("embeddings", exist_ok=True)

start_time = time.time()
total = len(sequences)

for i, (accession, seq) in enumerate(sequences.items()):
    # ESM-2 max input is 1022 tokens (excluding BOS/EOS)
    truncated_seq = seq[:1022]

    inputs = tokenizer(truncated_seq, return_tensors="pt", add_special_tokens=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        # Mean pool over sequence positions (exclude BOS at [0] and EOS at [-1])
        embedding = outputs.last_hidden_state[0, 1:-1, :].mean(dim=0).cpu().numpy()

    np.save(f"embeddings/{accession}.npy", embedding.astype(np.float32))

    if (i + 1) % 10 == 0 or (i + 1) == total:
        elapsed = time.time() - start_time
        rate = (i + 1) / elapsed
        remaining = (total - i - 1) / rate if rate > 0 else 0
        print(f"  [{i+1}/{total}] {accession} done | {elapsed:.0f}s elapsed | ~{remaining:.0f}s remaining")

elapsed_total = time.time() - start_time
print(f"\nAll {total} embeddings generated in {elapsed_total:.0f} seconds")
print(f"Embedding dimension: {embedding.shape[0]}")

# ============================================================
# STEP 6: Zip and download
# ============================================================
import shutil
shutil.make_archive("embeddings", "zip", ".", "embeddings")
print(f"Created embeddings.zip ({os.path.getsize('embeddings.zip') / 1024 / 1024:.1f} MB)")

files.download("embeddings.zip")
print("Download started! Save embeddings.zip to your Proti IQ project folder.")
