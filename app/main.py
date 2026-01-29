from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, database

# Initialisation des tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="SAE Bibliothèque API", 
    description="API RESTful complète (GET, POST, PUT, DELETE)",
    version="1.0.0"
)

# --- ROUTES AUTEURS ---

@app.post("/auteurs/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED, tags=["Auteurs"])
def create_author(author: schemas.AuthorCreate, db: Session = Depends(database.get_db)):
    db_author = models.Author(nom=author.nom)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.get("/auteurs/", response_model=list[schemas.Author], tags=["Auteurs"])
def read_authors(db: Session = Depends(database.get_db)):
    return db.query(models.Author).all()

@app.put("/auteurs/{author_id}", response_model=schemas.Author, tags=["Auteurs"])
def update_author(author_id: int, author_update: schemas.AuthorUpdate, db: Session = Depends(database.get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")
    if author_update.nom is not None:
        db_author.nom = author_update.nom
    db.commit()
    db.refresh(db_author)
    return db_author

@app.delete("/auteurs/{author_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Auteurs"])
def delete_author(author_id: int, db: Session = Depends(database.get_db)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")
    try:
        db.delete(db_author)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="L'auteur a encore des livres liés.")
    return None

# --- ROUTES LIVRES ---

@app.post("/livres/", response_model=schemas.Livre, status_code=status.HTTP_201_CREATED, tags=["Livres"])
def create_book(book: schemas.LivreCreate, db: Session = Depends(database.get_db)):
    db_book = models.Livre(titre=book.titre, auteur_id=book.auteur_id)
    if book.genre_ids:
        genres = db.query(models.Genre).filter(models.Genre.id.in_(book.genre_ids)).all()
        db_book.genres = genres
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/livres/", response_model=list[schemas.Livre], tags=["Livres"])
def read_books(db: Session = Depends(database.get_db)):
    return db.query(models.Livre).all()

@app.put("/livres/{livre_id}", response_model=schemas.Livre, tags=["Livres"])
def update_book(livre_id: int, book_update: schemas.LivreUpdate, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Livre).filter(models.Livre.id == livre_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    if book_update.titre is not None:
        db_book.titre = book_update.titre
    if book_update.auteur_id is not None:
        db_book.auteur_id = book_update.auteur_id
    if book_update.genre_ids is not None:
        genres = db.query(models.Genre).filter(models.Genre.id.in_(book_update.genre_ids)).all()
        db_book.genres = genres
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/livres/{livre_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Livres"])
def delete_book(livre_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Livre).filter(models.Livre.id == livre_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    db.delete(db_book)
    db.commit()
    return None
