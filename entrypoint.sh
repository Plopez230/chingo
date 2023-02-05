python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
/opt/bitnami/ctlscript.sh restart apache
