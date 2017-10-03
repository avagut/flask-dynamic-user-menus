"""Main Config File."""
import os
 
BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
SECRET_KEY = 'change_this_secret_key'
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://my_db_role:my_db_password@localhost/my_db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = True
WTF_CSRF_ENABLED = True
BCRYPT_LOG_ROUNDS = 12
TOKEN_TIMEOUT = 3600  # 1*60*60

#Example Email Settings for sending Mail Notifications
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'my_gmail_address'
MAIL_PASSWORD = 'my_gmail_password'
MAIL_DEFAULT_SENDER = 'my_gmail_address'