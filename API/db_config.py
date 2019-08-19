from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'statfive_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'statfive_password'
app.config['MYSQL_DATABASE_DB'] = 'statfive'
app.config['MYSQL_DATABASE_HOST'] = 'mariadb'
mysql.init_app(app)