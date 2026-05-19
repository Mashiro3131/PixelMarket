from flask import Blueprint

bp = Blueprint('artist', __name__, url_prefix='/artist')

from app.blueprints.artist import routes # noqa: F401, E402
