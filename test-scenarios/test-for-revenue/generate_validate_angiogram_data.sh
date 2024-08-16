#!/bin/bash

set -e
pwd=`pwd`
cd test-scenarios/test-for-revenue
export PYTHONPATH=test-scenarios/test-for-revenue:$PYTHONPATH
python generate_data.py
pytest test_for_generated_data.py
cd $pwd