from flask import Blueprint, render_template, request, redirect, url_for, session
from database_class import Database

projects_bp = Blueprint('projects', __name__)

# Database instance
#db = Database(database_name="TNSR")

@projects_bp.route('/projects', methods=['GET', 'POST'])
def projects():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        # Handle adding a new project
        pass
    return render_template('projects.html')

@projects_bp.route('/projects/<project_id>')
def view_project(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    # Handle viewing a specific project
    return render_template('view_project.html')