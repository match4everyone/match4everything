rm run/db.sqlite3
mkdir ___tmp
cp apps/matching/migrations/0002_permission_group_creation.py ___tmp
rm apps/matching/migrations/0*
python3 manage.py makemigrations
python3 manage.py migrate
mv ___tmp/0002_permission_group_creation.py apps/matching/migrations/
rm -r ___tmp
python3 manage.py migrate
