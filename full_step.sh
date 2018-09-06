#!/usr/bin/env sh
set -e

docker cp *.py dsm-to-color-scale:/home/dsm-to-color-scale
docker cp dsm.tif dsm-to-color-scale:/home/dsm-to-color-scale
docker start dsm-to-color-scale
docker exec dsm-to-color-scale python main.py dsm.tif result.tif
docker exec dsm-to-color-scale gdalwarp -t_srs EPSG:3857 result.tif target.tif
docker exec dsm-to-color-scale gdal2tiles.py --srcnodata=0,0,0 --zoom=16-22 ./target.tif ./tiles
docker cp dsm-to-color-scale:/home/dsm-to-color-scale/tiles .
docker cp dsm-to-color-scale:/home/dsm-to-color-scale/target.tif .
docker stop dsm-to-color-scale

set +e
