# LoL-Champion-Recommender 
The champion recommender (AKA Blitzcrank's Matchmaking Service) is a collaborative filtering, machine learning recommender system. It generates a set of attributes, then assigns levels of these attributes to each champion. For each app user, it tailors the user's preferences to champion attributes and generates play recommendations.

The app is currently hosted on [www.quocanhvu.com](http://www.quocanhvu.com)

# How To Train Recommender
1) Create a virtualenv directory called `env/`: 

Ex: `$ virtualenv env`

2) Install requirements specified in .requirements: `env/bin/pip install -r .requirements`. The *scipy* stack
will require some build dependencies. These scripts only use *postgres* for the caching db.

3) Create `secret_keys.py` from `secret_keys.example.py` and fill in the blanks using your credentials. 

4) Generate schema by running `model.py`.

5) Populate the db with data from Riot's API by running `populate_mastery_dataset.py`.

6) Convert db data to numpy objects and normalize the dataset by running `preprocess_dataset.py`. 
This step will generate `dataset_raw.npy` and `dataset_normal.npy`.

7) Train data. Run `train_recommender.py` to generate x (champion features) and theta (dataset user preferences).
This step will generate `result_x.npy`, `result_x.json`, `result_theta.npy`, and `result_theta.json`.

8) Predict with `predict_preferences.py` using arguments: region then summoner name. 

Ex: `$ ./predict_preferences NA Bjergsen`

9) Serve predictions over the web with `serve_predictions.py`. Run `serve_predictions.sh` to start the server on port 8080. This server only serves the prediction as a json. The rest of the app is inside web/ and must be served from a web server.