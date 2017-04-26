#!/bin/sh
python vmanager.py -c waspmq/waspmq.sh -a create waspmq
python vmanager.py -c waspmq/frontend.sh -a create waspmq-frontend
python vmanager.py -c waspmq/backend.sh -a create waspmq-backend
