#!/usr/bin/env bash
set -e -o pipefail
# First build containers, compile messages, collect static files (copy them to static_root) and migrate database
export CURRENT_UID=$(id -u):$(id -g)
export dc="docker-compose -f docker-compose.yml -f docker-compose.prod.yml"
$dc up -d --build
echo "Server started for setup"
$dc exec backend python3 manage.py migrate
$dc exec --env PYTHONPATH="/match4everyone-backend:$PYTHONPATH" backend django-admin makemessages --no-location --ignore 00_old_m4h_matching_code
$dc exec --env PYTHONPATH="/match4everyone-backend:$PYTHONPATH" backend django-admin compilemessages

$dc exec backend python3 manage.py collectstatic --no-input
$dc exec backend python3 manage.py migrate
$dc exec backend python3 manage.py check
# Restart container AFTER static files have been collected
$dc down
$dc up -d
echo "Server is ready for you"
