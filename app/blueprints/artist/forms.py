from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ArtworkForm(FlaskForm):

    # Nom de l'oeuvre
    name = StringField(
        'Nom de l\'œuvre',
        validators=[DataRequired(), Length(max=200)]
    )

    # Description de l'oeuvre
    description = TextAreaField(
        'Description',
        validators=[Length(max=2000)]
    )

    # Prix
    price = DecimalField(
        'Prix (CHF)',
        validators=[
            DataRequired(),
            NumberRange(min=0.01, message='Le prix doit être supérieur à 0.')
        ],
        places=2
    )

    # Catégorie
    category_id = SelectField(
        'Catégorie',
        coerce=int,
        validators=[DataRequired()]
    )

    # Image affichée sur le site
    preview = FileField(
        'Image de prévisualisation',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images uniquement.')
        ]
    )

    # Fichier original envoyé après achat
    file = FileField(
        'Fichier original',
        validators=[
            FileAllowed(
                ['jpg', 'jpeg', 'png', 'tif', 'webp', 'pdf', 'mp3', 'mp4'],
                'Format non supporté.'
            )
        ]
    )

    submit = SubmitField('Enregistrer')


# -------------------------------- SOURCES --------------------------------
# Flask-WTF FileField :   https://flask-wtf.readthedocs.io/en/1.2.x/form/
# WTForms DecimalField :  https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DecimalField
# WTForms SelectField :   https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.SelectField