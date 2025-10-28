"""Course-related routes."""

import sqlite3
from flask import render_template, session, redirect, request


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

        user = session.get('username')
        return render_template('courses.html', courses=courses_list, username=user)

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

    # Add course page (GET - show form)
    @app.route('/add-course')
    def add_course():
        """Add course page route - Admin only"""
        # Check if user is logged in
        if 'username' not in session:
            return redirect('/login')

        return render_template('add_course.html')

    # Add course submission (POST - handle form submission)
    @app.route('/add-course', methods=['POST'])
    def add_course_submit():
        """Handle add course form submission"""
        # Check if user is logged in
        if 'username' not in session:
            return redirect('/login')

        title = request.form['title']
        description = request.form['description']

        # Insert into database
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO courses (title, description) VALUES (?, ?)',
            (title, description)
        )

        conn.commit()
        conn.close()

        return render_template('add_course.html',
                               success='Course added successfully!')

