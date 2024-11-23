# Tracking Engine for Networks, States, and Outcome Reports (TENSOR)

from flask import Flask, render_template, redirect, url_for, request, session, jsonify

from flask_bcrypt import generate_password_hash, check_password_hash

# This allows me to use my custom decorator with multiple functions and decorators
from functools import wraps

# Datetime conversion
from datetime import datetime

# Used to generate a random key for the session
import secrets

# Importing the database class
from database_class import Database

app = Flask(__name__)

# Secret key for the session
app.secret_key = secrets.token_urlsafe(16)