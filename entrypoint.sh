python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
sudo /opt/bitnami/ctlscript.sh restart apache
