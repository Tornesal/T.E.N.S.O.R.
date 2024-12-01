from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from database_class import Database
import os

auth_bp = Blueprint('auth', __name__)

# Database instance
db = Database(database_name="TNSR")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return handle_login()
    return render_login_template()

def render_login_template():
    return render_template('login.html')

def handle_login():
    # If structure to get the username and password and pass it into the check function
    if request.method == 'POST':
        # Variables to hold username and password
        username = request.form['username']
        password = request.form['password']

        # If the credentials are good, then go to logged in page. Else, do nothing for now
        if check_login_credentials(username, password):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})

    return render_template('login.html')

def check_login_credentials(username, password):
    # Check if username or password is empty
    if not username or not password:
        return False

    # Finds the user that matches the username and store the corresponding database table
    user = db.find_one('users', {'username': username})

    if user is None:
        return False

    # Checks if the username and password match the database
    elif user['username'] == username and check_password_hash(user['password'], password):
        session['user_id'] = str(user['_id'])
        return True
    else:
        return False


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if email_already_used(email):
            return jsonify({'message': 'Email already in use'}), 403

        # Only add user if email is unique
        else:

            # Hash the password
            hashed_password = generate_password_hash(password).decode('utf-8')

            # Create a new user document
            user = {
                'username': username,
                'email': email,
                'password': hashed_password
            }

            # Insert the new user into the database
            db.insert_one('users', user)

            # Redirect to the login page after successful registration
            return redirect(url_for('auth.login'))

    return render_template('register.html')

# Function to check if email is already used
def email_already_used(email):
    if db.find_one('users', {'student_info.email': email}) is None:
        return False
    else:
        return True