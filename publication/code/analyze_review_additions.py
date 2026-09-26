#!/usr/bin/env python3
"""Post hoc review analyses of immutable P01-ID1 data. Not a new pilot.
Checks sign counts from unit data and trajectories; exact sign p-values;
Holm adjustment for four reported rows; concentration precision; transport
window diagnostics for two different encodings. No network or hidden inputs.
"""
from pathlib import Path
import argparse, json, math, csv, sys, platform
import numpy as np
import scipy
from scipy.stats import binomtest
from scipy.linalg import eigh

def writecsv(path,rows):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def exact_p(k,n):
 return min(1.,2*sum(math.comb(n,j) for j in range(min(k,n-k)+1))/2**n)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists() and any(a.out.iterdir()):raise ValueError('Choose an empty output directory')
 a.out.mkdir(parents=True,exist_ok=True)
 data=a.root/'data'/'pilot_run'; rows=json.loads((data/'per_unit.json').read_text()); report=[];checks=[];diagnostics=[]
 for n in [4,6]:
  pack=np.load(data/f'trajectories_n{n}.npz');ds=pack['distances'];ts=pack['times'];idx=np.arange(2,len(ts),2)
  for ai,arm in enumerate(['native','rotated']):
   selected=[x for x in rows if x['n']==n and x['arm']==arm];z=np.array([x['z'] for x in selected]);N=len(z)
   aa=ds[:,ai].mean(axis=-1);zz=((aa[:,0,idx]-aa[:,1,idx]).mean(axis=1)-(aa[:,0,0]-aa[:,1,0]))/2
   checks.append({'check':f'trajectory_z_n{n}_{arm}','max_difference':float(abs(z-zz).max()),'pass':bool(np.allclose(z,zz,atol=1e-13,rtol=0))})
   pos=int((z>1e-12).sum());neg=int((z< -1e-12).sum());tie=N-pos-neg;p=exact_p(pos,pos+neg);p2=binomtest(pos,pos+neg,.5).pvalue
   checks.append({'check':f'binomial_formula_n{n}_{arm}','difference':float(abs(p-p2)),'pass':bool(abs(p-p2)<1e-14)})
   report.append({'n':n,'arm':arm,'units':N,'positive':pos,'negative':neg,'ties':tie,'mean_z':float(z.mean()),'median_z':float(np.median(z)),'min_abs_z':float(np.min(abs(z))),'two_sided_sign_p':p,'holm_p':None,'observed_positive_fraction':pos/(pos+neg)})
   for fi,frame in enumerate(['L','C']):
    arr=ds[:,ai,fi];er=(1-arr)/2;eligible=er[:,0]>=.4999-1e-9
    diagnostics.append({'n':n,'arm':arm,'frame':frame,'total_singletons':int(eligible.size),'initially_eligible':int(eligible.sum()),'eligible_ever_d_at_least_0_8':int((eligible & (arr[:,1:].max(axis=1)>=.8)).sum()),'maximum_d_any_initially_eligible':float(np.where(eligible,arr[:,1:].max(axis=1),-1).max())})
 order=sorted(range(len(report)),key=lambda i:report[i]['two_sided_sign_p']);running=0
 for j,i in enumerate(order):
  running=max(running,(len(report)-j)*report[i]['two_sided_sign_p']);report[i]['holm_p']=min(1.,running)
 transport=[];windows=[[.5,1],[1,1.5],[1.5,2],[2,2.5]];tw=[];times=np.round(np.arange(0,6.00001,.025),3)
 for n in [4,6]:
  H=np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1);e,v=eigh(H);amplitudes=v@(np.exp(-1j*e[:,None]*times)*v[0,:,None].conj())
  prob=abs(amplitudes[-1])**2
  for encoding,d in [('vacuum_vs_excitation',prob),('opposite_phase_pulse',np.sqrt(prob))]:
   for t,dd,pp in zip(times,d,prob):transport.append({'n':n,'encoding':encoding,'time':float(t),'end_site_probability':float(pp),'end_site_distinguishability':float(dd),'error':float((1-dd)/2)})
   above=times[d>=.8]
   for lo,hi in windows:
    mask=(times>=lo)&(times<=hi);tw.append({'n':n,'encoding':encoding,'window_start':lo,'window_end':hi,'max_error_in_window':float(((1-d[mask])/2).max()),'passes_all_checkpoints':bool(np.all(d[mask]>=.8)),'first_passing_grid_time':float(above[0]) if len(above) else None,'last_passing_grid_time':float(above[-1]) if len(above) else None})
 precision={'N':96,'alpha':.05,'declared_range':[-1,1],'hoeffding_halfwidth':math.sqrt(2*math.log(40)/96),'N_for_halfwidth_0_015':math.ceil(2*math.log(40)/.015**2),'interpretation':'sufficient worst-case precision budget, not power or a universal minimum required sample size'}
 allout={'status':'POST_HOC_SECONDARY_REANALYSIS; four-row Holm family chosen during review, not preregistered','sign_null':'independent signs with Pr(z>0 | z!=0)=1/2; no whole-distribution symmetry assumed; not a zero-mean null','ties':'1e-12 reporting tolerance; no ties and all absolute contrasts exceed it','rows':report,'precision':precision,'initial_floor_diagnostics':diagnostics,'transport_windows':tw,'checks':checks,'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'environment':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__}}
 (a.out/'review_analysis.json').write_text(json.dumps(allout,indent=2));writecsv(a.out/'sign_tests.csv',report);writecsv(a.out/'transport_window_checks.csv',tw);writecsv(a.out/'transport_encodings.csv',transport);writecsv(a.out/'initial_floor_diagnostics.csv',diagnostics)
 print(json.dumps({k:allout[k] for k in ['rows','precision','initial_floor_diagnostics','passed','failed']},indent=2))
 if allout['failed']:raise SystemExit(1)
if __name__=='__main__':main()
