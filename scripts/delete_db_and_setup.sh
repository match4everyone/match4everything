rm backend/run/db.sqlite3
python3 backend/manage.py migrate
echo "Creating account with username \"admin\". "
echo "Please enter your desired email and password:"
python3 backend/manage.py createsuperuser  --username admin
python3 backend/manage.py loaddata backend/cms_export.json
