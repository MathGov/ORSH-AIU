# Reproduction and build tools

The numerical core uses the versions in requirements.txt; the environment actually used is recorded in verification/v17_environment.json. Compatibility with every platform is not asserted.

Run commands from the extracted release root. Choose fresh output directories. The original pilot solver, configuration and pre-execution plan retain their original hashes. No network, account, email or private-service access is required by the calculations.

- run_injection_pilot.py reproduces the original finite pilot, not a new experiment.
- validate_injection_pilot.py checks selected trajectories by another propagation/reduction method. It writes its report into the working copy; use a separate copy.
- analyze_review_additions.py performs the disclosed post hoc sign, precision, encoding and eligibility analyses. It refuses a nonempty output directory.
- check_v17_additions.py uses exact rational sign sums and full-space encoding controls; no import of the main secondary-analysis script.
- verify_release.py checks canonical hashes, ordered Word content, equation counts and manifest files. Its checks do not certify scientific truth or rendered equations.
- build_documents.py converts a specified canonical Markdown source with pandoc and styles the DOCX with python-docx. It requires python-docx and lxml, and the pandoc executable. Image paths are resolved relative to each manuscript.
- plot_pilot.py reproduces the original three pilot figures; it is not a new analysis.

The release PDFs were rendered from the final DOCX files with LibreOffice, not independently typeset from a competing text. Document conversion additionally uses PyMuPDF for diagnostics. A reproducer should install suitable fonts locally; no font files are distributed. Word application rendering and PDF/UA conformance are not certified.

Examples:

```text
python code/run_injection_pilot.py --config pilot/config.json --out /path/to/fresh_pilot
python code/analyze_review_additions.py --root . --out /path/to/fresh_secondary
python code/check_v17_additions.py --root .
python code/verify_release.py --root . --report /path/to/fresh_verification.json
python code/build_documents.py manuscripts/Frame_Aligned_Records_v0_4.md
libreoffice -env:UserInstallation=file:///tmp/orsh_local_profile --headless --convert-to pdf --outdir /path/to/pdf_output manuscripts/Frame_Aligned_Records_v0_4.docx
```

Limit BLAS threads for repeatable small-matrix timing. Rebuilding a document can change archive metadata and hashes; perform all rebuilds in a separate copy and regenerate its manifest. The retained historical scripts preserve their original configuration limitations and are not advertised as a single modern production package.
