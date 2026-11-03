"""Deterministic numerical check for the Hamiltonian section (Project 10).
Execute from the repository root with python experiments/hamiltonian_benchmark.py.
Tables go to experiments/ and figures to paper/figures/, replacing prior outputs.
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parent.parent
figures=root/'paper'/'figures'
figures.mkdir(parents=True, exist_ok=True)
omega=1.0
h=0.1
N=1000
q0,p0=1.0,0.0
qE,pE=q0,p0
qV,pV=q0,p0
rows=[]
for n in range(N+1):
    t=n*h
    Eexact=0.5*(q0**2*omega**2+p0**2)
    Ee=0.5*(omega**2*qE*qE+pE*pE)
    Ev=0.5*(omega**2*qV*qV+pV*pV)
    Etilde=0.5*(pV*pV+omega**2*(1-omega**2*h*h/4)*qV*qV)
    rows.append((n,t,Eexact,Ee,Ev,Etilde,qE,pE,qV,pV))
    # simultaneous explicit Euler step
    qE,pE=qE+h*pE,pE-h*omega**2*qE
    # velocity Verlet kick drift kick
    ph=pV-(h/2)*omega**2*qV
    qV=qV+h*ph
    pV=ph-(h/2)*omega**2*qV
with (root/'experiments'/'hamiltonian_energy.csv').open('w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['step','time','exact_energy','euler_energy','verlet_energy','verlet_modified_energy','euler_q','euler_p','verlet_q','verlet_p'])
    w.writerows(rows)
R=np.array(rows)
fig,ax=plt.subplots(figsize=(8,4.2))
ax.semilogy(R[:,1],R[:,3],label='Explicit Euler: true energy')
ax.semilogy(R[:,1],R[:,4],label='Velocity Verlet: true energy')
ax.semilogy(R[:,1],R[:,5],label='Velocity Verlet: modified energy',linestyle='--')
ax.axhline(0.5,linestyle=':',color='black',label='Exact energy')
ax.set(xlabel='Time',ylabel='Energy (logarithmic scale)',title='Harmonic oscillator: geometric versus non-symplectic integration')
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(figures/'hamiltonian_energy.pdf')
fig.savefig(figures/'hamiltonian_energy.png',dpi=180)
plt.close(fig)

m=(R[:,1]<=20)
fig,ax=plt.subplots(figsize=(6.6,4.5))
ax.plot(R[m,6],R[m,7],label='Explicit Euler',alpha=.9)
ax.plot(R[m,8],R[m,9],label='Velocity Verlet',alpha=.9)
q0v=np.cos(np.linspace(0,20,1000));p0v=-np.sin(np.linspace(0,20,1000))
ax.plot(q0v,p0v,'k--',label='Exact orbit',alpha=.7)
ax.set(xlabel='q',ylabel='p',title='Phase-space trajectories over 20 time units')
ax.set_aspect('equal','box'); ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(figures/'hamiltonian_phase.pdf')
fig.savefig(figures/'hamiltonian_phase.png',dpi=180)
plt.close(fig)
summary={
'h':h, 'N':N, 'T':N*h, 'exact_energy':R[0,2],
'euler_final_energy':R[-1,3], 'verlet_final_energy':R[-1,4],
'euler_energy_relative_drift':abs(R[-1,3]-0.5)/0.5,
'verlet_max_energy_abs_error':max(abs(R[:,4]-0.5)),
'verlet_max_modified_energy_abs_drift':max(abs(R[:,5]-R[0,5]))}
import json
(root/'experiments'/'hamiltonian_summary.json').write_text(json.dumps(summary,indent=2))
print(summary)
