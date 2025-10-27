"""Authentication routes for the TKA Learning platform."""

import sqlite3
from flask import request, session, redirect, render_template
from werkzeug.security import check_password_hash, generate_password_hash


def _get_db_connection():
    """Create a private database connection."""
    db_connection = sqlite3.connect('lms.db')
    db_connection.row_factory = sqlite3.Row  # This lets us access columns by name
    return db_connection


def register_auth_routes(flask_app):
    """Register authentication routes with the Flask app.
    
    Args:
        flask_app (Flask): The main Flask application instance.
    """

    # Login page route - shows the form
    @flask_app.route('/login')
    def login():
        """Login page route"""
        return render_template('login.html')

    # Handle login form submission
    @flask_app.route('/login', methods=['POST'])
    def login_submit():
        """Handle login form submission"""
        username = request.form['username']
        password = request.form['password']

        # Check against database
        db_connection = _get_db_connection()
        user_row = db_connection.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()
        db_connection.close()

        # Verify user exists and password matches
        if user_row and check_password_hash(user_row['password_hash'], password):
            session['username'] = username  # Store username in session
            return redirect('/')  # Redirect to home page

        # If login fails, re-render form with an error
        return render_template('login.html', error='Wrong username or password')

    # Add Register route
    @flask_app.route('/register')
    def register():
        """Registration page route"""
        return render_template('register.html')

    @flask_app.route('/register', methods=['POST'])
    def register_submit():
        """Handle registration form submission"""
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        # Check if username already exists
        db_connection = _get_db_connection()
        existing_user_row = db_connection.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        if existing_user_row:
            db_connection.close()
            return render_template('register.html', error='Username already taken')

        # Create new user
        password_hash = generate_password_hash(password)
        db_connection.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        db_connection.commit()
        db_connection.close()

        # Log them in automatically
        session['username'] = username
        return redirect('/')

    # Logout route
    @flask_app.route('/logout')
    def logout():
        """Logout route"""
        session.pop('username', None)  # Remove username from session
        return redirect('/')
