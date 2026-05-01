from flask import Flask
from config import Config
from app.extensions import db, login_manager, mail, bcrypt
from flask import Flask, render_template

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init des extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    # Blueprints
    
    from app.blueprints.auth     import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.blueprints.artworks import bp as artworks_bp
    app.register_blueprint(artworks_bp)
    
    from app.blueprints.artist   import bp as artist_bp
    app.register_blueprint(artist_bp)
    
    from app.blueprints.admin    import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    from app.blueprints.account  import bp as account_bp
    app.register_blueprint(account_bp)

    # User loader pour Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Création des tables si elles n'existent pas
    with app.app_context():
        db.create_all()



    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    return app


# -------------------------------- SOURCES --------------------------------
# Application factory pattern :     https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
# Flask-Login user_loader :         https://flask-login.readthedocs.io/en/latest/#how-it-works
# db.session.get (SQLAlchemy 2.0) : https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get
# Database :                        https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
