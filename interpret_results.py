#!./env/bin/python
# Interpret Results
# Prints out generated champion attribute data alongside the champion's name.
from model import *
from sqlalchemy import func
import numpy as np
import pdb

# Create list of champion names sorted by champion id
db = Session()
champions = list(zip(*db.query(Champion.champion_name).order_by(Champion.champion_id).all()))[0]

x = []
for i in range(10):
    x_i = np.load(open("trainedX_%i.npy" % i, "rb"))
    x.append(x_i)


avgs = np.average(x, axis=2).T  # average of all features for each run
list(zip(champions, np.std(avgs, axis=1)))

# # Loads trained champion attribute data
# x = np.load(open('result_x.npy', 'rb'))

# # Zips dictionary alongside attribute data to get labelled attributes
# result = zip(champions, x)
# for c in result:
#     print('{0}: {1}'.format(c[0][1], c[1].tolist()))
# simple_result = [(r[0][1], r[1]) for r in result]
# # pdb.set_trace()
# # sorted(simple_result, key=lambda x: x[1][0])
