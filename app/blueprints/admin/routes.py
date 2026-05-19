from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.extensions import db
from app.blueprints.admin import bp
from app.models import User, Artwork


def admin_required(f):
    """Décorateur "@admin_required", refuse l'accès si l'utilisateur n'est pas admin."""

    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Accès réservé aux administrateurs !', 'danger')
            return redirect(url_for('artworks.index'))
        return f(*args, **kwargs)

    return decorated


# -------------------------------- USERS --------------------------------


@bp.route('/users')
@login_required
@admin_required
def users():

    all_users = User.query.order_by(User.created_at.desc()).all()

    return render_template('admin/users.html', users=all_users)


@bp.route('/users/<int:id>/role', methods=['POST'])
@login_required
@admin_required
def change_role(id):

    user = User.query.get_or_404(id)

    # Empêche l'admin de changer son propre rôle
    if user.id == current_user.id:
        flash('Vous ne pouvez pas modifier votre propre rôle... ;)', 'danger')
        return redirect(url_for('admin.users'))

    new_role = request.form.get('role')

    # Vérifie que le rôle est valide
    if new_role not in ['user', 'artist', 'admin']:
        flash('Rôle invalide.', 'danger')
        return redirect(url_for('admin.users'))

    user.role = new_role
    db.session.commit()

    flash(f'Rôle de {user.username} changé en {new_role}.', 'success')
    return redirect(url_for('admin.users'))


@bp.route('/users/<int:id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_user(id):

    user = User.query.get_or_404(id)

    # Empêche l'admin de se désactiver lui-même
    if user.id == current_user.id:
        flash('Vous ne pouvez pas désactiver votre propre compte... ;)', 'danger')
        return redirect(url_for('admin.users'))

    # Bascule entre actif et inactif (soft delete)
    user.is_active = not user.is_active
    db.session.commit()

    status = 'activé' if user.is_active else 'désactivé'
    flash(f'Compte de {user.username} {status}.', 'success')
    return redirect(url_for('admin.users'))


@bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):

    user = User.query.get_or_404(id)

    # Empêche l'admin de se supprimer lui-même
    if user.id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte... ;)', 'danger')
        return redirect(url_for('admin.users'))

    db.session.delete(user)
    db.session.commit()

    flash(f'Utilisateur {user.username} supprimé !', 'info')
    return redirect(url_for('admin.users'))


# -------------------------------- ARTWORKS --------------------------------

@bp.route('/artworks')
@login_required
@admin_required
def artworks():

    all_artworks = Artwork.query.order_by(Artwork.created_at.desc()).all()

    return render_template('admin/artworks.html', artworks=all_artworks)


@bp.route('/artworks/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_artwork(id):

    artwork = Artwork.query.get_or_404(id)

    if artwork.is_sold:
        flash('Impossible de supprimer une œuvre déjà vendue.', 'danger')
        return redirect(url_for('admin.artworks'))

    db.session.delete(artwork)
    db.session.commit()

    flash('Œuvre supprimée !', 'info')
    return redirect(url_for('admin.artworks'))


# -------------------------------- SOURCES --------------------------------
# functools wraps :  https://docs.python.org/3/library/functools.html#functools.wraps