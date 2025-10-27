"""Application entry point for the LMS."""

from flask import Flask, session, render_template
from routes.auth import register_auth_routes
from routes.courses import register_course_routes

# Create a Flask application instance
app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this-later'

# Register routes from different modules
register_auth_routes(app)
register_course_routes(app)

# Home page route
@app.route('/')
def home():
    """Home page route"""
    user = session.get('username')
    return render_template('home.html', username=user)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
