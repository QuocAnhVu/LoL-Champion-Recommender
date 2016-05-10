#!/bin/bash
# Quick startup script for running python backend on port 8080
env/bin/uwsgi --socket localhost:8080 --protocol=http -w serve_predictions
