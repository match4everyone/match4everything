#!/bin/bash -e
# To run script in Docker call for example "delete_db_and_setup.sh 'docker-compose exec backend'"
EXEC_ENV="$*"

$EXEC_ENV python3 manage.py reset_db
$EXEC_ENV python3 manage.py migrate
$EXEC_ENV echo "Creating account with username \"admin\". "
$EXEC_ENV echo "Please enter your desired email and password."
$EXEC_ENV python3 manage.py createsuperuser  --username admin
$EXEC_ENV python3 manage.py loaddata cms_export.json
