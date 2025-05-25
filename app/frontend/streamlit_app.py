import streamlit as st
import requests
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io
import json
import os
from datetime import datetime
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.operations import save_user_data, get_user_data

# Initialize session state variables
if "semester_data" not in st.session_state:
    st.session_state.semester_data = [
        {"name": f"Semester {i+1}", "modules": []} for i in range(8)
    ]

if "name" not in st.session_state:
    st.session_state.name = ""

if "reg_number" not in st.session_state:
    st.session_state.reg_number = ""

if "department" not in st.session_state:
    st.session_state.department = ""

if "batch" not in st.session_state:
    st.session_state.batch = ""

st.set_page_config(page_title="SGPA Calculator", layout="wide")
st.title("🎓 SGPA Calculator | University of Moratuwa - Faculty of Business")

BASE_URL = "http://localhost:8000"  # FastAPI backend

# Student Information Section
st.sidebar.title("Student Information")
student_name = st.sidebar.text_input("Full Name")
reg_number = st.sidebar.text_input("Registration Number")
department = st.sidebar.selectbox(
    "Department",
    ["Business Analytics",
     "Financial Service Management",
     "Business Process Management"]
)
batch = st.sidebar.text_input("Batch (e.g., Batch 20)")

# Grade input UI per module
def get_grade_point_input(sem_index, mod_index):
    st.write(f"**Module {mod_index + 1}**")
    code = st.text_input("Module Code", key=f"code_{sem_index}_{mod_index}")
    title = st.text_input("Module Title", key=f"title_{sem_index}_{mod_index}")
    grade = st.selectbox(
        "Grade",
        ["Not Selected", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "I-we", "F"],
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
    # Validate student information
    if not all([student_name, reg_number, department, batch]):
        st.error("Please fill in all student information fields in the sidebar.")
    else:
        with st.spinner("Calculating..."):
            # Filter out empty semesters
            filled_semesters = []
            for semester in semesters:
                has_data = False
                for module in semester["modules"]:
                    if module["code"] and module["title"] and module["grade"] != "Not Selected":
                        has_data = True
                        break
                if has_data:
                    filled_semesters.append(semester)
            
            # Calculate semester-wise GPAs
            semester_gpas = []
            for semester in filled_semesters:
                response = requests.post(f"{BASE_URL}/sgpa/", json=semester)
                if response.status_code == 200:
                    sem_data = response.json()
                    semester_gpas.append({
                        "semester": semester["name"],
                        "sgpa": sem_data["sgpa"],
                        "credits": sem_data["credits"]
                    })
            
            # Calculate final SGPA
            response = requests.post(f"{BASE_URL}/final-sgpa/", json=filled_semesters)
            if response.status_code == 200:
                data = response.json()
                
                # Display student information
                st.subheader("Student Information")
                st.write(f"**Name:** {student_name}")
                st.write(f"**Registration Number:** {reg_number}")
                st.write(f"**Department:** {department}")
                st.write(f"**Batch:** {batch}")
                
                # Display semester-wise results
                st.success(f"🎓 Final SGPA: {data['final_sgpa']}")
                st.info(f"🏅 Academic Standing: {data['standing']}")
                
                # Display semester-wise GPAs
                st.subheader("Semester-wise Results")
                for sem_result in semester_gpas:
                    st.write(f"📚 {sem_result['semester']}: SGPA = {sem_result['sgpa']} (Credits: {sem_result['credits']})")
                
                # Export options
                st.subheader("📥 Export Results")
                
                # Create two columns for export buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    # Create Excel file
                    excel_data = []
                    # Add student information
                    excel_data.append({
                        "Semester": "Student Information",
                        "Module Code": "Name",
                        "Module Title": student_name,
                        "Grade": "-",
                        "Credits": "-",
                        "Is GPA Module": False
                    })
                    excel_data.append({
                        "Semester": "Student Information",
                        "Module Code": "Registration Number",
                        "Module Title": reg_number,
                        "Grade": "-",
                        "Credits": "-",
                        "Is GPA Module": False
                    })
                    excel_data.append({
                        "Semester": "Student Information",
                        "Module Code": "Degree",
                        "Module Title": "Bachelor of Business Science",
                        "Grade": "-",
                        "Credits": "-",
                        "Is GPA Module": False
                    })
                    excel_data.append({
                        "Semester": "Student Information",
                        "Module Code": "Department",
                        "Module Title": department,
                        "Grade": "-",
                        "Credits": "-",
                        "Is GPA Module": False
                    })
                    excel_data.append({
                        "Semester": "Student Information",
                        "Module Code": "Batch",
                        "Module Title": batch,
                        "Grade": "-",
                        "Credits": "-",
                        "Is GPA Module": False
                    })
                    
                    # Add module data
                    for semester in filled_semesters:
                        for module in semester["modules"]:
                            if module["code"] and module["title"] and module["grade"] != "Not Selected":
                                excel_data.append({
                                    "Semester": semester["name"],
                                    "Module Code": module["code"],
                                    "Module Title": module["title"],
                                    "Grade": module["grade"],
                                    "Credits": module["credits"],
                                    "Is GPA Module": module["is_gpa"]
                                })
                    
                    # Add semester GPAs
                    for sem_gpa in semester_gpas:
                        excel_data.append({
                            "Semester": sem_gpa["semester"],
                            "Module Code": "SGPA",
                            "Module Title": f"Semester GPA: {sem_gpa['sgpa']}",
                            "Grade": "-",
                            "Credits": sem_gpa["credits"],
                            "Is GPA Module": True
                        })
                    
                    # Add final SGPA
                    excel_data.append({
                        "Semester": "Final Results",
                        "Module Code": "Final SGPA",
                        "Module Title": f"Final SGPA: {data['final_sgpa']}",
                        "Grade": "-",
                        "Credits": "-",
                        "Is GPA Module": True
                    })
                    
                    excel_data.append({
                        "Semester": "Final Results",
                        "Module Code": "Academic Standing",
                        "Module Title": data["standing"],
                        "Grade": "-",
                        "Credits": "-",
                        "Is GPA Module": True
                    })
                    
                    df = pd.DataFrame(excel_data)
                    
                    # Create Excel file
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='SGPA Results', index=False)
                    excel_data = excel_buffer.getvalue()
                    
                    st.download_button(
                        label="📊 Download Excel",
                        data=excel_data,
                        file_name="sgpa_results.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="excel_download"
                    )
                
                with col2:
                    try:
                        # Create PDF file
                        pdf_buffer = io.BytesIO()
                        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                        styles = getSampleStyleSheet()
                        elements = []
                        
                        # Add university header
                        elements.append(Paragraph("University of Moratuwa", styles['Title']))
                        elements.append(Paragraph("Faculty of Business", styles['Title']))
                        elements.append(Spacer(1, 20))
                        
                        # Add title
                        elements.append(Paragraph("SGPA Calculation Results", styles['Heading1']))
                        elements.append(Spacer(1, 20))
                        
                        # Add student information
                        elements.append(Paragraph("Student Information", styles['Heading2']))
                        elements.append(Paragraph(f"Name: {student_name}", styles['Normal']))
                        elements.append(Paragraph(f"Registration Number: {reg_number}", styles['Normal']))
                        elements.append(Paragraph(f"Degree: Bachelor of Business Science", styles['Normal']))
                        elements.append(Paragraph(f"Department: {department}", styles['Normal']))
                        elements.append(Paragraph(f"Batch: {batch}", styles['Normal']))
                        elements.append(Spacer(1, 20))
                        
                        # Add summary
                        elements.append(Paragraph("Academic Summary", styles['Heading2']))
                        elements.append(Paragraph(f"Final SGPA: {data['final_sgpa']}", styles['Heading3']))
                        elements.append(Paragraph(f"Academic Standing: {data['standing']}", styles['Heading3']))
                        elements.append(Spacer(1, 20))
                        
                        # Add semester-wise results
                        elements.append(Paragraph("Semester-wise Results", styles['Heading2']))
                        for sem_result in semester_gpas:
                            elements.append(Paragraph(f"{sem_result['semester']}: SGPA = {sem_result['sgpa']} (Credits: {sem_result['credits']})", styles['Normal']))
                        elements.append(Spacer(1, 20))
                        
                        # Add detailed results table
                        elements.append(Paragraph("Detailed Module Results", styles['Heading2']))
                        table_data = [["Semester", "Module Code", "Module Title", "Grade", "Credits", "Is GPA Module"]]
                        for semester in filled_semesters:
                            for module in semester["modules"]:
                                if module["code"] and module["title"] and module["grade"] != "Not Selected":
                                    table_data.append([
                                        semester["name"],
                                        module["code"],
                                        module["title"],
                                        module["grade"],
                                        str(module["credits"]),
                                        "Yes" if module["is_gpa"] else "No"
                                    ])
                        
                        # Calculate table width based on page width
                        table_width = letter[0] - 40  # 20 points margin on each side
                        col_widths = [table_width * 0.15, table_width * 0.15, table_width * 0.3, 
                                    table_width * 0.1, table_width * 0.1, table_width * 0.2]
                        
                        table = Table(table_data, colWidths=col_widths)
                        table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 12),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, -1), 10),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('WORDWRAP', (0, 0), (-1, -1), True)
                        ]))
                        elements.append(table)
                        
                        # Build PDF
                        doc.build(elements)
                        pdf_data = pdf_buffer.getvalue()
                        
                        st.download_button(
                            label="📄 Download PDF",
                            data=pdf_data,
                            file_name="sgpa_results.pdf",
                            mime="application/pdf",
                            key="pdf_download"
                        )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
            
            # Save to database
            if save_user_data(student_name, reg_number, department, batch, filled_semesters):
                st.success("Data saved successfully!")
            else:
                st.error("Error saving data to database")

# Add a new section to load previous data
st.sidebar.markdown("---")
st.sidebar.subheader("Load Previous Data")
load_reg_number = st.sidebar.text_input("Enter Registration Number to Load")

# Add a button to load data
if st.sidebar.button("Load Data"):
    with st.spinner("Loading data..."):
        user_data = get_user_data(load_reg_number)
        if user_data:
            # Update session state variables
            st.session_state.name = user_data["user"]["name"]
            st.session_state.reg_number = user_data["user"]["registration_number"]
            st.session_state.department = user_data["user"]["department"]
            st.session_state.batch = user_data["user"]["batch"]
            
            # Reset semester data
            st.session_state.semester_data = [
                {"name": f"Semester {i+1}", "modules": []} for i in range(8)
            ]
            
            # Load semester data
            for record in user_data["sgpa_records"]:
                semester_name = record["semester"]
                if semester_name.startswith("Semester "):
                    semester_idx = int(semester_name.split()[1]) - 1
                    if 0 <= semester_idx < len(st.session_state.semester_data):
                        st.session_state.semester_data[semester_idx]["modules"].append({
                            "code": record["module_code"],
                            "title": record["module_title"],
                            "grade": record["grade"],
                            "credits": record["credits"],
                            "is_gpa": record["is_gpa"]
                        })
            
            # Update the UI to reflect loaded data
            student_name = st.session_state.name
            reg_number = st.session_state.reg_number
            department = st.session_state.department
            batch = st.session_state.batch
            
            # Display loaded data
            st.sidebar.success("Data loaded successfully!")
            st.sidebar.write("**Loaded Student Information:**")
            st.sidebar.write(f"Name: {student_name}")
            st.sidebar.write(f"Registration Number: {reg_number}")
            st.sidebar.write(f"Department: {department}")
            st.sidebar.write(f"Batch: {batch}")

            # Create two columns for export buttons
            col1, col2 = st.sidebar.columns(2)
            
            with col1:
                # Create Excel file
                excel_data = []
                # Add student information
                excel_data.append({
                    "Semester": "Student Information",
                    "Module Code": "Name",
                    "Module Title": student_name,
                    "Grade": "-",
                    "Credits": "-",
                    "Is GPA Module": False
                })
                excel_data.append({
                    "Semester": "Student Information",
                    "Module Code": "Registration Number",
                    "Module Title": reg_number,
                    "Grade": "-",
                    "Credits": "-",
                    "Is GPA Module": False
                })
                excel_data.append({
                    "Semester": "Student Information",
                    "Module Code": "Degree",
                    "Module Title": "Bachelor of Business Science",
                    "Grade": "-",
                    "Credits": "-",
                    "Is GPA Module": False
                })
                excel_data.append({
                    "Semester": "Student Information",
                    "Module Code": "Department",
                    "Module Title": department,
                    "Grade": "-",
                    "Credits": "-",
                    "Is GPA Module": False
                })
                excel_data.append({
                    "Semester": "Student Information",
                    "Module Code": "Batch",
                    "Module Title": batch,
                    "Grade": "-",
                    "Credits": "-",
                    "Is GPA Module": False
                })
                
                # Add module data
                for record in user_data["sgpa_records"]:
                    if record["module_code"] and record["module_title"] and record["grade"] != "Not Selected":
                        excel_data.append({
                            "Semester": record["semester"],
                            "Module Code": record["module_code"],
                            "Module Title": record["module_title"],
                            "Grade": record["grade"],
                            "Credits": record["credits"],
                            "Is GPA Module": record["is_gpa"]
                        })
                        # Add semester SGPA if available
                        if record["semester_sgpa"]:
                            excel_data.append({
                                "Semester": record["semester"],
                                "Module Code": "SGPA",
                                "Module Title": f"Semester GPA: {record['semester_sgpa']}",
                                "Grade": "-",
                                "Credits": record["semester_credits"],
                                "Is GPA Module": True
                            })
                
                # Add final SGPA if available
                if user_data["sgpa_records"] and user_data["sgpa_records"][0]["final_sgpa"]:
                    excel_data.append({
                        "Semester": "Final Results",
                        "Module Code": "Final SGPA",
                        "Module Title": f"Final SGPA: {user_data['sgpa_records'][0]['final_sgpa']}",
                        "Grade": "-",
                        "Credits": "-",
                        "Is GPA Module": True
                    })
                    excel_data.append({
                        "Semester": "Final Results",
                        "Module Code": "Academic Standing",
                        "Module Title": user_data["sgpa_records"][0]["academic_standing"],
                        "Grade": "-",
                        "Credits": "-",
                        "Is GPA Module": True
                    })
                
                df = pd.DataFrame(excel_data)
                
                # Create Excel file
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='SGPA Results', index=False)
                excel_data = excel_buffer.getvalue()
                
                st.download_button(
                    label="📊 Download Excel",
                    data=excel_data,
                    file_name="sgpa_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="excel_download"
                )
            
            with col2:
                try:
                    # Create PDF file
                    pdf_buffer = io.BytesIO()
                    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                    styles = getSampleStyleSheet()
                    elements = []
                    
                    # Add university header
                    elements.append(Paragraph("University of Moratuwa", styles['Title']))
                    elements.append(Paragraph("Faculty of Business", styles['Title']))
                    elements.append(Spacer(1, 20))
                    
                    # Add title
                    elements.append(Paragraph("SGPA Calculation Results", styles['Heading1']))
                    elements.append(Spacer(1, 20))
                    
                    # Add student information
                    elements.append(Paragraph("Student Information", styles['Heading2']))
                    elements.append(Paragraph(f"Name: {student_name}", styles['Normal']))
                    elements.append(Paragraph(f"Registration Number: {reg_number}", styles['Normal']))
                    elements.append(Paragraph(f"Degree: Bachelor of Business Science", styles['Normal']))
                    elements.append(Paragraph(f"Department: {department}", styles['Normal']))
                    elements.append(Paragraph(f"Batch: {batch}", styles['Normal']))
                    elements.append(Spacer(1, 20))
                    
                    # Add summary
                    elements.append(Paragraph("Academic Summary", styles['Heading2']))
                    if user_data["sgpa_records"] and user_data["sgpa_records"][0]["final_sgpa"]:
                        elements.append(Paragraph(f"Final SGPA: {user_data['sgpa_records'][0]['final_sgpa']}", styles['Heading3']))
                        elements.append(Paragraph(f"Academic Standing: {user_data['sgpa_records'][0]['academic_standing']}", styles['Heading3']))
                    elements.append(Spacer(1, 20))
                    
                    # Add semester-wise results
                    elements.append(Paragraph("Semester-wise Results", styles['Heading2']))
                    for record in user_data["sgpa_records"]:
                        if record["semester_sgpa"]:
                            elements.append(Paragraph(f"{record['semester']}: SGPA = {record['semester_sgpa']} (Credits: {record['semester_credits']})", styles['Normal']))
                    elements.append(Spacer(1, 20))
                    
                    # Add detailed results table
                    elements.append(Paragraph("Detailed Module Results", styles['Heading2']))
                    table_data = [["Semester", "Module Code", "Module Title", "Grade", "Credits", "Is GPA Module"]]
                    for record in user_data["sgpa_records"]:
                        if record["module_code"] and record["module_title"] and record["grade"] != "Not Selected":
                            table_data.append([
                                record["semester"],
                                record["module_code"],
                                record["module_title"],
                                record["grade"],
                                str(record["credits"]),
                                "Yes" if record["is_gpa"] else "No"
                            ])
                    
                    # Calculate table width based on page width
                    table_width = letter[0] - 40  # 20 points margin on each side
                    col_widths = [table_width * 0.15, table_width * 0.15, table_width * 0.3, 
                                table_width * 0.1, table_width * 0.1, table_width * 0.2]
                    
                    table = Table(table_data, colWidths=col_widths)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 10),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('WORDWRAP', (0, 0), (-1, -1), True)
                    ]))
                    elements.append(table)
                    
                    # Build PDF
                    doc.build(elements)
                    pdf_data = pdf_buffer.getvalue()
                    
                    st.download_button(
                        label="📄 Download PDF",
                        data=pdf_data,
                        file_name="sgpa_results.pdf",
                        mime="application/pdf",
                        key="pdf_download"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
            
            # Update the form fields
            st.session_state.student_name = student_name
            st.session_state.reg_number = reg_number
            st.session_state.department = department
            st.session_state.batch = batch
        else:
            st.sidebar.error("No data found for this registration number")
