from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from backend.database_class import Database

auth_bp = Blueprint('auth', __name__)

# Database instance
db = Database(database_name="TNSR")

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        return handle_login()
    # return render_login_template()

def handle_login():
    # If structure to get the username and password and pass it into the check function
    if request.method == 'POST':

        # Fetching json for text input
        data = request.get_json()

        # Variables to hold username and password
        username = data['username']
        password = data['password']

        # If the credentials are good, then go to logged in page. Else, do nothing for now
        if check_login_credentials(username, password):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})

    # return render_template('login.html')

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
        session['user_id'], session['username'] = str(user['_id']), user['username']
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

        # Fetching json for text input
        data = request.get_json()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if email_already_used(email):
            return jsonify({'message': 'Email already in use'}), 403

        elif db.find_one('users', {'username': username}) is not None:
            return jsonify({'message': 'Username already in use'}), 403

        # Only add user if email and username is unique
        else:

            # Hash the password
            hashed_password = generate_password_hash(password).decode('utf-8')

            # Create a new user document
            user = {
                'username': username,
                'email': email,
                'password': hashed_password,
                'projects': []
            }

            # Insert the new user into the database
            db.insert_one('users', user)

            # Redirect to the login page after successful registration
            return redirect(url_for('auth.login'))


# Function to check if email is already used
def email_already_used(email):
    if db.find_one('users', {'student_info.email': email}) is None:
        return False
    else:
        return True