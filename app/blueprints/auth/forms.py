from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        'Nom d\'utilisateur',
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Mot de passe',
        validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        'Confirmer le mot de passe',
        validators=[
            DataRequired(),
            EqualTo(
                'password',
                message='Les mots de passe ne correspondent pas.'
            ),
        ]
    )
    submit = SubmitField('S\'inscrire')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Mot de passe',
        validators=[DataRequired()]
    )
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')


class ForgotForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Envoyer le lien de réinitialisation')


class ResetForm(FlaskForm):
    password = PasswordField(
        'Nouveau mot de passe',
        validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        'Confirmer le mot de passe',
        validators=[
            DataRequired(),
            EqualTo('password', message='Les mots de passe ne correspondent pas.'),
        ]
    )
    submit = SubmitField('Réinitialiser le mot de passe')
