from flask import Blueprint

bp = Blueprint('account', __name__, url_prefix='/account')

from app.blueprints.account import routes # noqa: F401, E402
