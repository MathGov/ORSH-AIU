"""Add a neutral comparator: internal dynamics local in an independent third brickwork frame W (W H_S W^dagger).
Claude, 26 September 2026. Exploratory, post hoc."""
import json, numpy as np
from reimpl_id1 import H_S, U_C
from factorial_id1 import z_arm
n, N = 6, 6000
rng = np.random.default_rng(777)
acc = {k: [] for k in ('injL_dynL', 'injL_dynC', 'injL_dynW', 'injC_dynL', 'injC_dynC', 'injC_dynW')}
for _ in range(N):
    H = H_S(n, rng); UC = U_C(n, rng); W = U_C(n, rng)
    E, VL = np.linalg.eigh(H)
    for inj, Vinj in (('injL', np.eye(2 ** n)), ('injC', UC)):
        for dyn, V in (('dynL', VL), ('dynC', UC @ VL), ('dynW', W @ VL)):
            acc[f'{inj}_{dyn}'].append(z_arm(E, V, n, Vinj, UC)[0])
out = {}
for k, v in acc.items():
    v = np.array(v); se = v.std(ddof=1) / np.sqrt(N); out[k] = [float(v.mean()), float(1.96 * se)]
for inj in ('injL', 'injC'):
    for a, b in (('dynL', 'dynW'), ('dynW', 'dynC')):
        e = np.array(acc[f'{inj}_{a}']) - np.array(acc[f'{inj}_{b}'])
        out[f'{inj}: {a} minus {b}'] = [float(e.mean()), float(1.96 * e.std(ddof=1) / np.sqrt(N)), float((e > 0).mean())]
json.dump(out, open('factorial_neutral.json', 'w'), indent=1)
for k, v in out.items(): print(k, [round(x, 5) for x in v])
