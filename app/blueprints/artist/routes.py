import os
import uuid

from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Artwork, Category
from app.blueprints.artist import bp
from app.blueprints.artist.forms import ArtworkForm
from slugify import slugify


def save_file(file, folder):
    """Sauvegarde un fichier uploadé avec un nom unique (uuid) et retourne son chemin."""

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join('uploads', folder, filename)
    full_path = os.path.join('app', 'static', path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    file.save(full_path)

    return path.replace('\\', '/')


def artist_required(function):
    """Décorateur "@artist_required", refuse l'accès si l'utilisateur n'est pas artiste ou admin."""

    from functools import wraps

    @wraps(function)
    def decorated(*args, **kwargs):
        if not current_user.is_artist() and not current_user.is_admin():
            abort(403)
        return function(*args, **kwargs)

    return decorated


@bp.route('/dashboard')
@login_required
@artist_required
def dashboard():

    # Récupère uniquement les œuvres de l'artiste connecté
    artworks = Artwork.query.filter_by(
        artist_id=current_user.id
    ).order_by(Artwork.created_at.desc()).all()

    return render_template('artist/dashboard.html', artworks=artworks)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
@artist_required
def add():

    form = ArtworkForm()

    # Remplit les choix de catégories dynamiquement
    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]

    if form.validate_on_submit():

        artwork = Artwork()
        artwork.name = form.name.data
        artwork.description = form.description.data
        artwork.price = form.price.data
        artwork.category_id = form.category_id.data
        artwork.artist_id = current_user.id

        # Sauvegarde l'image de prévisualisation si fournie
        if form.preview.data:
            artwork.preview_path = save_file(form.preview.data, 'previews')

        # Sauvegarde le fichier original si fourni
        if form.file.data:
            artwork.file_path = save_file(form.file.data, 'files')

        db.session.add(artwork)
        db.session.flush() # Récupère l'id avant le commit pour le slug

        # Génère le slug avec l'id
        artwork.slug = f"{slugify(artwork.name)}-{artwork.id}" # type: ignore

        db.session.commit()

        flash('Œuvre ajoutée avec succès !', 'success')
        return redirect(url_for('artist.dashboard'))

    return render_template('artist/form.html', form=form, title='Ajouter une œuvre')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@artist_required
def edit(id):

    artwork = Artwork.query.get_or_404(id)

    # Vérifie que l'artiste est bien le propriétaire
    if artwork.artist_id != current_user.id and not current_user.is_admin():
        abort(403)

    form = ArtworkForm(obj=artwork)

    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]

    if form.validate_on_submit():

        artwork.name = form.name.data
        artwork.description = form.description.data
        artwork.price = form.price.data
        artwork.category_id = form.category_id.data

        # Met à jour le slug si le nom a changé
        artwork.slug = f"{slugify(artwork.name)}-{artwork.id}" # type: ignore

        # Remplace l'image si une nouvelle est uploadée
        if form.preview.data:
            artwork.preview_path = save_file(form.preview.data, 'previews')

        # Remplace le fichier si un nouveau est uploadé
        if form.file.data:
            artwork.file_path = save_file(form.file.data, 'files')

        db.session.commit()

        flash('Œuvre modifiée avec succès !', 'success')
        return redirect(url_for('artist.dashboard'))

    return render_template('artist/form.html', form=form, title='Modifier l\'œuvre', artwork=artwork)


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@artist_required
def delete(id):

    artwork = Artwork.query.get_or_404(id)

    # Vérifie que l'artiste est bien le propriétaire
    if artwork.artist_id != current_user.id and not current_user.is_admin():
        abort(403)

    db.session.delete(artwork)
    db.session.commit()

    flash('Œuvre supprimée.', 'info')
    return redirect(url_for('artist.dashboard'))


# -------------------------------- SOURCES --------------------------------
# uuid pour noms de fichiers : https://docs.python.org/3/library/uuid.html
# os.path :                    https://docs.python.org/3/library/os.path.html
# Flask abort :                https://flask.palletsprojects.com/en/3.0.x/api/#flask.abort
# functools wraps :            https://docs.python.org/3/library/functools.html#functools.wraps