from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User  # <--- მოაქციე სწორად
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('index.html', user=user)

@main.route('/account', methods=['GET', 'POST'])
def account():
    user = None
    appointments = []

    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    if request.method == 'POST':
        # Login
        if 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('თქვენ წარმატებით შეხვალთ სისტემაში!', 'success')
                return redirect(url_for('main.account'))
            else:
                flash('მომხმარებელი ან პაროლი არასწორია.', 'error')

        # Register
        elif 'register' in request.form:
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                flash('მომხმარებელი უკვე არსებობს.', 'error')
            else:
                hashed_pw = generate_password_hash(password)
                new_user = User(username=username, password=hashed_pw, role=role)
                db.session.add(new_user)
                db.session.commit()
                flash('რეგისტრაცია წარმატებით დასრულდა. ახლა შეგიძლიათ შედით.', 'success')
                return redirect(url_for('main.account'))

        # Book appointment
        elif user and request.form.get('action') == 'book':
            from app.models import Appointment
            service = request.form['service']
            date_str = request.form['date']
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

            new_appt = Appointment(service=service, date=date, user_id=user.id, doctor_id=user.id)  # უბრალოდ ტესტად ორივე ID ერთია
            db.session.add(new_appt)
            db.session.commit()
            flash('ვიზიტი დაჯავშნილია.', 'success')

        # Delete appointment
        elif user and request.form.get('action') == 'delete':
            from app.models import Appointment
            appt_id = request.form['appointment_id']
            appt = Appointment.query.get(appt_id)
            if appt and appt.user_id == user.id:
                db.session.delete(appt)
                db.session.commit()
                flash('ვიზიტი წაშლილია.', 'success')

    if user and user.role == 'patient':
        from app.models import Appointment
        appointments = Appointment.query.filter_by(user_id=user.id).order_by(Appointment.date).all()

    return render_template('account.html', user=user, appointments=appointments)

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('თქვენ გამოხვედით სისტემიდან.', 'info')
    return redirect(url_for('main.account'))
