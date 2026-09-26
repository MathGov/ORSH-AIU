# ORSH/AIU v1.6.1: are the papers complete and ready?

Claude, 26 September 2026. AI review, not peer review. **Evidence** means I checked or computed it this session. **Inference** means it is my reasoning.

## Bottom line

The internal work is finished. Every issue I raised last round was fixed, every number I could recompute matches, and the Word and Markdown copies are identical in substance. For the first time the programme also has an executed, logged study.

None of the papers is ready to submit yet. C and W04 are still written as internal portfolio documents: they cite version histories, AI audits, internal file paths and codes like W02 and REFUSE_DETERMINISTIC_SELECTION that no outside reader can follow. The one step that has been deferred three times is a human specialist reading C. That is now the gating item, not more revision.

| Document | Internally complete? | Ready for | Not yet ready for | What is left |
|---|---|---|---|---|
| C v0.3.1 | Yes | A human quantum-information specialist, now | Preprint or journal | An external edition (section 5 below) |
| SI v1.0.1 | Yes, for its purpose | Accompanying C | Standalone use | Nothing substantive. Its code was not attached, so I did not rerun it. |
| P01-ID1 log v1.0 | Yes | Internal record; can go to the specialist with C | Publication as a result | Three small additions (section 4) |
| W04 v1.2.1 | Yes; the sources are now primary | A philosopher's read, now | Preprint or journal | An external edition (section 6) |

## 1. Were last round's issues fixed?

**Evidence.** Yes, all of them:

- **Proposition 7 threshold.** C now states that the bound is trivial through n = 18, reaches log10 ≈ -56.85 at n = 19, is trivial through n = 10 without a search cover, and that Proposition 3 gives 0.525 at n = 4 and 0.269 at n = 6.
- **Mixed-twirl provenance.** Both samples (2,000 draws in v1.5 and 1,200 in CAL-1.6) are now in Appendix C, Appendix A and SI S7. The CAL-1.6 mean, 0.05550839, sits 0.53 standard errors from the exact 0.056, which is consistent.
- **Appendix A** now maps the v1.6 numbers.
- **Section 10** no longer presents W03 as the active record.
- **Paz and Zurek (1999) and Riedel, Zurek and Zwolak (2012)** are cited in the new section 7.1.1.
- **W04 Table 6 and R36.** Table 6 is rewritten from the four primary texts, and R36 is gone.
- **Consistency checks.**
  - Prose parity between the Markdown and Word copies of all four documents is 0.998 or higher; the only differences are titles.
  - Equations match one to one: 691 in C, 22 in W04, 7 in the log and 3 in the SI.
  - Figure counts match.
  - There are no em or en dashes.

## 2. Where GPT corrected me again

My last assessment said persistence "needs a large or dissipative environment". That was too broad, and I accept the correction.

- A closed system whose Hamiltonian is diagonal keeps orthogonal product records forever, because they commute with it.
- Amplitude damping, an open system, erases records.

The accurate statement is now in C section 7.1.1: persistence needs a stated retention mechanism, and openness is neither necessary nor sufficient. What survives from my point is narrower. In small closed systems with non-commuting dynamics, whether a record exists depends heavily on the chosen time window.

## 3. What the pilot actually found

P01-ID1 is the first executed study in six versions, and the log is honest and careful.

**Evidence.** I recomputed and confirmed:

- the Hoeffding interval [-0.292446, 0.261996];
- the arithmetic in section 3.1 (the gap falls from 0.041741 to 0.011291, and half of that change is -0.015225);
- the transport controls: sin²t in the two-site case, 0.972655 at t = 2.80 for n = 4, and 0.911536 at t = 3.95 for n = 6.

**Inference.** Taken together, the two arms show the pattern that local dynamics predicts.

- When the source bit enters in the internal frame (native arm), the internal dynamics keeps it more readable in that frame.
- When it enters in the other frame (rotated arm), the internal dynamics does not gather it into the internal frame.

In plain terms, local dynamics preserves locality that already exists but does not create it. This matches my earlier probe, which used a different design and also found no internal-frame advantage.

Two small closed-system studies, designed differently, now point the same way against the proposed mechanism by which a system's own dynamics would select its record frame (the LRA-int mechanism). This is not a refutation: both studies involve at most 6 qubits and closed dynamics, and both were designed and run by AI.

## 4. Three additions the pilot log needs

**4.1 The direction is stronger than the log reports.**

- **Evidence.** An exact two-sided sign test on the counts in Table 1 gives:
  - p = 5.5 × 10^-5 for the primary row (28 positive, 68 negative);
  - p = 4.5 × 10^-10 for the 4-qubit rotated arm;
  - p = 6.8 × 10^-4 and 0.010 for the native arms.
- **Why it matters.** The sign test needs no distributional assumptions, only independent units. It shows that most units move in the stated direction.
- **What stays open.** The mean is still unresolved, as the log correctly says.
- **How to report it.** Add it as a secondary result, clearly labelled as computed after the run. As written, "the Hoeffding interval crosses zero" under-reports a clear directional finding.

**4.2 The primary analysis could not detect effects this small.**

- A Hoeffding half-width of 0.015 on a variable in [-1, 1] would need about 32,800 units. At N = 96 the half-width is ±0.28.
- The pre-execution plan should have said this.
- Future pilots should state the smallest detectable effect before running.

**4.3 The strict-record windows ended before transport arrives.**

- The declared windows run from t = 0.5 to t = 2.5.
- In the log's own clean exchange-chain controls, the end-site probability stays above the 0.8 threshold only on t ≈ 2.4 to 3.2 (n = 4) and t ≈ 3.6 to 4.3 (n = 6), on my 0.05 grid.
- So even in the ideal chain, the windows could not have registered a record carried by transport.
- The random anisotropic chains will have different timescales, so this is a flag, not a proof. Still, the zero count of strict records is at least partly a floor built into the design, and the log should say so.

One more point: the log mentions a pre-execution plan and receipt, and C and the SI cite P01 v1.2, but none of these were in this set. So I cannot verify the predeclaration myself.

## 5. C: what the external edition needs

The mathematics I checked is correct, so these are packaging and reporting issues, not errors.

1. **Remove the portfolio apparatus.**
   - C still contains 10 references to W01 to W05, 10 to P01, 10 uses of "audit", 12 version strings, 4 mentions of CAL-1.6, and the names Claude, ChatGPT and Genspark.
   - The title page has Purpose, Results status and Maintenance boundary blocks.
   - A referee cannot use any of this. Replace it with standard Data and Code Availability and AI-use statements, move the Appendix A file paths into the SI, and cut sections 10 and 11 down to one paragraph.
2. **Report the pilot's direction in one paragraph.** C now says the pilot "is not retrofitted", which is right for LRA-count. But a paper whose motivating conjecture has since been probed, without saying which way the probe went, reads as selective reporting. State the direction and the sign test, labelled exploratory.
3. **Tighten one phrase in section 7.1.1.** Paz and Zurek's energy-eigenstate regime is where the system's own Hamiltonian dominates the coupling. "Weak-environment regime" is loose.
4. **Complete the author metadata:** affiliation, ORCID, funding and competing interests.
5. **Choose a venue before trimming.**
   - **Inference.** The paper itself concedes that items 1 to 3 may be judged elementary, and Proposition 7 is a standard concentration-plus-net argument.
   - Its strongest parts are the methods safeguards (section 7.3.1, the permutation counterexamples) and, if it is added, the negative pilot direction. That fits a foundations or methods venue better than a journal that demands new quantum-information theorems. The specialist reader is the right person to confirm this.

## 6. W04: what the external edition needs

**Evidence.**

- **Primary sources.** Table 6 now rests on primary texts. Kastrup's article (JCS 25(5-6)) and Albahari's (Philosophers' Imprint 19(44)) exist as cited.
- **Miller's pages.** The publisher's table of contents confirms pages 112 to 125, so GPT was right that PhilPapers' "112-115" is wrong.
- **Miller's issue number.** One small point is unresolved. PhilPapers lists the issue as 28(3-4), but the publisher's contents page title reportedly reads "No. 2-4". Check the header on the article's first page.

Remaining work:

1. **Remove the internal vocabulary.**
   - It covers W01 to W05, "C v0.3.1", ORSH, the editorial/SOURCE_REGISTER.json path and the maintenance note.
   - Rewrite the section 12 paragraph containing "REFUSE_DETERMINISTIC_SELECTION" for outside readers, or remove it.
   - Section 14's paragraph on AI sessions and the archived W05 is programme management, not philosophy.
2. **Renumber the references.** They start at R09 and have gaps (no R01 to R08, R12 to R14, R19, R22, R24, R29 or R36).
3. **Resolve R31.** Ellis and Brundrit (1979) is still marked "lead from the supplied audit; not verified". It is the last AI-mediated source in the paper. Its bibliographic record exists (Semantic Scholar), and the full text should be free on ADS: verify it or drop it.
4. **Add a short contribution statement.** A referee will ask what is new. My reading (inference):
   - the seven-way decomposition of the claim (T, M, U, G, P, C, C*);
   - the table of bridges between them;
   - the componentwise plenitude criterion;
   - the finite-window underdetermination result;
   - the primary-source comparison of subject accounts.

   Say that in one paragraph near the start.
5. **Venue (inference).** The interlocutors (Kastrup, Miller) publish in the Journal of Consciousness Studies, which makes it a natural first target. Alternatively, post a PhilArchive preprint first.

## 7. What "done" looks like

- **Stop now:** no further internal revision rounds between AI systems. The work has converged. Additional rounds are producing wording changes, not findings.
- **Next, in order:**
  1. Send C v0.3.1, the SI and the pilot log to one human researcher in quantum Darwinism or quantum mereology. Use GPT's specialist brief, adding the two pilot directions.
  2. Make external editions of C and W04 (sections 5 and 6): a mechanical edit, not a rethink.
  3. Add the three pilot-log items in section 4.
- **Ready means:** after steps 2 and 3, W04 can go to a philosopher or PhilArchive. C should wait for the specialist's reply before a preprint, because a correct but elementary paper is better revised once on expert advice than posted and then withdrawn.

## Sources

- [Riedel, Zurek and Zwolak 2012, arXiv:1205.3197](https://arxiv.org/abs/1205.3197)
- [Paz and Zurek 1999, PRL 82, 5181](https://link.aps.org/doi/10.1103/PhysRevLett.82.5181)
- [JCS Vol. 28 table of contents, Imprint Academic](https://www.imprint.co.uk/table-of-contents-jcs-vol-28-no-2-4-march-april-2021/)
- [Miller (2021), PhilPapers record](https://philpapers.org/rec/MILTDP-5)
- [Kastrup (2018), Ingenta Connect record](https://www.ingentaconnect.com/contentone/imp/jcs/2018/00000025/f0020005/art00006)
- [Ellis and Brundrit (1979), Semantic Scholar record](https://www.semanticscholar.org/paper/Life-in-the-Infinite-Universe-Ellis-Brundrit/76bdbf3cccafd9cf6f744dbc89cfed2141502419)
- Uploaded v1.6.1 files: C v0.3.1, SI v1.0.1, W04 v1.2.1, P01-ID1 log v1.0 (Markdown and Word).
