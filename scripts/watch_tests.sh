#!/bin/bash
clear

# Define the omitted paths
OMIT_PATHS="tests/*,src/main.py,src/app.py,*/__init__.py,*/constants.py"

while true; do
  coverage run --rcfile=.coveragerc -m pytest
  coverage report --omit="$OMIT_PATHS" --show-missing
  
  sleep 5  # Adjust delay between test runs if needed
  clear
done