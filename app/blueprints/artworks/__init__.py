from flask import Blueprint

bp = Blueprint('artworks', __name__)

from app.blueprints.artworks import routes  # noqa: F401, E402
