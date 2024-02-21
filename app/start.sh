#!/bin/bash

# Suppression des anciens services
docker rm --force email-marks-myges && docker rmi --force email-marks-myges:latest

# Construction de l'image
docker build -t email-marks-myges:latest .

# Lancement du nouveau service
docker run -d --name email-marks-myges email-marks-myges:latest

