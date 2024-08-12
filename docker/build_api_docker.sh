#!/bin/bash
cp ../*.py .
poetry export --without-hashes --format=requirements.txt > requirements.txt

DOCKER_ARGS="--output=type=registry"
PLATFORM="linux/amd64,linux/arm64"

TAGS="-t jaihind213/angiogram-api:1.0"
export DOCKER_BUILDKIT=1
docker buildx create --use
docker buildx build $DOCKER_ARGS --platform $PLATFORM $TAGS -f DockerfileApi .
rm -rf ./*.py
docker builder prune -f;
docker buildx rm -f --all-inactive;
