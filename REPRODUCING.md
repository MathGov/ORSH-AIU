# Reproduce and audit the collection

## 1. Obtain a fixed edition

Use the `v1.8-open.1` release assets. `ORSH_AIU_v1_8_Finalized_Complete.zip`
is the unchanged original archive; `ORSH_AIU_v1_8_Open_Publication_1.zip`
is the separately licensed public repository bundle. `Reproduction_v1_8.zip`
contains the curated source/data/code and these instructions. Compare downloads
with the release's `SHA256SUMS.txt` (PowerShell: `Get-FileHash -Algorithm SHA256 FILE`;
Linux: `sha256sum FILE`). Extract into a new directory.

The normal checkout intentionally omits bulky historical bundles and review
correspondence. `provenance/source-inventory.json` lists every retained and
archive-only file. Original archive checks must run on the **complete** archive,
not the curated `publication/` subset.

## 2. Install an isolated numerical environment

Use Python 3.13 (the original snapshot used 3.13.5). A local publication check
also uses Python 3.12; exact local versions are recorded in the new receipt.

```sh
python -m venv .venv
# Linux/macOS
. .venv/bin/activate
# Windows PowerShell, instead:
# .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-numerics.txt
```

Set `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1` and `PYTHONUTF8=1` before
running. On PowerShell use `$env:OPENBLAS_NUM_THREADS='1'` and likewise for
the other two names. Run all commands below from the repository/bundle root.

## 3. Fast, scoped checks

```sh
python scripts/verify_publication.py
python scripts/check_numerics.py
```

The numerical check recomputes the factorial analysis from retained arrays and
compares all output fields; it also runs selected four- and six-qubit propagation
checks using exponential action and density matrices. It writes fresh outputs
to a temporary directory, preserving the published research files. The numerical
check is not a replay of every original trajectory or external replication.

## 4. Full pilot and reviewer replay

Choose output directories that do not already contain results.

```sh
python publication/code/run_injection_pilot.py --config publication/pilot/config.json --out fresh-pilot
python publication/code/replay_reviewer.py --root publication --out fresh-reviewer --task all
```

The full reviewer replay can take many minutes or substantially longer on slower
machines. Inspect `fresh-reviewer/comparisons.json`: every `match` must be true.
Its comparison uses `rtol=1e-8`, `atol=1e-10`; a completed process alone is not
proof of agreement. The manually dispatched **Full research replay** workflow
performs these runs and asserts agreement. It is separate from pull-request CI.

## 5. Complete original package and document checks

Extract the original archive to a separate directory. Install Pandoc **3.1.11.1**
and the dependencies in `requirements-site.txt` (including `lxml` and
`python-docx`). With that directory as ROOT:

```sh
python ROOT/code/verify_release.py --root ROOT --report original-structure.json
```

The original `verify_archive.py` uses platform-native path separators; its
unlisted-file comparison is Linux-oriented. The maintained verifier's
`--archive PATH.zip` option performs a portable complete ZIP/hash audit:

```sh
python scripts/verify_publication.py --archive ORSH_AIU_v1_8_Finalized_Complete.zip
```

PDFs are preserved from the source package's **Pandoc + XeLaTeX** build, not
the older LibreOffice process mentioned in `publication/code/README.md`.
Full PDF rebuilding requires TeX Live and the fonts recorded in
`publication/verification/environment.json`; byte-identical rebuilt PDFs are
not promised. DOCX files contain native Word math. Rebuild only in a working copy.

## 6. Build the accessible reading site

Install Pandoc 3.1.11.1, Python dependencies and Node 22.12 or later:

```sh
python -m pip install -r requirements-site.txt
npm ci
python scripts/build_site.py
python scripts/check_site.py
npx playwright install chromium
npm test
python -m http.server 4173 --directory _site
```

The site uses locally bundled KaTeX, local full-text search, no analytics and no
account requirement. Generated `_site/` is deployed by GitHub Pages Actions.
