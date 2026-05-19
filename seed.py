from app import create_app
from app.extensions import db, bcrypt
from app.models import User, Artwork, Category
from colorama import Fore, Style
from slugify import slugify

app = create_app()



with app.app_context():

    # Remet la bd à zéro
    db.drop_all()
    db.create_all()

# ----------------------------- CATEGORIES --------------------------------
    photo = Category(name="Photo") # type: ignore
    video = Category(name="Vidéo") # type: ignore
    musique = Category(name="Musique") # type: ignore
    affiche = Category(name="Affiche") # type: ignore

    db.session.add_all([photo, video, musique, affiche])
    db.session.commit()

# -------------------------------- USERS --------------------------------
    
    admin = User()
    admin.username = "admin"
    admin.email = "admin@pixelmarket.com"
    admin.password_hash = bcrypt.generate_password_hash("admin1234").decode("utf-8")
    admin.role = "admin"

    artiste = User()
    artiste.username = "Nyrio_O"
    artiste.email = "nyria.graber@ecal.ch"
    artiste.password_hash = bcrypt.generate_password_hash("empanadas123!").decode("utf-8")
    artiste.role = "artist"
    
    user = User()
    user.username = "n2cotine"
    user.email = "mengisennico@gmail.com"
    user.password_hash = bcrypt.generate_password_hash("user1234!").decode("utf-8")
    user.role = "user"

    db.session.add_all([admin, artiste, user])
    db.session.commit()

# -------------------------------- OEUVRES --------------------------------
    oeuvre1 = Artwork()
    oeuvre1.name = "Keltainen Kuu"
    oeuvre1.description = "Une photo capturant la lumière du coucher de soleil."
    oeuvre1.price = 2500.00
    oeuvre1.artist_id = artiste.id
    oeuvre1.category_id = photo.id

    oeuvre2 = Artwork()
    oeuvre2.name = "Lonely Boys"
    oeuvre2.description = "Affiche de deux frères errant dans les rues de londres"
    oeuvre2.price = 85.00
    oeuvre2.artist_id = artiste.id
    oeuvre2.category_id = photo.id

    oeuvre3 = Artwork()
    oeuvre3.name = "Abstract Noir"
    oeuvre3.description = "Composition abstraite en noir et blanc."
    oeuvre3.price = 200.00
    oeuvre3.artist_id = artiste.id
    oeuvre3.category_id = affiche.id

    oeuvre4 = Artwork()
    oeuvre4.name = "Kou 2 Tatane"
    oeuvre4.description = "Sample d'un remix tek acide bounce"
    oeuvre4.price = 15.00
    oeuvre4.artist_id = artiste.id
    oeuvre4.category_id = musique.id

    oeuvre5 = Artwork()
    oeuvre5.name = "The setting sun"
    oeuvre5.description = "Vidéo 4K d\"un soleil couchant en montagne."
    oeuvre5.price = 45.00
    oeuvre5.artist_id = artiste.id
    oeuvre5.category_id = video.id
    
    db.session.add_all([oeuvre1, oeuvre2, oeuvre3, oeuvre4, oeuvre5])
    db.session.commit()
    
# -------------------------------- SLUGGIFY --------------------------------
    
    for artwork in Artwork.query.all():
            artwork.slug = f"{slugify(artwork.name)}-{artwork.id}" 
    db.session.commit()
    
# -------------------------------- RECAP --------------------------------

    print("Base de données remplie avec succès !")
    print(f"{Category.query.count()} catégories")
    print(f"{User.query.count()} utilisateurs")
    print(f"{Artwork.query.count()} œuvres")
    print()
    print(Fore.GREEN + "Comptes de test :")
    print(Fore.LIGHTGREEN_EX + "admin@pixelmarket.com  / admin1234!   (admin)")
    print(Fore.LIGHTGREEN_EX + "nyria.graber@ecal.ch   / empanadas123!(artiste)")
    print(Fore.LIGHTGREEN_EX + "mengisennico@gmail.com / user1234!    (user)")
    print(Style.RESET_ALL)