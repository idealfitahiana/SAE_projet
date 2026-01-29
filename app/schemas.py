from pydantic import BaseModel, Field
from typing import List, Optional

# --- SCHÉMAS POUR LES GENRES ---
class GenreBase(BaseModel):
    nom: str = Field(..., example="Science-Fiction", description="Nom unique du genre littéraire")

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True

# --- SCHÉMAS POUR LA BIOGRAPHIE ---
class BiographieBase(BaseModel):
    contenu: str = Field(..., example="Né à Paris en 1802, écrivain romantique...", description="Détails de la vie de l'auteur")

class BiographieCreate(BiographieBase):
    # Lors de la création, on doit spécifier à quel auteur elle appartient
    auteur_id: int

class Biographie(BiographieBase):
    id: int
    
    class Config:
        from_attributes = True

# --- SCHÉMAS POUR LES LIVRES ---
class LivreBase(BaseModel):
    titre: str = Field(..., example="Les Misérables")

class LivreCreate(LivreBase):
    # La contrainte 'nullable=False' du modèle est répercutée ici : l'ID de l'auteur est obligatoire
    auteur_id: int
    # On permet d'associer des genres dès la création
    genre_ids: List[int] = []

class Livre(LivreBase):
    id: int
    auteur_id: int
    genres: List[Genre] = []

    class Config:
        from_attributes = True

# --- SCHÉMAS POUR LES AUTEURS ---
class AuthorBase(BaseModel):
    nom: str = Field(..., example="Victor Hugo")

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    # On ajoute ces champs pour que le GET /auteurs/ affiche 
    # automatiquement les données liées (grâce aux relations SQLAlchemy)
    biographie: Optional[Biographie] = None
    livres: List[Livre] = []

    class Config:
        from_attributes = True
