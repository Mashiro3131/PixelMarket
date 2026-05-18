import os
from flask import render_template
from flask_mail import Message

from app.extensions import mail


def send_email(to, subject, template, **kwargs):
    """Envoie un email HTML à partir d'un template Jinja2."""

    msg = Message(
        subject=subject,
        recipients=[to]
    )

    # Génère le corps de l'email depuis le template
    msg.html = render_template(template, **kwargs)

    mail.send(msg)


def send_purchase_email(user, artwork):
    """Envoie l'email de confirmation d'achat avec le fichier en pièce jointe."""

    msg = Message(
        subject=f'PixelMarket — Votre achat : {artwork.name}',
        recipients=[user.email]
    )

    msg.html = render_template(
        'emails/purchase.html',
        user=user,
        artwork=artwork
    )

    # Attache le fichier original si disponible
    if artwork.file_path:
        full_path = os.path.join('app', 'static', artwork.file_path)
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                filename = artwork.file_path.split('/')[-1]
                msg.attach(
                    filename=filename,
                    content_type='application/octet-stream',
                    data=f.read()
                )

    mail.send(msg)


def send_reset_email(user):
    """Envoie l'email de reset de mot de passe."""

    from flask import url_for

    reset_url = url_for(
        'auth.reset',
        token=user.reset_token,
        _external=True
    )

    msg = Message(
        subject='PixelMarket — Réinitialisation de mot de passe',
        recipients=[user.email]
    )

    msg.html = render_template(
        'emails/reset.html',
        user=user,
        reset_url=reset_url
    )

    mail.send(msg)


# -------------------------------- SOURCES --------------------------------
# Flask-Mail : https://flask-mail.readthedocs.io/en/latest/
# Attachments: https://flask-mail.readthedocs.io/en/latest/#attachments