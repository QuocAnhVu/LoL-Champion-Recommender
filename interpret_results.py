#!./env/bin/python
# Interpret Results
# Prints out generated champion attribute data alongside the champion's name.
from model import *
from sqlalchemy import func
import numpy as np
import pdb

db = Session()

# Creates a dictionary by sorting champions by id
champ_dict = []
for champ in db.query(Champion):
    champ_dict.append((champ.champion_id, champ.champion_name))
champ_dict = sorted(champ_dict, key=lambda x: x[0])

# Loads trained champion attribute data
x = np.load(open('result_x.npy', 'rb'))

# Zips dictionary alongside attribute data to get labelled attributes
result = zip(champ_dict, x)
for c in result:
    print('{0}: {1}'.format(c[0][1], c[1].tolist()))
simple_result = [(r[0][1], r[1]) for r in result]
# pdb.set_trace()
# sorted(simple_result, key=lambda x: x[1][0])
