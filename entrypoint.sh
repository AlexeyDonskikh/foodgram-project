python manage.py migrate --noinput || exit 1

python manage.py collectstatic --noinput
python manage.py loaddata fixtures.json
