"""Main FLask application entry point."""

from flask import Flask, session
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
    if user:
        return f'''<h1>Hello World!</h1>
                <p>Welcome back, {user}!</p>
                <a href="/courses">View Courses</a> |  
                <a href="/logout">Logout</a>
            '''
    else:
        return '''
            <h1>Hello World!</h1>
            <p>Your first Flask app is running!</p>
            <a href="/courses">View Courses</a> | 
            <a href="/login">Login</a>
        '''

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
# End of app.py
