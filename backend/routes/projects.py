from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from backend.database_class import Database
import datetime

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

@projects_bp.route('/api/projects', methods=['POST'])
def create_project(self, project_name, username, description=None):
    collection = self.get_collection("projects")

    # Find the lowest available ID
    existing_ids = collection.distinct("_id")
    numeric_ids = sorted(int(id) for id in existing_ids)
    new_id = 1
    for id in numeric_ids:
        if id != new_id:
            break
        new_id += 1
    new_project_id = str(new_id).zfill(3)

    document = {
        "_id": new_project_id,
        "name": project_name,
        "username": username,
        "description": description,
        "created_at": datetime.utcnow(),
        "metrics": []
    }
    try:
        return collection.insert_one(document)
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")