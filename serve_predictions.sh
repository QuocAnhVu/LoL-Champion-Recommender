#!/bin/bash
env/bin/uwsgi --socket localhost:8080 --protocol=http -w serve_predictions
