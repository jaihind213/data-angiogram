#!/bin/bash

set -e
pwd=`pwd`
cd test-scenarios/test-for-revenue
export PYTHONPATH=test-scenarios/test-for-revenue:$PYTHONPATH
python generate_data.py
pytest test_for_generated_data.py

cd $pwd

file_path="path/to/your/file.txt"

# Check if the file exists
if [[ ! -f "$file_path" ]]; then
  echo "File $file_path does not exist."
  exit 1
fi

# Read each line from the file and send a POST request
while read -r line; do
  curl -X POST -H "Content-Type: application/json" -d "$line" http://localhost:8080/taxis
done < "$file_path"