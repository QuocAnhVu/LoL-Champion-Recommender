#!./env/bin/python
# Preprocess Dataset
# Normalizes data by dividing by standard deviation
# Converts data to numpy array for vectorization
from model import *
from sqlalchemy import func
import numpy as np

# Setup session
db = Session()
summ_count = db.query(func.count('*')).select_from(Summoner).scalar()
champ_count = db.query(func.count('*')).select_from(Champion).scalar()

# Convert dataset from psql rows to python arrays
dataset = []
seed_dict = {}
for champ in db.query(Champion):
    seed_dict[champ.champion_id] = 0
for summ in db.query(Summoner):
    print(summ.summoner_name)
    summ_dict = dict(seed_dict)  # Copies seed node
    mastery_query = db.query(ChampionMastery.champion_id, ChampionMastery.champion_points).filter(summ.summoner_id==ChampionMastery.summoner_id)
    for champ_id, summ_mastery in mastery_query:
        summ_dict[champ_id] = summ_mastery
    summ_mastery = [summ_dict[champ_id] for champ_id in sorted(summ_dict.keys())]
    dataset.append(summ_mastery)

# Convert dataset from python object to numpy matrix
data_np = np.asmatrix(dataset)
np.save(open('dataset_raw.npy', 'wb'), data_np)

# Normalize data
data_np = np.load(open('dataset_raw.npy', 'rb'))
data_np = np.asmatrix(data_np)
# avgs = np.average(data_np, axis=1)
stds = np.std(data_np, axis=1)
# avgs = np.dot(avgs, np.ones((1, champ_count)))
stds = np.dot(stds, np.ones((1, champ_count)))
normal_data_np = np.divide(data_np, stds)
np.save(open('dataset_normal.npy', 'wb'), normal_data_np)
