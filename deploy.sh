#!/usr/bin/env bash
set -e -o pipefail
# First build containers, compile messages, collect static files (copy them to static_root) and migrate database
export CURRENT_UID=$(id -u):$(id -g)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
echo "Server started for setup"
docker exec backend python3 manage.py migrate
docker exec --env PYTHONPATH="/match4everyone-backend:$PYTHONPATH" backend django-admin makemessages --no-location --ignore 00_old_m4h_matching_code
docker exec --env PYTHONPATH="/match4everyone-backend:$PYTHONPATH" backend django-admin compilemessages
docker exec backend python3 manage.py collectstatic --no-input
docker exec backend python3 manage.py migrate
docker exec backend python3 manage.py check
# Restart container AFTER static files have been collected
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
echo "Server is ready for you"
