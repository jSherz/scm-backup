#!/bin/sh

if [[ ! -f "config.env" ]]
then
  echo "No config file - see config.env.example and create one in 'config.env'."
  exit 1
fi

$VIRTUALENV_SOURCE_COMMAND

echo "Installing required Python modules..."

pip install -r requirements.txt

echo "Performing GitHub backup..."

python github.py

# echo "Performing BitBucket backup..."

# python bitbucket.py
