from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
import utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import validators
import sqlite3

app = Flask(__name__)
connection = db.connect_to_database('database.db')
app.secret_key = "zs9XYCbTPKvux46UJckflw"
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per minute"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute") 
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user(connection, username)
        
        if user:
            if username == 'admin' and utils.is_password_match(password, user[2]):
                session['username'] = user[1]
                session['user_id'] = user[0]
                return redirect(url_for('admin_panel'))
            elif utils.is_password_match(password, user[2]):
                session['username'] = user[1]
                session['user_id'] = user[0]
                return redirect(url_for('index'))
            else:
                flash("Password does not match", "danger")
                return render_template('login.html')
            
        else:
            flash("Invalid username", "danger")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per minute") 
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not utils.is_strong_password(password):
            flash("Sorry You Entered a weak Password Please Choose a stronger one", "danger")
            return render_template('register.html')
        
        user = db.get_user(connection, username)
        if user:
            flash("Username already exists. Please choose a different username.", "danger")
            return render_template('register.html')
        else:
            db.add_user(connection, username, password)
            return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/admin')
def admin_panel():
    if 'username' in session and session['username'] == 'admin':
        notes = db.get_all_notes(connection)
        return render_template('admin_panel.html', notes=notes)
    else:
        flash("You are not authorized to access the admin panel", "danger")
        return redirect(url_for('index'))
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/notes')
def notes():
    if 'username' in session:
        username = session['username']
        #conn = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM notes')
        notes = cursor.fetchall()
        connection.close()
        return render_template('notes.html', username=username, notes=notes)
    else:
        return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            db.add_note(connection, title , content)
            return redirect(url_for('notes'))
        else:
            return render_template('add_note.html')
    else:
        return redirect(url_for('login'))    

if __name__ == '__main__':
    db.init_db(connection)
    db.init_gadget_table(connection)
    db.init_notes_table(connection)
    db.seed_admin_user(connection)
    app.run(debug=True)