import secrets
from datetime import datetime, timedelta, timezone

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db, bcrypt
from app.models import User
from app.blueprints.auth import bp
from app.blueprints.auth.forms import RegisterForm, LoginForm, ForgotForm, ResetForm


@bp.route('/register', methods=['GET', 'POST'])
def register():

    # Redirige si déjà connecté
    if current_user.is_authenticated:
        return redirect(url_for('artworks.index'))

    form = RegisterForm()

    if form.validate_on_submit():

        # Hash du mot de passe avant de le stocker
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        user = User(
            username=form.username.data, # type: ignore
            email=form.email.data, # type: ignore
            password_hash=hashed_password # type: ignore
        )

        db.session.add(user)
        db.session.commit()

        flash('Compte créé avec succès ! Vous pouvez vous connecter.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():

    # Redirige si déjà connecté
    if current_user.is_authenticated:
        return redirect(url_for('artworks.index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        # Vérifie que l'user existe et est actif puis que le mdp est correct
        if not user or not user.is_active or not bcrypt.check_password_hash(
            user.password_hash, form.password.data
        ):
            flash('Email ou mot de passe incorrect.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember.data)

        # Redirige vers la page demandée avant le login, sinon l'accueil
        next_page = request.args.get('next')
        return redirect(next_page or url_for('artworks.index'))

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous êtes déconnecté.', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/forgot', methods=['GET', 'POST'])
def forgot():

    form = ForgotForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        # Pour des raisons de sécurité, on envoie toujours le même message même si l'email 
        # n'existe pas pour ne pas révéler si un email est enregistré ou non :)
        if user and user.is_active:

            # Génère un token sécurisé valable pendant 1h
            token = secrets.token_urlsafe(48)
            user.reset_token = token
            user.reset_expires = datetime.now(timezone.utc) + timedelta(hours=1)
            db.session.commit()

            # TODO: envoyer l'email avec le token (feature/orders-email)
            reset_url = url_for('auth.reset', token=token, _external=True)
            print(f'Reset URL (dev only): {reset_url}')

        flash(
            'Si cet email existe, un lien de réinitialisation a été envoyé.',
            'info'
        )
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot.html', form=form)


@bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):

    # Cherche l'user avec ce token et vérifie qu'il n'est pas expiré
    user = User.query.filter_by(reset_token=token).first()

    if not user or user.reset_expires < datetime.now(timezone.utc):
        flash('Le lien de réinitialisation est invalide ou expiré.', 'danger')
        return redirect(url_for('auth.forgot'))

    form = ResetForm()

    if form.validate_on_submit():

        # Hash du nouveau mdp avant de le stocker
        user.password_hash = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        # Supprime le token après utilisation
        user.reset_token = None
        user.reset_expires = None

        db.session.commit()

        flash('Mot de passe réinitialisé ! Vous pouvez vous connecter.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset.html', form=form, token=token)


# -------------------------------- SOURCES --------------------------------
# Flask-Login :    https://flask-login.readthedocs.io/en/latest/
# Flask-Bcrypt :   https://flask-bcrypt.readthedocs.io/en/1.0.1/
# secrets module : https://docs.python.org/3/library/secrets.html
# Forgot Passowrd: https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
