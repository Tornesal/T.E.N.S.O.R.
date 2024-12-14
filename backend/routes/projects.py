from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from backend.database_class import Database

projects_bp = Blueprint('projects', __name__)

# Database instance
db = Database(database_name="TNSR")

@projects_bp.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        # Fetch projects associated with the user
        projects = db.get_projects(session['username'])

        # Create a list of project dictionaries
        projects_list = [
            {
                'id': str(project['_id']),  # Convert '_id' to string
                'name': project.get('name', 'Unnamed Project'),  # Provide a default if 'name' is missing
                'description': project.get('description', 'No description'),  # Default description
                'last_updated': project.get('last_updated', 'Unknown')  # Default if 'last_updated' is missing
            }
            for project in projects
        ]

        return jsonify(projects_list), 200

    except Exception as e:
        # Handle and log any errors
        return jsonify({"error": str(e)}), 500

@projects_bp.route('/projects/<project_id>')
def view_project(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    # Handle viewing a specific project
    return render_template('view_project.html')