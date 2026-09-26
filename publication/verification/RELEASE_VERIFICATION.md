# Release verification: v1.8 finalized build

26 September 2026. Portfolio and manuscript version labels are unchanged. The finalized build is distinguished by its content manifest and the finalization change record. This report states the checks performed in this finalization, separately from inherited execution claims.

## Preservation and change scope

The input v1.8 ZIP passed its original 338-file manifest before editing. The five original MD/DOCX/PDF pairs, collected PDF and prior release records are preserved under `historical/v1_8_before_finalization`. Before/after source hashes and a unified text diff are in `editorial/`.

All 39 baseline data files, 26 figure files, 15 existing code files, 135 historical files and 22 feedback files remain byte-identical. All three original pre-execution hash entries are unchanged. The added collection-build helper changes document production only. No numerical result, sample, source pulse, threshold, pre-outcome specification or statistical conclusion was changed.

## Fresh executable checks

| Check | Result | Scope |
| --- | --- | --- |
| Original source-off pilot replay in empty directory | 7/7 numerical/configuration files byte-identical | Environment report differs as expected; not a numerical mismatch |
| Separate pilot implementation | 36 passed; 0 failed | Selected trajectory and analytic controls, not external replication |
| Separate factorial implementation | 32 passed; 0 failed | Selected trajectories and paired calculations, not a new full population run |
| Factorial analysis replay | 3/3 outputs byte-identical | Reanalysis of delivered per-unit outcomes |
| Original pre-execution hashes | 3/3 unchanged | Integrity, not an independent timestamp or preregistration |

The full 60,000-unit reimplementation and all large factorial population runs were not rerun again during this limited finalization. Their original v1.8 outputs, code, input seeds and recorded replay checks remain unchanged and available. This distinction prevents inherited evidence from being advertised as another new experiment.

## Reader and production checks

| Check | Result |
| --- | --- |
| Canonical sources matching their build records | 5/5 |
| Ordered converted content blocks matching delivered Word files | 1169 |
| Markdown math objects / native Word equations | 811/811 |
| Referenced Word styles undefined | 0 |
| Tables with explicit borders | 26/26 |
| Embedded figures in the five readers | 12 |
| Current Markdown figure paths resolved | 12/12 |
| Genuine OOXML ZIP signatures and readable Word contents | 5/5 |
| Collected PDF page images visually inspected | 66/66 |
| DOCX-render page images visually inspected | 67/67 |
| Fonts listed by pdffonts in the collected PDF | All embedded |

Raw UTF-8 inspection confirms Brandão, Rényi, Zanghì, naïve and TeX probability/Greek notation. No new encoding loss was found. Two actual DOCX-render subscript issues were corrected with equivalent labels, then rechecked. The cover spells out both programme names and gives page ranges derived from the five actual PDFs. The reference ordering in AIU was changed with an explicit identifier crosswalk, not by changing the cited sources.

Delivered PDFs are generated through XeLaTeX from canonical Markdown. DOCX uses editable Office mathematics. LibreOffice was used only to inspect Word rendering; no Microsoft Word application test is claimed. Equation counts and ordered block checks are not a proof of mathematical semantic identity. Visual inspection found no unresolved clipping, missing inline equations or duplicated contribution item on the reviewed pages. Small inherited TeX table-width warnings below 0.13 point are documented in build reports; they were not visible as clipping. No PDF/A, PDF/UA or formal floating-point certification is claimed.

## Archive verification

`MANIFEST_SHA256.json` and `SHA256SUMS.txt` describe this finalized build. The finalized ZIP is tested, extracted into a fresh directory and checked by `code/verify_archive.py` and `code/verify_release.py`; the external delivery receipt records the final archive hash, byte size and exact file/check counts. A manifest does not hash itself; the two manifest files are explicitly excluded from its content inventory.

## Readiness boundary

Complete for technical and philosophical specialist review at the documents' declared scope. Submission declarations, any public persistent deposit, licence selection, venue-specific checks and independent human criticism are not supplied by these checks. No email, deposit or submission was made. Separate Core 15 and Aligners Sheet findings were not audited or changed in this portfolio finalization.
