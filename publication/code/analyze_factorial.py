"""Secondary analysis of the supplied factorial extension.
All reported sampling intervals condition on the declared iid law and faithful
numerical evaluation. No external preregistration or mechanistic identification.
"""
from pathlib import Path
import argparse,json,csv,math
import numpy as np

def load(path):
    with np.load(path,allow_pickle=False) as a:return {str(k):a['values'][:,i] for i,k in enumerate(a['columns'])}

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists() and any(a.out.iterdir()):raise SystemExit('Output must be empty')
    a.out.mkdir(parents=True,exist_ok=True)
    rows=[];cells=[];decomp=[];alpha=.05;K=6;L=math.log(4*K/alpha)
    for n in (4,6,8):
        d=load(a.root/f'data/reviewer_replay/factorial_n{n}.npz');N=len(d['injL_dynL'])
        for inj in ('injL','injC'):
            e=d[inj+'_dynL']-d[inj+'_dynC'];s2=float(e.var(ddof=1));mu=float(e.mean())
            # Same initial gap cancels exactly; hence e is in [-1,1], not [-2,2].
            direct=.5*((d[inj+'_dynL_aL.1']-d[inj+'_dynL_aC.1'])-(d[inj+'_dynC_aL.1']-d[inj+'_dynC_aC.1']))
            rad=math.sqrt(2*s2*L/N)+14*L/(3*(N-1))
            h=math.sqrt(2*math.log(2*K/alpha)/N)
            rows.append(dict(qubits=n,units=N,injection=inj,mean=mu,variance=s2,positive=int((e>0).sum()),normal_lo=mu-1.96*math.sqrt(s2/N),normal_hi=mu+1.96*math.sqrt(s2/N),hoeffding_simultaneous_lo=max(-1,mu-h),hoeffding_simultaneous_hi=min(1,mu+h),bernstein_simultaneous_lo=max(-1,mu-rad),bernstein_simultaneous_hi=min(1,mu+rad),cancellation_max_error=float(abs(e-direct).max()),min_unit=float(e.min()),max_unit=float(e.max())))
        for inj in ('injL','injC'):
            for dyn in ('dynL','dynC'):
                key=inj+'_'+dyn;v=d[key]
                cells.append(dict(qubits=n,units=N,injection=inj,dynamics=dyn,mean=float(v.mean()),se=float(v.std(ddof=1)/np.sqrt(N)),aL_initial=float(d[key+'_aL.0'].mean()),aC_initial=float(d[key+'_aC.0'].mean()),aL_post=float(d[key+'_aL.1'].mean()),aC_post=float(d[key+'_aC.1'].mean())))
        eL=d['injL_dynL']-d['injL_dynC'];eC=d['injC_dynL']-d['injC_dynC']
        decomp.append(dict(qubits=n,average_rotation_contrast=float(((eL+eC)/2).mean()),interaction_difference=float((eL-eC).mean()),injection_contrast_dynL=float((d['injL_dynL']-d['injC_dynL']).mean()),injection_contrast_dynC=float((d['injL_dynC']-d['injC_dynC']).mean()),warning='Finite-design contrasts; not a unique causal decomposition into injection and locality mechanisms.'))
    for name,data in [('factorial_intervals.csv',rows),('factorial_cells.csv',cells)]:
        with (a.out/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    report=dict(alpha=alpha,family_size=K,log_term=L,source='Maurer and Pontil (2009), Theorem 4, rescaling plus union over two tails and six targets',scope='post hoc finite-family sampling analysis; not original ID1 primary; numerical roundoff not formally enclosed',effects=rows,design_decomposition=decomp)
    (a.out/'analysis.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
