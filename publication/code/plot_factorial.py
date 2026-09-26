from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.hashsalt']='ORSH-AIU-v1.8'
import matplotlib.pyplot as plt

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();r=a.root
 rows=list(csv.DictReader((r/'data/factorial_analysis/factorial_intervals.csv').open()))
 fig,ax=plt.subplots(figsize=(7.0,4.1));y=np.arange(len(rows));means=np.array([float(x['mean']) for x in rows]);lo=np.array([float(x['bernstein_simultaneous_lo']) for x in rows]);hi=np.array([float(x['bernstein_simultaneous_hi']) for x in rows]);ax.errorbar(means,y,xerr=np.array([means-lo,hi-means]),fmt='o',capsize=4,label='Simultaneous empirical-Bernstein 95% interval')
 ax.axvline(0,linestyle=':',linewidth=1);ax.set_yticks(y,[f"{x['qubits']} qubits, inject {x['injection'][-1]}" for x in rows]);ax.invert_yaxis();ax.set_xlabel('Paired Hamiltonian-orientation contrast, e');ax.set_title('Positive means do not imply equally precise bounds');ax.grid(axis='x',alpha=.25);ax.legend(loc='lower right',fontsize=8);fig.tight_layout()
 for ext in ('png','svg'):fig.savefig(r/f'figures/factorial_intervals.{ext}',dpi=220,metadata={'Date':None} if ext=='svg' else None)
 plt.close(fig)
 cells=list(csv.DictReader((r/'data/factorial_analysis/factorial_cells.csv').open()));fig,ax=plt.subplots(figsize=(6.6,3.8))
 for inj in ('injL','injC'):
  rr=[x for x in cells if x['qubits']=='6' and x['injection']==inj];ax.errorbar([0,1],[float(x['mean']) for x in rr],yerr=[1.96*float(x['se']) for x in rr],marker='o',capsize=4,label=f'Injection {inj[-1]}')
 ax.set_xticks([0,1],['Dynamics native to L','Dynamics native to C']);ax.axhline(0,linestyle=':',linewidth=1);ax.set_ylabel('Change from frozen evolution, z');ax.set_title('One negative change and one positive intervention can coexist');ax.legend();ax.grid(axis='y',alpha=.25);fig.tight_layout()
 for ext in ('png','svg'):fig.savefig(r/f'figures/factorial_cells.{ext}',dpi=220,metadata={'Date':None} if ext=='svg' else None)
 plt.close(fig);print('Two figures created in PNG and SVG')
if __name__=='__main__':main()
