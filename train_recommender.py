#!./env/bin/python
# Train Recommender
# Algorithm: collaborative filtering, linear, gradient descent
# Trains recommender system using previously formatted dataset.
import numpy as np
from matplotlib import pyplot as plt
# import json


# Simultaneously trains x and theta using collaborative filtering
def gradientDescent(x, y, theta, lamb, alpha, steps):
    # Precompute regularization terms
    x_reg = np.sum(x) ** 2 / x.size
    theta_reg = np.sum(theta) ** 2 / theta.size
    cost_reg = lamb * (x_reg + theta_reg)
    grad_x_reg = lamb * x
    grad_theta_reg = lamb * theta

    # Run training iterations
    cost_iteration_curve = []
    for step in range(steps):
        # Print progress
        if ((step+1) % 1000) == 0:
            print("Step %i/%i" % (step+1, steps))

        # Calculate error
        hypothesis = np.dot(theta, x.T)
        loss = np.multiply(hypothesis, y > 0) - y

        # Update variables
        x = x - alpha * (np.dot(loss.T, theta) + grad_x_reg)
        theta = theta - alpha * (np.dot(loss, x) + grad_theta_reg)

        # Track costs
        cost = np.sum(loss) ** 2 + cost_reg
        cost_iteration_curve.append(cost)
    return (cost_iteration_curve, x, theta)

# Load dataset
dataset = np.load(open('tmp/dataset_normal.npy', 'rb'))
m_users = dataset.shape[0]
m_champs = dataset.shape[1]

# Set gradient descent variables
n = 16  # Number of champion features to train for
lamb = .1  # Regularization strength
alpha = .0001  # Amount of change per gradient descent step
steps = 20000  # Amount of gradient descent steps per run
iterations = 100  # Amount of times to run algorithm
m = None  # Specify subset of dataset to use. None means include entire dataset
temp_dataset = dataset[0:m]

# Repeat training step `iterations` times
x_list = []
for iteration in range(iterations):
    print("Iteration %i/%i" % (iteration+1, iterations))
    # Train recommender
    init_theta = (np.random.random_sample((m_users, n)) - 0.5) / 1000
    init_x = (np.random.random_sample((m_champs, n)) - 0.5) / 1000
    curve, x, theta = gradientDescent(init_x, temp_dataset, init_theta,
                                      lamb, alpha, steps)
    x_list.append(x)
    # Save data as npy for future loading and json for browser usage
    # json.dump(x.tolist(), open('tmp/trainedX_%i.json' % iteration, 'w'))
    np.save(open('tmp/trainedX_%i.npy' % iteration, 'wb'), x)

    # Save average of each iteration THUS FAR
    x_avg = np.average(x_list, axis=0)
    # json.dump(x_avg.tolist(), open('tmp/trainedX_avg.json', 'w'))
    np.save(open('tmp/trainedX_avg.npy', 'wb'), x_avg)

    # Plot cost-iteration curve
    plt.plot(curve)

# Examine validity of each run
plt.show()
