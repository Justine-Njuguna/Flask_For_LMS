"""Course-related routes."""

import sqlite3
from flask import render_template



def register_course_routes(app):
    """Register course routes"""

    def get_db_connection():
        """Create a database connection."""
        conn = sqlite3.connect('lms.db')
        conn.row_factory = sqlite3.Row  # This lets us access columns by name
        return conn

    # Courses list page
    @app.route('/courses')
    def courses():
        """Courses page route"""
        # Connect to database and fetch all courses
        conn = get_db_connection()
        courses_list = conn.execute('SELECT * FROM courses').fetchall()
        conn.close()

        return render_template('courses.html', courses=courses_list)

    # Individual course details
    @app.route('/course/<int:course_id>')
    def course_details(course_id):
        """Course details page route"""
        # Connect to database and fetch specific course
        conn = get_db_connection()
        course = conn.execute(
            'SELECT * FROM courses WHERE id = ?', 
            (course_id,)
        ).fetchone()
        conn.close()

        return render_template('course_detail.html', course=course)
