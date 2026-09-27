# CRISPR gRNA Designer

A simple Python tool that scans a DNA sequence and identifies candidate CRISPR-Cas9 guide RNAs (gRNAs).

## Background

CRISPR-Cas9 gene editing requires a short "PAM" site (pattern: NGG) next to the DNA region being targeted. The 20 bases immediately upstream of the PAM site become the guide RNA that directs the Cas9 enzyme to cut at that location.

This tool automates the first step of guide RNA design: scanning a gene sequence for all valid PAM sites and reporting the candidate guide RNAs along with their GC content — a simple, widely used indicator of guide quality (guides with 40–60% GC content are generally considered more reliable in the lab).

## Motivation

ITGB6 (Integrin subunit beta 6, RefSeq NM\_000888) encodes a host cell-surface receptor that Foot-and-Mouth Disease Virus (FMDV) uses to enter host cells. My M.Phil research focused on comparative genomic analysis of FMDV field and vaccine strains, and this project extends that interest from the viral side to the host side of infection — scanning ITGB6 for candidate CRISPR-Cas9 target sites as a step toward exploring host-receptor-based resistance strategies, an active area of current livestock disease research. Scanning the full 31,268 bp human ITGB6 transcript identified 1,437 candidate guide RNA sites, each scored by GC content as an initial quality filter.

## How to use it

1. Make sure you have Python 3 installed.
2. Place your DNA sequence in a FASTA file (see `example\_gene.fasta` for the expected format).
3. Run:

```
   python crispr\_grna\_designer.py ITGB6\_human.fasta
   ```

4. The tool will print all candidate guide RNAs to the screen and save them to `results.csv`.

## Example output

```
Position  Guide RNA (20 nt)       PAM     GC %
---------------------------------------------------
5         CTAGCTAGCTAGGCGATCGA    TCG     55.0
...
```

## What this tool does NOT do (yet)

This is a foundational, educational implementation. It does not currently check for:

* Off-target binding elsewhere in the genome
* Secondary structure / self-complementarity of the guide
* Species-specific PAM variants (e.g., for Cas12a, SaCas9)

These are natural next steps for extending this project.

## Tools/skills used

Python, sequence analysis, CRISPR-Cas9 fundamentals, GC content calculation.

