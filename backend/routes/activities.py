from flask import Blueprint, jsonify
from backend.models import Activity  # Assuming you have an Activity model

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('/api/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    activities_list = [
        {
            'date': activity.date,
            'count': activity.count
        }
        for activity in activities
    ]
    return jsonify(activities_list)