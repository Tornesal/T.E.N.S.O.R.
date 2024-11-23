from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_bcrypt import generate_password_hash, check_password_hash
from database_class import Database

auth_bp = Blueprint('auth', __name__)

# Database instance
db = Database(uri="your_mongo_uri", database_name="your_db_name")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        pass
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic
        pass
    return render_template('register.html')