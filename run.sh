#!/usr/bin/env sh
set -e

docker start dsm-to-color-scale
docker exec dsm-to-color-scale python main.py dsm.tif result.tif
docker stop dsm-to-color-scale

set +e
