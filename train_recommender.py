#!./env/bin/python
import numpy as np
from sqlalchemy import func
from model import *
from matplotlib import pyplot as plt
import json


def gradientDescent(x, y, theta, lamb, alpha, m, numIterations):
    cost_iteration_curve = []
    for i in range(numIterations):
        hypothesis = np.dot(theta, np.transpose(x))
        loss = np.multiply(hypothesis, y > 0) - y

        x = x - alpha * (np.dot(loss.T, theta) + lamb * x)
        theta = theta - alpha * (np.dot(loss, x) + lamb * theta)

        costReg = lamb * (np.sum(x) ** 2 + np.sum(theta) ** 2)
        cost = np.sum(loss) ** 2
        cost_iteration_curve.append(cost)
    return (cost_iteration_curve, x, theta)


def cost(x, y, theta):
    hypothesis = np.dot(theta, np.transpose(x))
    loss = np.multiply(hypothesis, y > 0) - y
    cost = loss ** 2

db = Session()
summ_count = db.query(func.count('*')).select_from(Summoner).scalar()
champ_count = db.query(func.count('*')).select_from(Champion).scalar()

validation_curve = []
dataset = np.load(open('dataset_normal.npy', 'rb'))
# for m in xrange(100, 7100, 100):
    # temp_dataset = dataset[0:m]
temp_dataset = dataset[0:100]
FEATURE_COUNT = 16
x = np.random.random_sample((champ_count, FEATURE_COUNT))
theta = np.random.random_sample((len(temp_dataset), FEATURE_COUNT))
curve, x, theta = gradientDescent(x, temp_dataset, theta, .1, .0001, len(temp_dataset), 1000)
validation_curve.append(cost(x, temp_dataset, theta))

print(x)
print(theta)
json.dump(x.tolist(), open('result_x.json', 'wb'))
json.dump(theta.tolist(), open('result_theta.json', 'wb'))
np.save(open('result_x.npy', 'wb'), x)
np.save(open('result_theta.npy', 'wb'), theta)
# plt.plot(curve[100:])
plt.plot(curve)
plt.show()
