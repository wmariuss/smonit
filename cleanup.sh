#!/bin/bash

set -e

VOLUME_LIST=(
            smonit_grafana-storage
            smonit_influxdb-storage
            smonit_redis-storage
            )

docker-compose stop
docker-compose rm -v -f

for volume in "${VOLUME_LIST[@]}"; do
    docker volume rm $volume
done
