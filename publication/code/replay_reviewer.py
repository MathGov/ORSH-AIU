"""Replay supplied reviewer implementations, preserving per-unit observables.
Same-code reproduction, not external replication or preregistration.
"""
from pathlib import Path
import argparse, json, sys, time, hashlib, platform
import numpy as np

def save_rows(path, rows):
    if 'native' in rows[0]:
        keys=[a+'.'+k for a in ('native','rotated') for k in rows[0][a]]
        vals=[[r[a][k] for a in ('native','rotated') for k in rows[0][a]] for r in rows]
    else:
        keys=[]
        for k,v in rows[0].items():
            keys.extend([f'{k}.{j}' for j in range(len(v))] if isinstance(v,list) else [k])
        vals=[]
        for r in rows:
            row=[]
            for v in r.values(): row.extend(v if isinstance(v,list) else [v])
            vals.append(row)
    np.savez_compressed(path,columns=np.array(keys),values=np.array(vals,dtype=float))

def compare(a,b,path='root',errors=None):
    errors=[] if errors is None else errors
    if isinstance(a,dict) and isinstance(b,dict):
        if set(a)!=set(b): errors.append(path+': keys differ')
        for k in set(a)&set(b): compare(a[k],b[k],path+'.'+k,errors)
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): errors.append(path+': lengths differ')
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+f'[{i}]',errors)
    elif isinstance(a,(int,float)) and isinstance(b,(int,float)):
        if not np.isclose(a,b,rtol=1e-8,atol=1e-10): errors.append(f'{path}: {a} != {b}')
    elif a!=b: errors.append(path+': value differs')
    return errors

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--task',choices=['factorial','reimplementation','neutral','all'],default='all');args=p.parse_args()
    if args.out.exists() and any(args.out.iterdir()):raise SystemExit('Output must be empty.')
    args.out.mkdir(parents=True,exist_ok=True)
    source=args.root/'feedback/current';sys.path.insert(0,str(source))
    import reimpl_id1 as r
    import factorial_id1 as f
    started=time.time(); comparisons=[]
    def dump(name,out):
        (args.out/name).write_text(json.dumps(out,indent=2)+'\n')
        exp=json.loads((source/name).read_text()); errs=compare(out,exp)
        comparisons.append({'file':name,'match':not errs,'errors':errs,'rtol':1e-8,'atol':1e-10})
        print(name, 'MATCH' if not errs else errs[:5], 'elapsed',round(time.time()-started,1),flush=True)
        (args.out/'comparisons.json').write_text(json.dumps(comparisons,indent=2))
    if args.task in ('all','factorial'):
        out={}
        for n,N in ((6,20000),(4,20000),(8,1000)):
            rows=f.run(n,N,4242+n);save_rows(args.out/f'factorial_n{n}.npz',rows);s={}
            for k in ('injL_dynL','injC_dynL','injL_dynC','injC_dynC'):
                z=np.array([row[k] for row in rows]);se=z.std(ddof=1)/np.sqrt(len(z))
                s[k]=dict(mean=float(z.mean()),ci95=[float(z.mean()-1.96*se),float(z.mean()+1.96*se)],aL=[float(np.mean([row[k+'_aL'][j] for row in rows])) for j in (0,1)],aC=[float(np.mean([row[k+'_aC'][j] for row in rows])) for j in (0,1)])
            for inj in ('injL','injC'):
                e=np.array([row[f'{inj}_dynL']-row[f'{inj}_dynC'] for row in rows]);se=e.std(ddof=1)/np.sqrt(len(e))
                s[f'locality_effect_{inj}']=dict(mean=float(e.mean()),ci95=[float(e.mean()-1.96*se),float(e.mean()+1.96*se)],frac_positive=float((e>0).mean()))
            out[f'n{n}_N{N}']=s;print('factorial',n,N,round(time.time()-started,1),flush=True)
        dump('factorial_results.json',out)
    if args.task in ('all','reimplementation'):
        out={}
        for n in (4,6):
            reps=[]
            for k in range(5):
                rows=r.run(n,96,7000+100*n+k);save_rows(args.out/f'reimpl_n{n}_rep{k}.npz',rows)
                reps.append({a:r.summ(rows,a) for a in ('native','rotated')})
            out[f'n{n}_96unit_replicates']=reps
        for n,N,seed in ((6,60000,9606),(8,2000,9808)):
            rows=r.run(n,N,seed);save_rows(args.out/f'reimpl_n{n}_N{N}.npz',rows)
            out[f'n{n}_{N}']={a:r.summ(rows,a) for a in ('native','rotated')}
            print('reimpl',n,N,round(time.time()-started,1),flush=True)
        dump('reimpl_id1_results.json',out)
    if args.task in ('all','neutral'):
        n,N=6,6000;rng=np.random.default_rng(777);rows=[]
        for _ in range(N):
            H=r.H_S(n,rng);UC=r.U_C(n,rng);W=r.U_C(n,rng);E,V=np.linalg.eigh(H);row={}
            for inj,Vinj in (('injL',np.eye(2**n)),('injC',UC)):
                for dyn,Vd in (('dynL',V),('dynC',UC@V),('dynW',W@V)):
                    row[f'{inj}_{dyn}']=float(f.z_arm(E,Vd,n,Vinj,UC)[0])
            rows.append(row)
        save_rows(args.out/'neutral_n6.npz',rows);out={}
        for k in rows[0]:
            x=np.array([row[k] for row in rows]);out[k]=[float(x.mean()),float(1.96*x.std(ddof=1)/np.sqrt(N))]
        for inj in ('injL','injC'):
            for a,b in (('dynL','dynW'),('dynW','dynC')):
                e=np.array([row[f'{inj}_{a}']-row[f'{inj}_{b}'] for row in rows]);out[f'{inj}: {a} minus {b}']=[float(e.mean()),float(1.96*e.std(ddof=1)/np.sqrt(N)),float((e>0).mean())]
        dump('factorial_neutral.json',out)
    receipt={'task':args.task,'python':platform.python_version(),'numpy':np.__version__,'elapsed_seconds':time.time()-started,'comparisons':comparisons,'wrapper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'same supplied implementations, preserved per-unit observables; no external replication'}
    (args.out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if any(not c['match'] for c in comparisons):raise SystemExit(1)
if __name__=='__main__':main()
