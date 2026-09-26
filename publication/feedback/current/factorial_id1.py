"""2x2 factorial control for the P01-ID1 readability contrast: injection frame x dynamics-locality frame.
Claude, 26 September 2026. Uses reimpl_id1 conventions. Paired: all four arms share H_S and U_C per unit."""
import json, time, numpy as np
from reimpl_id1 import H_S, U_C, bloch, TS

def z_arm(E, V, n, Vinj, UC):
    base = np.zeros(2 ** n, complex); base[0] = 1
    flip = np.zeros(2 ** n, complex); flip[2 ** (n - 1)] = 1
    d = {}
    for frame, D in (('L', np.eye(2 ** n)), ('C', UC)):
        r = []
        for s in (-1, 1):
            psi0 = Vinj @ ((base + s * 1j * flip) / np.sqrt(2))
            c = V.conj().T @ psi0
            Psi = np.vstack([psi0[None, :], (V @ (np.exp(-1j * np.outer(E, TS)) * c[:, None])).T])
            r.append(bloch(Psi @ D.conj(), n))
        d[frame] = 0.5 * np.linalg.norm(r[0] - r[1], axis=2)
    aL = d['L'].mean(1); aC = d['C'].mean(1)
    return 0.5 * ((aL[1:] - aC[1:]).mean() - (aL[0] - aC[0])), aL, aC

def run(n, N, seed):
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(N):
        H = H_S(n, rng); UC = U_C(n, rng)
        EL, VL = np.linalg.eigh(H)           # local in L
        EC, VC = EL, UC @ VL                  # U_C H U_C^dagger: same spectrum, rotated eigenvectors (local in C)
        row = {}
        for inj, Vinj in (('injL', np.eye(2 ** n)), ('injC', UC)):
            for dyn, (E, V) in (('dynL', (EL, VL)), ('dynC', (EC, VC))):
                z, aL, aC = z_arm(E, V, n, Vinj, UC)
                row[f'{inj}_{dyn}'] = float(z)
                row[f'{inj}_{dyn}_aL'] = [float(aL[0]), float(aL[1:].mean())]
                row[f'{inj}_{dyn}_aC'] = [float(aC[0]), float(aC[1:].mean())]
        rows.append(row)
    return rows

if __name__ == '__main__':
    t0 = time.time()
    out = {}
    for n, N in ((6, 20000), (4, 20000), (8, 1000)):
        rows = run(n, N, 4242 + n)
        s = {}
        for k in ('injL_dynL', 'injC_dynL', 'injL_dynC', 'injC_dynC'):
            z = np.array([r[k] for r in rows]); se = z.std(ddof=1) / np.sqrt(len(z))
            s[k] = dict(mean=float(z.mean()), ci95=[float(z.mean() - 1.96 * se), float(z.mean() + 1.96 * se)],
                        aL=[float(np.mean([r[k + '_aL'][i] for r in rows])) for i in (0, 1)],
                        aC=[float(np.mean([r[k + '_aC'][i] for r in rows])) for i in (0, 1)])
        for inj in ('injL', 'injC'):
            eff = np.array([r[f'{inj}_dynL'] - r[f'{inj}_dynC'] for r in rows]); se = eff.std(ddof=1) / np.sqrt(len(eff))
            h = np.sqrt(2 * np.log(40) / len(eff)) * 2  # locality-effect variable ranges over [-2, 2]
            s[f'locality_effect_{inj}'] = dict(mean=float(eff.mean()), ci95=[float(eff.mean() - 1.96 * se), float(eff.mean() + 1.96 * se)],
                                              frac_positive=float((eff > 0).mean()))
        out[f'n{n}_N{N}'] = s
        print(f'n={n} N={N} done {time.time()-t0:.0f}s'); print(json.dumps(s, indent=1))
    json.dump(out, open('factorial_results.json', 'w'), indent=1)
