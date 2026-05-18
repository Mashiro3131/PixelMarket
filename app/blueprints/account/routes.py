from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.blueprints.account import bp
from app.blueprints.account.forms import ProfileForm


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
    user_orders = current_user.orders.copy()
    user_orders.sort(key=lambda o: o.created_at, reverse=True)

    return render_template('account/orders.html', orders=user_orders)


# -------------------------------- SOURCES --------------------------------
# Flask-Login current_user : https://flask-login.readthedocs.io/en/latest/#flask_login.current_user
# SQLAlchemy session : https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/

