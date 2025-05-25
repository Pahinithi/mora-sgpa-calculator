# University of Moratuwa - Faculty of Business SGPA Calculator - Developer Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Setup and Installation](#setup-and-installation)
6. [Database Schema](#database-schema)
7. [API Documentation](#api-documentation)
8. [Frontend Components](#frontend-components)
9. [Expected Output](#expected-output)

## Project Overview
The University of Moratuwa - Faculty of Business SGPA Calculator is a comprehensive web application designed for students of the Faculty of Business at the University of Moratuwa. This application enables students to calculate their Semester Grade Point Average (SGPA) and monitor their academic progress throughout their degree program. The application features an intuitive interface for entering module grades and generates professional reports in both Excel and PDF formats, making it easier for students to track and document their academic performance.

### Key Features
- Student information management
- Module grade input and validation
- SGPA calculation
- Academic standing determination
- Export functionality (Excel and PDF)
- Data persistence
- Previous data loading

## System Architecture
The application follows a client-server architecture:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │     │   Backend   │     │  Database   │
│ (Streamlit) │◄───►│  (FastAPI)  │◄───►│  (SQLite)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Technology Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **PDF Generation**: ReportLab
- **Excel Generation**: Pandas with openpyxl
- **Python Version**: 3.11.11

## Project Structure
```
mora-sgpa-calculator/
├── app/
│   ├── frontend/
│   │   └── streamlit_app.py
│   ├── grade/
│   │   └── function.py
│   ├── schema/
│   │   └── gpa_schema.py
│   └── main.py
├── database/
│   ├── models.py
│   ├── operations.py
│   └── init_db.py
├── docs/
│   └── developer-documentation.md
├── requirements.txt
└── start.sh
```

## Setup and Installation

### Prerequisites
- Python 3.11.11
- pip (Python package manager)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Pahinithi/mora-sgpa-calculator.git
   cd mora-sgpa-calculator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python database/init_db.py
   ```

5. Start the application:
   ```bash
   # Option 1: Using start script
   ./start.sh

   # Option 2: Manual start
   # Terminal 1 - Start FastAPI
   fastapi dev app/main.py

   # Terminal 2 - Start Streamlit
   streamlit run app/frontend/streamlit_app.py
   ```

## Database Management

### Clearing and Reinitializing Database
To clear the existing database and start fresh:
```bash
# Remove existing database
rm database/sgpa.db

# Initialize new database
python database/init_db.py
```

Expected output:
```
Initializing database...
Database initialized successfully!
```

## API Documentation

### FastAPI Endpoints

#### 1. Calculate SGPA
- **Endpoint**: `/sgpa/`
- **Method**: POST
- **Description**: Calculates SGPA for a given semester
- **Request Body**:
  ```json
  {
    "name": "Semester 1",
    "modules": [
      {
        "code": "MATH101",
        "title": "Mathematics",
        "grade": "A",
        "credits": 3.0,
        "is_gpa": true
      }
    ]
  }
  ```

#### 2. Calculate Final SGPA
- **Endpoint**: `/final-sgpa/`
- **Method**: POST
- **Description**: Calculates final SGPA across all semesters
- **Request Body**: Array of semester objects

## Frontend Components

### Streamlit App Structure
1. **Student Information Section**
   - Name input
   - Registration number input
   - Department selection
   - Batch input

2. **Module Input Section**
   - Dynamic semester expansion panels
   - Module details input forms
   - Grade selection dropdowns

3. **Results Section**
   - SGPA display
   - Academic standing
   - Export options

4. **Data Loading Section**
   - Registration number search
   - Previous data loading
   - Results display

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
MIT License

## Contact
- **Developer**: Nithilan Pahirathan
- **Email**: nithilan32@gmail.com
- **GitHub**: https://github.com/Pahinithi 

## Expected Output

### Frontend Interface
When you run the application successfully, you will see the following interface:

1. **Main Application Window**
   - Title: "🎓 SGPA Calculator | University of Moratuwa - Faculty of Business"
   - Clean, modern interface with a white background

2. **Sidebar Components**
   - Student Information section with input fields for:
     - Full Name
     - Registration Number
     - Department (dropdown with options)
     - Batch
   - Settings section
   - Load Previous Data section

3. **Main Content Area**
   - Semester expansion panels (1-8)
   - Internship section
   - Each semester panel contains:
     - Number of modules selector
     - Module input forms with:
       - Module Code
       - Module Title
       - Grade selection
       - Credits input
       - GPA module checkbox

4. **Results Section** (appears after calculation)
   - Student Information display
   - Final SGPA result
   - Academic Standing
   - Semester-wise results
   - Export options (Excel and PDF)

5. **Success Messages**
   - "Data saved successfully!" when data is saved
   - "Data loaded successfully!" when previous data is loaded
   - "Calculating..." spinner during calculations

The application provides an intuitive, user-friendly interface that guides students through the process of entering their grades and viewing their academic results. 