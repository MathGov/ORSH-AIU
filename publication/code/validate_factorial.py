"""Small independent propagation check using exponential action and density matrices.
Input generators are shared with reviewer code; propagation and reduction are not.
"""
from pathlib import Path
import json,sys,argparse
import numpy as np
from scipy.sparse.linalg import expm_multiply

def reduce_one(rho,n,j):
    r=rho.reshape([2]*2*n);rest=[k for k in range(n) if k!=j]
    r=r.transpose([j]+rest+[n+j]+[n+k for k in rest]).reshape(2,2**(n-1),2,2**(n-1))
    return np.einsum('arbr->ab',r)

def independent_z(H,Vinj,U,n):
    v=np.zeros(2**n,complex);v[0]=1;w=np.zeros_like(v);w[2**(n-1)]=1
    psi=[Vinj@(v+s*1j*w)/np.sqrt(2) for s in (-1,1)]
    traj=[expm_multiply(-1j*H,q,start=0,stop=2.5,num=51,endpoint=True,traceA=-1j*np.trace(H)) for q in psi]
    a=[]
    for D in (np.eye(2**n),U):
        vals=[]
        for t in range(51):
            r=[np.outer(D.conj().T@b[t],(D.conj().T@b[t]).conj()) for b in traj]
            vals.append(np.mean([.5*np.sum(np.abs(np.linalg.eigvalsh(reduce_one(r[0]-r[1],n,j)))) for j in range(n)]))
        a.append(np.array(vals))
    g=a[0]-a[1];return .5*(g[1:].mean()-g[0])

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path);args=p.parse_args();sys.path.insert(0,str(args.root/'feedback/current'))
    import reimpl_id1 as r, factorial_id1 as f
    checks=[]
    def check(label,value,limit=1e-10):checks.append(dict(label=label,residual=float(value),limit=limit,passed=bool(value<=limit)))
    for n in (4,6):
        for seed in (171,299):
            rng=np.random.default_rng(seed+n);H=r.H_S(n,rng);U=r.U_C(n,rng);E,V=np.linalg.eigh(H);zs={}
            for inj,A in [('L',np.eye(2**n)),('C',U)]:
                for dyn,Hd,Vd in [('L',H,V),('C',U@H@U.conj().T,U@V)]:
                    z0=f.z_arm(E,Vd,n,A,U)[0];z1=independent_z(Hd,A,U,n);zs[inj+dyn]=z1
                    check(f'n{n} seed{seed} {inj}{dyn} independent solver',abs(z0-z1))
            for inj in ('L','C'):check(f'n{n} seed{seed} {inj} contrast range',max(0,abs(zs[inj+'L']-zs[inj+'C'])-1))
            # Swapping orientation requires U inverse, not merely relabelling the original circuit law.
            zinv=f.z_arm(E,V,n,np.eye(2**n),U.conj().T)[0]
            check(f'n{n} seed{seed} inverse-frame identity',abs(zs['CC']+zinv))
    # Deterministic statistical identities checked separately from main analysis.
    for values in [np.array([-1.,0.,1.]),np.array([.1,.2,.4,.8])]:
        N=len(values);pair=sum((values[i]-values[j])**2 for i in range(N) for j in range(i+1,N))/(N*(N-1));check('pairwise variance equals sample variance',abs(pair-values.var(ddof=1)))
        log=np.log(24/.05);x=(values+1)/2
        scaled=2*(np.sqrt(2*x.var(ddof=1)*log/N)+7*log/(3*(N-1)))
        direct=np.sqrt(2*values.var(ddof=1)*log/N)+14*log/(3*(N-1));check('Bernstein affine rescaling',abs(scaled-direct))
    out={'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'scope':'selected inputs; different propagator and full-density reduction; not independent research team'}
    (args.out or args.root/'verification/factorial_independent_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['failed']==0
if __name__=='__main__':main()
