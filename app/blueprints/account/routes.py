from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from email_validator import validate_email, EmailNotValidError

from app.extensions import db
from app.blueprints.account import bp
from app.blueprints.account.forms import ProfileForm
from app.models import Newsletter




@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():

        current_user.username = form.username.data

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        
        current_user.phone = form.phone.data
        
        current_user.street = form.street.data
        current_user.city = form.city.data
        current_user.zip_code = form.zip_code.data
        
        current_user.state = form.state.data
        current_user.country = form.country.data

        db.session.commit()

        flash('Profil mis à jour avec succès !', 'success')
        return redirect(url_for('account.profile'))

    return render_template('account/profile.html', form=form)




@bp.route('/orders')
@login_required
def orders():

    # Récupère toutes les commandes du user connecté, les plus récentes en premier
    user_orders = sorted(current_user.orders, key=lambda o: o.created_at, reverse=True)

    return render_template('account/orders.html', orders=user_orders)




@bp.route('/newsletter', methods=['POST'])
def newsletter():

    email = request.form.get('email', '').strip()

    # Validation format email
    try:
        validate_email(email)
    except EmailNotValidError:
        flash('Adresse email invalide.', 'danger')
        return redirect(url_for('artworks.index'))

    # Vérifie si déjà abonné
    existing = Newsletter.query.filter_by(email=email).first()

    if existing:
        if existing.is_active:
            flash('Vous êtes déjà abonné à la newsletter.', 'info')
        else:
            # Réactive l'abonnement si désabonné
            existing.is_active = True
            db.session.commit()
            flash('Votre abonnement a été réactivé !', 'success')
        return redirect(url_for('artworks.index'))

    # Nouvel abonnement
    subscriber = Newsletter()
    subscriber.email = email
    db.session.add(subscriber)
    db.session.commit()

    flash('Merci pour votre abonnement !', 'success')
    return redirect(url_for('artworks.index'))

# -------------------------------- SOURCES --------------------------------
# Flask-Login current_user : https://flask-login.readthedocs.io/en/latest/#flask_login.current_user
# SQLAlchemy session : https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/

