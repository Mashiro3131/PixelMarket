import os
from dotenv import load_dotenv

# Charge le .env
load_dotenv() 

# Répertoire de base pour les chemins relatifs
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Sécuriser les sessions et les forms
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Config de la BD SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Config du serveur SMTP
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # Config d'upload de fichiers
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'pdf'}
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # Limite de 50 Mo

    # Active / désactive le mode debug en fonction du .env
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'


# -------------------------------- SOURCES --------------------------------
# Flask configuration : https://flask.palletsprojects.com/en/3.0.x/config/
# python-dotenv :       https://pypi.org/project/python-dotenv/
# Flask-Mail config :   https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-email-support
# os.path :             https://docs.python.org/3/library/os.path.html
# Flask-Debug :         https://flask.palletsprojects.com/en/stable/config/
# MDP App Gmail :       https://support.google.com/accounts/answer/185833?dark=1&hl=en-GB&utm_source=google-account&utm_medium=search-screen