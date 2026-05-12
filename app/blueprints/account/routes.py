from flask_login import login_required
from flask import render_template

from app.blueprints.account import bp

# Pour eviter les erreurs Jinja de redirection sur cette page
@bp.route('/profile')
@login_required
def profile():
    return 'Profil — bientôt disponible'