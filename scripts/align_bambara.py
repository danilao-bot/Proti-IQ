"""
Bambara Alignment Engine - Proti IQ
Aligns Cowpea and Mung Bean 7S vicilin and 11S legumin sequences against all Bambara proteins.
Records any hits with >= 40% sequence identity as candidate storage proteins.
"""

import os
import sys
import json
from typing import List, Dict, Tuple

sys.path.insert(0, os.path.abspath("."))
from sqlalchemy.orm import Session
from api.db import SessionLocal, Protein


def calculate_identity(seq1: str, seq2: str) -> Tuple[float, int, int]:
    """
    Calculates sequence identity using a robust dynamic programming local alignment (Smith-Waterman style).
    Returns (identity_percentage, matches, alignment_length).
    """
    m, n = len(seq1), len(seq2)
    if m == 0 or n == 0:
        return 0.0, 0, 0

    # Fast heuristic filter: check k-mer sharing before full DP
    k = 4
    kmers1 = {seq1[i:i+k] for i in range(len(seq1) - k + 1)}
    kmers2 = {seq2[i:i+k] for i in range(len(seq2) - k + 1)}
    common_kmers = kmers1.intersection(kmers2)
    if len(common_kmers) < 3 and min(m, n) > 50:
        # Very low sequence similarity, bound below 25%
        return 15.0, 0, min(m, n)

    # Simplified Smith-Waterman matrix
    match_score = 2
    mismatch_penalty = -1
    gap_penalty = -2

    # To be memory efficient, use 2 rows
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_score = 0
    max_i, max_j = 0, 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            score = match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty
            dp[i][j] = max(
                0,
                dp[i-1][j-1] + score,
                dp[i-1][j] + gap_penalty,
                dp[i][j-1] + gap_penalty
            )
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_i, max_j = i, j

    if max_score == 0:
        return 0.0, 0, 0

    # Traceback to calculate aligned matches and length
    i, j = max_i, max_j
    matches = 0
    aln_len = 0
    while i > 0 and j > 0 and dp[i][j] > 0:
        score = match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty
        if dp[i][j] == dp[i-1][j-1] + score:
            if seq1[i-1] == seq2[j-1]:
                matches += 1
            aln_len += 1
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i-1][j] + gap_penalty:
            aln_len += 1
            i -= 1
        else:
            aln_len += 1
            j -= 1

    identity = (matches / aln_len) * 100.0 if aln_len > 0 else 0.0
    return identity, matches, aln_len


def run_bambara_alignment():
    db: Session = SessionLocal()
    try:
        # Load Bambara proteins
        bambara_prots = db.query(Protein).filter(Protein.crop_id == "bambara_groundnut").all()
        print(f"Loaded {len(bambara_prots)} Bambara groundnut proteins from database.")

        # Load reference Cowpea and Mung bean storage proteins
        ref_prots = db.query(Protein).filter(
            Protein.crop_id.in_(["cowpea", "mung_bean"]),
            Protein.family.in_(["7S", "11S"])
        ).all()
        print(f"Loaded {len(ref_prots)} reference 7S/11S storage proteins (Cowpea + Mung bean).")

        hits_above_40 = []
        max_identity_overall = 0.0
        best_pair = None

        print("\nAligning reference storage globulins against all Bambara proteins...")
        for b in bambara_prots:
            b_acc = b.accession
            b_name = b.name
            b_seq = b.sequence
            max_b_id = 0.0

            for ref in ref_prots:
                r_acc = ref.accession
                r_crop = ref.crop_id
                r_fam = ref.family
                r_seq = ref.sequence

                ident, matches, aln_len = calculate_identity(r_seq, b_seq)
                if ident > max_b_id:
                    max_b_id = ident
                if ident > max_identity_overall:
                    max_identity_overall = ident
                    best_pair = (ref, b, ident, matches, aln_len)

                if ident >= 40.0 and aln_len >= 50:
                    hits_above_40.append({
                        "bambara_accession": b_acc,
                        "bambara_name": b_name,
                        "ref_crop": r_crop,
                        "ref_accession": r_acc,
                        "ref_family": r_fam,
                        "identity_pct": round(ident, 2),
                        "matches": matches,
                        "alignment_length": aln_len
                    })

            print(f"  Bambara protein {b_acc} ({b_name[:30]}): Max identity to any ref storage globulin = {max_b_id:.1f}%")

        print("\n--- BAMBARA ALIGNMENT SUMMARY ---")
        print(f"Total Bambara proteins evaluated: {len(bambara_prots)}")
        print(f"Total reference storage proteins used: {len(ref_prots)}")
        print(f"Candidate hits with >= 40% identity: {len(hits_above_40)}")
        print(f"Maximum identity observed across all pairs: {max_identity_overall:.1f}%")

        if best_pair:
            r, b, ident, matches, aln_len = best_pair
            print(f"Highest alignment pair: {r.crop_id} {r.accession} ({r.name[:25]}) vs {b.accession} ({b.name[:25]}) -> {ident:.1f}% ({matches}/{aln_len} aa)")

        # Save results
        out_path = "data/processed/bambara_alignment_hits.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({
                "total_bambara_proteins": len(bambara_prots),
                "total_reference_storage_proteins": len(ref_prots),
                "threshold_pct": 40.0,
                "hits_above_40_count": len(hits_above_40),
                "max_identity_pct": round(max_identity_overall, 2),
                "candidates": hits_above_40
            }, f, indent=2)
        print(f"Detailed alignment results written to {out_path}")

        # Decision rule enforcement
        if len(hits_above_40) == 0:
            print("\nCONCLUSION: 0 storage globulin homologs found above 40% identity.")
            print("POLICY: Bambara groundnut MUST NOT be ranked by the sequence model.")
            print("        Bambara is evaluated exclusively via Tier 1 empirical wet-lab measurements.")
        else:
            print(f"\nCONCLUSION: {len(hits_above_40)} candidates identified for potential ranking.")

        return hits_above_40
    finally:
        db.close()


if __name__ == "__main__":
    run_bambara_alignment()
