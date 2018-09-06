#!/usr/bin/env sh
set -e

docker cp *.py dsm-to-color-scale:/home/dsm-to-color-scale
docker cp dsm.tif dsm-to-color-scale:/home/dsm-to-color-scale

set +e
