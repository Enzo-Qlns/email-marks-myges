from services.myges import myges
from services.database import Marks
from services.mail import mail

from serializers.gradesSerializers import messageListEntity

from config import settings

from datetime import datetime, timedelta

import schedule
import time

import utils

# Services

mygesService = myges(
    LOGIN=settings.LOGIN,
    PASSWORD=settings.PASSWORD
)
mailService = mail()

def schedule_job():
    # Traitement du resultat
    result = mygesService.get_grades()

    objectToInsert = [
        {
            'course' :element.get('course'),
            'grades' :element.get('grades'),
            'exam' :element.get('exam'),
        }
        for element in result
    ]

    # Recupere le dernier object de note
    objectInserted = messageListEntity(Marks.find().sort({"_id":-1}).limit(1))
    if objectInserted != []:
        # Ajoute en base le nouvel object de note
        Marks.insert_one({"list_grades":objectToInsert, "created_at":datetime.now()})
        
        # Calcul de la date limite (1 heure plus tôt que maintenant)
        date_limite = datetime.now() - timedelta(seconds=30)

        # Supprimer tous les documents de plus de 1h
        Marks.delete_many({"created_at": {"$lt": date_limite}})

        # Compare l'object de note recupere de l'api et celui en base
        grade_updates = utils.compare_grades(objectInserted[0].get('list_grades'), objectToInsert)
        if grade_updates != []:
            mailService.send_marks_email(
                to='equelenis@myges.fr',
                grade_updates=grade_updates
            )
    else:
        Marks.insert_one({"list_grades":objectToInsert, "created_at":datetime.now()})

# Planifier l'exécution de la fonction toutes les 15 secondes
schedule.every(5).seconds.do(schedule_job)

while True:
    schedule.run_pending()
    time.sleep(1)
