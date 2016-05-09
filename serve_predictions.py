#!./env/bin/python
import predict_preferences as predictor
import json
from urlparse import urlparse
import uwsgi


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    input_dict = urlparse.parse_qs(env['REQUEST_URI'])
    region = input_dict['region']
    summoner_name = input_dict['summoner_name']
    predictions = predictor.predict(region, summoner_name)
    return ["<h1 style='color:blue'>Hello There!</h1>"]
