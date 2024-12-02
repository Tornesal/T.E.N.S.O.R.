from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')