from flask import Blueprint, jsonify, session
from backend.database_class import Database

activities_bp = Blueprint('activities', __name__)

# Database instance
db = Database(database_name="TNSR")

@activities_bp.route('/api/activities', methods=['GET'])
def get_activities():
    try:
        projects = db.get_projects(session['username'])

        # Collect all update timestamps
        update_timestamps = []
        for project in projects:
            update_history = project.get("update_history", [])
            update_timestamps.extend(update_history)  # Already a list of timestamps

        # Aggregate timestamps by date and calculate counts
        date_counts = {}
        for timestamp in update_timestamps:
            date = timestamp.split("T")[0]  # Extract the date part (YYYY-MM-DD)
            date_counts[date] = date_counts.get(date, 0) + 1

        # Format data for the heatmap
        heatmap_data = [{"date": date, "count": count} for date, count in date_counts.items()]

        return jsonify(heatmap_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500