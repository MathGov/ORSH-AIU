# P01-ID1: injection, source removal and redistribution

Specification recorded before generating pilot outcomes. This is a computational feasibility study, not external preregistration, independent peer review, or an experiment on fundamental spacetime. The seed is an arbitrary integer, not a date/time attestation.

## Question
After a one-site binary signal is injected, does subsequent internal evolution shift average single-site readability toward the supplied internal-locality frame, compared with the supplied injection frame and a paired zero-evolution control? This differs from the old persistent count-contrast hypothesis. It tests redistribution, not recovery of an unknown tensor-product structure.

## Inputs and sampling
For each of 4 and 6 sites, generate 96 independent units. A unit contains independently sampled nearest-neighbour Hamiltonian coefficients and a depth-two adjacent-pair Haar-gate circuit U_C. Each bond has independent XX, YY and ZZ coefficients distributed N(0,1/3); each site has independent X,Y,Z fields distributed N(0,0.35^2). No size-dependent Frobenius renormalization is applied. These units are independent within each size, while arms, frames, fragments and times within a unit are paired, not independent observations. Hbar=1. Time is in the inverse coefficient scale. The adjacency graph, all site algebras, readout abilities, controls and clocks are supplied.

Two paired injection arms use U=I and U=U_C. The common pre-pulse state is U|0...0>. The internal Hamiltonian is held off during a pulse of angle pi/4 under source-conditioned generators plus/minus U X_0 U-dagger. The resulting states are orthogonal. At switch-off t=0, the source coupling is removed entirely. Both branches then evolve under the SAME internal H. A matched control instead evolves both states under H=0. This quench is a supplied intervention, not a derived law.

## Primary target
The rotated-injection arm at 6 sites is primary. Four sites is a size sensitivity check, not a pool of extra independent confirmation. Let d_F(t)=||rho_F,0(t)-rho_F,1(t)||_1/2 and a_D(t) be its mean over single sites in frame D. Use exactly 50 post-pulse readouts at t=0.05,0.10,...,2.50. Define z_i as half the mean of [(a_L^on-a_C^on)-(a_L^off-a_C^off)]. This lies in [-1,1]. Positive means relative readability shifts towards L. Negative means the reverse. Zero need not mean absence of propagation. Report its mean, observed range, a distribution-free Hoeffding interval and an explicitly approximate paired unit-bootstrap interval. No imposed expectation of a positive answer. This checkpoint-average is not a certified continuum time integral.

## Secondary outputs
Retain full per-site readability at 101 checkpoints. Count new-after-pulse fragments only when initial error is at least 0.4999. For each declared half-unit window report guaranteed-under-the-numerical-guard lower counts and possible upper counts using endpoint-inclusive grids and the smaller of the global and complement-subtracted continuity constants. Do NOT equate failure of the upper certificate with absence. The numerical guard is independently checked empirically; it is NOT a formally proved floating-point enclosure. Claims involving these counts are conditional on that guard and are not strict interval-arithmetic certification. Also report raw checkpoint-passing counts with that label.

## Controls
1. Orthogonality and global distinguishability must remain one after source removal under common unitary dynamics.
2. No evolution must yield exactly constant reduced information and zero new-after-pulse records.
3. Identical source branches must give no information in every frame.
4. Passive common conjugation of H, states and frame access must leave scores unchanged.
5. A two-site exchange Hamiltonian must transfer an excitation as sin^2(t); a longer number-conserving chain must match its one-excitation reduction.
6. A closed diagonal Hamiltonian with two orthogonal stationary product records must retain them indefinitely. Thus open systems are not necessary for every persistent record.
7. Compare selected general-model trajectories against independently applied scipy expm_multiply, not only the spectral solver.

## Predictions and decision rule
Global conservation, frozen-control constancy and the analytic controls are exact mathematical expectations. For generic interacting systems, local signal may redistribute or become accessible only jointly. No sign is assumed for the primary target. Success of a transfer control is not a discovery; no strong singleton redundancy is predicted for a number-conserving single-excitation control. Do not activate an open-system study automatically: consider it only after stating whether the next target is retention, transport, redundancy or identifiability and declaring the dissipator's own preferred structure. A shared channel with a unique attractive fixed state can erase branch information.

No outcomes are used to change coefficients, sample size, primary times or thresholds. Implementation defects may be corrected, but the defect and rerun must be logged and the configuration left intact. A second execution of the same seed tests reproduction, not independent confirmation.
