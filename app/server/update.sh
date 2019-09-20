#!/bin/bash

container=${1:-pathfinder_server_dev}

echo "Updating server script in ${container} ..."

docker cp server.py ${container}:/server

echo "Update complete."