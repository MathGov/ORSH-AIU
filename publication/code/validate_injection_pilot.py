#!/usr/bin/env python3
"""Second numerical implementation and analytic controls. Does not import pilot code.
This is same-project validation, not external replication or interval arithmetic.
"""
import argparse,json,csv,hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.sparse.linalg import expm_multiply
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1])
def op(a,j,n):
    h=np.array([[1.]],complex)
    for k in range(n):h=np.kron(h,a if k==j else I)
    return h

def rho_from_vector(v,j,n):
    # Full density-matrix reduction, independent of the main einsum routine.
    rho=np.outer(v,v.conj()).reshape([2]*(2*n))
    order=[j]+[k for k in range(n) if k!=j]+[j+n]+[k+n for k in range(n) if k!=j]
    return np.trace(rho.transpose(order).reshape(2,2**(n-1),2,2**(n-1)),axis1=1,axis2=3)

def td(a,b,j,n):
    return float(np.abs(np.linalg.eigvalsh(rho_from_vector(a,j,n)-rho_from_vector(b,j,n))).sum()/2)

def validate(root):
    c=json.loads((root/'pilot/config.json').read_text());data=root/'data/pilot_run';records=[];maxdiff=0;controls=[]
    def check(name,error,tol=1e-9,extra=None):
        records.append({'name':name,'error':float(error),'tolerance':tol,'passed':bool(error<=tol),'detail':extra})
        if error>tol:raise AssertionError(name)
    for n in c['n_sites']:
        d=2**n;stored=np.load(data/f'trajectories_n{n}.npz');ts=stored['times'];D=stored['distances']
        e0=np.zeros(d,complex);e0[0]=1;M=op(X,0,n)
        pre=[expm(-1j*s*c['pulse_angle']*M)@e0 for s in (1,-1)]
        for i in range(3):
            H=stored['check_H'][i];U=stored['check_U'][i]
            for arm,inj in enumerate([np.eye(d),U]):
                inp=[inj@q for q in pre]
                series=[expm_multiply(-1j*H,v,start=0,stop=c['post_time_max'],num=len(ts),endpoint=True) for v in inp]
                err=0
                for f,V in enumerate([np.eye(d),U]):
                    for ti in [0,1,8,20,40,60,80,100]:
                        aa,bb=[V.conj().T@a[ti] for a in series]
                        for j in range(n):err=max(err,abs(td(aa,bb,j,n)-D[i,arm,f,ti,j]))
                maxdiff=max(maxdiff,err);check(f'separate_propagation_n{n}_u{i}_arm{arm}',err)
                if i==0:
                    frozen=[expm(-1j*np.zeros_like(H))@v for v in inp]
                    er=max(np.max(abs(a-b)) for a,b in zip(frozen,inp));check(f'zero_generator_n{n}_arm{arm}',er)
        # All zeros for identical source states are exact by linearity, plus numerical checks.
        check(f'identical_source_n{n}',max(td(pre[0],pre[0],j,n) for j in range(n)))
        # Passive Fourier conjugation checked on the rotated-injection case at selected times.
        H=stored['check_H'][0];U=stored['check_U'][0];G=np.exp(2j*np.pi*np.outer(np.arange(d),np.arange(d))/d)/np.sqrt(d)
        Hp=G@H@G.conj().T;V=G@U;inp=[G@U@q for q in pre];err=0
        for ti in [0,20,60,100]:
            aa,bb=[V.conj().T@expm(-1j*Hp*ts[ti])@v for v in inp]
            for j in range(n):err=max(err,abs(td(aa,bb,j,n)-D[0,1,1,ti,j]))
        check(f'passive_common_conjugation_n{n}',err)
        # Uniform exchange chain: vacuum versus one excitation, comparison to n-dimensional hopping.
        XY=sum((op(X,j,n)@op(X,j+1,n)+op(Y,j,n)@op(Y,j+1,n))/2 for j in range(n-1))
        hopping=np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1)
        exc=op(X,0,n)@e0;seed=np.zeros(n,complex);seed[0]=1;ct=np.linspace(0,8,161)
        full=expm_multiply(-1j*XY,exc,start=0,stop=8,num=161)
        reduced=expm_multiply(-1j*hopping,seed,start=0,stop=8,num=161)
        err=0;all_probs=np.abs(reduced)**2
        for ti in range(161):
            ds=np.array([td(e0,full[ti],j,n) for j in range(n)])
            err=max(err,float(np.max(abs(ds-all_probs[ti]))))
            controls.extend({'control':'exchange_chain','n':n,'time':float(ct[ti]),'site':j,'trace_distance':float(ds[j])} for j in range(n))
        check(f'one_excitation_reduction_n{n}',err)
        check(f'one_excitation_conservation_n{n}',float(np.max(abs(all_probs.sum(axis=1)-1))))
        check(f'one_excitation_at_most_one_strong_record_n{n}',max(0,int((all_probs>=.8-1e-10).sum(axis=1).max())-1),0)
        # Closed stationary records: all-Z generator commutes with each conditional projector.
        Hd=sum(op(Z,j,n) for j in range(n));allone=np.zeros(d,complex);allone[-1]=1
        check(f'closed_stationary_commutators_n{n}',max(np.linalg.norm(Hd@np.outer(v,v.conj())-np.outer(v,v.conj())@Hd) for v in [e0,allone]))
        check(f'closed_stationary_singletons_n{n}',max(abs(td(e0,allone,j,n)-1) for j in range(n)))
    # Analytic 2-site transfer.
    HH=(np.kron(X,X)+np.kron(Y,Y))/2;vac=np.array([1,0,0,0],complex);ex=np.array([0,0,1,0],complex)
    error=max(abs(td(vac,expm(-1j*HH*t)@ex,1,2)-np.sin(t)**2) for t in np.linspace(0,np.pi,51))
    check('two_site_transfer_sin_squared',error)
    # First-order cancellation with common initial state.
    H=np.kron(Z,X)+.3*np.kron(Y,I);K=np.kron(X,I);rho=np.diag([1.,0,0,0])
    comm=lambda a,b:a@b-b@a
    check('source_difference_cancels_common_H_at_t0',np.linalg.norm(-1j*(comm(H+K,rho)-comm(H-K,rho))+1j*comm(2*K,rho)))
    # Ordinary amplitude damping has one fixed point and erases the source bit.
    damp=[]
    for t in [0.,1.,2.,8.]:
        s=np.exp(-t);A=np.diag([1,np.sqrt(s)]);B=np.array([[0,np.sqrt(1-s)],[0,0]])
        r0=np.diag([1.,0]);r1=np.diag([0.,1]);channel=lambda r:A@r@A.conj().T+B@r@B.conj().T
        dist=float(np.abs(np.linalg.eigvalsh(channel(r0)-channel(r1))).sum()/2)
        check(f'amplitude_damping_t{t}',abs(dist-s));damp.append({'time':t,'distance':dist,'exact':s})
    out={'checks':records,'passed':sum(x['passed'] for x in records),'failed':sum(not x['passed'] for x in records),'separate_solver_max_difference':maxdiff,'amplitude_damping':damp,'scope':'selected n=4/6 trajectories and analytic controls; not all-unit independent replication or certified rounding','checked_units_per_size':3,'formal_numeric_enclosure':False}
    (root/'verification/independent_pilot_checks.json').write_text(json.dumps(out,indent=2))
    with (root/'data/transport_control.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(controls[0]));w.writeheader();w.writerows(controls)
    print(json.dumps({k:out[k] for k in ['passed','failed','separate_solver_max_difference']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path);a=p.parse_args();validate(a.root)
