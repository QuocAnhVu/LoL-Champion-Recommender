#!./env/bin/python
# Populate Mastery Dataset
# Queries 8 regions and pulls summoner_ids and champion_masteries
# of each master tier and challenger tier player.
from model import *
from sqlalchemy.orm import sessionmaker
from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
import secret_keys
import time
import sys


# Query match data from Riot with error handling
def query_riot_api(function, *args):
    while(True):
        try:
            data = function(*args)
        except APIError as err:
            print(err)
            if(err.error_code == 404):
                break
            else:
                time.sleep(10)
                continue
        break
    return data

# Setup libraries
riotapi.set_api_key(secret_keys.riotapikey)
riotapi.set_rate_limits((9, 10), (499, 600))
Session = sessionmaker()
Session.configure(bind=engine)  # engine is from model

# Constrain querying to certain regions (to continue from a previously
# interrupted run)
if not sys.argv[1:]:
    regions = ['BR', 'EUNE', 'EUW', 'KR',
               'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR']
else:
    regions = sys.argv[1:]

# Iterating over each region
for region in regions:
    # Customize libraries to region
    session = Session()
    riotapi.set_region(region)

    # Query summoner ids
    print('Querying {region} Challenger Tier list'.format(**locals()))
    challengers = query_riot_api(riotapi.get_challenger)
    print('Querying {region} Master Tier list'.format(**locals()))
    masters = query_riot_api(riotapi.get_master)
    players = [entry.summoner for entry in (
        challengers.entries + masters.entries)]

    # Iterating over each summoner
    count = 0
    total_count = len(players)
    for player in players:
        count += 1
        print('[{region}][{count}/{total_count}]'
              ' {player.name}'.format(**locals()))

        # Save summoner id
        db_summoner = Summoner(
            region=region, summoner_id=player.id, summoner_name=player.name)
        session.merge(db_summoner)

        # Save summoner mastery
        champion_masteries = query_riot_api(player.champion_masteries)
        if champion_masteries is not None:
            for champion, champion_mastery in champion_masteries.items():
                db_champion = Champion(
                    champion_id=champion.id,
                    champion_name=champion.name)
                db_champion_mastery = ChampionMastery(
                    summoner_region=region,
                    summoner_id=player.id,
                    champion_id=champion.id,
                    champion_points=champion_mastery.points,
                    highest_grade=champion_mastery.highest_grade,
                    last_play_time=champion_mastery.last_played)
                session.merge(db_champion)
                session.merge(db_champion_mastery)

        session.commit()

    # Saves the session to db
    print("Saving {region} summoners' ids and masteries".format(region=region))
    session.commit()
    session.close()
