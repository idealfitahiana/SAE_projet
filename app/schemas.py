from pydantic import BaseModel
from typing import List, Optional

# --- Schemas pour Genre ---
class GenreBase(BaseModel):
    nom: str

class Genre(GenreBase):
    id: int
    class Config:
        orm_mode = True

# --- Schemas pour Livre ---
class LivreBase(BaseModel):
    titre: str

class LivreCreate(LivreBase):
    auteur_id: int
    genre_ids: List[int] = []

class Livre(LivreBase):
    id: int
    genres: List[Genre] = []
    class Config:
        orm_mode = True

# --- Schemas pour Auteur ---
class AuthorBase(BaseModel):
    nom: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    livres: List[Livre] = []
    class Config:
        orm_mode = True
