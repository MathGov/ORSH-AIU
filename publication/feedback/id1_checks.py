import numpy as np
from math import comb, log, sqrt
from scipy.linalg import expm
# 1. Hoeffding interval for primary row, z in [-1,1], N=96, alpha=0.05
N=96; h=sqrt(2*log(2/0.05)/N); print('Hoeffding half-width', round(h,6), 'interval', round(-0.015225-h,6), round(-0.015225+h,6))
print('units needed for Hoeffding half-width 0.015:', int(np.ceil(2*log(40)/0.015**2)))
# 2. exact two-sided sign tests for the four rows (no ties reported)
def sign_p(k,n):
    lo=min(k,n-k); p=sum(comb(n,i) for i in range(lo+1))/2**n; return min(1,2*p)
for lab,pos,neg in [('n4 native',61,35),('n4 rotated',18,78),('n6 native',65,31),('n6 rotated (primary)',28,68)]:
    print(f'{lab:22s} pos {pos} neg {neg}  exact two-sided sign-test p = {sign_p(pos,pos+neg):.2e}')
# 3. arithmetic in section 3.1
dL0,dC0,dL1,dC1=0.208408,0.166667,0.197702,0.186411
g0=dL0-dC0; g1=dL1-dC1; print('gap0',round(g0,6),'gap1',round(g1,6),'half change',round((g1-g0)/2,6))
# 4. transport control: one-excitation hopping, XX exchange (XX+YY)/2 -> hopping amplitude 1
for n,tq,claim in [(4,2.80,0.972655),(6,3.95,0.911536)]:
    Hh=np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1)
    ts=np.round(np.arange(0,6.0001,0.05),2)
    p=[abs(expm(-1j*Hh*t)[n-1,0])**2 for t in ts]
    i=int(np.argmax(p)); pq=abs(expm(-1j*Hh*tq)[n-1,0])**2
    # time above 0.8 around the peak
    above=[t for t,v in zip(ts,p) if v>=0.8]
    print(f'n={n}: |f|^2 at t={tq}: {pq:.6f} (log {claim}); grid max {max(p):.6f} at t={ts[i]}; grid times with p>=0.8: {above[:1]}..{above[-1:] if above else None} count {len(above)}')
# two-site: recipient distinguishability sin^2 t
print('two-site p at pi/2:', abs(expm(-1j*np.array([[0,1],[1,0]])*np.pi/2)[1,0])**2)
