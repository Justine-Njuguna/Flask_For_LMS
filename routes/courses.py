"""Course-related routes."""

import sqlite3
from flask import render_template, session, redirect, request


def register_course_routes(app):
    """Register course routes"""

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
        admin = is_admin()
        return render_template('courses.html', courses=courses_list, username=user, is_admin=admin)

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

        user = session.get('username')
        admin = is_admin()
        return render_template('course_detail.html', course=course, username=user, is_admin=admin)

    # Add course page (GET - show form)
    @app.route('/add-course')
    def add_course():
        """Add course page route - Admin only"""
        # Check if user is logged in
        if not is_admin():
            return redirect('/login')

        return render_template('add_course.html')

    # Add course submission (POST - handle form submission)
    @app.route('/add-course', methods=['POST'])
    def add_course_submit():
        """Handle add course form submission"""
        # Check if user is logged in
        if not is_admin():
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

        return redirect('/courses')
        # Delete course (POST only!)
    @app.route('/delete-course/<int:course_id>', methods=['POST'])
    def delete_course(course_id):
        """Delete a course"""
        # Check if user is admin
        if not is_admin():
            return redirect('/login')
        
        # Delete from database
        conn = get_db_connection()
        conn.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
        conn.close()
        
        return redirect('/courses')
    
        # Edit course page (GET - show form with current data)
    @app.route('/edit-course/<int:course_id>')
    def edit_course(course_id):
        """Edit course page - admin only"""
        if not is_admin():
            return redirect('/login')
        
        # Fetch the course to edit
        conn = get_db_connection()
        course = conn.execute(
            'SELECT * FROM courses WHERE id = ?',
            (course_id,)
        ).fetchone()
        conn.close()
        
        return render_template('edit_course.html', course=course)

    # Edit course submission (POST - update database)
    @app.route('/edit-course/<int:course_id>', methods=['POST'])
    def edit_course_submit(course_id):
        """Handle edit course form submission"""
        if not is_admin():
            return redirect('/login')
        
        title = request.form['title']
        description = request.form['description']
        
        # Update in database
        conn = get_db_connection()
        conn.execute(
            'UPDATE courses SET title = ?, description = ? WHERE id = ?',
            (title, description, course_id)
        )
        conn.commit()
        conn.close()
        
        # Redirect to course detail page (PRG pattern!)
        return redirect(f'/course/{course_id}')