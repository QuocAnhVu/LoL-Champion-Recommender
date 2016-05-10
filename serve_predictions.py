#!./env/bin/python
# Serve Predictions
# Serves predictions, skipping need for cgi with wsgi.
# Inputs single region and summoner name and outputs user preferences.
import predict_preferences as predictor
import json
from urllib.parse import parse_qs
import uwsgi
from cassiopeia.type.api.exception import APIError


def application(env, start_response):
    qs = ''.join(env['REQUEST_URI'].split('?')[1:])
    query_dict = parse_qs(qs)
    region = query_dict['region'][0]
    summoner_name = query_dict['summoner_name'][0]

    try:
        predictions = predictor.predict(region, summoner_name)
    except APIError as err:
        code = str(err.error_code)
        start_response(code, [('Content-Type', 'text/plain')])
        if(code == '404'):
            message = 'Server returned 404. Summoner {0} was not found in '\
                      'region {1}.'.format(summoner_name, region.upper())
        elif(code == '500'):
            message = "Server returned 500. Riot's API is probably busy."
        else:
            message = "Server returned {0}.".format(code)
        return [message]
    start_response('200 OK', [('Content-Type', 'application/json')])
    pred_json = json.dumps(dict(predictions))
    return [pred_json]
