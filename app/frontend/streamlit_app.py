import streamlit as st
import requests

st.set_page_config(page_title="SGPA Calculator", layout="wide")
st.title("🎓 SGPA Calculator | University of Moratuwa - Faculty of Business")

BASE_URL = "http://localhost:8000"  # FastAPI backend


# Grade input UI per module
def get_grade_point_input(sem_index, mod_index):
    st.write(f"**Module {mod_index + 1}**")
    code = st.text_input("Module Code", key=f"code_{sem_index}_{mod_index}")
    title = st.text_input("Module Title", key=f"title_{sem_index}_{mod_index}")
    grade = st.selectbox(
        "Grade",
        ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "I-we", "F"],
        key=f"grade_{sem_index}_{mod_index}",
    )
    credits = st.number_input(
        "Credits", 0.0, 6.0, step=0.5, key=f"cred_{sem_index}_{mod_index}"
    )
    is_gpa = st.checkbox(
        "Is GPA Module", value=True, key=f"gpa_{sem_index}_{mod_index}"
    )
    return {
        "code": code,
        "title": title,
        "grade": grade,
        "credits": credits,
        "is_gpa": is_gpa,
    }


st.sidebar.title("Settings")
num_semesters = 8
semesters = []

# Semester input blocks
for s in range(num_semesters):
    with st.expander(f"Semester {s + 1}", expanded=(s == 0)):
        module_count = st.number_input(
            f"Number of Modules (Semester {s + 1})", 1, 20, 5, key=f"mod_count_{s}"
        )
        modules = [get_grade_point_input(s, i) for i in range(int(module_count))]
        semesters.append({"name": f"Semester {s + 1}", "modules": modules})

# Internship
with st.expander("Internship", expanded=False):
    intern_module_count = st.number_input(
        "Number of Internship Modules", 1, 10, 1, key="intern_mods"
    )
    intern_modules = [
        get_grade_point_input(8, i) for i in range(int(intern_module_count))
    ]
    semesters.append({"name": "Internship", "modules": intern_modules})

# Submit
if st.button("Calculate Final SGPA"):
    with st.spinner("Calculating..."):
        response = requests.post(f"{BASE_URL}/final-sgpa/", json=semesters)
        if response.status_code == 200:
            data = response.json()
            st.success(f"🎓 Final SGPA: {data['final_sgpa']}")
            st.info(f"🏅 Academic Standing: {data['standing']}")
        else:
            st.error("Failed to calculate SGPA. Please check inputs and backend.")
