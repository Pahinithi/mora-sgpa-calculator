# Mora SGPA Calculator - Developer Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Setup and Installation](#setup-and-installation)
6. [Database Schema](#database-schema)
7. [API Documentation](#api-documentation)
8. [Frontend Components](#frontend-components)
9. [Development Guidelines](#development-guidelines)
10. [Testing](#testing)
11. [Deployment](#deployment)

## Project Overview
The Mora SGPA Calculator is a web application designed for the University of Moratuwa's Faculty of Business students to calculate their Semester Grade Point Average (SGPA) and track their academic progress. The application provides a user-friendly interface for entering module grades and generates detailed reports in both Excel and PDF formats.

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
- **Python Version**: 3.8+

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
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone [repository-url]
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
   ./start.sh
   ```

## Database Schema

### User Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    registration_number TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    batch TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### SGPA Table
```sql
CREATE TABLE sgpa_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    semester TEXT NOT NULL,
    module_code TEXT NOT NULL,
    module_title TEXT NOT NULL,
    grade TEXT NOT NULL,
    credits REAL NOT NULL,
    is_gpa BOOLEAN NOT NULL,
    semester_sgpa REAL,
    semester_credits REAL,
    final_sgpa REAL,
    academic_standing TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
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

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

### Git Workflow
1. Create feature branches from main
2. Write descriptive commit messages
3. Create pull requests for code review
4. Merge only after approval

### Error Handling
- Use try-except blocks for database operations
- Validate user input
- Provide meaningful error messages
- Log errors appropriately

## Testing

### Unit Tests
- Test database operations
- Test SGPA calculations
- Test input validation

### Integration Tests
- Test API endpoints
- Test frontend-backend integration
- Test database integration

## Deployment

### Local Development
1. Run FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Run Streamlit app:
   ```bash
   streamlit run app/frontend/streamlit_app.py
   ```

### Production Deployment
1. Set up a production server
2. Configure environment variables
3. Set up a reverse proxy (e.g., Nginx)
4. Use a production-grade database
5. Implement proper security measures

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
[Specify your license here]

## Contact
[Add contact information] 