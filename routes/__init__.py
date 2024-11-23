# Initialize the routes package
from flask import Blueprint

# Create a blueprint for the routes
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
projects_bp = Blueprint('projects', __name__)

# Import the routes
from . import main, auth, projects