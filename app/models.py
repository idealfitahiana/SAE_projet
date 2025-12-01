from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Table d'association pour la relation Many-to-Many entre Livres et Genres
# Comme demandé, cela crée la table de liaison dans la BDD [cite: 23]
livre_genre_association = Table(
    'livre_genre', Base.metadata,
    Column('livre_id', Integer, ForeignKey('livres.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

class Author(Base):
    __tablename__ = "auteurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)

    # Relation One-to-One : Un auteur a une seule biographie [cite: 21]
    biographie = relationship("Biographie", back_populates="auteur", uselist=False)

    # Relation One-to-Many : Un auteur peut écrire plusieurs livres [cite: 22]
    livres = relationship("Livre", back_populates="auteur")

class Biographie(Base):
    __tablename__ = "biographies"

    id = Column(Integer, primary_key=True, index=True)
    contenu = Column(String)
    auteur_id = Column(Integer, ForeignKey("auteurs.id"), unique=True)

    # Lien inverse pour la relation One-to-One
    auteur = relationship("Author", back_populates="biographie")

class Livre(Base):
    __tablename__ = "livres"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, index=True)
    auteur_id = Column(Integer, ForeignKey("auteurs.id"))

    # Lien inverse pour la relation Many-to-One (Plusieurs livres -> Un auteur)
    auteur = relationship("Author", back_populates="livres")

    # Relation Many-to-Many : Un livre peut avoir plusieurs genres [cite: 23]
    genres = relationship("Genre", secondary=livre_genre_association, back_populates="livres")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True)

    # Lien inverse Many-to-Many
    livres = relationship("Livre", secondary=livre_genre_association, back_populates="genres")
