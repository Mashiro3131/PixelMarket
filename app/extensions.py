# Extensions initialisées sans app pour éviter les imports circulaires, une application factory !!

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login" # type: ignore
login_manager.login_message = "Connecte-toi pour accéder à cette page." # type: ignore
login_manager.login_message_category = "warning" # type: ignore

# Gestionnaire de mails
mail = Mail()

# Hashage et verification de mdp
bcrypt = Bcrypt()

# -------------------------------- SOURCES --------------------------------
# Flask-SQLAlchemy :  https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
# Flask-Login :       https://flask-login.readthedocs.io/en/latest/
# Flask-Mail :        https://pythonhosted.org/Flask-Mail/
# Flask-Bcrypt :      https://flask-bcrypt.readthedocs.io/en/1.0.1/
