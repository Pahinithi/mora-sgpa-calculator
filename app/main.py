from fastapi import FastAPI
from schema.gpa_schema import Semester
from grade.function import calculate_sgpa, get_academic_standing

app = FastAPI()


@app.post("/sgpa/")
def calculate_semester_sgpa(semester: Semester):
    sgpa, credits = calculate_sgpa(semester.modules)
    return {"semester": semester.name, "sgpa": sgpa, "credits": credits}


@app.post("/final-sgpa/")
def calculate_final_sgpa(semesters: list[Semester]):
    total_credits = 0
    total_points = 0
    for sem in semesters:
        sgpa, credits = calculate_sgpa(sem.modules)
        total_credits += credits
        total_points += sgpa * credits
    final_sgpa = round(total_points / total_credits, 2) if total_credits else 0.0
    return {"final_sgpa": final_sgpa, "standing": get_academic_standing(final_sgpa)}
