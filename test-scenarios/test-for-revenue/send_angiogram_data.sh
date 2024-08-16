#!/bin/bash

set -e
pwd=`pwd`
cd test-scenarios/test-for-revenue
file_path="taxi_rides.txt"

# Check if the file exists
if [[ ! -f "$file_path" ]]; then
  echo "File $file_path does not exist."
  exit 1
fi

ERRORS_OCCURED=no
MSG_SENT=0
MSG_READ=0

# Read each line from the file and send a POST request
while read -r line; do
  let MSG_READ=MSG_READ+1
  curl -X POST -H "Content-Type: application/json" -d "$line" http://localhost:8000/taxis
  return_code=$?
   if [ $return_code -ne 0 ]; then
    echo "Send encountered an error. return code: $return_code"
    ERRORS_OCCURED=yes
   else
    let MSG_SENT=MSG_SENT+1
  fi
done < "$file_path"

cd $pwd

touch /tmp/msgs_sent
touch /tmp/msgs_read
#append to file count
echo $MSG_SENT >> /tmp/msgs_sent
echo $MSG_READ >> /tmp/msgs_read
#awk '{ sum += $1 } END { print sum }' /tmp/msg_sents

if [ "$ERRORS_OCCURED" == "yes" ];then
    echo "error occurred while sending data... hence exiting with code 2"
    exit 2
fi
