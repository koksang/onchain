#!/bin/sh
poetry export -o requirements.txt --without-hashes
docker build --rm -t rayproject/ray:2.2.0-py310-cpu-extended -f ./infra/Dockerfile .