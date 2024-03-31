#!/bin/bash
clear

while true; do
  coverage run --rcfile=.coveragerc -m pytest
  coverage report --omit="tests/*,src/main.py,src/app.py,*/__init__.py,*/constants.py" --show-missing
  
  sleep 5  # Adjust delay between test runs if needed
  clear
done