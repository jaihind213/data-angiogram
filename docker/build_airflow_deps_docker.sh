#!/bin/bash
TAGS="-t jaihind213/angiogram-airflow:4.0"

SPARK_TAR=spark-3.4.0-bin-hadoop3-scala2.13.tgz
if [ -f $SPARK_TAR ]; then
   echo "File $SPARK_TAR exists."
else
  wget https://archive.apache.org/dist/spark/spark-3.4.0/$SPARK_TAR
fi
cp ../*.py .
poetry export --without-hashes --format=requirements.txt > requirements.txt


DOCKER_ARGS="--output=type=registry"
PLATFORM="linux/amd64,linux/arm64"

export DOCKER_BUILDKIT=1
docker buildx create --use
docker buildx build $DOCKER_ARGS --platform $PLATFORM $TAGS -f DockerfileAirflowWithDeps .
exit_status=$?
rm -rf ./*.py

docker builder prune -f;
docker volume prune -f;
docker buildx prune --all -f;
echo "build status: $exit_status"
