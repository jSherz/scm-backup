#!/bin/bash

if [[ ! -f "config.env" ]]
then
  echo "No config file - see config.env.example and create one in 'config.env'."
  exit 1
fi

source config.env
source $VIRTUALENV_ACTIVATE_SCRIPT

echo "Installing required Python modules..."

pip install -r requirements.txt

echo "Performing GitHub backup..."

python backup-github.py

echo "Performing BitBucket backup..."

python bitbucket.py

echo "Uploading to cloud storage..."

duplicity github/ gs://$BUCKET/github/
duplicity bitbucket/ gs://$BUCKET/bitbucket/
