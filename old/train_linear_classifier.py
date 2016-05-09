#!/usr/bin/python3
import sqlite3
# from sklearn import svm
from sklearn import linear_model as lm
import matplotlib.pyplot as plt
import retriever

# Initialize resources
# clf = svm.SVC(random_state=1234)
clf = lm.LogisticRegression(max_iter=1000, n_jobs=-1)
test_x = data.test_x
test_y = data.test_y
train_x = data.train_x
train_y = data.train_y

# Create validation curve
x_axis = []
test_set_scores = []
train_set_scores = []
steps = 40
for m in range(1000, len(train_x), int(len(train_x) / steps)):
    clf.fit(train_x[0:m], train_y[0:m])
    x_axis.append(m)
    test_set_scores.append(clf.score(test_x, test_y))
    train_set_scores.append(clf.score(train_x[0:m], train_y[0:m]))
plt.plot(x_axis, test_set_scores, 'b')
plt.plot(x_axis, train_set_scores, 'r')
plt.show()
