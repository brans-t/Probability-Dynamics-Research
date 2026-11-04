"""Reproducible Chapter 1 experiments. Python 3.11; NumPy, SciPy, Matplotlib, PyTorch."""
import csv, json, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from _paths import FIGURES as FIG, RESULTS as OUT
SEED=20261102
rng=np.random.default_rng(SEED)

# 1. Time-dependent, noncommuting matrix A(t).
def A(t):
    return np.array([[-.25, 1.+t],[-.6+.3*t, .10]],dtype=float)
def rk4_U(N):
    h=1./N; U=np.eye(2)
    for k in range(N):
        t=k*h
        k1=A(t)@U; k2=A(t+h/2)@(U+h*k1/2)
        k3=A(t+h/2)@(U+h*k2/2); k4=A(t+h)@(U+h*k3)
        U=U+h*(k1+2*k2+2*k3+k4)/6
    return U
def euler_U(N):
    h=1./N; U=np.eye(2)
    for k in range(N): U=(np.eye(2)+h*A(k*h))@U
    return U
Uref=solve_ivp(lambda t,y: (A(t)@y.reshape(2,2)).ravel(),[0,1],np.eye(2).ravel(),rtol=1e-13,atol=1e-14).y[:,-1].reshape(2,2)
true_det=np.exp(-.15)
assert abs(np.linalg.det(Uref)-true_det)<1e-10
Nvals=[8,16,32,64,128]
det_rows=[]
for N in Nvals:
    eu=np.linalg.det(euler_U(N)); rk=np.linalg.det(rk4_U(N))
    det_rows.append({'N':N,'h':1/N,'Euler_det':eu,'Euler_error':abs(eu-true_det),'RK4_det':rk,'RK4_error':abs(rk-true_det)})
with open(OUT/'jacobian_convergence.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=det_rows[0]);w.writeheader();w.writerows(det_rows)
fig,ax=plt.subplots(figsize=(6.1,4.2));
for method in ('Euler','RK4'):
    ax.loglog([r['h'] for r in det_rows],[r[f'{method}_error'] for r in det_rows],'-o',label=method)
ax.set_xlabel('Step size h'); ax.set_ylabel('Absolute error in det U(1,0)');ax.set_title('Jacobian determinant convergence');ax.legend();ax.grid(True,alpha=.25,which='both')
fig.tight_layout();fig.savefig(FIG/'jacobian_convergence.pdf');plt.close(fig)

def integralA(): return np.array([[-.25,1.5],[-.45,.10]])
false_error=np.linalg.norm(Uref-expm(integralA()),ord='fro')
comm=np.linalg.norm(A(0)@A(1)-A(1)@A(0),ord='fro')

# 2. A coupled stationary OU process: exactly matching one-time marginals, unequal correlations.
a,c,kappa,beta=.8,1.7,1.1,1.
K=np.array([[a+c*kappa**2,-c*kappa],[-c*kappa,c]])
Sinf=np.linalg.inv(K)/beta
ts=np.linspace(0,4,180)
Cfull=np.array([(expm(-K*t)@Sinf)[0,0] for t in ts])
Cclosure=Sinf[0,0]*np.exp(-a*ts)
fig,ax=plt.subplots(figsize=(6.1,4.2))
ax.plot(ts,Cfull,label='Microscopic 2D OU projected on X',lw=2)
ax.plot(ts,Cclosure,'--',label='Equilibrium Markov closure',lw=2)
ax.set_xlabel('Time lag t');ax.set_ylabel('Stationary covariance C(t)');ax.set_title('Equal marginals, different temporal correlations')
ax.legend();ax.grid(True,alpha=.25);fig.tight_layout();fig.savefig(FIG/'ou_correlation.pdf');plt.close(fig)

# 3. Conditional drift regression: fixed-time Gaussian slices, held-out true conditional-mean target.
import torch
from torch import nn
torch.manual_seed(SEED)
torch.set_num_threads(2)
m0=np.array([1.,-.8]);S0=np.diag([.12,.25]);times=np.array([.25,.5,1.,2.])
params=[]
for t in times:
    E=expm(-K*t); m=E@m0;S=Sinf+E@(S0-Sinf)@E
    g_slope=S[1,0]/S[0,0];g_intercept=m[1]-g_slope*m[0]
    params.append((m,S,g_slope,g_intercept))

def sample(n):
    # evenly allocate per time, shuffle
    ids=rng.integers(0,len(times),size=n)
    Z=np.zeros((n,2));Y=np.zeros((n,1));Tgt=np.zeros((n,1))
    for j,(m,S,k,b) in enumerate(params):
        mask=ids==j;nj=int(mask.sum())
        if nj:
            vals=rng.multivariate_normal(m,S,size=nj)
            Z[mask]=np.column_stack((np.full(nj,times[j]),vals[:,0]))
            Y[mask,0]=vals[:,1]
            Tgt[mask,0]=k*vals[:,0]+b
    perm=rng.permutation(n)
    return Z[perm].astype('float32'),Y[perm].astype('float32'),Tgt[perm].astype('float32')

Ztest,Ytest,target=sample(12000)

def train_nn(n,epochs=260):
    Z,Y,_=sample(n)
    # feature transformation t remains explicit; standardize both using training data
    xm=Z.mean(axis=0);xs=Z.std(axis=0)
    ym=Y.mean(axis=0);ys=Y.std(axis=0)
    inp=torch.tensor((Z-xm)/xs);outs=torch.tensor((Y-ym)/ys)
    model=nn.Sequential(nn.Linear(2,48),nn.Tanh(),nn.Linear(48,48),nn.Tanh(),nn.Linear(48,1))
    opt=torch.optim.Adam(model.parameters(),lr=.008)
    for ep in range(epochs):
        permutation=torch.randperm(n)
        for batch in permutation.split(256):
            pred=model(inp[batch]); loss=((pred-outs[batch])**2).mean()
            opt.zero_grad();loss.backward();opt.step()
    with torch.no_grad():
        pred=model(torch.tensor((Ztest-xm)/xs)).numpy()*ys+ym
    return pred.ravel()

ml_rows=[];preds={}
# Affine regression constrained by the Gaussian conditional structure (physics-informed baseline).
affine_rows=[]
for n in [512,4096]:
    ztr,ytr,_=sample(n)
    predicted=np.zeros(len(Ztest),dtype=float)
    for j,t in enumerate(times):
        tr=ztr[:,0]==t; te=Ztest[:,0]==t
        design=np.column_stack((np.ones(tr.sum()),ztr[tr,1]))
        coef=np.linalg.lstsq(design,ytr[tr,0],rcond=None)[0]
        predicted[te]=coef[0]+coef[1]*Ztest[te,1]
    e=float(np.sqrt(np.mean((predicted-target.ravel())**2)))
    affine_rows.append({'train_samples':n,'conditional_mean_RMSE':e,'projected_drift_RMSE':abs(c*kappa)*e})
with open(OUT/'affine_regression.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=affine_rows[0]);w.writeheader();w.writerows(affine_rows)
for n in [512,4096]:
    pr=train_nn(n)
    gerr=np.sqrt(np.mean((pr-target.ravel())**2))
    drift_err=abs(c*kappa)*gerr
    raw_y_rmse=np.sqrt(np.mean((pr-Ytest.ravel())**2))
    ml_rows.append({'train_samples':n,'test_samples':len(Ztest),'conditional_mean_RMSE':float(gerr),'projected_drift_RMSE':float(drift_err),'noisy_Y_RMSE':float(raw_y_rmse)})
    preds[n]=pr
with open(OUT/'conditional_regression.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=ml_rows[0]);w.writeheader();w.writerows(ml_rows)
# plot t=1 conditional mean vs model on grid
ix=2;t=times[ix];m,S,k,b=params[ix]
xg=np.linspace(-2.1,2.1,180);zg=np.column_stack((np.full(len(xg),t),xg)).astype('float32')
# Need recover model predictions on grid; retrain n=4096? Instead plot scatter using held-out at t=1.
mask=Ztest[:,0]==t
fig,ax=plt.subplots(figsize=(6.1,4.2))
inds=np.flatnonzero(mask)[::13]
ax.scatter(Ztest[inds,1],preds[4096][inds],s=8,alpha=.45,label='Neural prediction (held-out)')
ax.plot(xg,k*xg+b,lw=2,color='black',label='Exact conditional mean')
ax.set_xlabel('Collective variable x');ax.set_ylabel('E[Y | X=x, t=1]')
ax.set_title('Learning a conditional coefficient for the projected dynamics')
ax.legend();ax.grid(True,alpha=.25);fig.tight_layout();fig.savefig(FIG/'conditional_regression.pdf');plt.close(fig)

# 4. Semidiscrete continuous-time Markov approximation: exactly stochastic (mass/positive) under exp(Q t).
from scipy.sparse import diags
from scipy.sparse.linalg import expm_multiply
D=.5;N=60;h=1./N;x=(np.arange(N)+.5)*h; V=2*(x-.3)**2+0.7*x
fwd=D/h**2*np.exp(-(V[1:]-V[:-1])/(2*D))
bwd=D/h**2*np.exp((V[1:]-V[:-1])/(2*D))
Q=np.zeros((N,N))
for i in range(N-1):
    Q[i+1,i]+=fwd[i];Q[i,i]-=fwd[i]
    Q[i,i+1]+=bwd[i];Q[i+1,i+1]-=bwd[i]
pi=np.exp(-V/D);pi/=pi.sum()
m=np.exp(-((x-.75)/.11)**2);m/=m.sum()
markov_rows=[]
for t in [0.,.015,.05,.2,.5]:
    mt=expm_multiply(Q*t,m)
    kl=float(np.dot(mt,np.log(mt/pi)))
    markov_rows.append({'time':t,'mass':float(mt.sum()),'minimum_cell_mass':float(mt.min()),'KL_to_pi':kl})
with open(OUT/'markov_semidiscrete.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=markov_rows[0]);w.writeheader();w.writerows(markov_rows)

results={'seed':SEED,'K':K.tolist(),'Sigma_infinity':Sinf.tolist(),'det_exact':true_det,'matrix_exponential_false_frobenius_error':false_error,'A_commutator_frobenius_norm':comm,'Jacobian':det_rows,'ML':ml_rows,'Affine':affine_rows,'Markov':markov_rows,'OU_Cfull_t1':float((expm(-K)@Sinf)[0,0]),'OU_Cclosure_t1':float(Sinf[0,0]*np.exp(-a))}
(OUT/'results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
