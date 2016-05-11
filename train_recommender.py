#!./env/bin/python
# Train Recommender
# Algorithm: collaborative filtering, linear, gradient descent
# Trains recommender system using previously formatted dataset.
import numpy as np
from matplotlib import pyplot as plt
import json


# Simultaneously trains x and theta using collaborative filtering
def gradientDescent(x, y, theta, lamb, alpha, m, steps):
    cost_iteration_curve = []
    for step in range(steps):
        print("Step %i" % step)
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

# Load dataset
dataset = np.load(open('dataset_normal.npy', 'rb'))
m_users = dataset.shape[0]
m_champs = dataset.shape[1]

# Set gradient descent variables
n = 16  # Number of champion features to train for
lamb = .1  # Regularization strength
alpha = .0001  # Amount of change per gradient descent step
steps = 20000  # Amount of gradient descent steps per run
iterations = 10  # Amount of times to run algorithm
m = None  # Specify subset of dataset to use. None means include entire dataset
temp_dataset = dataset[0:m]

# Repeat training step `iterations` times
for iteration in range(iterations):
    print("Iteration %i" % iteration)
    # Train recommender
    init_theta = (np.random.random_sample((m_users, n)) - 0.5) / 1000
    init_x = (np.random.random_sample((m_champs, n)) - 0.5) / 1000
    curve, x, theta = gradientDescent(init_x, temp_dataset, init_theta,
                                      lamb, alpha, len(temp_dataset), steps)

    # Save data as npy for future loading and json for browser usage
    json.dump(x.tolist(), open('trainedX_%i.json' % iteration, 'w'))
    np.save(open('trainedX_%i.npy' % iteration, 'wb'), x)

    # Plot cost-iteration curve
    plt.plot(curve)
plt.show()
