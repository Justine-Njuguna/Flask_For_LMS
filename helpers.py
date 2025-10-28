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