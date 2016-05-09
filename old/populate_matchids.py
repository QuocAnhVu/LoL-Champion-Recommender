#!./env/bin/python
import time
import sqlite3
import urllib.error
from cassiopeia import baseriotapi
import secret_keys

sel_conn = sqlite3.connect('db/summoner.db')
sel_cur = sel_conn.cursor()
ins_conn = sqlite3.connect('db/matchid.db')
ins_cur = ins_conn.cursor()

baseriotapi.set_region('NA')
baseriotapi.set_api_key(secret_keys.riotapikey)
baseriotapi.set_rate_limits((10, 10), (500, 600))

count = sel_cur.execute('SELECT COUNT(*) FROM matchids').fetchone()[0]
for idx, row in enumerate(sel_cur.execute('SELECT * FROM matchids')):
    current_sum = idx + 1
    summoner_id = row[0]
    summoner_name = row[1]

    print('{current_sum}/{count} Obtaining match list for '.
          format(**locals()) + summoner_name)

    while(True):
        try:
            match_list = baseriotapi.get_match_list(summoner_id,
                                                    ranked_queues='TEAM_BUILDER_DRAFT_RANKED_5x5',
                                                    seasons='SEASON2016')
        except urllib.error.HTTPError:
            print("Error with HTTP request (probably 500, server is busy)")
            time.sleep(20)
            continue
        break
    matchids = ((match.matchId,) for match in match_list.matches)

    ins_cur.executemany('INSERT OR IGNORE INTO matchids VALUES (?)', matchids)
    ins_conn.commit()

ins_conn.close()
sel_conn.close()
