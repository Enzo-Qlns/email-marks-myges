# Utilisation de l'image Python officielle en tant qu'image de base
FROM python:3.11

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Met a l'heure le container
ENV TZ=Europe/Paris
RUN apt install tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# Copie du fichier requirements.txt contenant les dépendances du projet dans le conteneur
COPY . .

# Installation des dépendances du projet
RUN pip install --no-cache-dir -r requirements.txt

# Commande pour exécuter le service quand le conteneur démarre
CMD ["python", "main.py"]