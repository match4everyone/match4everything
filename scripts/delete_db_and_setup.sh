#!/bin/bash -e
# To run script in Docker call for example "delete_db_and_setup.sh 'docker-compose exec backend'"
#MODE={$1:-"None"}
MODE=$1
if [[  $MODE == '' ]]; then
  echo "You have to put either 'DEV' or 'PROD' as argument"
  exit 1
fi
if [[  $MODE != 'DEV' && $MODE != 'PROD' ]]; then
  echo "Supplied mode is not supported. We only support 'DEV' and 'PROD'"
  exit 1
fi
if [ $MODE == 'DEV' ]; then
  echo "DO NOT USE THE 'DEV' MODE IN PRODUCTION"
  echo "THIS SCRIPT SETS AN INSECURE ADMIN PASSWORD"
  DJANGO_SUPERUSER_PASSWORD="admin"
fi
shift
EXEC_ENV="$*"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" && cd $DIR/../
$EXEC_ENV python3 backend/manage.py reset_db --skip-checks
$EXEC_ENV python3 backend/manage.py migrate --skip-checks
echo "Creating account with username \"admin\". "
if [ $MODE == 'PROD' ]; then
  echo "Please enter your desired email and password."
  $EXEC_ENV python3 backend/manage.py createsuperuser --username admin --skip-checks
else
  $EXEC_ENV python3 backend/manage.py createsuperuser --username admin --email admin@example.com --no-input --skip-checks
  $EXEC_ENV python3 backend/manage.py createfakeusers --add-helper=40 --add-institution=20 --skip-checks
  echo "Created admin account and fake accounts"
fi
$EXEC_ENV python3 backend/manage.py loaddata backend/cms_export.json
echo "Site successfully set up"
