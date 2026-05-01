import os
from dotenv import load_dotenv

# Charge le .env
load_dotenv() 

# Répertoire de base pour les chemins relatifs
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clé secrète pour sécuriser les sessions et les formulaires CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-en-prod'

    # Config de la BD SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Config du serveur SMTP
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True # Sécurité de cryptage mail
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@pixelmarket.com')

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