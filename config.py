import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Application configuration
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Abuu_254'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_PASS = 'pass'

    # Config for sending mail, reset passwords and error messages
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS =True
    MAIL_USERNAME = 'abuu.developer@gmail.com'
    MAIL_PASSWORD = 'testingmail'
    ADMINS = ['abuu.developer@gmail.com']

    # pagination
    TICKETS_PER_PAGE = 10