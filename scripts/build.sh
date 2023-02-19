#!/bin/sh
poetry export -o requirements.txt --without-hashes
docker build --rm -t k3d-registry.localhost:7777/rayproject/ray:2.3.0-py310-cpu-extended -f ./infra/Dockerfile .
# docker tag rayproject/ray:2.2.0-py310-cpu-extended k3d-registry.localhost:5000/rayproject/ray:2.2.0-py310-cpu-extended
docker push k3d-registry.localhost:7777/rayproject/ray:2.3.0-py310-cpu-extended