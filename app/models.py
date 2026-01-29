from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# --- TABLE D'ASSOCIATION (MANY-TO-MANY) ---
# Nous utilisons cette table technique pour lier les Livres et les Genres.
# Un livre peut avoir plusieurs genres et un genre peut contenir plusieurs livres.
# Nous avons ajouté 'ondelete="CASCADE"' pour que le nettoyage des liaisons 
# soit automatique si un livre ou un genre est supprimé.
livre_genre_association = Table(
    'livre_genre',
    Base.metadata,
    Column('livre_id', Integer, ForeignKey('livres.id', ondelete="CASCADE"), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True)
)

class Author(Base):
    """
    Représente un écrivain dans notre bibliothèque.
    """
    __tablename__ = "auteurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)

    # RELATION 1-1 : Un auteur a une seule biographie.
    # 'cascade="all, delete-orphan"' garantit que si l'auteur est supprimé, 
    # sa biographie disparait aussi de la base de données.
    biographie = relationship(
        "Biographie", 
        back_populates="auteur", 
        uselist=False, 
        cascade="all, delete-orphan"
    )

    # RELATION 1-N : Un auteur peut avoir écrit plusieurs livres.
    # Même logique de cascade pour éviter les livres sans auteur (orphelins).
    livres = relationship(
        "Livre", 
        back_populates="auteur", 
        cascade="all, delete-orphan"
    )

class Biographie(Base):
    """
    Détails personnels sur un auteur. 
    Lien strict 1-1 avec la table 'auteurs'.
    """
    __tablename__ = "biographies"

    id = Column(Integer, primary_key=True, index=True)
    contenu = Column(String)
    
    # La clé étrangère pointe vers l'auteur. 
    # 'unique=True' assure qu'un auteur ne peut pas avoir deux biographies.
    auteur_id = Column(
        Integer, 
        ForeignKey("auteurs.id", ondelete="CASCADE"), 
        unique=True,
        nullable=False
    )
    auteur = relationship("Author", back_populates="biographie")

class Livre(Base):
    """
    Représente un ouvrage physique ou numérique.
    """
    __tablename__ = "livres"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, index=True)
    
    # Clé étrangère vers l'auteur (Relation Many-to-One).
    # nullable=False car un livre dans notre système doit obligatoirement avoir un auteur.
    auteur_id = Column(
        Integer, 
        ForeignKey("auteurs.id", ondelete="CASCADE"),
        nullable=False
    )
    auteur = relationship("Author", back_populates="livres")
    
    # Lien vers les genres via la table d'association définie plus haut.
    genres = relationship(
        "Genre", 
        secondary=livre_genre_association, 
        back_populates="livres"
    )

class Genre(Base):
    """
    Catégories littéraires (ex: Science-Fiction, Drame, etc.).
    """
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, index=True)

    # Relation inverse pour savoir quels livres appartiennent à ce genre.
    livres = relationship(
        "Livre", 
        secondary=livre_genre_association, 
        back_populates="genres"
    )
