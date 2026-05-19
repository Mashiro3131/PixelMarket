from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Optional, ValidationError, Regexp
 
from app.models import User
 
 
class ProfileForm(FlaskForm):
 
    # -- Identité --
    username = StringField(
        'Nom d\'utilisateur',
        validators=[
            Optional(),
            Length(min=3, max=80),
            Regexp(
                r'^[\w\-]+$',
                message='Seuls les lettres, chiffres, _ et - sont autorisés.'
            )
        ]
    )
 
    first_name = StringField(
        'Prénom',
        validators=[
            Optional(),
            Length(max=80),
            Regexp(
                r'^[a-zA-ZÀ-ÿ\s\-]+$',
                message='Lettres et tirets uniquement.'
            )
        ]
    )
 
    last_name = StringField(
        'Nom',
        validators=[
            Optional(),
            Length(max=80),
            Regexp(
                r'^[a-zA-ZÀ-ÿ\s\-]+$',
                message='Lettres et tirets uniquement.'
            )
        ]
    )
 
    phone = StringField(
        'Téléphone',
        validators=[
            Optional(),
            Length(max=20),
            Regexp(
                r'^\+[1-9]\d{7,14}$',
                message='Numéro invalide. Ex: +41781234567'
            )
        ]
    )
 
    # -- Adresse de facturation --
    street = StringField(
        'Rue',
        validators=[Optional(), Length(max=200)]
    )
 
    city = StringField(
        'Ville',
        validators=[Optional(), Length(max=100)]
    )
 
    zip_code = StringField(
        'Code postal',
        validators=[
            Optional(),
            Length(max=20),
            Regexp(
                r'^[A-Z0-9\s]{2,10}$',
                flags=2, # re.IGNORECASE
                message='Code postal invalide. Ex: 1020'
            )
        ]
    )
 
    state = StringField(
        'Canton / État',
        validators=[Optional(), Length(max=100)]
    )
 
    country = StringField(
        'Pays',
        validators=[Optional(), Length(max=100)]
    )
 
    submit = SubmitField('Enregistrer')
 
    # Vérifie que le nouveau username n'est pas déjà pris
    def validate_username(self, username):
        if username.data and username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Ce nom d\'utilisateur est déjà pris !')
                
# -------------------------------- SOURCES --------------------------------
# WTForms Optional :       https://wtforms.readthedocs.io/en/3.1.x/validators/#wtforms.validators.Optional
# WTForms Regexp :         https://wtforms.readthedocs.io/en/3.1.x/validators/#wtforms.validators.Regexp
# Format E.164 téléphone : https://www.twilio.com/docs/glossary/what-e164
# phonenumbers (prod) :    https://pypi.org/project/project/phonenumbers/
# re.IGNORECASE :          https://docs.python.org/3/library/re.html#re.IGNORECASE