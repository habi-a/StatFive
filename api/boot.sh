source venv/bin/activate
sleep 1
rm -rf migrations
for i in $(seq 1 10);
do
#    nohup python manage.py db init
#    nohup python manage.py db upgrade
#    nohup python manage.py db migrate
    sleep 1
done
nohup python -u app.py --host 0.0.0.0 --port 5000 --conf docker
exec tail -f /dev/null