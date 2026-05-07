# app/blueprints/artworks/routes.py

from flask import render_template, request, jsonify
from flask_login import current_user

from app.blueprints.artworks import bp
from app.models import Artwork, Category


@bp.route('/')
def index():

    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', None, type=int)
    is_ajax = request.args.get('ajax', 0, type=int)

    # Filtre des oeuvres dispo
    query = Artwork.query.filter_by(is_sold=False)

    # Filtre par catégorie via click
    if category_id:
        query = query.filter_by(category_id=category_id)

    # Tri par date — les plus récentes en premier
    query = query.order_by(Artwork.created_at.desc())

    # 12 oeuvres max par page
    artworks = query.paginate(page=page, per_page=12, error_out=False)

    # Toutes les catégories pour les filtres
    categories = Category.query.all()

    # Si requête AJAX (filtre par catégorie), on retourne juste les cartes HTML à injecter, pas la page entière
    if is_ajax:
        html = render_template(
            'artworks/_cards.html',
            artworks=artworks.items
        )
        return jsonify({
            'html': html,
            'has_more': artworks.has_next
        })

    return render_template(
        'artworks/index.html',
        artworks=artworks,
        categories=categories,
        current_category=category_id
    )

# Sans slug mais avec ID
# @bp.route('/artwork/<int:id>')
# def detail(id):
    
#     artwork = Artwork.query.get_or_404(id)

#     return render_template('artworks/detail.html', artwork=artwork)

# Slug pour les URL
@bp.route('/artwork/<slug>')
def detail(slug):
    artwork = Artwork.query.filter_by(slug=slug).first_or_404()
    return render_template('artworks/detail.html', artwork=artwork)

@bp.route('/search')
def search():

    query_str = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    # Recherche dans le nom et la description
    artworks = Artwork.query.filter(
        Artwork.is_sold == False,
        Artwork.name.contains(query_str) | Artwork.description.contains(query_str)
    ).paginate(page=page, per_page=12, error_out=False)

    return render_template(
        'artworks/search.html',
        artworks=artworks,
        query=query_str
    )


# -------------------------------- SOURCES --------------------------------
# Flask-SQLAlchemy pagination : https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/api/#flask_sqlalchemy.SQLAlchemy.paginate
# Flask request.args :         https://flask.palletsprojects.com/en/3.0.x/api/#flask.Request.args
# SQLAlchemy ilike :           https://docs.sqlalchemy.org/en/20/core/operators.html#match-operators
# Flask jsonify :              https://flask.palletsprojects.com/en/3.0.x/api/#flask.json.jsonify