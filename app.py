"""Application entry point for the LMS."""

from flask import Flask, session, render_template
from routes.auth import register_auth_routes
from routes.courses import register_course_routes
from helpers import is_admin  # Add this import

# Create a Flask application instance
app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this-later'

# Register routes from different modules
register_auth_routes(app)
register_course_routes(app)

@app.route('/')
def home():
    """Home page route"""
    user = session.get('username')
    admin = is_admin() if user else False
    return render_template('home.html', username=user, is_admin=admin)


@app.errorhandler(404)
def not_found_error(error):
    """Handles 404 Not Found errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handles 500 Internal Server errors."""
    return render_template('500.html'), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
