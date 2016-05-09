#!/usr/bin/python3
import tensorflow as tf
import retrieve_dataset
import pickle
import pdb

# Import variables from db
golden = retrieve_dataset.Retriever()
golden.shuffle()
data = golden.get_data(10000)
train_set = data[0:int(len(data) * 0.7)]
test_set = data[int(len(data) * 0.7):]
train_x, train_y = zip(*train_set)
test_x, test_y = zip(*test_set)
train_y = [(not y, y) for y in train_y]
test_y = [(not y, y) for y in test_y]


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# Define variables for nn
X = tf.placeholder(tf.float32, shape=[None, 260])
Y = tf.placeholder(tf.float32, shape=[None, 2])
theta1 = weight_variable([260, 100])
b1 = bias_variable([100])
theta2 = weight_variable([100, 2])
b2 = bias_variable([2])

# Define methods for Session
h1 = tf.nn.relu(tf.matmul(X, theta1) + b1)
H = tf.nn.softmax(tf.matmul(h1, theta2) + b2)

reg = 0.001

# Minimize error
cross_entropy = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(H) +
                                              (1-Y) * tf.log(1-H),
                                              reduction_indices=[1]) +
                               reg * (tf.reduce_sum(theta1) +
                                      tf.reduce_sum(theta2)))
optimizer = tf.train.AdamOptimizer(1e-4)
train_step = optimizer.minimize(cross_entropy)

# Calculate accuracy
correct_prediction = tf.equal(tf.argmax(H, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Save results
saver = tf.train.Saver(max_to_keep=20)

pickles = ([], [], [])

with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())
    saver.save(sess, 'tmp/validation.chkpt')

    for i in range(1000):
        train_step.run(feed_dict={X: train_x, Y: train_y})
        train_accuracy = accuracy.eval(feed_dict={X: train_x, Y: train_y})
        test_accuracy = accuracy.eval(feed_dict={X: test_x, Y: test_y})
        print("[Step {0}] Train Accuracy: {1}, Test Accuracy: {2}".
              format(i+1, train_accuracy, test_accuracy))

        # Save accuracy
        train_accuracy = accuracy.eval(feed_dict={X: train_x, Y: train_y})
        test_accuracy = accuracy.eval(feed_dict={X: test_x, Y: test_y})
        pickles[0].append(i)
        pickles[1].append(train_accuracy)
        pickles[2].append(test_accuracy)
    pickle.dump(pickles, open("pickles.pkl", "wb"))
    save_path = saver.save(sess, "tmp/2layer/model.chkpt", global_step=i)
    print("Model saved in file: %s" % save_path)

    # step_count = 100
    # step_size = int(len(train_x) / step_count)
    # for m in range(step_size, len(train_x)+1, step_size):
    #     saver.restore(sess, 'tmp/validation.chkpt')
    #     temp_x = train_x[0:m]
    #     temp_y = train_y[0:m]
    #     for i in range(200):
    #         train_step.run(feed_dict={X: temp_x, Y: temp_y})
    #         train_accuracy = accuracy.eval(feed_dict={X: temp_x, Y: temp_y})
    #         test_accuracy = accuracy.eval(feed_dict={X: test_x, Y: test_y})
    #         print("[m {0}, Step {1}] Train Accuracy: {2}, Test Accuracy: {3}"
    #               .format(m, i+1, train_accuracy, test_accuracy))
    #         # if i%1000 == 0:
    #         #   # Save the variables to disk.
    #         #   save_path = saver.save(sess, "tmp/2layer/model.chkpt", global_step=i)
    #         #   print("Model saved in file: %s" % save_path)