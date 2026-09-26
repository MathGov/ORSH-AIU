"""Independent reimplementation of the P01-ID1 source-off pilot from the P01 v1.2 protocol text.

Claude, 26 September 2026. Not GPT's code. Own seeds. Conventions inferred where the text is silent:
open chain; U_C = L2 @ L1 (L1 pairs (0,1),(2,3),...; L2 pairs (1,2),(3,4),...); site 0 leftmost.
Usage: python3 reimpl_id1.py
"""
import json, sys, time
import numpy as np

X = np.array([[0, 1], [1, 0]], complex); Y = np.array([[0, -1j], [1j, 0]]); Z = np.diag([1., -1.]).astype(complex)
I2 = np.eye(2)

def op(ops, n):
    """ops: dict site->2x2; returns full operator, site 0 leftmost."""
    out = np.array([[1.]], complex)
    for k in range(n):
        out = np.kron(out, ops.get(k, I2))
    return out

_cache = {}
def paulis(n):
    if n not in _cache:
        P = {'X': X, 'Y': Y, 'Z': Z}
        bonds = {(j, a): op({j: P[a], j + 1: P[a]}, n) for j in range(n - 1) for a in 'XYZ'}
        fields = {(j, a): op({j: P[a]}, n) for j in range(n) for a in 'XYZ'}
        _cache[n] = (bonds, fields)
    return _cache[n]

def haar(k, rng):
    A = (rng.normal(size=(k, k)) + 1j * rng.normal(size=(k, k))) / np.sqrt(2)
    Q, R = np.linalg.qr(A)
    return Q * (np.diag(R) / abs(np.diag(R)))

def two_site(g, a, n):
    return np.kron(np.kron(np.eye(2 ** a), g), np.eye(2 ** (n - a - 2)))

def U_C(n, rng):
    L1 = np.eye(2 ** n, dtype=complex)
    for a in range(0, n - 1, 2):
        L1 = two_site(haar(4, rng), a, n) @ L1
    L2 = np.eye(2 ** n, dtype=complex)
    for a in range(1, n - 1, 2):
        L2 = two_site(haar(4, rng), a, n) @ L2
    return L2 @ L1

def H_S(n, rng):
    bonds, fields = paulis(n)
    H = np.zeros((2 ** n, 2 ** n), complex)
    for key, M in bonds.items():
        H += rng.normal(0, np.sqrt(1 / 3)) * M
    for key, M in fields.items():
        H += rng.normal(0, 0.35) * M
    return H

def bloch(Phi, n):
    """Phi: (T, 2^n) states. Returns (T, n, 3) Bloch vectors."""
    T = Phi.shape[0]
    out = np.empty((T, n, 3))
    for j in range(n):
        R = Phi.reshape(T, 2 ** j, 2, 2 ** (n - j - 1))
        a, b = R[:, :, 0, :], R[:, :, 1, :]
        ab = np.einsum('tik,tik->t', a.conj(), b)
        out[:, j, 0] = 2 * ab.real
        out[:, j, 1] = 2 * ab.imag
        out[:, j, 2] = np.einsum('tik,tik->t', a.conj(), a).real - np.einsum('tik,tik->t', b.conj(), b).real
    return out

TS = 0.05 * np.arange(1, 51)

def unit(n, rng):
    H = H_S(n, rng); UC = U_C(n, rng)
    E, V = np.linalg.eigh(H)
    base = np.zeros(2 ** n, complex); base[0] = 1
    flip = np.zeros(2 ** n, complex); flip[2 ** (n - 1)] = 1
    res = {}
    for arm, Vinj in (('native', np.eye(2 ** n)), ('rotated', UC)):
        d = {}
        for frame, D in (('L', np.eye(2 ** n)), ('C', UC)):
            r = []
            for s in (-1, +1):
                psi0 = Vinj @ ((base + s * 1j * flip) / np.sqrt(2))
                c = V.conj().T @ psi0
                Psi = np.vstack([psi0[None, :], (V @ (np.exp(-1j * np.outer(E, TS)) * c[:, None])).T])
                r.append(bloch(Psi @ D.conj(), n))  # rows: (D^dagger psi)^T = psi^T D^*
            d[frame] = 0.5 * np.linalg.norm(r[0] - r[1], axis=2)  # (51, n): t=0 then 50 checkpoints
        aL = d['L'].mean(1); aC = d['C'].mean(1)
        z = 0.5 * ((aL[1:] - aC[1:]).mean() - (aL[0] - aC[0]))
        eligL = int((d['L'][0] < 2e-4).sum()); eligC = int((d['C'][0] < 2e-4).sum())
        transL = int(((d['L'][0] < 2e-4) & (d['L'][1:].max(0) >= 0.8)).sum())
        transC = int(((d['C'][0] < 2e-4) & (d['C'][1:].max(0) >= 0.8)).sum())
        res[arm] = dict(z=float(z), aL0=float(aL[0]), aC0=float(aC[0]), aLpost=float(aL[1:].mean()),
                        aCpost=float(aC[1:].mean()), eligL=eligL, eligC=eligC, transL=transL, transC=transC)
    return res

def run(n, N, seed):
    rng = np.random.default_rng(seed)
    return [unit(n, rng) for _ in range(N)]

def summ(rows, arm):
    z = np.array([r[arm]['z'] for r in rows]); N = len(z)
    h = np.sqrt(2 * np.log(40) / N)
    se = z.std(ddof=1) / np.sqrt(N)
    keys = ['aL0', 'aC0', 'aLpost', 'aCpost']
    return dict(N=N, mean=float(z.mean()), sd=float(z.std(ddof=1)), clt95=[float(z.mean() - 1.96 * se), float(z.mean() + 1.96 * se)],
                hoeffding95=[float(z.mean() - h), float(z.mean() + h)], pos=int((z > 0).sum()), neg=int((z < 0).sum()),
                **{k: float(np.mean([r[arm][k] for r in rows])) for k in keys},
                eligL_per_unit=sorted(set(r[arm]['eligL'] for r in rows)), eligC_per_unit=sorted(set(r[arm]['eligC'] for r in rows)),
                transient_L=int(sum(r[arm]['transL'] for r in rows)), transient_C=int(sum(r[arm]['transC'] for r in rows)))

if __name__ == '__main__':
    out = {}
    t0 = time.time()
    for n in (4, 6):
        reps = []
        for k in range(5):
            rows = run(n, 96, 7000 + 100 * n + k)
            reps.append({arm: summ(rows, arm) for arm in ('native', 'rotated')})
        out[f'n{n}_96unit_replicates'] = reps
    print('96-unit replicates done', round(time.time() - t0, 1), 's'); sys.stdout.flush()
    big = run(6, 60000, 9606)
    out['n6_60000'] = {arm: summ(big, arm) for arm in ('native', 'rotated')}
    print('n=6 60000 done', round(time.time() - t0, 1), 's'); sys.stdout.flush()
    b8 = run(8, 2000, 9808)
    out['n8_2000'] = {arm: summ(b8, arm) for arm in ('native', 'rotated')}
    print('n=8 done', round(time.time() - t0, 1), 's')
    json.dump(out, open('reimpl_id1_results.json', 'w'), indent=1)
    def line(tag, s):
        print(f"{tag:28s} N={s['N']:6d} mean={s['mean']:+.6f} sd={s['sd']:.4f} CLT95=[{s['clt95'][0]:+.5f},{s['clt95'][1]:+.5f}] "
              f"Hoeff95=[{s['hoeffding95'][0]:+.4f},{s['hoeffding95'][1]:+.4f}] +/-={s['pos']}/{s['neg']} "
              f"aL0={s['aL0']:.4f} aC0={s['aC0']:.4f} aLpost={s['aLpost']:.4f} aCpost={s['aCpost']:.4f} "
              f"elig/unit L={s['eligL_per_unit']} C={s['eligC_per_unit']} transL={s['transient_L']} transC={s['transient_C']}")
    for n in (4, 6):
        for k, rep in enumerate(out[f'n{n}_96unit_replicates']):
            for arm in ('native', 'rotated'):
                line(f'n{n} 96u rep{k} {arm}', rep[arm])
    for arm in ('native', 'rotated'):
        line(f'n6 60000 {arm}', out['n6_60000'][arm])
    for arm in ('native', 'rotated'):
        line(f'n8 2000 {arm}', out['n8_2000'][arm])
