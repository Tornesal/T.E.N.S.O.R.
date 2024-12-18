# Tracking Engine for Networks, States, and Outcome Reports (TENSOR)

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Used to generate a random key for the session
import secrets

# Import blueprints
from backend.routes.auth import auth_bp
from backend.routes.main import main_bp
from backend.routes.projects import projects_bp
from backend.routes.activities import activities_bp

app = Flask(__name__)

# Enable CORS
CORS(app, origins=["http://localhost:3000"])

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(activities_bp)

# Secret key for the session
app.secret_key = secrets.token_urlsafe(16)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and os.path.exists(f"../frontend/build/{path}"):
        return send_from_directory('../frontend/build', path)
    return send_from_directory('../frontend/build', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)