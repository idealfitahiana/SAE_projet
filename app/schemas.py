from pydantic import BaseModel
from typing import List, Optional

# --- Schémas pour la Biographie (Relation One-to-One) ---
class BiographieBase(BaseModel):
    contenu: str

class BiographieCreate(BiographieBase):
    auteur_id: int

class Biographie(BiographieBase):
    id: int
    class Config:
        orm_mode = True

# --- Schémas pour les Genres ---
class GenreBase(BaseModel):
    nom: str

class Genre(GenreBase):
    id: int
    class Config:
        orm_mode = True

# --- Schémas pour les Livres ---
class LivreBase(BaseModel):
    titre: str

class LivreCreate(LivreBase):
    auteur_id: int
    genre_ids: List[int] = []

# Modèle pour la mise à jour (PUT)
class LivreUpdate(BaseModel):
    titre: Optional[str] = None
    auteur_id: Optional[int] = None
    genre_ids: Optional[List[int]] = None

class Livre(LivreBase):
    id: int
    genres: List[Genre] = []
    class Config:
        orm_mode = True

# --- Schémas pour les Auteurs ---
class AuthorBase(BaseModel):
    nom: str

class AuthorCreate(AuthorBase):
    pass

# Modèle pour la mise à jour (PUT)
class AuthorUpdate(BaseModel):
    nom: Optional[str] = None

class Author(AuthorBase):
    id: int
    livres: List[Livre] = []
    biographie: Optional[Biographie] = None
    class Config:
        orm_mode = True
