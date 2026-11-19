"""
Unified Command-Line Interface for Proti IQ Offline Pipeline.
Usage:
    python -m pipeline.cli run-all
    python -m pipeline.cli import-config
    python -m pipeline.cli ingest-uniprot
    python -m pipeline.cli ingest-af
    python -m pipeline.cli features
    python -m pipeline.cli embed
    python -m pipeline.cli score
    python -m pipeline.cli backtest
"""

import argparse
import sys
from pipeline.import_csv import run_import
from pipeline.ingest_uniprot import run_ingest
from pipeline.ingest_alphafold import run_af_ingest
from pipeline.features import run_features
from pipeline.embeddings import run_embeddings
from pipeline.scoring import run_scoring
from pipeline.backtest import run_backtest
from pipeline.export import run_export


def main():
    parser = argparse.ArgumentParser(
        prog="proti-iq-pipeline",
        description="Proti IQ Data & Machine Learning Offline Pipeline",
    )
    parser.add_argument(
        "stage",
        choices=[
            "import-config",
            "ingest-uniprot",
            "ingest-af",
            "features",
            "embed",
            "score",
            "backtest",
            "export",
            "run-all",
        ],
        help="Pipeline stage to execute",
    )

    args = parser.parse_args()

    print(f"\n=== Proti IQ Pipeline: Executing '{args.stage}' ===")

    if args.stage == "import-config":
        run_import()
    elif args.stage == "ingest-uniprot":
        run_ingest()
    elif args.stage == "ingest-af":
        run_af_ingest()
    elif args.stage == "features":
        run_features()
    elif args.stage == "embed":
        run_embeddings()
    elif args.stage == "score":
        run_scoring()
    elif args.stage == "backtest":
        run_backtest()
    elif args.stage == "export":
        run_export()
    elif args.stage == "run-all":
        print("\n[Stage 1/7] Importing Configuration & Answer Key...")
        run_import()

        print("\n[Stage 2/7] Ingesting UniProt Storage Proteins...")
        run_ingest()

        print("\n[Stage 3/7] Ingesting AlphaFold 3D Confidence & Coordinates...")
        run_af_ingest()

        print("\n[Stage 4/7] Computing Biophysical & Sequence Features...")
        run_features()

        print("\n[Stage 5/7] Generating ESM-2 8M Embeddings...")
        run_embeddings()

        print("\n[Stage 6/7] Computing Multi-Criteria Job Scoring...")
        run_scoring()

        print("\n[Stage 7/7] Running Literature Back-Test & Evidence Validation...")
        run_backtest()
        run_export()

        print("\n=== Proti IQ Pipeline: All Stages Successfully Executed! ===\n")


if __name__ == "__main__":
    main()
