import schedule
import time
from datetime import datetime, timedelta
from services.myges import myges
from services.database import Marks
from services.mail import mail
from serializers.gradesSerializers import messageListEntity
from config import settings
import utils

mygesService = myges(LOGIN=settings.LOGIN, PASSWORD=settings.PASSWORD)
mailService = mail()

def schedule_job():
    # Traitement du resultat
    result = mygesService.get_grades()

    objectToInsert = [
        {
            'course': element.get('course'),
            'grades': element.get('grades'),
            'exam': element.get('exam'),
        }
        for element in result
    ]

    # Récupérer le dernier object de note
    objectInserted = messageListEntity(Marks.find().sort({"_id": -1}).limit(1))
    if objectInserted != []:
        # Ajouter en base le nouvel object de note
        Marks.insert_one({"listGrades": objectToInsert, "created_at": datetime.now()})
        
        # Calcul de la date limite (1 heure plus tôt que maintenant)
        date_limite = datetime.now() - timedelta(seconds=30)

        # Supprimer tous les documents de plus de 1h
        Marks.delete_many({"created_at": {"$lt": date_limite}})

        # Compare l'object de note récupéré de l'api et celui en base
        grade_updates = utils.compare_grades(objectInserted[0].get('listGrades'), objectToInsert)
        if grade_updates != []:
            mailService.send_marks_email(
                to='equelenis@myges.fr',
                is_exam=False,
                grade_updates=grade_updates
            )

        exam_updates = utils.compare_exam(objectInserted[0].get('listGrades'), objectToInsert)
        if exam_updates != []:
            mailService.send_marks_email(
                to='equelenis@myges.fr',
                is_exam=True,
                grade_updates=exam_updates
            )
    else:
        Marks.insert_one({"listGrades": objectToInsert, "created_at": datetime.now()})

# Planifier l'exécution de la fonction toutes les 15 secondes
schedule.every(5).seconds.do(schedule_job)

while True:
    schedule.run_pending()
    time.sleep(1)
