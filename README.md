# LoL-Champion-Recommender
Use your Champion Mastery Points to determine which other champions you would enjoy playing.

This recommender system is trained with a collaborative filtering, gradient descent algorithm.

# How To Train Recommender
1) Install requirements specified in .requirements: `pip install -r .requirements`. The *scipy* stack
will require some build dependencies. These scripts only use *postgres* for the caching db.

2) Create `secret_keys.py` and fill in the information. 

3) Run `model.py` to generate schema.

4) Run `populate_mastery_dataset.py` to populate db with data from Riot's API.

5) Run `preprocess_dataset.py` to convert db data to numpy objects and normalize the dataset. 
This step will generate `dataset_raw.npy` and `dataset_normal.npy`.

6) Run `train_recommender.py` to generate x (champion features) and theta (dataset user preferences).

7) You can use `interpret_results.py` to align champion names with their x's (features).
