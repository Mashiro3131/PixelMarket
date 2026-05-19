from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user

from app.blueprints.artworks import bp
from app.extensions import db
from app.models import Artwork, Category, Order, User
from app.utils import send_purchase_email


@bp.route('/')
def index():

    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', None, type=int)
    is_ajax = request.args.get('ajax', 0, type=int)

    # Filtre des oeuvres disponibles
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

    # Si requête AJAX (filtre par catégorie), retourne juste les cards HTML
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


@bp.route('/artwork/<slug>')
def detail(slug):

    artwork = Artwork.query.filter_by(slug=slug).first_or_404()

    return render_template('artworks/detail.html', artwork=artwork)


@bp.route('/search')
def search():

    query_str = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    # Fait un JOIN entre les tables pour aussi chercher par artiste
    artworks = Artwork.query.join(User, Artwork.artist_id == User.id).filter(
        Artwork.is_sold == False,
        Artwork.name.contains(query_str) |
        Artwork.description.contains(query_str) |
        User.username.contains(query_str)
    ).paginate(page=page, per_page=12, error_out=False)

    return render_template(
        'artworks/search.html',
        artworks=artworks,
        query=query_str
    )



@bp.route('/buy/<int:id>', methods=['POST'])
@login_required
def buy(id):

    artwork = Artwork.query.get_or_404(id)

    # Vérifie que l'oeuvre est encore disponible
    if artwork.is_sold:
        flash('Cette oeuvre a déjà été vendue.', 'danger')
        return redirect(url_for('artworks.detail', slug=artwork.slug))

    # Vérifie que l'acheteur n'est pas l'artiste
    if artwork.artist_id == current_user.id:
        flash('Vous ne pouvez pas acheter votre propre oeuvre.', 'danger')
        return redirect(url_for('artworks.detail', slug=artwork.slug))

    # Crée la commande
    order = Order()
    order.buyer_id = current_user.id
    order.artwork_id = artwork.id
    order.amount = artwork.price

    # Marque l'oeuvre comme vendue
    artwork.is_sold = True

    db.session.add(order)
    db.session.commit()

    # Envoie l'email avec le fichier en pièce jointe
    try: # Si l'email échoue, annule la commande et remet l'oeuvre disponible
        send_purchase_email(current_user, artwork)
        order.email_sent = True
        db.session.commit()
    except Exception as e:
        db.session.delete(order)
        artwork.is_sold = False
        db.session.commit()
        flash('Erreur lors de l\'envoi de l\'email. Veuillez réessayer.', 'danger')
        return redirect(url_for('artworks.detail', slug=artwork.slug))

    flash('Achat confirmé ! Vous recevrez votre oeuvre par email.', 'success')
    return redirect(url_for('account.orders'))



@bp.route('/artwork/<slug>/recap')
@login_required
def recap(slug):

    artwork = Artwork.query.filter_by(slug=slug).first_or_404()

    # Vérifie que l'oeuvre est encore disponible
    if artwork.is_sold:
        flash('Cette œuvre a déjà été vendue.', 'danger')
        return redirect(url_for('artworks.detail', slug=slug))

    return render_template('artworks/recap.html', artwork=artwork)

# -------------------------------- SOURCES --------------------------------
# Flask-SQLAlchemy pagination : https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/api/
# Flask request.args :          https://flask.palletsprojects.com/en/3.0.x/api/#flask.Request.args
# Flask jsonify :               https://flask.palletsprojects.com/en/3.0.x/api/#flask.json.jsonify
# Flask-Login login_required :  https://flask-login.readthedocs.io/en/latest/#flask_login.login_required