#!./env/bin/python
# Predict Preferences
# Algorithm: linear, gradient descent
# Generates the input user's preferences based on previously generated
# champion attribute data and user's champion masteries.
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


def predict(summ_region, summ_name):
    # Set up libraries, load saved x
    x = np.load(open('result_x.npy', 'rb'))
    api.set_api_key(keys.riotapikey)
    api.set_region(summ_region)

    # TODO: Handle unicode characters in summoner names
    # Retrieve summoner
    summ_name_key = summ_name.lower().replace(' ', '')
    summ = api.get_summoners_by_name(summ_name)[summ_name_key]

    # Create template summoner w/ empty ratings
    db = Session()
    champ_dict = {}
    for champ in db.query(Champion):
        champ_dict[champ.champion_id] = 0

    # Fill in template summoner w/ specified summoner champion points
    masteries = api.get_champion_masteries(summ.id)
    for m in masteries:
        champ_dict[m.championId] = m.championPoints
    y_raw = [champ_dict[champ_id] for champ_id in sorted(champ_dict.keys())]

    # Normalize summoner champion points
    y_raw = np.asarray(y_raw)
    y_std = np.std(y_raw)
    y = y_raw / y_std

    # Train theta for user
    lamb = .1
    alpha = .0001
    iterations = 2000
    feature_count = len(x[0])
    init_theta = np.random.random_sample((1, feature_count))
    theta = train_theta(x, y, init_theta, lamb, alpha, iterations)

    # Create champ_id: champ_name dictionary
    champ_dict = []
    for champ in db.query(Champion):
        champ_dict.append((champ.champion_id, champ.champion_name))
    champ_dict = sorted(champ_dict, key=lambda x: x[0])

    # Make predictions and print formatted results
    h = np.dot(theta, x.T)
    champ_ids, champ_names = zip(*champ_dict)
    predictions = zip(champ_names, h[0])
    predictions = sorted(predictions, key=lambda x: x[1])
    return predictions

if(len(sys.argv) > 1):
    summ_region = sys.argv[1]
    summ_name = sys.argv[2]
    predictions = predict(summ_region, summ_name)
    print(predictions)
