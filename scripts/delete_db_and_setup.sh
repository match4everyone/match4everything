rm backend/run/db.sqlite3
python3 backend/manage.py migrate
python3 backend/manage.py createsuperuser  --username admin
python3 backend/manage.py loaddata backend/cms_export.json
