import numpy as np
from probflow.gaussian import CoupledOU, gaussian_kl
from probflow.projected import solve_projected_moments, equilibrium_closure_moments
from probflow.learning import fit_conditional_y_given_x, inferred_drift


def test_equilibrium_covariance_and_conditional():
    model=CoupledOU(a=1.2,c=2,kappa=1.4,beta=2)
    cov=model.invariant_cov
    np.testing.assert_allclose(model.H@cov,np.eye(2)/model.beta,atol=1e-12)
    np.testing.assert_allclose(cov[0,0],1/(model.beta*model.a),atol=1e-12)
    np.testing.assert_allclose(cov[1,0]/cov[0,0],model.kappa,atol=1e-12)


def test_time_dependent_projection_mimics_one_time_marginals():
    model=CoupledOU()
    m0=np.array([-1.,.8]); C0=np.diag([.2,.15]); times=np.linspace(0,4,81)
    m,v=solve_projected_moments(model,times,m0,C0)
    exact=[model.moments(float(t),m0,C0) for t in times]
    np.testing.assert_allclose(m,[e[0][0] for e in exact],atol=1e-8)
    np.testing.assert_allclose(v,[e[1][0,0] for e in exact],atol=1e-8)
    me,ve=equilibrium_closure_moments(model,times,m0,C0)
    assert np.max(np.abs(me-m))>0.05
    assert np.max(np.abs(ve-v))>0.005


def test_correlation_mismatch_and_gaussian_kl():
    model=CoupledOU()
    assert abs(model.stationary_correlation(.8)-model.free_energy_correlation(.8))>0.005
    assert gaussian_kl(0,1,0,1)==0
    assert gaussian_kl(0,1,1,1)>0


def test_learned_conditional_drift():
    rng=np.random.default_rng(3)
    model=CoupledOU()
    m0=np.array([-1.,.8]); C0=np.diag([.2,.15]); t=0.7
    mean,cov=model.moments(t,m0,C0)
    pairs=rng.multivariate_normal(mean,cov,size=100_000)
    intercept,slope=fit_conditional_y_given_x(pairs[:,0],pairs[:,1])
    learned=np.array(inferred_drift(model,intercept,slope))
    exact=np.array(model.projected_coefficients(t,m0,C0))
    np.testing.assert_allclose(learned,exact,atol=.07)
