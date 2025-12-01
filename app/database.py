from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Je récupère l'URL de la base de données depuis les variables d'environnement (bonnes pratiques Docker)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/bibliotheque")

# J'initialise le moteur de base de données avec SQLAlchemy
engine = create_engine(DATABASE_URL)

# Je crée une session locale pour mes transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour mes modèles ORM
Base = declarative_base()

# Fonction utilitaire pour récupérer la session DB dans mes routes API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
