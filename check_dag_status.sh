#!/usr/bin/env bash

set -e

DAG_NAME=$1
RUN_ID=$2
USER=airflow
PASSWD=airflow
AIRFLOW_HOST=localhost:8080
AIRFLOW_PORT=8080

touch /tmp/dag_status_${RUN_ID}
curl  -o /tmp/dag_status_${RUN_ID} -X GET "http://localhost:8080/api/v1/dags/${DAG_NAME}/dagRuns/${RUN_ID}" \
-H "Content-Type: application/json" \
--user "${USER}:${PASSWD}"

cat /tmp/dag_status_${RUN_ID}
cat /tmp/dag_status_${RUN_ID}| grep -i '"state": "success"' || exit 1