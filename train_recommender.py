#!./env/bin/python
import numpy as np
from sqlalchemy import func
from model import *
from matplotlib import pyplot as plt
import json


def gradientDescent(x, y, theta, lamb, alpha, m, numIterations):
    cost_iteration_curve = []
    for i in range(numIterations):
        hypothesis = np.dot(theta, x.T)
        loss = np.multiply(hypothesis, y > 0) - y

        x = x - alpha * (np.dot(loss.T, theta) + lamb * x)
        theta = theta - alpha * (np.dot(loss, x) + lamb * theta)

        x_reg = np.sum(x) ** 2 / x.size
        theta_reg = np.sum(theta) ** 2 / theta.size
        cost_reg = lamb * (x_reg + theta_reg)
        cost = np.sum(loss) ** 2 + cost_reg
        cost_iteration_curve.append(cost)
    return (cost_iteration_curve, x, theta)


def cost(x, y, theta):
    hypothesis = np.dot(theta, np.transpose(x))
    loss = np.multiply(hypothesis, y > 0) - y
    cost = loss ** 2

db = Session()
summ_count = db.query(func.count('*')).select_from(Summoner).scalar()
champ_count = db.query(func.count('*')).select_from(Champion).scalar()
dataset = np.load(open('dataset_normal.npy', 'rb'))

# Validation Curve
# validation_curve = []
# for m in xrange(100, 7100, 100):
#     temp_dataset = dataset[0:m]
#     temp_dataset = dataset[0:100]
#     feature_count = 16
#     lamb = .1
#     alpha = .0001
#     init_x = np.random.random_sample((champ_count, feature_count))
#     theta = np.random.random_sample((len(temp_dataset), feature_count))
#     curve, x, theta = gradientDescent(init_x, temp_dataset, init_theta,
#                                       lamb, alpha, len(temp_dataset), 1000)
#     validation_curve.append(cost(x, temp_dataset, theta))
# plt.plot(validation_curve)

# Normal Training
m = None
feature_count = 16
lamb = .1
alpha = .0001
temp_dataset = dataset[0:m]
init_x = np.random.random_sample((champ_count, feature_count))
init_theta = np.random.random_sample((len(temp_dataset), feature_count))
curve, x, theta = gradientDescent(init_x, temp_dataset, init_theta,
                                  lamb, alpha, len(temp_dataset), 1000)
plt.plot(curve[100:])  # Initial cost is much higher than end

json.dump(x.tolist(), open('result_x.json', 'wb'))
json.dump(theta.tolist(), open('result_theta.json', 'wb'))
np.save(open('result_x.npy', 'wb'), x)
np.save(open('result_theta.npy', 'wb'), theta)

plt.show()
