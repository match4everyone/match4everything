#!/bin/bash -e
# To run script in Docker call for example "delete_db_and_setup.sh 'docker-compose exec backend'"
EXEC_ENV="$*"
DJANGO_SUPERUSER_PASSWORD="admin"

$EXEC_ENV echo "DO NOT USE THIS SCRIPT IN PRODUCTION"
$EXEC_ENV echo "THIS SCRIPT SETS AN INSECURE ADMIN PASSWORD"
$EXEC_ENV python3 manage.py reset_db
$EXEC_ENV python3 manage.py migrate
$EXEC_ENV echo "Creating account with username \"admin\". "
$EXEC_ENV echo "Please enter your desired email and password."
$EXEC_ENV python3 manage.py createsuperuser --username admin --email admin@examplee.com --no-input
$EXEC_ENV python3 manage.py loaddata cms_export.json
$EXEC_ENV python3 manage.py createfakeusers --add-a=40 --add-b=20
