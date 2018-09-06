#!/usr/bin/env sh
set -e

docker build . -t dsm-to-color-scale
docker create -it --name dsm-to-color-scale dsm-to-color-scale

set +e
