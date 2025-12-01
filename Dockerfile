# J'utilise une image Python officielle légère
FROM python:3.9-slim

# Je définis le répertoire de travail dans le conteneur
WORKDIR /app

# Je copie les dépendances et les installe
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Je copie tout le code de l'application
COPY . .

# Je lance l'application avec Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
