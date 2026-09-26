#!/usr/bin/env python3
"""Generate standalone figures from delivered pilot data; no custom palette."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv

def main(root):
    figdir=root/'figures';figdir.mkdir(exist_ok=True)
    units=json.loads((root/'data/pilot_run/per_unit.json').read_text())
    fig,ax=plt.subplots(figsize=(7.4,4.3))
    for offset,n in enumerate([4,6]):
        z=np.array([r['z'] for r in units if r['n']==n and r['arm']=='rotated'])
        # deterministic display jitter, not a statistical variable
        xx=n+np.linspace(-.22,.22,len(z))
        ax.scatter(xx,z,s=15,alpha=.60,label=f'{n} sites: mean {z.mean():.4f}')
        ax.plot([n-.3,n+.3],[z.mean(),z.mean()],linewidth=2)
    ax.axhline(0,linestyle=':',linewidth=1);ax.set_xticks([4,6],['4 qubits','6 qubits (primary)'])
    ax.set_ylabel('Within-unit readability-gap change, z');ax.set_title('Source-off pilot: rotated injection')
    ax.legend(loc='best',fontsize=9);fig.tight_layout()
    for ext in ('png','svg'):fig.savefig(figdir/f'pilot_contrast_distribution.{ext}',dpi=180)
    plt.close(fig)
    f=np.load(root/'data/pilot_run/trajectories_n6.npz');t=f['times'];d=f['distances'][:,1]
    curves=d.mean(axis=(0,3)) # frames,times, average over units and sites
    fig,ax=plt.subplots(figsize=(7.4,4.3))
    ax.plot(t,curves[0],label='Internal-frame access L, H on')
    ax.plot(t,curves[1],label='Injection-frame access C, H on')
    ax.axhline(curves[0,0],linestyle='--',label='L, no-evolution control')
    ax.axhline(curves[1,0],linestyle=':',label='C, no-evolution control')
    ax.set_xlabel('Time after source removal');ax.set_ylabel('Mean single-site trace distance')
    ax.set_title('The source is absent; global distinguishability remains 1')
    ax.legend(fontsize=8.5);fig.tight_layout()
    for ext in ('png','svg'):fig.savefig(figdir/f'pilot_readability_curves.{ext}',dpi=180)
    plt.close(fig)
    rows=list(csv.DictReader((root/'data/transport_control.csv').open()))
    r=[x for x in rows if int(x['n'])==6];times=sorted(set(float(x['time']) for x in r));a=np.zeros((6,len(times)));idx={v:i for i,v in enumerate(times)}
    for x in r:a[int(x['site']),idx[float(x['time'])]]=float(x['trace_distance'])
    fig,ax=plt.subplots(figsize=(7.4,4.3))
    image=ax.imshow(a,origin='lower',aspect='auto',extent=[min(times),max(times),-.5,5.5],vmin=0,vmax=1)
    ax.set_xlabel('Time after a one-excitation injection');ax.set_ylabel('Supplied chain site')
    ax.set_yticks(range(6));ax.set_title('Transport control: signal moves without redundant copying')
    fig.colorbar(image,ax=ax,label='Singleton trace distance = excitation probability');fig.tight_layout()
    for ext in ('png','svg'):fig.savefig(figdir/f'pilot_transport_control.{ext}',dpi=180)
    plt.close(fig)
    print('Created three pilot figures in PNG and SVG.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();main(a.root)
