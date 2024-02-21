#!/bin/bash

docker rm --force send-email-new-mark && docker rmi --force send-email-new-mark:latest
docker build -t send-email-new-mark:latest .  # Construire l'image Docker à partir du Dockerfile
docker run -d --name send-email-new-mark send-email-new-mark:latest  # Exécuter le conteneur en arrière-plan avec un nom spécifié

