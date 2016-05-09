#!./env/bin/python
import sqlite3
import itertools
from cassiopeia import riotapi
import secret_keys

conn = sqlite3.connect('db/gamedata.db')
c = conn.cursor()
riotapi.set_region("NA")
riotapi.set_api_key(secret_keys.riotapikey)

champions = riotapi.get_champions()
c.executemany('INSERT OR IGNORE INTO champions (champid, name) VALUES (?,?)',
              [(champ.id, champ.name) for champ in champions])


conn.commit()
conn.close()
