from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Appointment
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        if request.form.get('login'):
            # ლოგინი
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('წარმატებით შეხვედით სისტემაში!', 'success')
                return redirect(url_for('main.account'))
            else:
                flash('არასწორი მომხმარებელი ან პაროლი.', 'error')

        elif request.form.get('register'):
            # რეგისტრაცია
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
                flash('რეგისტრაცია წარმატებით დასრულდა!', 'success')
                return redirect(url_for('main.account'))

        elif request.form.get('action') == 'book':
            # ვიზიტის დაჯავშნა
            if 'user_id' in session:
                service = request.form['service']
                date_str = request.form['date']
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
                    new_appointment = Appointment(user_id=session['user_id'], service=service, date=date)
                    db.session.add(new_appointment)
                    db.session.commit()
                    flash('ვიზიტი დაჯავშნილია.', 'success')
                except Exception as e:
                    flash(f'დროის ფორმატი არასწორია. {e}', 'error')

        elif request.form.get('action') == 'delete':
            # ვიზიტის წაშლა
            appointment_id = request.form['appointment_id']
            appt = Appointment.query.filter_by(id=appointment_id, user_id=session['user_id']).first()
            if appt:
                db.session.delete(appt)
                db.session.commit()
                flash('ვიზიტი წაშლილია.', 'success')
            else:
                flash('ვიზიტი ვერ მოიძებნა.', 'error')

    user = None
    appointments = []
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user.role == 'patient':
            appointments = Appointment.query.filter_by(user_id=user.id).order_by(Appointment.date).all()

    return render_template('account.html', user=user, appointments=appointments)
