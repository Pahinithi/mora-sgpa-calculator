from sqlalchemy.orm import sessionmaker
from .models import engine, User, SGPA
from datetime import datetime
import requests

# Create session factory
Session = sessionmaker(bind=engine)

def save_user_data(name, reg_number, department, batch, semester_data):
    """
    Save user data and their SGPA records to the database
    """
    session = Session()
    try:
        # Create or get user
        user = session.query(User).filter_by(registration_number=reg_number).first()
        if not user:
            user = User(
                name=name,
                registration_number=reg_number,
                department=department,
                batch=batch
            )
            session.add(user)
            session.flush()  # Get the user ID
        
        # Calculate semester-wise GPAs
        semester_gpas = []
        for semester in semester_data:
            response = requests.post("http://localhost:8000/sgpa/", json=semester)
            if response.status_code == 200:
                sem_data = response.json()
                semester_gpas.append({
                    "semester": semester["name"],
                    "sgpa": sem_data["sgpa"],
                    "credits": sem_data["credits"]
                })
        
        # Calculate final SGPA
        response = requests.post("http://localhost:8000/final-sgpa/", json=semester_data)
        if response.status_code == 200:
            final_data = response.json()
            final_sgpa = final_data["final_sgpa"]
            standing = final_data["standing"]
        else:
            final_sgpa = None
            standing = None
        
        # Save SGPA records
        for semester in semester_data:
            for module in semester["modules"]:
                if module["code"] and module["title"] and module["grade"] != "Not Selected":
                    # Find the corresponding semester GPA
                    sem_gpa = next((g for g in semester_gpas if g["semester"] == semester["name"]), None)
                    
                    sgpa_record = SGPA(
                        user_id=user.id,
                        semester=semester["name"],
                        module_code=module["code"],
                        module_title=module["title"],
                        grade=module["grade"],
                        credits=module["credits"],
                        is_gpa=module["is_gpa"],
                        semester_sgpa=sem_gpa["sgpa"] if sem_gpa else None,
                        semester_credits=sem_gpa["credits"] if sem_gpa else None,
                        final_sgpa=final_sgpa,
                        academic_standing=standing
                    )
                    session.add(sgpa_record)
        
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error saving data: {str(e)}")
        return False
    finally:
        session.close()

def get_user_data(reg_number):
    """
    Retrieve user data and their SGPA records
    """
    session = Session()
    try:
        print(f"Searching for registration number: {reg_number}")  # Debug log
        user = session.query(User).filter_by(registration_number=reg_number).first()
        if user:
            print(f"Found user: {user.name}")  # Debug log
            sgpa_records = session.query(SGPA).filter_by(user_id=user.id).all()
            print(f"Found {len(sgpa_records)} SGPA records")  # Debug log
            return {
                "user": {
                    "name": user.name,
                    "registration_number": user.registration_number,
                    "department": user.department,
                    "batch": user.batch
                },
                "sgpa_records": [
                    {
                        "semester": record.semester,
                        "module_code": record.module_code,
                        "module_title": record.module_title,
                        "grade": record.grade,
                        "credits": record.credits,
                        "is_gpa": record.is_gpa,
                        "semester_sgpa": record.semester_sgpa,
                        "semester_credits": record.semester_credits,
                        "final_sgpa": record.final_sgpa,
                        "academic_standing": record.academic_standing
                    }
                    for record in sgpa_records
                ]
            }
        print("No user found")  # Debug log
        return None
    except Exception as e:
        print(f"Error retrieving data: {str(e)}")  # Debug log
        return None
    finally:
        session.close() 