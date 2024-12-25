from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from pymongo import ReturnDocument

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
def create_project():
    projects_collection = db.get_collection("projects")
    users_collection = db.get_collection("users")
    counters_collection = db.get_collection("counters")

    try:
        # Step 1: Generate a unique project ID
        new_id = counters_collection.find_one_and_update(
            {"_id": "project_id"},
            {"$inc": {"value": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )["value"]
        new_project_id = f"proj{str(new_id).zfill(3)}"

        # Fetching json for text input
        data = request.get_json()

        print(data)

        # Step 2: Prepare the project document
        current_time = datetime.datetime.utcnow()
        project_document = {
            "_id": new_project_id,
            "name": data['project_name'],
            "description": data['description'],
            "user_name": session["username"],
            "created_at": current_time,
            "last_updated": current_time,
            "attributes": data['parameters'],
            "update_history": []
        }

        # Step 3: Insert the project into the projects collection
        projects_collection.insert_one(project_document)

        # Step 4: Update the user document to reference the new project
        users_collection.update_one(
            {"username": session["username"]},
            {"$push": {"projects": new_project_id}}
        )

        # Return success message
        return {"_id": new_project_id, "message": "Project created successfully"}

    except Exception as e:
        raise Exception(f"Database error: {str(e)}")