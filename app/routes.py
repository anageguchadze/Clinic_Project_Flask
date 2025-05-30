from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

# დროებითი მომხმარებლების „ბაზა“
users = {}

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        if 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            user = users.get(username)

            if user and check_password_hash(user['password'], password):
                session['user'] = username
                flash('თქვენ წარმატებით შეხვალთ სისტემაში!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('მომხმარებელი ან პაროლი არასწორია.', 'error')

        elif 'register' in request.form:
            username = request.form['username']
            password = request.form['password']
            if username in users:
                flash('მომხმარებელი უკვე არსებობს.', 'error')
            else:
                users[username] = {'password': generate_password_hash(password)}
                flash('რეგისტრაცია წარმატებით დასრულდა. ახლა შეგიძლიათ შედით.', 'success')
                return redirect(url_for('main.account'))

    return render_template('account.html')

@main.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('გთხოვთ, ჯერ შედით სისტემაში.', 'error')
        return redirect(url_for('main.account'))
    return f"<h1>მოგესალმები, {session['user']}!</h1>"
