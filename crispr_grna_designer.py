"""
CRISPR gRNA (Guide RNA) Designer
--------------------------------
A simple tool that scans a DNA sequence for CRISPR-Cas9 target sites.

How it works:
- CRISPR-Cas9 requires a "PAM" site with the pattern NGG (N = any base).
- The 20 bases immediately BEFORE each PAM site are a candidate guide RNA.
- This script finds all candidate guide RNAs and reports their GC content,
  a simple and commonly used quality indicator (guides with 40-60% GC
  tend to work better in the lab).

Usage:
    python crispr_grna_designer.py my_gene.fasta

Input:
    A plain FASTA file containing one DNA sequence (see example_gene.fasta).

Output:
    A table (printed to screen and saved as results.csv) listing each
    candidate guide RNA, its position in the sequence, and its GC content.
"""

import sys
import csv


def read_fasta(filepath):
    """Read a simple single-sequence FASTA file and return the DNA sequence as a string."""
    sequence_lines = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">") or line == "":
                continue  # skip header lines and blank lines
            sequence_lines.append(line.upper())
    return "".join(sequence_lines)


def gc_content(sequence):
    """Calculate the percentage of G and C bases in a sequence."""
    if len(sequence) == 0:
        return 0.0
    gc_count = sequence.count("G") + sequence.count("C")
    return round((gc_count / len(sequence)) * 100, 1)


def find_grna_candidates(dna_sequence, guide_length=20):
    """
    Scan the DNA sequence for NGG PAM sites and extract the candidate
    guide RNA sequence immediately upstream of each one.
    """
    candidates = []
    # We scan every position looking for a PAM (any base, then G, then G)
    for i in range(guide_length, len(dna_sequence) - 2):
        pam = dna_sequence[i:i + 3]
        if len(pam) == 3 and pam[1] == "G" and pam[2] == "G":
            guide = dna_sequence[i - guide_length:i]
            if len(guide) == guide_length:
                candidates.append({
                    "position": i - guide_length + 1,  # 1-based position for readability
                    "guide_rna": guide,
                    "pam": pam,
                    "gc_content_percent": gc_content(guide)
                })
    return candidates


def main():
    if len(sys.argv) != 2:
        print("Usage: python crispr_grna_designer.py <fasta_file>")
        sys.exit(1)

    fasta_path = sys.argv[1]
    dna_sequence = read_fasta(fasta_path)

    if not dna_sequence:
        print("No sequence found in the file. Please check the FASTA format.")
        sys.exit(1)

    print(f"Loaded sequence: {len(dna_sequence)} bases\n")

    candidates = find_grna_candidates(dna_sequence)

    if not candidates:
        print("No NGG PAM sites found in this sequence.")
        sys.exit(0)

    print(f"Found {len(candidates)} candidate guide RNAs.\n")
    print(f"{'Position':<10}{'Guide RNA (20 nt)':<25}{'PAM':<8}{'GC %':<8}")
    print("-" * 51)
    for c in candidates:
        print(f"{c['position']:<10}{c['guide_rna']:<25}{c['pam']:<8}{c['gc_content_percent']:<8}")

    # Save results to a CSV file so they can be opened in Excel
    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["position", "guide_rna", "pam", "gc_content_percent"])
        writer.writeheader()
        writer.writerows(candidates)

    print("\nResults also saved to results.csv")


if __name__ == "__main__":
    main()
