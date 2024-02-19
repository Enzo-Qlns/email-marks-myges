# Fonction pour comparer les notes
def compare_grades(old_grades, new_grades):
    result = []
    for old, new in zip(old_grades, new_grades):
        if new is not None or old is not None :
            if old["grades"] != new["grades"]:
                old_grade = old["grades"]
                new_grade = new["grades"]
                course_name = old["course"]
                diff_grade = [grade for grade in new_grade if grade not in old_grade]
                result.append({course_name : diff_grade})
    return result