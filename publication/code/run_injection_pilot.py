#!/usr/bin/env python3
"""P01-ID1, a pre-specified exploratory source-off redistribution pilot.
No network calls. Individual n/seed histories are the independent units.
Use --out with an empty directory. No metric or preferred TPS is recovered.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, os, platform, sys, time
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import eigh

I=np.eye(2,dtype=complex)
PAULI=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.]).astype(complex)]
KEYS={'experiment_id','status','master_seed','n_sites','units_per_size','coupling_circuit_depth','pulse_angle','source_site','post_time_max','post_time_steps','primary_stride','pair_coefficient_sd','field_coefficient_sd','record_epsilon','initial_error_floor','windows','numerical_guard','bootstrap_resamples','confidence_alpha'}
def load_config(path: Path) -> dict:
    c=json.loads(path.read_text())
    if set(c)!=KEYS: raise ValueError(f'Unexpected/missing fields: {set(c)^KEYS}')
    if c['n_sites']!=[4,6] or c['units_per_size']<2: raise ValueError('Unsupported model sizes/sample count')
    if not 0<c['record_epsilon']<c['initial_error_floor']<=.5: raise ValueError('Invalid record thresholds')
    if c['post_time_steps']%c['primary_stride']: raise ValueError('Nondivisible grid')
    return c

def site_ops(n:int)->list[list[np.ndarray]]:
    def embed(a,j):
        x=np.array([[1.]],complex)
        for k in range(n):x=np.kron(x,a if k==j else I)
        return x
    return [[embed(a,j) for a in PAULI] for j in range(n)]

def haar_gate(rng:np.random.Generator)->np.ndarray:
    a=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
    q,r=np.linalg.qr(a); diag=np.diag(r)
    return q*(diag/np.abs(diag))[None,:]

def circuit(n:int,rng:np.random.Generator,depth:int)->np.ndarray:
    u=np.eye(2**n,dtype=complex)
    for layer in range(depth):
        for j in range(layer%2,n-1,2):
            gate=np.kron(np.kron(np.eye(2**j),haar_gate(rng)),np.eye(2**(n-j-2)))
            u=gate@u
    return u

def local_density_series(psi:np.ndarray,j:int,n:int)->np.ndarray:
    # psi[d,t] -> rho[a,b,t]
    a=np.moveaxis(psi.reshape([2]*n+[psi.shape[1]]),j,0).reshape(2,-1,psi.shape[1])
    return np.einsum('art,brt->abt',a,a.conj(),optimize=True)

def distances(a:np.ndarray,b:np.ndarray,n:int)->np.ndarray:
    out=[]
    for j in range(n):
        x=local_density_series(a,j,n)-local_density_series(b,j,n)
        # Hermitian trace-zero 2x2 difference: half trace norm is its positive eigenvalue.
        v=np.sqrt(np.real((x[0,0]-x[1,1])/2)**2+np.abs(x[0,1])**2)
        if v.min() < -1e-10 or v.max()>1+1e-9:raise AssertionError('Invalid trace distance')
        out.append(np.clip(v,0,1))
    return np.array(out).T

def omega(h:np.ndarray)->float:
    e=eigh(h,eigvals_only=True,check_finite=False)
    return float((e[-1]-e[0])/2)

def complement_subtracted(h:np.ndarray,j:int,n:int)->np.ndarray:
    rest=[k for k in range(n) if k!=j]; axes=[j]+rest+[j+n]+[k+n for k in rest]
    x=h.reshape([2]*(2*n)).transpose(axes).reshape(2,2**(n-1),2,2**(n-1))
    comp=np.trace(x,axis1=0,axis2=2)/2
    y=np.kron(I,comp).reshape([2]*(2*n)).transpose(np.argsort(axes)).reshape(h.shape)
    return (h-y+(h-y).conj().T)/2

def phi(u:np.ndarray,ops:list[list[np.ndarray]])->float:
    d=u.shape[0]; basis=np.array([a.reshape(-1)/np.sqrt(d) for row in ops for a in row])
    rotated=np.array([(u@a@u.conj().T).reshape(-1)/np.sqrt(d) for row in ops for a in row])
    overlap=basis.conj()@rotated.T
    return float(np.clip(1-np.sum(np.abs(overlap)**2)/len(basis),0,1))

def counts(D:np.ndarray,K:np.ndarray,ts:np.ndarray,c:dict)->list[dict]:
    # D[t,site]. Conditional on a numerical guard; not formal interval arithmetic.
    errors=(1-D)/2; guard=c['numerical_guard']; h=float(np.max(np.diff(ts)))
    initial_lo=errors[0]-guard>=c['initial_error_floor']
    initial_hi=errors[0]+guard>=c['initial_error_floor']
    result=[]
    for left,right in c['windows']:
        idx=(ts>=left-1e-12)&(ts<=right+1e-12)
        if not np.isclose(ts[idx][0],left) or not np.isclose(ts[idx][-1],right):raise AssertionError('Missing window endpoint')
        worst=errors[idx].max(axis=0)
        lo=initial_lo & (worst+K*h/2+guard<=c['record_epsilon'])
        hi=initial_hi & (worst-guard<=c['record_epsilon'])
        sample=initial_lo & (worst+guard<=c['record_epsilon'])
        result.append({'window':[left,right],'lower_conditional':int(lo.sum()),'upper_possible':int(hi.sum()),'checkpoint_passing':int(sample.sum())})
    return result

def unit(n:int,index:int,c:dict,ops:list[list[np.ndarray]],ts:np.ndarray):
    # independent reproducible substreams for H and U; arms reuse the same unit.
    seed=np.random.SeedSequence([c['master_seed'],n,index]); sh,su=seed.spawn(2)
    rh,ru=np.random.default_rng(sh),np.random.default_rng(su)
    fields=rh.normal(scale=c['field_coefficient_sd'],size=(n,3))
    bonds=rh.normal(scale=c['pair_coefficient_sd'],size=(n-1,3))
    d=2**n;H=np.zeros((d,d),complex)
    for j in range(n):
        for a in range(3):H+=fields[j,a]*ops[j][a]
    for j in range(n-1):
        for a in range(3):H+=bonds[j,a]*(ops[j][a]@ops[j+1][a])
    UC=circuit(n,ru,c['coupling_circuit_depth']); frames=[np.eye(d,dtype=complex),UC]
    eh,vh=eigh(H,check_finite=False); global_K=float((eh[-1]-eh[0])/2)
    Ks=np.array([[min(global_K,omega(complement_subtracted(U.conj().T@H@U,j,n))) for j in range(n)] for U in frames])
    v0=np.zeros(d,complex);v0[0]=1;flipped=ops[c['source_site']][0]@v0
    theta=c['pulse_angle'];pre=[np.cos(theta)*v0-1j*np.sin(theta)*flipped,np.cos(theta)*v0+1j*np.sin(theta)*flipped]
    D=np.empty((2,2,len(ts),n));rows=[];norm_err=0.;orth_err=0.
    for arm,U in enumerate(frames):
        init=[U@p for p in pre]
        branches=[vh@(np.exp(-1j*eh[:,None]*ts)*(vh.conj().T@p)[:,None]) for p in init]
        norm_err=max(norm_err,max(float(np.max(np.abs(np.sum(abs(p)**2,axis=0)-1))) for p in branches))
        orth_err=max(orth_err,float(np.max(np.abs(np.sum(branches[0].conj()*branches[1],axis=0)))))
        for frame,V in enumerate(frames):D[arm,frame]=distances(V.conj().T@branches[0],V.conj().T@branches[1],n)
        avg=D[arm].mean(axis=-1) # frame,time
        inds=np.arange(c['primary_stride'],len(ts),c['primary_stride'])
        gap=avg[0]-avg[1];z=float((np.mean(gap[inds])-gap[0])/2)
        result={'n':n,'unit_index':index,'unit_id':f'n{n}-u{index:03d}','arm':['native','rotated'][arm],
                'z':z,'gap_at_switch':float(gap[0]),'gap_post_average':float(gap[inds].mean()),
                'mean_d_L_switch':float(avg[0,0]),'mean_d_C_switch':float(avg[1,0]),
                'mean_d_L_post':float(avg[0,inds].mean()),'mean_d_C_post':float(avg[1,inds].mean()),
                'L_windows':counts(D[arm,0],Ks[0],ts,c),'C_windows':counts(D[arm,1],Ks[1],ts,c)}
        rows.append(result)
    meta={'n':n,'unit_index':index,'seed_entropy':[c['master_seed'],n,index],'fields':fields.tolist(),'bonds':bonds.tolist(),'phi_LC':phi(UC,ops),'global_K':global_K,'K_L':Ks[0].tolist(),'K_C':Ks[1].tolist(),'norm_error':norm_err,'orthogonality_error':orth_err}
    if norm_err>1e-10 or orth_err>1e-10:raise AssertionError('Global evolution check failed')
    return D,rows,meta,H,UC

def summarize(rows:list[dict],c:dict)->list[dict]:
    out=[];rng=np.random.default_rng(c['master_seed']+987)
    for n in c['n_sites']:
        for arm in ['native','rotated']:
            r=[x for x in rows if x['n']==n and x['arm']==arm];z=np.array([x['z'] for x in r]);N=len(z)
            boots=z[rng.integers(N,size=(c['bootstrap_resamples'],N))].mean(axis=1)
            h=np.sqrt(2*np.log(2/c['confidence_alpha'])/N)
            out.append({'n':n,'arm':arm,'units':N,'mean_z':float(z.mean()),'sd_z':float(z.std(ddof=1)),'min_z':float(z.min()),'max_z':float(z.max()),'positive_count':int((z>1e-12).sum()),'negative_count':int((z< -1e-12).sum()),'tie_count':int((abs(z)<=1e-12).sum()),'bootstrap_95_approx':np.quantile(boots,[.025,.975]).tolist(),'hoeffding_95':[max(-1,float(z.mean()-h)),min(1,float(z.mean()+h))],
                'windows':[{'window':window,**{f'{f}_{key}_mean':float(np.mean([x[f'{f}_windows'][j][key] for x in r])) for f in ['L','C'] for key in ['lower_conditional','upper_possible','checkpoint_passing']}} for j,window in enumerate(c['windows'])]})
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args();c=load_config(a.config)
    if a.out.exists() and any(a.out.iterdir()):raise ValueError('Output directory must be empty')
    a.out.mkdir(parents=True,exist_ok=True);start=time.time();ts=np.linspace(0,c['post_time_max'],c['post_time_steps']+1)
    rows=[];metas=[]
    for n in c['n_sites']:
        ops=site_ops(n);ds=[];controls_H=[];controls_U=[]
        for i in range(c['units_per_size']):
            D,rr,meta,H,U=unit(n,i,c,ops,ts);ds.append(D);rows.extend(rr);metas.append(meta)
            if i<3:controls_H.append(H);controls_U.append(U)
        np.savez_compressed(a.out/f'trajectories_n{n}.npz',distances=np.array(ds),times=ts,check_H=np.array(controls_H),check_U=np.array(controls_U))
        print(f'Finished n={n}: {c["units_per_size"]} independent units; two paired injection arms.',flush=True)
    (a.out/'per_unit.json').write_text(json.dumps(rows,indent=2));(a.out/'model_inputs.json').write_text(json.dumps(metas,indent=2))
    summary={'experiment_id':c['experiment_id'],'interpretation':'source-off finite-model exploratory feasibility, no recovered TPS or cosmology','independent_units_total':len(metas),'paired_arm_evaluations':len(rows),'primary':{'n':6,'arm':'rotated'},'summary':summarize(rows,c),'numerical_guard_status':'empirical guard, not formally proved floating-point enclosure','max_norm_error':max(x['norm_error'] for x in metas),'max_orthogonality_error':max(x['orthogonality_error'] for x in metas),'phi_range':[min(x['phi_LC'] for x in metas),max(x['phi_LC'] for x in metas)]}
    (a.out/'results.json').write_text(json.dumps(summary,indent=2));(a.out/'effective_config.json').write_text(json.dumps(c,indent=2))
    (a.out/'environment.json').write_text(json.dumps({'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform(),'elapsed_seconds':time.time()-start,'config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
    with (a.out/'per_unit_summary.csv').open('w',newline='') as f:
        keys=[k for k in rows[0] if not k.endswith('_windows')];w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:r[k] for k in keys} for r in rows)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
