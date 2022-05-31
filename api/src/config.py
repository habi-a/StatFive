import os


class Development:
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = "secret"
    SECRET_KEY = 'secret!'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'jaouad'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'statfive'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 465)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', True)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'Villepinte93420')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'elhorm_j@etna-alternance.net')


class Docker:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'secret!')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret!')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'statfive_user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'statfive_password')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'mariadb')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'statfive')
    SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_DATABASE_URI', False)

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'ssl0.ovh.net')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', True)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '9A47cmAmCSor4@mo')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'noreply@statfive.fr')


class Kubernetes:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'secret!')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret!')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'statfive_user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'statfive_password')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'mariadb')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'statfive')
    SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_DATABASE_URI', False)

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'ssl0.ovh.net')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', True)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '9A47cmAmCSor4@mo')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'noreply@statfive.fr')

app_config = {
    'development': Development,
    'docker': Docker,
    'kubernetes': Kubernetes
}
