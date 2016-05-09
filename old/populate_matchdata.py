#!./env/bin/python
import time
import urllib.error
import sqlite3
from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
import secret_keys

sel_conn = sqlite3.connect('db/matchid.db')
sel_cur = sel_conn.cursor()
ins_conn = sqlite3.connect('db/matches.db')
ins_cur = ins_conn.cursor()

riotapi.set_region('NA')
riotapi.set_api_key(secret_keys.riotapikey)
riotapi.set_rate_limits((9, 10), (499, 600))

count = sel_cur.execute('SELECT COUNT(*) FROM matchids').fetchone()[0]
lastRunIdx = ins_cur.execute('SELECT COUNT(*) FROM matches').fetchone()[0]
for idx, row in enumerate(sel_cur.execute('SELECT * FROM matchids')):
    # If program previously crashed, continue from last run
    if idx < lastRunIdx - 1:
        continue

    # Query match data from Riot
    while(True):
        try:
            matchid = row[0]
            print('[{time}] {curr}/{total} - Obtaining match list for '
                  .format(time=time.strftime("%H:%M:%S"), curr=idx+1, total=count) + str(matchid))
            match_data = riotapi.get_match(matchid, include_timeline=False)
        except APIError as err:
            print(err)
            if(err.error_code == 404):
                break
            else:
                time.sleep(10)
                continue
        break

    # Parse relevant data into a tuple
    blue_champs = (p.champion.id for p in match_data.blue_team.participants)
    red_champs = (p.champion.id for p in match_data.red_team.participants)
    match_summary = (match_data.id, match_data.creation,
                     match_data.blue_team.win) + tuple(blue_champs) + tuple(red_champs)

    # Insert data into db
    while(True):
        try:
            ins_cur.execute(
                'INSERT OR IGNORE INTO matches VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', match_summary)
            ins_conn.commit()
        except sqlite3.OperationalError as err:
            print(err)
            time.sleep(1)
            continue
        except sqlite3.ProgrammingError as err:
            print(err)
            break
        break

ins_conn.close()
sel_conn.close()
