rm run/db.sqlite3
rm apps/matching/migrations/0003*
python3 manage.py makemigrations matching
python3 manage.py migrate
