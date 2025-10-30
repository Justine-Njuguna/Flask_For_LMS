"""Helper functions used across the application."""
import sqlite3
from flask import session

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect('lms.db')
    conn.row_factory = sqlite3.Row
    return conn

def is_admin():
    """Check if current user is admin."""
    if 'username' not in session:
        return False

    conn = get_db_connection()
    user = conn.execute(
        'SELECT is_admin FROM users WHERE username = ?',
        (session['username'],)
    ).fetchone()
    conn.close()

    return user and user['is_admin'] == 1

def get_user_id(username):
    """Get user ID from username."""
    conn = get_db_connection()
    user = conn.execute(
        'SELECT id FROM users WHERE username = ?',
        (username,)
    ).fetchone()
    conn.close()
    return user['id'] if user else None

def is_course_completed(user_id, course_id):
    """Check if a user has completed a course."""
    conn = get_db_connection()
    progress = conn.execute(
        'SELECT completed FROM course_progress WHERE user_id = ? AND course_id = ?',
        (user_id, course_id)
    ).fetchone()
    conn.close()
    return progress and progress['completed'] == 1

def get_user_completed_courses(user_id):
    """Get list of course IDs that user has completed."""
    conn = get_db_connection()
    completed = conn.execute(
        'SELECT course_id FROM course_progress WHERE user_id = ? AND completed = 1',
    ).fetchall()
    conn.close()
    return [row['course_id'] for row in completed]
