#!/usr/bin/python3
import pickle
import matplotlib.pyplot as plt

# Create validation curve
pickles = pickle.load(open("pickles.pkl", "rb"))
x_axis = pickles[0]
train_set_scores = pickles[1]
test_set_scores = pickles[2]
plt.plot(x_axis, train_set_scores, 'b', label="train")
plt.plot(x_axis, test_set_scores, 'r', label="test")
plt.legend()
plt.show()
