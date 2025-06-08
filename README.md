# Clinic_Project_Flask

This is a web application that allows patients to book appointments with doctors, and enables doctors to view upcoming appointments with their patients. The app is built with Flask and uses SQLite as the database.

---

## 🔧 Technologies Used

- Python 3.12+
- Flask
- Flask SQLAlchemy
- Jinja2 (Templating)
- SQLite
- HTML/CSS

---

## ✨ Features

### 👤 User Functionality

- Register as either a **patient** or a **doctor**
- Login and logout functionality

### 🧑‍⚕️ Patient

- Book an appointment by selecting a doctor
- View a list of your upcoming appointments
- Cancel an appointment

### 👨‍⚕️ Doctor

- View all booked appointments with patients
- See patient name, service requested, and scheduled date/time

---

## 📁 Project Structure

Clinic_Project_Flask/
│
├── app/
│ ├── init.py
│ ├── models.py
│ ├── routes.py
│ └── templates/
│ ├── index.html
│ └── account.html
│
├── venv/ # Virtual environment
├── run.py # Entry point
└── README.md
---

## 🚀 Setup and Run Instructions

1. **Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Initialize the database:
from app import db
db.create_all()

Run the application:
flask run
Visit http://localhost:5000 in your browser.

🗃️ Requirements (requirements.txt)
Flask
Flask-SQLAlchemy
Werkzeug

📝 Notes
If the database is deleted and recreated, make sure to run db.create_all() to ensure all tables (especially doctor_id) are present.

Role selection (patient or doctor) is done during registration.

Patients can only view and manage their own appointments. Doctors can see all appointments assigned to them.

