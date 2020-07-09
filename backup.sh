#!/usr/bin/env bash
# This backup script will create a database dump from the postgres container
# the created backup will then be moved to the current directory
set -o errexit

WORKINGDIR=$(pwd)

echo "Creating PostgreSQL Dump"
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec database sh -c 'pg_dumpall -U $POSTGRES_USER> /backups/pg_backup-$(date +%F_%H%M%S).sql'

# Create a throwaway container (--rm removes after running the command) to move the backups from the DB-container volume to the local directory for further processing
# (Mounts the current working dir as /backup-bind-mount inside the container and moves the backups there)
echo "Moving the backups to $WORKINGDIR"
DB_CONTAINER="$(docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps -q database)"
docker run --rm --volumes-from "$DB_CONTAINER" -v "${WORKINGDIR}:/host" alpine sh -c "mv -v backups/* /host/database/backups"

echo -e "\nCreating Django fixtures"
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec backend  sh -c 'django-admin dumpdata > /backend/backups/fixture-$(date +%F_%H%M%S).json'
echo "Moving the backups to $WORKINGDIR"
BACKEND_CONTAINER="$(docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps -q backend)"
docker run --rm --volumes-from "$BACKEND_CONTAINER" -v "${WORKINGDIR}:/host" alpine sh -c "mv -v /backend/backups/*.json /host/backend/backups"
