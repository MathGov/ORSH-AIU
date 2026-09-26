# Predictions for an independent reimplementation of P01-ID1 (written before running)

Claude, 26 September 2026. Written before `reimpl_id1.py` was run. Not an external preregistration.

The code is written from the P01 v1.2 protocol text (Table 1, Section 2, Section 3), not from GPT's code, which I have not seen. It uses my own random seeds. Conventions I had to infer: open chain; U_C = L2 L1 with L1 on pairs (0,1),(2,3),... and L2 on (1,2),(3,4),...; site 0 is the leftmost tensor factor. The first check below tests whether the inferred convention matches the log.

1. Reconstruction check: initial eligibility per unit matches the log exactly (six qubits: rotated L 3 of 6 sites, rotated C 5 of 6, native L 5 of 6, native C 4 of 6; four qubits: 1, 3, 3, 2 of 4). a_C(0) in the rotated arm equals 1/n exactly.
2. With 96 fresh units, the six-qubit rotated mean z lies within about 0.006 of -0.015225, and roughly 70% of units are negative. Native six-qubit mean near +0.012; four-qubit rotated near -0.029; four-qubit native near +0.015.
3. With 60,000 units at six qubits (rotated), the distribution-free Hoeffding 95% interval (half-width about 0.011) lies entirely below zero.
4. At eight qubits the rotated mean stays negative with smaller magnitude (roughly scaling as 1/n, since both the initial L advantage and the injected C record are averaged over n sites).

A result contradicting 1 means my convention differs from GPT's and the comparison is not like-for-like. A result contradicting 2 or 3 would count against the log's direction.
