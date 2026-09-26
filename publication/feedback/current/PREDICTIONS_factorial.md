# Predictions for the 2x2 factorial control (written before running)

Claude, 26 September 2026. Added after seeing the reimplementation results, before running this script.

Design: same units as the pilot law (n = 6), four arms per unit: injection frame in {L, C} crossed with the frame in which the internal Hamiltonian is local, {L (H_S), C (U_C H_S U_C^dagger)}. Readout in L and C as in the pilot; z defined exactly as in the pilot.

Reasoning: conjugating a whole configuration by U_C^dagger swaps the roles of the two frames, so the two new arms should approximately mirror the pilot arms with the sign of z reversed.

Predictions:
1. z(inject L, dynamics local in C) is about +0.014; z(inject C, dynamics local in C) is about -0.014.
2. The locality effect, z(dynamics local in L) minus z(dynamics local in C) at fixed injection frame, is near zero (absolute value below 0.002) for both injection frames.
3. Hence the sign of z in the pilot is set by the injection frame, not by which frame the internal dynamics is local in.
A locality effect of the same size as the pilot's primary mean (about 0.014) would contradict this and support the pilot's reading.
