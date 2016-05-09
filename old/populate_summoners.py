#!./env/bin/python
import sqlite3
from cassiopeia import riotapi
import secret_keys

conn = sqlite3.connect('db/summoner.db')
c = conn.cursor()
riotapi.set_region("NA")
riotapi.set_api_key(secret_keys.riotapikey)

challengers = riotapi.get_challenger().entries
masters = riotapi.get_master().entries
entries = challengers + masters
for entry in entries:
    c.executemany('INSERT OR REPLACE INTO summoners VALUES (?, ?)',
                  (entry.summoner.id, entry.summoner.name))

conn.commit()
conn.close()
