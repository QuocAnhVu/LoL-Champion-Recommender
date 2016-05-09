#!./env/bin/python
import numpy as np
import sys
from cassiopeia import baseriotapi as api
import secret_keys as keys
from model import *


# Train theta (user preferences)
def train_theta(x, y, theta, lamb, alpha, numIterations):
    for i in range(numIterations):
        hypothesis = np.dot(theta, np.transpose(x))
        loss = np.multiply(hypothesis, y > 0) - y
        theta = theta - alpha * (np.dot(loss, x) + lamb * theta)
    return theta

# Set up libraries, load saved x & load args
x = np.load(open('result_x.npy', 'rb'))
summ_region = sys.argv[1]
summ_id = int(sys.argv[2])
api.set_api_key(keys.riotapikey)
api.set_region(summ_region)

# Create template user w/ empty ratings
db = Session()
champ_dict = {}
for champ in db.query(Champion):
    champ_dict[champ.champion_id] = 0

# Fill in template user w/ summoner champion points
masteries = api.get_champion_masteries(summ_id)
for m in masteries:
    champ_dict[m.championId] = m.championPoints
m_list = [champ_dict[champ_id] for champ_id in sorted(champ_dict.keys())]
y = np.asarray(m_list)

# Train theta for user
lamb = .1
alpha = .0001
iterations = 1000
feature_count = len(x[0])
init_theta = np.random.random_sample((1, feature_count))
theta = train_theta(x, y, init_theta, lamb, alpha, iterations)

print(theta)
