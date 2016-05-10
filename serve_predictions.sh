#!/bin/bash
# Quick startup script for running python backend on port 8080
env/bin/uwsgi --daemonize=./log/serve_predictions.log --socket localhost:8080 --protocol=http --harakiri=20  --max-requests=5000 -w serve_predictions  
# env/bin/uwsgi --socket localhost:8080 --protocol=http --harakiri=20  --max-requests=5000 -w serve_predictions  
