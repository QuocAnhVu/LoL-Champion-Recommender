

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


# Unregulated cost function for metrics
def cost(x, y, theta):
    hypothesis = np.dot(theta, np.transpose(x))
    loss = np.multiply(hypothesis, y > 0) - y
    cost = loss ** 2