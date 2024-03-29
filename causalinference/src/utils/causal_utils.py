import numpy as np
from scipy.stats import logistic


def random_data(N=5000, K=3, unobservables=False, **kwargs):
    """
    Function that generates data according to one of two simple models that
    satisfies the unconfoundedness assumption.

    The covariates and error terms are generated according to
        X ~ N(mu, Sigma), epsilon ~ N(0, Gamma).

    The counterfactual outcomes are generated by
        Y0 = X*beta + epsilon_0,
        Y1 = delta + X*(beta+theta) + epsilon_1.

    Selection is done according to the following propensity score function:
        P(T=1|X) = Lambda(X*beta).

    Here Lambda is the standard logistic CDF.

    Parameters
    ----------
    N: int
        Number of units to draw. Defaults to 5000.
    K: int
        Number of covariates. Defaults to 3.
    unobservables: bool
        Returns potential outcomes and true propensity score
        in addition to observed outcome and covariates if True.
        Defaults to False.
    mu, Sigma, Gamma, beta, delta, theta: NumPy ndarrays, optional
        Parameter values appearing in data generating process.

    Returns
    -------
    tuple
        A tuple in the form of (Y, T, X) or (Y, T, X, Y0, Y1) of
        observed outcomes, treatment indicators, covariate matrix,
        and potential outomces.
    """

    mu = kwargs.get('mu', np.zeros(K))
    beta = kwargs.get('beta', np.ones(K))
    theta = kwargs.get('theta', np.ones(K))
    delta = kwargs.get('delta', 3)
    Sigma = kwargs.get('Sigma', np.identity(K))
    Gamma = kwargs.get('Gamma', np.identity(2))

    X = np.random.multivariate_normal(mean=mu, cov=Sigma, size=N)
    Xbeta = X.dot(beta)
    pscore = logistic.cdf(Xbeta)
    T = np.array([np.random.binomial(1, p, size=1) for p in pscore]).flatten()

    epsilon = np.random.multivariate_normal(mean=np.zeros(2), cov=Gamma, size=N)
    Y0 = Xbeta + epsilon[:, 0]
    Y1 = delta + X.dot(beta + theta) + epsilon[:, 1]
    Y = (1 - T) * Y0 + T * Y1

    if unobservables:
        return Y, T, X, Y0, Y1, pscore
    else:
        return Y, T, X


def is_match_parenthesis(str_list):
    """
    Check if the parenthesis in the string list is matched.
    ------------------------------------------------------
    :param str_list: list of strings
    :return: True if the parenthesis is matched, False otherwise
    """
    stack = []
    for cur_str in str_list:
        if cur_str == "(":
            stack.append(str)
        elif cur_str == ")":
            if len(stack) == 0:
                return False
            stack.pop()
    if len(stack) != 0:
        return False
    return True