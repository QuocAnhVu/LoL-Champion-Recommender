#!./env/bin/python
import numpy as np
import numpy.random as random
from scipy.optimize import minimize


def unpack(theta_and_x, n, m_users, m_champs):
    theta_len = m_users * n
    theta = theta_and_x[0:theta_len].reshape((m_users, n))
    x = theta_and_x[theta_len:].reshape((m_champs, n))
    return (theta, x)


def gen_costfn(y, lamb, n, m_users, m_champs):
    def costfn(theta_and_x):
        theta, x = unpack(theta_and_x, n, m_users, m_champs)
        hypothesis = np.dot(theta, x.T)
        loss = np.multiply(hypothesis, y > 0) - y
        reg = lamb * (np.sum(x ** 2) + np.sum(theta ** 2))
        cost = np.sum(loss ** 2) + reg
        return cost
    return costfn


def train_recommender(y, lamb, n):
    m_users = y.shape[0]
    m_champs = y.shape[1]

    init_flat_theta = random.sample((m_users, n)).flatten() / 1000
    init_flat_x = random.sample((m_champs, n)).flatten() / 1000
    init_theta_and_x = np.concatenate((init_flat_x, init_flat_theta))

    costfn = gen_costfn(y, lamb, n, m_users, m_champs)

    theta_and_x = minimize(costfn, init_theta_and_x, method='BFGS',
                           options={'xtol': 1e-8, 'disp': True})
    theta, x = unpack(theta_and_x)
    return (theta, x)

dataset = np.load(open('tmp/dataset_normal.npy', 'rb'))[0:100]
lamb = 0.1
feature_count = 16
theta, x = train_recommender(dataset, lamb, feature_count)

np.save(open('tmp/trained_x.npy', 'wb'), x)
np.save(open('tmp/trained_theta.npy', 'wb'), theta)
