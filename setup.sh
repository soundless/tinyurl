#!/bin/bash

# Initial setup script for development

CWD=$(dirname $0)

virtualenv ${CWD}/venv
source ${CWD}/venv/bin/activate
pip install -r ${CWD}/requirements.txt

echo 
echo "Using following command to activate the virtual env ..."
echo "$ source ${CWD}/venv/bin/activate && python ${CWD}/main.py" 
echo

exit 0
