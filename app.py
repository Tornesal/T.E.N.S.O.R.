# Tracking Engine for Networks, States, and Outcome Reports (TENSOR)

from flask import Flask, render_template, redirect, url_for, request, session, jsonify

from flask_bcrypt import generate_password_hash, check_password_hash

# This allows me to use my custom decorator with multiple functions and decorators
from functools import wraps

# Datetime conversion
from datetime import datetime

# Used to generate a random key for the session
import secrets

# Import blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.projects import projects_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(projects_bp)

# Secret key for the session
app.secret_key = secrets.token_urlsafe(16)

if __name__ == '__main__':
    app.run(debug=True)