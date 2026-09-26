# ORSH/AIU v1.7 core files: complete and ready?

Claude, 26 September 2026. AI review, not peer review. **Evidence** means I checked or computed it this session. **Inference** means it is my reasoning. Files reviewed:

- Frame-Aligned Records v0.4
- its Supplement v1.1
- the Post-Injection Results log v1.1
- the P01 v1.2 protocol
- Absolute Infinite Union v1.3
- the v1.7 collected PDF

Each is in both Markdown and Word except the PDF.

## Bottom line

**The editing is essentially finished, but the science needs one correction first.** All five documents are complete, internally consistent and now written for outside readers, and every item from my last review was handled except one small citation check (section 7).

**The correction.** I reimplemented the source-off pilot independently from the protocol text and reproduced it closely (section 3). I then added the control the design lacked, which varies the frame in which the internal dynamics is local. That control reverses the pilot's interpretation.

- **What it shows.** Holding the injection frame fixed, dynamics that is local in the internal frame shifts single-site readability toward that frame, by about +0.011 at six qubits. This is significant in 20,000 paired units.
- **Why the pilot missed it.** The pilot's negative primary mean is produced mainly by which frame the source bit was injected in, not by locality.

C, the results log and AIU section 11.1 currently read the pilot as adverse, so that reading has to change before a specialist sees it.

**Readiness by document:**

| Document | Complete? | Ready for | Not yet ready for | What is left |
|---|---|---|---|---|
| Frame-Aligned Records v0.4 | Yes | A specialist, once the pilot paragraph is corrected | arXiv or a journal | The pilot reinterpretation plus about ten small edits (section 4) |
| Supplement v1.1 | Yes | Going out with C | A journal SI in its present order | Put the scientific sections first and shrink the lineage (section 5) |
| Results log v1.1 and P01 v1.2 | Yes | Internal record | Publication as a finding | Revise the interpretation; add the factorial control (section 6) |
| Absolute Infinite Union v1.3 | Yes | A philosopher's read, now | PhilArchive or a journal | Engage the canonical prior art for its own core claims (section 7) |
| Collected PDF | Yes | Nothing external | Any circulation | Its equations misrender; regenerate it (section 8) |

## 1. What changed, and what I checked (evidence)

**Last round's list is done.**

- **External editions.**
  - C no longer mentions W01 to W05, P01, CAL-1.6 or portfolio versions in its main text.
  - The AIU paper has numbered references [1] to [21], no internal codes, a "Contribution and limits" paragraph, and a new worked comparison (section 10.2.2).
  - The unverified Ellis and Brundrit lead was dropped rather than kept.
- **Pilot results in C.**
  - The abstract and section 6.2 now report the pilot's result.
  - The Holm-adjusted sign tests are correct: 5.4592 × 10⁻⁵ × 3 = 1.638 × 10⁻⁴.
  - The historical three-qubit study moved to Supplement S9 intact: 96% word overlap, with every number preserved.
- **Pilot log.** It adds the sign tests, the precision budget, eligibility and transient-access diagnostics, and the encoding-specific transport windows.
- **Word against Markdown.**
  - Prose parity is 0.998 or higher in all five pairs.
  - The equations match one to one: 581, 29, 14, 21 and 116.
  - The figures match: 6, 2, 3, 0 and 0.
  - There are no em or en dashes.
- **Equations in the Word files.** The delimiters are defined correctly in the Word equation code: [ ], ( ), | ⟩ and ⟨ |.

## 2. GPT corrected me, and I accept it

- **Encoding.** My window warning used the vacuum-versus-excitation code, where distinguishability is |f|². The pilot's actual code is an opposite-phase superposition, where distinguishability is |f|.
  - I checked this independently: under the pilot code, the far-end arrival is above 0.8 on about t = 2.17 to 3.43 (four sites) and 3.32 to 4.52 (six sites).
  - No declared window fits inside either interval, so GPT's corrected statement stands.
- **My earlier reading of the pilot.** Last round I wrote that local dynamics "preserves locality that already exists but does not create it", and that two studies now point against the internal-frame mechanism. Section 3 shows that was over-read. I withdraw it.

## 3. The pilot: independent reimplementation and the missing control

### 3.1 Reimplementation (evidence)

I wrote new code from the P01 v1.2 text alone, without GPT's code, using my own seeds. Where the text was silent I had to infer conventions: an open chain, the circuit written U_C = L2·L1 with the first layer on pairs (0,1), (2,3), and so on, and site 0 as the leftmost qubit.

- **Structural match.** The number of initially uninformative sites per unit matches the log exactly in all eight size, arm and frame cells (for example, 3 of 6 in L and 5 of 6 in C for the six-qubit rotated arm). The injection frame's starting readability is exactly 1/n. This confirms that my inferred conventions are GPT's.
- **Five fresh 96-unit replicates:**

  | Cell | My replicates | Log |
  |---|---|---|
  | 6 qubits, rotated | -0.0138 to -0.0170 | -0.0152 |
  | 6 qubits, native | +0.0099 to +0.0137 | +0.0117 |
  | 4 qubits, rotated | -0.0179 to -0.0284 | -0.0288 |
  | 4 qubits, native | +0.0105 to +0.0217 | +0.0151 |

- **Readability levels.** The starting and post-evolution readability means match the log's 0.208, 0.167, 0.198 and 0.186.
- **60,000 units at six qubits (5.3 minutes).**
  - The rotated mean is -0.01413. Its distribution-free Hoeffding 95% interval, [-0.0252, -0.0030], excludes zero.
  - The native mean is +0.01375, with Hoeffding interval [+0.0027, +0.0248].
  - The log's "precision limitation" therefore costs minutes to remove. Future pilots should simply run enough units for a distribution-free interval.
- **Eight qubits (2,000 units).** Rotated -0.0086, native +0.0113.

All four of my written predictions for this step held.

### 3.2 The control the design lacked (evidence; post hoc; my prediction was wrong)

The pilot varies where the source bit is injected, but the internal dynamics is always local in L. It therefore cannot separate two effects:

- whether readability shifts toward the injection frame;
- whether it shifts toward the frame in which the dynamics is local.

I added the missing factor by giving the same Hamiltonian, the same spectrum and the same units, but rotating the Hamiltonian's locality into C (U_C H U_C†).

**Six qubits, 20,000 paired units** (mean z; 95% half-widths about 0.0003):

| | Dynamics local in L | Dynamics local in C |
|---|---|---|
| Injected in L | +0.0140 | +0.0035 |
| Injected in C | -0.0140 | -0.0267 |

**The locality effect** is z with dynamics local in L minus z with dynamics local in C, at a fixed injection frame:

| Qubits | Units | Injected in L | Injected in C |
|---|---|---|---|
| 4 | 20,000 | +0.0058 (57% of units positive) | +0.0111 (63%) |
| 6 | 20,000 | +0.0105 (71%) | +0.0126 (74%) |
| 8 | 1,000 | +0.0104 (78%) | +0.0121 (79%) |

**A neutral comparator** makes the same point. With the dynamics local in an unrelated third frame (six qubits, 6,000 units), the order for both injection frames is: local in L, then neutral, then local in C.

**My own error.** Before running, I predicted a locality effect near zero, using a symmetry argument. That argument was wrong: the circuit and its inverse spread the edge-injected bit differently. I recorded the prediction before running, and the direct computation overruled it.

**Inference.**

- The pilot's contrast mixes an injection-frame effect (about ±0.02) with a positive locality effect (about +0.011). In the rotated arm the injection effect dominates, which produces the negative mean.
- The quantity that answers the pilot's own question ("does internal evolution shift accessibility toward the internal-locality frame?") is the locality effect. In this family it is positive, grows more consistent with size, and matches ordinary light-cone physics (Lieb and Robinson 1972): local dynamics spreads information slowly in its own frame.
- This concerns average single-site readability, not strict or redundant records. It is expected physics, not new evidence for ORSH.
- **What this means for the documents.**
  - The log's literal result stands.
  - Its inference ("a reason not to assume the proposed recovery direction", in log section 7) does not.
  - Neither does C section 6.3's "adverse or inconclusive", or the AIU paper's section 11.1 wording.

## 4. Frame-Aligned Records v0.4: what is left

**Needed before a specialist reads it:**

1. **Correct the pilot interpretation.** Revise the abstract, section 6.2 and section 6.3 so they:
   - state the injection-frame confound;
   - either add the 2×2 control as a disclosed post hoc analysis or say it is needed;
   - stop presenting the pilot as adverse evidence about locality.

**Before arXiv (small and mechanical):**

2. **Section 7.1.1.** A sentence starts in lowercase ("the source-off pilot is..."), and the internal phrase "Its results reside in a computational log rather than a new paper" should go.
3. **Appendix C.** "The 1,200-draw calibration used 1,200 draws" repeats itself.
4. **Stale cross-references.**
   - Section 2.4 says "Section 6 shows that the choice can reverse a verdict", but that evidence is now Supplement S9.6.
   - Section 5.3's "cells of Section 6" is now Supplement Table S4.
   - Section 1.3, item 6, still points to Section 6 for the toy.
5. **Two contribution lists that disagree.** Section 1.3 has seven items and section 8 has five; neither mentions the certificate safeguard (7.3.1) or the pilot. Merge them into one list.
6. **Section 9 limitations** still mention only the three-qubit toy. Add the pilot's limitations: 4 to 8 qubits, closed dynamics, supplied frames, a readability metric rather than records.
7. **References.** Cao, Carroll and Michalakis (2017) is listed but never cited: cite it in section 7.5 or delete it. The list is also out of alphabetical order (Hemerik sits after Page, and seven entries are appended at the end).
8. **Affiliation.** "MathGov / RippleLogic Research Program" is an author decision. Quant-ph readers expect an institution or "Independent researcher", and a program named after an ethics framework will prompt questions on a physics paper.
9. **Typesetting.** Word equations are acceptable for some venues (Foundations of Physics and Entropy take Word). LaTeX is the norm for arXiv quant-ph and for Quantum. Either way, do not use the LibreOffice PDF (section 8).

**Scientific status (inference).** The mathematics is unchanged since my full check of v0.3, and I found no new errors. The paper remains a correct methods paper whose first results are elementary by its own admission. The corrected pilot, a positive but expected locality effect, is modest. It is still worth reporting because it shows the safeguards doing their job, and it also shows how a missing factor can flip a conclusion.

## 5. Supplement v1.1

- It is complete for its role, and S8 (the numbers crosswalk), S9 (the toy) and S10 (the post hoc analyses) are good.
- Its first seven sections still open with internal lineage: the "supplied post-v1.5 Claude audit" is listed as the first execution layer, followed by CAL-1.6, version-1.6 paths and W03 (seven version strings in total).
- For a journal SI, put S8 to S10 first and condense S1 to S7 into a short provenance appendix. This does not block a specialist read.
- If the factorial control is adopted, add it as S11 with the code.

## 6. Results log v1.1 and P01 v1.2

- **Results log.**
  - It is careful and complete as a log, and every number I could recompute is right.
  - Revise the interpretation (sections 1 and 7) as described in section 3.2, and state the confound.
  - The best follow-up is a declared P01-ID2: a 2×2 design (injection frame by dynamics-locality frame) with the locality effect as the primary estimand, a stated precision target, and enough units for a distribution-free interval. It runs in minutes.
- **P01 v1.2.** It is fine as a preserved protocol. Its header still reads "Maintenance patch v1.6.1" inside the v1.7 set; relabel it or add a note.

## 7. Absolute Infinite Union v1.3

**What is good.**

- The external edition is clean.
- Table 6 rests on primary texts.
- The claim decomposition and bridge tables are the paper's real contribution, and the new contribution paragraph says so.

**The substantive gap.** The paper's three strongest commitments each have a canonical literature that the text never mentions (evidence: a search of the text finds zero occurrences of each name):

- **M and the title itself.** Spinoza's *Ethics*, Part I, Definition 6, defines God as "a being absolutely infinite": one substance with infinitely many attributes. That is the historical source of "Absolute Infinite" alongside Cantor.
- **P, plenitude.**
  - Lovejoy's *The Great Chain of Being* (1936) named "the principle of plenitude".
  - P-modal ("every logically coherent reality is actual") is close to Lewis's modal realism (*On the Plurality of Worlds*, 1986) and Nozick's principle of fecundity (*Philosophical Explanations*, 1981).
  - Tegmark's mathematical universe hypothesis (Foundations of Physics, 2008) is the physics-side version.
- **C\*, cosmopsychism.** Goff's *Consciousness and Fundamental Reality* (2017) and Shani (2015, Philosophical Papers) are the standard references beside Nagasawa and Wager.

A metaphysics referee will raise these first. Engaging them is a real revision (reading plus a few pages), not an edit. Please verify each bibliographic detail before citing; I have given the standard citations from memory, not fresh checks.

**Smaller items.**

- **Section 10.2.2, the worked comparison.** It is correct, but the Bayes factor of one is stipulated by construction: the cosmic subject has no observable consequence in the model. Label it plainly as an illustration of the identification limit (it currently says "schematic") or shorten it.
- **Section 11.1.** Update the pilot sentence per section 3.2.
- **Miller [18].** Confirm the issue number (28(3-4) against the publisher page title's "2-4") on the article's first page.
- **Affiliation.** Same point as for C.

## 8. The collected PDF

The PDF was rendered from Word by LibreOffice, which mishandles the equation delimiters (evidence, pages 5 and 22):

- closing square brackets print as parentheses: "E_z[ρ⊗ρ)" and "{[D):";
- kets print as ")": "|0)";
- operator names such as Tr, Stab, span, min and sgn print as italic letter strings.

The Word files themselves are correct, as the equation code shows. Do not send this PDF to anyone. Export the PDF from Word itself, or typeset C in LaTeX.

## 9. The finish line

1. Correct the pilot interpretation in C, the log and the AIU paper's section 11.1 (section 3.2). If possible, run the 2×2 control as a declared study first; it takes minutes.
2. Send C, the supplement and the log to one quantum-information specialist, with a PDF exported from Word. This step has now been deferred four times.
3. Make the small C edits (section 4, items 2 to 9) and reorder the supplement. That is mechanical work.
4. Revise AIU for the canonical prior art (section 7). After that it is ready for PhilArchive or the Journal of Consciousness Studies.

**Honest status.** After step 1, C is ready for specialist review. After step 3, it is ready for arXiv, preferably after the specialist replies. After step 4, AIU is ready for a preprint. Nothing else is required, and further rounds between AIs beyond these steps would not add value.

## Sources

- Lieb, E. H., and Robinson, D. W. (1972). The finite group velocity of quantum spin systems. Communications in Mathematical Physics 28, 251-257. (Standard reference, cited from memory; verify before use.)
- The v1.7 files listed above.
- The reimplementation and factorial code and outputs in this package.
