# LoL-Champion-Recommender
Use your Champion Mastery Points to determine which other champions you would enjoy playing.

This recommender system is trained with a collaborative filtering, gradient descent algorithm.

# How To Train Recommender
1) Create a virtualenv directory called `env/`: `virtualenv env`

2) Install requirements specified in .requirements: `env/bin/pip install -r .requirements`. The *scipy* stack
will require some build dependencies. These scripts only use *postgres* for the caching db.

3) Create `secret_keys.py` and fill in the information. 

4) Run `model.py` to generate schema.

5) Run `populate_mastery_dataset.py` to populate db with data from Riot's API.

6) Run `preprocess_dataset.py` to convert db data to numpy objects and normalize the dataset. 
This step will generate `dataset_raw.npy` and `dataset_normal.npy`.

7) Run `train_recommender.py` to generate x (champion features) and theta (dataset user preferences).
This step will generate `result_x.npy`, `result_x.json`, `result_theta.npy`, and `result_theta.json`.

8) Predict with `predict_preferences.py` using arguments: region then summoner name. 
Ex: `$ ./predict_preferences NA Bjergsen`