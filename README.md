# University of Moratuwa - Faculty of Business SGPA Calculator

A web application designed for students of the Faculty of Business at the University of Moratuwa to calculate their Semester Grade Point Average (SGPA) and track their academic progress.

## Features

- 🎓 Calculate SGPA for individual semesters
- 📊 Calculate final SGPA across all semesters
- 📝 Track academic standing
- 💾 Save and load previous data
- 📤 Export results in Excel and PDF formats
- 📱 User-friendly interface
- 🔒 Secure data storage

## Prerequisites

- Python 3.11.11
- pip (Python package manager)

## Installation

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

## Running the Application

### Option 1: Using start script
```bash
./start.sh
```

### Option 2: Manual start
```bash
# Terminal 1 - Start FastAPI
fastapi dev app/main.py

# Terminal 2 - Start Streamlit
streamlit run app/frontend/streamlit_app.py
```

## Usage

1. Enter your student information:
   - Full Name
   - Registration Number
   - Department
   - Batch

2. Enter module grades for each semester:
   - Module Code
   - Module Title
   - Grade
   - Credits
   - GPA Module status

3. Calculate SGPA:
   - Click "Calculate Final SGPA"
   - View your results
   - Export in Excel or PDF format

4. Load previous data:
   - Enter your registration number
   - Click "Load Data"

## Grade Points

| Grade | Points |
|-------|--------|
| A+    | 4.0    |
| A     | 4.0    |
| A-    | 3.7    |
| B+    | 3.3    |
| B     | 3.0    |
| B-    | 2.7    |
| C+    | 2.3    |
| C     | 2.0    |
| C-    | 1.7    |
| D     | 1.0    |
| F     | 0.0    |

## Academic Standing

- First Class: SGPA ≥ 3.70
- Second Class (Upper Division): 3.30 ≤ SGPA < 3.70
- Second Class (Lower Division): 3.00 ≤ SGPA < 3.30
- Pass: 2.00 ≤ SGPA < 3.00

## Documentation

- [User Documentation](docs/user-documentation.md)
- [Developer Documentation](docs/developer-documentation.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Tech Stack

### Backend
- FastAPI - High-performance web framework
- SQLAlchemy - SQL toolkit and ORM
- SQLite - Lightweight database
- Python 3.11.11

### Frontend
- Streamlit - Web application framework
- Pandas - Data manipulation and analysis
- OpenPyXL - Excel file handling
- ReportLab - PDF generation

### Development Tools
- Git - Version control
- pip - Package management
- venv - Virtual environment

## License

MIT License

## Developer

- **Name**: Nithilan Pahirathan
- **GitHub**: [Pahinithi](https://github.com/Pahinithi) 