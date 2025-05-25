grade_point_map = {
    "A+": 4.2,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.5,
    "D": 1.0,
    "F": 0.0,
    "I-we": 0.0,
}


def calculate_sgpa(modules):
    total_credits = 0
    total_points = 0
    for m in modules:
        if m.is_gpa and m.grade in grade_point_map:
            gp = grade_point_map[m.grade]
            total_credits += m.credits
            total_points += gp * m.credits
    sgpa = round(total_points / total_credits, 2) if total_credits else 0.0
    return sgpa, total_credits


def get_academic_standing(gpa):
    if gpa >= 3.7:
        return "First Class"
    elif gpa >= 3.3:
        return "Second Class - Upper Division"
    elif gpa >= 3.0:
        return "Second Class - Lower Division"
    elif gpa >= 2.0:
        return "Pass"
    else:
        return "Fail"
