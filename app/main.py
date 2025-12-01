from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

# J'initialise la création des tables dans la BDD au démarrage
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SAE Bibliothèque API", description="API RESTful conteneurisée")

# --- Routes pour les Auteurs (CRUD) ---

@app.post("/auteurs/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(database.get_db)):
    # Je crée un nouvel auteur dans la base via l'ORM
    db_author = models.Author(nom=author.nom)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.get("/auteurs/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    # Je récupère la liste des auteurs avec pagination
    return db.query(models.Author).offset(skip).limit(limit).all()

# --- Routes pour les Livres ---

@app.post("/livres/", response_model=schemas.Livre)
def create_book(book: schemas.LivreCreate, db: Session = Depends(database.get_db)):
    # Je vérifie d'abord si l'auteur existe
    author = db.query(models.Author).filter(models.Author.id == book.auteur_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")
    
    # Création du livre
    db_book = models.Livre(titre=book.titre, auteur_id=book.auteur_id)
    
    # Gestion de la relation Many-to-Many (Genres)
    if book.genre_ids:
        genres = db.query(models.Genre).filter(models.Genre.id.in_(book.genre_ids)).all()
        db_book.genres = genres

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# --- Route pour les Genres ---
@app.post("/genres/", response_model=schemas.Genre)
def create_genre(genre: schemas.GenreBase, db: Session = Depends(database.get_db)):
    db_genre = models.Genre(nom=genre.nom)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de gestion de bibliothèque SAE"}
