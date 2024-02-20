# Utilisation de l'image Python officielle en tant qu'image de base
FROM python:3.10

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copie du fichier requirements.txt contenant les dépendances du projet dans le conteneur
COPY requirements.txt .

# Installation des dépendances du projet
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source du service dans le conteneur
COPY . .

# Commande pour exécuter le service quand le conteneur démarre
CMD ["python", "main.py"]
