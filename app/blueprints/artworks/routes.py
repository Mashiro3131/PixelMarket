from app.blueprints.artworks import bp

@bp.route('/')
def index():
    return 'Galerie — bientôt disponible'