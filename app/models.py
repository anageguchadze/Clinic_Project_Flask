from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'patient' or 'doctor'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # პაციენტი
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ექიმი

    user = db.relationship('User', foreign_keys=[user_id], backref='appointments')
    doctor = db.relationship('User', foreign_keys=[doctor_id], backref='doctor_appointments')
