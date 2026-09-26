#!/usr/bin/env python3
"""Separate formulas for the v1.7 post hoc additions. No import of analysis code.
Finite checks, not independent scientific replication or a proof of consciousness.
"""
import argparse,json,math,csv
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.linalg import expm

def main(root):
    checks=[]
    def check(name,err,tol=1e-11):
        checks.append({'name':name,'error':float(err),'tolerance':tol,'passed':bool(err<=tol)})
        if err>tol:raise AssertionError(name)
    source=json.loads((root/'data/review_additions/review_analysis.json').read_text())
    for row in source['rows']:
        k=min(row['positive'],row['negative']);n=row['units']
        p=float(min(Fraction(1),2*sum((Fraction(math.comb(n,j),2**n) for j in range(k+1)),Fraction(0))))
        check(f"exact_fraction_sign_n{row['n']}_{row['arm']}",abs(p-row['two_sided_sign_p']))
    # Match the two source codes using full tensor-space propagation/reduction.
    I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex)
    def site(a,j,n):
        z=np.ones((1,1),complex)
        for k in range(n):z=np.kron(z,a if j==k else I)
        return z
    def reduce(v,j,n):
        axes=[j]+[k for k in range(n) if k!=j]
        a=v.reshape([2]*n).transpose(axes).reshape(2,-1)
        return a@a.conj().T
    for n in (4,6):
        opsX=[site(X,j,n) for j in range(n)];opsY=[site(Y,j,n) for j in range(n)]
        H=sum((opsX[j]@opsX[j+1]+opsY[j]@opsY[j+1])/2 for j in range(n-1))
        small=np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1)
        vac=np.eye(2**n,dtype=complex)[:,0];exc=opsX[0]@vac
        for t in (0.75,2.4,2.8,3.95):
            U=expm(-1j*t*H);amp=abs(expm(-1j*t*small)[-1,0])
            for label,states,target in [('vac_exc',[vac,exc],amp**2),('phase',[(vac-1j*exc)/np.sqrt(2),(vac+1j*exc)/np.sqrt(2)],amp)]:
                r0,r1=[reduce(U@v,n-1,n) for v in states]
                distance=np.abs(np.linalg.eigvalsh(r0-r1)).sum()/2
                check(f'{label}_n{n}_t{t}',abs(distance-target))
    # Enumeration for the stipulated W04 operational comparison.
    cases=[]
    for a in (0,1):
        for link in (0,1):
            mass={0:Fraction(0),1:Fraction(0)}
            for b0 in (0,1):
                for noise,pn in [(0,Fraction(9,10)),(1,Fraction(1,10))]:
                    b1=(a^noise) if link else b0
                    mass[b1]+=Fraction(1,2)*pn
            check(f'subject_example_normalization_{a}_{link}',abs(float(sum(mass.values()))-1))
            expected=Fraction(9,10) if link else Fraction(1,2)
            check(f'subject_example_readout_{a}_{link}',abs(float(mass[a]-expected)))
            cases.append({'intervention_A':a,'link':link,'P_B0':float(mass[0]),'P_B1':float(mass[1]),'same_for_both_stipulated_subject_accounts':True})
    check('precision_N',abs(math.ceil(2*math.log(40)/(.015**2))-source['precision']['N_for_halfwidth_0_015']),0)
    out=root/'verification';out.mkdir(exist_ok=True)
    (out/'v17_secondary_checks.json').write_text(json.dumps({'scope':'same-project second formulas; no external replication','checks':checks,'failed':sum(not x['passed'] for x in checks),'subject_example':cases},indent=2))
    print(f'{len(checks)} checks passed; zero failures')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();main(a.root)
