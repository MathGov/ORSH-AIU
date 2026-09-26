# P01: source-off information redistribution

## A bounded feasibility pilot, not a recovered geometry

**P01 reader edition v1.3 | 26 September 2026**

**Publication note.** This reader edition updates terminology only. The executed scientific specification and local freeze remain those of protocol v1.2, preserved byte-for-byte in `historical/v1_7_core/protocols/P01_Post_Injection_Pilot_v1_2.md`. Later review-stage factorial controls are not additions to the original pre-execution plan. Their specification, scripts and outcomes are separately supplied.

**Status.** P01-ID1 is executed. Its local pre-execution plan, configuration and hashes are supplied. This is a pre-specified exploratory computational study, not external preregistration, a laboratory experiment or a confirmatory test of the older LRA hypotheses. The outcomes are in the separate results log. The v1.1 protocol and original manuscripts remain unchanged in the historical record.

## 1. The revised question

Once a controlled external source has injected information and has been decoupled, does internal evolution shift average single-site accessibility toward the supplied internal-locality frame, relative to the supplied injection frame and a paired no-evolution control? This question separates the initial source interaction from later redistribution. It does not assume that the preparation imprint disappears or that redundant records must develop.

The previous continuously driven comparison is retained as a control question, not treated as a compulsory primary experiment. For a common initial state, the first derivative of the branch difference depends on $K_0-K_1$, with the common internal Hamiltonian cancelling. That fact does not determine a later winning frame. The primary target below is a different quantity from LRA-count, LRA-int and LRA-tot.

## 2. Complete model specification

**Table 1. Fixed inputs**

| Element | Implementation | Limitation |
| --- | --- | --- |
| System | 4 or 6 qubits, with a supplied nearest-neighbour chain | The graph and tensor-product structure are inputs, not outputs |
| Sampling | 96 independent Hamiltonian/circuit units at each size | Sizes are separate populations; paired conditions are not extra independent units |
| Hamiltonian | Each XX, YY and ZZ bond coefficient is independent normal with variance 1/3; each X,Y,Z field is normal with standard deviation 0.35 | One explicit finite model family, not a distribution for nature |
| Injection frame | A depth-two adjacent-pair circuit with independent Haar two-qubit gates, independent of Hamiltonian coefficients | This circuit family itself uses the supplied chain |
| Preparation | All-zero product state in the chosen injection frame | A deliberately prepared resource, not frame-neutral formlessness |
| Source pulse | Source-conditioned plus/minus one-site X generator, pulse angle pi/4; internal Hamiltonian held off during pulse | A supplied quench intervention; not continuous autonomous source coupling |
| Post-pulse evolution | The same internal Hamiltonian for both branches; all source-dependent terms set to zero | Global distinguishability is preserved, not regenerated |
| Access | Unrestricted measurements on each singleton algebra in the declared frames | Actual implementation costs of nonnative observables are not matched or assessed |
| Readout | 101 diagnostic checkpoints from 0 to 2.5; 50 positive-time primary readouts spaced 0.05 | Primary target is a discrete-time average, not a continuum integral |

Let $V=I$ for the native-injection arm and $V=U_C$ for the rotated arm. Just after the pulse, with site zero addressed,
$$\left| \psi_0(0)\right\rangle=V( \left|0\cdots0\right\rangle-i\left|10\cdots0\right\rangle)/\sqrt2,$$
$$\left| \psi_1(0)\right\rangle=V( \left|0\cdots0\right\rangle+i\left|10\cdots0\right\rangle)/\sqrt2.$$
For $t>0$, both evolve with $e^{-iH_St}$. The matched control uses the same initial states but $H_S=0$. The source bit is external and is not an accessible fragment. The addressed system site contains an injected copy; it is not a newly formed record after switch-off.

Both arms are evaluated in $D_L=I$ and the same alternate $D_C=U_C$. In the rotated arm $D_C$ is the actual injection frame. In the native arm the actual injection frame is $D_L$; the symbol C labels only the paired alternate frame. This clarification prevents a comparator label being mistaken for a physical intervention. The primary analysis uses only the rotated arm at six qubits.

## 3. Primary estimand and baseline

For frame $D$, singleton $j$ and time $t$, let
$$d_{D,j}(t)=\tfrac12\|\rho^D_{j,0}(t)-\rho^D_{j,1}(t)\|_1,\qquad a_D(t)=\frac1n\sum_j d_{D,j}(t).$$
The optimal binary error is $(1-d_{D,j})/2$. Average distinguishing advantage is not the number of strong, redundant records. With $M=50$ predeclared positive-time readouts, define
$$z_i=\frac{1}{2M}\sum_{m=1}^{M}\left[(a_L^{\mathrm{on}}(t_m)-a_C^{\mathrm{on}}(t_m))-(a_L^{\mathrm{off}}(t_m)-a_C^{\mathrm{off}}(t_m))\right].$$
Then $z_i\in[-1,1]$. The control is constant, so it subtracts the initial frame-readability gap. Positive $z_i$ means relative accessibility shifts towards L; negative means the gap shifts in the other direction. A negative value does not imply that C is absolutely better at every time. It can arise because a pre-existing L advantage shrinks.

The primary population is the explicit six-qubit rotated-injection sampling law. Four qubits and native injection are sensitivity/calibration analyses. No units are selected by their records or by the sign of the result. A descriptive mean, win/loss/tie counts, an approximate unit-bootstrap interval, and a conservative Hoeffding interval are reported. Bootstrap intervals are not distribution-free certificates or external confirmation. No hypothesis margin was tuned to the outcome.

## 4. Secondary record and uncertainty contract

New-after-pulse singleton records require initial error at least 0.4999 and final error at most 0.1 throughout one of the four windows [0.5,1.0], [1.0,1.5], [1.5,2.0], [2.0,2.5]. The windows were specified before outcomes. The singleton cap is n. Initial source leakage and pre-existing records are not counted as new.

For each frame and fragment use the smaller of the global and complement-subtracted Lipschitz constants from the methods paper. A maximum grid gap h gives a continuity allowance Kh/2. Upper certificates include a 1e-9 numerical guard; a failed certificate remains unresolved unless a checkpoint proves failure. Lower and upper possible record counts are retained, not replaced by a one-sided count. A guard checked by a second numerical method is not a formally verified floating-point enclosure: continuum classifications remain conditional on that guard. Checkpoint failures far above threshold nevertheless supply useful numerical evidence against the strict window criterion.

These counts answer a different question from the continuous primary readability score. Relaxing the threshold after seeing failure would create another exploratory analysis; it is not part of this run.

## 5. Controls and traceability

**Table 2. Control obligations**

| Control | Required observation |
| --- | --- |
| Common unitary after pulse | Global source-state distinguishability remains one |
| No evolution | Local readability is constant; new-after-pulse count is zero |
| Identical source branches | Zero distinguishing information |
| Common passive conjugation | Same reduced statistics when states, H and access are all transported |
| Exchange-chain calibration | Full-space evolution agrees with the one-excitation hopping model |
| Two-site transport | For the vacuum-versus-excitation control, recipient distinguishability is $\sin^2 t$; for the pilot phase code it is $|\sin t|$ |
| Closed stationary record | Diagonal H preserves orthogonal product records; openness is not necessary |
| Independent numerical method | Selected spectral trajectories agree with exponential action and density-matrix partial traces |

Random streams are generated from SeedSequence(master seed, site count, unit index), with separate child streams for H and circuit gates. Coefficients, per-unit identifiers, effective configuration, raw readability trajectories and execution environment are retained. The local pre-execution receipt records code and specification hashes but is not an independently timestamped registration service. No external specialist has reviewed the pilot.

## 6. Stop rule and possible open-system successor

Run the declared sample once, then inspect it. A fresh identical-seed run is reproduction, not another experiment. No coefficient, threshold, time window or sample size is changed to obtain a favourable answer. Implementation corrections, if necessary, must be logged separately.

Do not proceed directly to a larger frame contest. First decide whether the target is transport, retention, redundancy or identifying a structure from observations. Those are distinct. A future open-system study would use a source-off Lindblad or collision-model stage, with dissipator operators, reservoir state, temperature assumptions, clock and access all listed as supplied primitives. Include an erasure control with a unique attractive stationary state and a known record-preserving control. Multiple invariant or metastable sectors must be specified rather than assumed from the word dissipation. This successor is NOT EXECUTED and is not activated merely because the closed pilot lacks strong records.

The next physical identification question would require a response family from multiple independently declared injections, a method that is not given the target frame, and held-out recovery tests. The present two-frame comparison supplies none of those by itself. It is a feasibility result, not hidden metric reconstruction.

## 7. Evidence boundary

This protocol is now instantiated by P01-ID1. Its law, primary observable and raw finite outputs can be checked. Its supplied locality, prepared resource, small size and access assumptions prevent any result from establishing the relational-substrate hypothesis, Absolute Infinite Union, global infinity or subject individuation. The mathematical methods paper and the philosophical paper retain their separate evidential standards.
