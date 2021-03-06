# LoL-Champion-Recommender 
The champion recommender (AKA Blitzcrank's Matchmaking Service) is a collaborative filtering, machine learning recommender system. It generates a set of attributes, then assigns levels of these attributes to each champion. For each app user, it tailors the user's preferences to champion attributes and generates play recommendations.

Super long writeup is at [www.quocanhvu.com/documentation](http://www.quocanhvu.com/documentation.html)

# How do I run this app?

Go to [www.quocanhvu.com](http://www.quocanhvu.com)

# How do I train the recommender myself?
0) Install the dependencies listed in `package_dependencies.txt`. Those dependencies were tested for Ubuntu 14.04+. These scripts use *postgres* for the caching db. After installing postgresql, you will need configure postgres by creating a daemon role and editing your pga_hba.conf to allow password authentication.

1) Create a virtualenv directory called `env/`. Cassiopeia requires python3, so include that. I included system-wide packages so that the scipy stack would not have to be recompiled for the virtual environment.

`$ virtualenv -p python3 --system-site-packages env`

2) Install required python packages. The packages are specified in `.requirements`.

`env/bin/pip install -r .requirements`

3) Create `secret_keys.py` from `secret_keys.example.py` and fill in the blanks using your credentials. 

4) Generate the schema by running `model.py`.

5) Populate the db with data from Riot's API by running `populate_mastery_dataset.py`.

6) Convert db data to numpy objects and normalize the dataset by running `preprocess_dataset.py`. 
This step will generate `dataset_raw.npy` and `dataset_normal.npy`.

7) Train data. Run `train_recommender.py` to generate x (champion features) and theta (dataset user preferences).
This step will generate `result_x.npy`, `result_x.json`, `result_theta.npy`, and `result_theta.json`.

8) Predict with `predict_preferences.py` using the arguments: region summoner_name. 

`$ env/bin/python predict_preferences NA Bjergsen`

9) Serve predictions over the web with `serve_predictions.py`. Run `serve_predictions.sh` to start the server on port 8080. This server only serves the prediction as a json. The rest of the app is inside web/ and must be served from a web server.