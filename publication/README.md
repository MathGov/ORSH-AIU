# ORSH / AIU research release v1.8

26 September 2026. Complete specialist-review release, not journal acceptance, external replication or a validated ontology.

ORSH is the historical **Open Relational Substrate Hypothesis** programme label. AIU denotes **Absolute Infinite Union** in the philosophical manuscript; the explicit commitments, not an acronym, define its subject. No external MathGov or SGP document is amended.


## Finalized build, same versions

This distribution retains portfolio v1.8 and all five current manuscript version labels. The limited finalization clarifies operator/frame notation, transport encoding, implementation provenance and citation order, and rebuilds the readers. `editorial/FINALIZATION_NOTES.md` states accepted and rejected suggestions; `editorial/FINALIZATION.diff` and source hashes show every textual change. The original v1.8 active files are preserved under `historical/v1_8_before_finalization`. Use this build's manifest, not a version label alone, to identify these files.

The scientific results, data, numerical code and frozen experiment specification are unchanged. Fresh checks performed for this finalization are distinguished from historical full population replays in `verification/RELEASE_VERIFICATION.md`. The cover now spells out ORSH and has embedded fonts; no PDF/A or PDF/UA certification is claimed.

## Read these five current documents

1. `manuscripts/Frame_Aligned_Records_v0_5` (.md, .docx, .pdf): the methods paper.
2. `supplement/Frame_Aligned_Records_Supplement_v1_2` (.md, .docx, .pdf): scientific tables, reproduction instructions and historical provenance.
3. `pilot/Post_Injection_Results_v1_2` (.md, .docx, .pdf): original source-off result and the separately identified factorial extension.
4. `protocols/P01_Post_Injection_Protocol_v1_3` (.md, .docx, .pdf): reader edition of the unchanged executed specification, with a publication note.
5. `manuscripts/Absolute_Infinite_Union_v1_4` (.md, .docx, .pdf): separate philosophical inquiry.

The collected PDF starts with a one-page contents/reading-order guide. The reviewer Markdown bundle is a convenient text edition, not an independent manuscript. Relative figure links resolve inside the extracted directory; standalone Markdown cannot supply images that were not transferred with it. DOCX and PDF embed their figures.

## Main scientific distinction

The original source-off result compares evolution with matched frozen evolution. Its negative mean remains negative. The later factorial contrast compares two Hamiltonian orientations at the same injection. Its positive mean does not reverse the original estimand. The intervention changes an entire Hamiltonian relative to fixed preparation and access; isospectrality alone does not make it a locality-only manipulation. No tensor-product structure or spacetime metric was reconstructed.

In the original v1.8 build, the supplied review scripts were re-executed at their original sizes and seeds. All three supplied numerical summary files match within relative tolerance 1e-8 and absolute tolerance 1e-10. Per-unit scalar observables are now retained. A separate method checks selected trajectories. A new six-target empirical-Bernstein analysis is explicitly post hoc and assumes iid model units, a fixed target family and faithful numerical evaluation. It is not an external preregistration or a normal-approximation interval.

## Reproduce without overwriting the evidence

Use a copy of this directory, Python and the versions in `verification/environment.json`. Set `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`. The numerical requirements are in `requirements.txt`; document builds additionally require pandoc, XeLaTeX, python-docx, lxml and fonts already installed in the build environment. No font files are distributed.

```sh
python code/verify_release.py --root . --report /path/to/new_structural_report.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/run_injection_pilot.py --config pilot/config.json --out /path/to/fresh_original_pilot
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/replay_reviewer.py --root . --out /path/to/fresh_reviewer_replay --task all
python code/analyze_factorial.py --root . --out /path/to/fresh_factorial_analysis
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/validate_factorial.py --root . --out /path/to/fresh_factorial_checks.json
```

The factorial analysis reads the delivered `data/reviewer_replay`. For a fresh-data comparison, put the new replay in that location in a separate working copy. It refuses a nonempty analysis output directory. The supplied source functions and seeds completely specify the generated Hamiltonians and circuits; the new factorial NPZ files retain scalar per-unit outcomes, not all time-resolved many-body states. The original pilot's full saved trajectories remain under `data/pilot_run`.

## Typesetting and portability

Each current `.md` is UTF-8 canonical text. `code/build_documents.py` generates editable native Word mathematics and explicitly writes intended delimiters and upright operator runs. The PDF is independently typeset from the same Markdown through XeLaTeX by `code/build_pdf.py`; it is **not** the problematic historical LibreOffice export. The `.tex` files and header/filter are supplied. From an individual `typesetting/<stem>` directory, `xelatex <stem>.tex` resolves its relative figure paths. Layouts and page numbers differ between Word and PDF; substantive source identity does not mean identical pagination.

## Archives, versions and limits

New active editions have two-component version labels. Historical versions, including older three-component labels, are preserved rather than renamed to falsify their identity. `historical/v1_7_core` contains prior active texts, PDFs and build records; larger earlier releases are retained in `historical`. Those old PDFs are superseded reading copies and must not be circulated as current corrected outputs.

`pilot/PRE_EXECUTION_PLAN.md`, its configuration, its original code hash and receipt remain unchanged. A matching local hash proves integrity, not an externally witnessed pre-outcome timestamp. New review predictions are preserved with the same limitation. No human reviewer has been represented as having approved the work, no email was sent, and no repository or preprint deposit was made.

The author must approve declarations, rights, affiliations and any eventual submission. The source register makes access limits visible: some philosophical sources were checked only at publisher-abstract level, and Nozick remains a bibliographic lead rather than an evidentially relied-on reading. Readiness for specialist criticism is not completeness of the research programme or guaranteed publication suitability.

## Rendering and portability

The mathematical source remains Markdown with TeX math. DOCX equations retain native editable Office mathematics. For renderer compatibility, delimiter glyphs are explicit and the vertical stroke uses U+2223; plain operator-letter runs are joined without changing their meaning. PDFs use a separate XeLaTeX rendering of the same canonical source, not a LibreOffice PDF conversion. Portable .tex sources, the LaTeX header and build scripts are included. No font binaries are distributed. Different line/page breaks between Word and PDF are expected.

To rebuild the collected PDF after typesetting the component PDFs, run `python code/build_collection.py --root .`. Its contents ranges are derived from the actual component PDFs.
