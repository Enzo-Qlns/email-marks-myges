#!/bin/bash

# Suppression des anciens services
docker rm --force send-email-new-mark && docker rmi --force send-email-new-mark:latest

# Construction de l'image
docker build -t send-email-new-mark:latest .

# Lancement du nouveau service
docker run -d --name send-email-new-mark send-email-new-mark:latest

