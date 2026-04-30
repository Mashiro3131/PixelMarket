# app/models.py
# Définit la structure de la base de données
# Chaque classe = une table dans SQLite

from datetime import datetime, timezone
from flask_login import UserMixin
from app.extensions import db

 
 
 
# -------------------------------- USER --------------------------------

class User(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    
    password_hash = db.Column(db.String(255), nullable=False)
 
    role = db.Column(db.String(10), nullable=False, default='user') # user / artist / admin
 
    # Compte actif ou désactivé
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
 
    # Infos de facturation (peuvent être remplies plus tard sous le profil)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
 
    country = db.Column(db.String(100), nullable=True)
    street = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
 
    # Méthode de sécurité pour reset le mdp 
    reset_token   = db.Column(db.String(100), unique=True, nullable=True)
    reset_expires = db.Column(db.DateTime, nullable=True)
 
    # Relations amoureuses avec les autres tables
    artworks = db.relationship('Artwork', backref='artist', lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy=True)
 
    # Permets de vérifier les rôles plus facilement dans les templates et routes
    def is_artist(self):
        return self.role == 'artist'
 
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'




# -------------------------------- CATEGORY --------------------------------

class Category(db.Model):
    __tablename__ = 'categories'
 
    id       = db.Column(db.Integer,    primary_key=True)
    name     = db.Column(db.String(50), unique=True, nullable=False)
 
    artworks = db.relationship('Artwork', backref='category', lazy=True)
 
    def __repr__(self):
        return f'<Category {self.name}>'




# -------------------------------- ARTWORK --------------------------------

class Artwork(db.Model):
    __tablename__ = 'artworks'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    
    is_sold = db.Column(db.Boolean, nullable=False, default=False)
 
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
 
    # Freview_path = image affichée sur le site
    preview_path = db.Column(db.String(512), nullable=True)
    
    # Fichier original en haute qualité envoyé par mail après achat
    file_path = db.Column(db.String(512), nullable=True)
 
    # ─── Foreign Keys ─────────────────────────────────────
    artist_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
 
    def __repr__(self):
        return f'<Artwork {self.name} - {"vendu" if self.is_sold else "disponible"}>'
 
 
 
 
# -------------------------------- ORDER --------------------------------

class Order(db.Model):
    __tablename__ = 'orders'
 
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
 
    # Passe à True une fois le fichier envoyé par mail à l'acheteur
    email_sent = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
 
    # FK
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artworks.id'), nullable=False)
 
    # Relation
    artwork = db.relationship('Artwork', backref='orders')
 
    def __repr__(self):
        return f'<Order {self.id} - buyer:{self.buyer_id} artwork:{self.artwork_id}>'
 



# -------------------------------- NEWSLETTER --------------------------------
class Newsletter(db.Model):
    __tablename__ = 'newsletter'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
 
    # Voir si le user est abonné ou s'il à demandé à se désabonner
    is_active  = db.Column(db.Boolean, nullable=False, default=True)
 
    # Date d'inscription à la newsletter ou de demande de désabonnement
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)) 
 
    def __repr__(self):
        return f'<Newsletter {self.email}>'




# -------------------------------- SOURCES --------------------------------
# Flask-SQLAlchemy modèles :  https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/models/
# Flask-Login UserMixin :     https://flask-login.readthedocs.io/en/latest/#flask_login.UserMixin
# SQLAlchemy types :          https://docs.sqlalchemy.org/en/20/core/types.html
# datetime.utcnow :           https://docs.python.org/3/library/datetime.html
# minimisation des donnéees : https://www.talend.com/fr/resources/minimisation-donnees/
# argon2id longueur hash :    https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html