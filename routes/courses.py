"""Course-related routes."""

import sqlite3
from urllib.parse import urlparse, parse_qs
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

    # In routes/courses.py, after get_db_connection

    def get_youtube_embed_url(video_url):
        """Converts a standard YouTube URL into an embeddable URL."""
        if not video_url:
            return None

        # Parse the URL to get its components
        parsed_url = urlparse(video_url)
        
        # Check if it's a standard YouTube 'watch' link
        if parsed_url.hostname in ('www.youtube.com', 'youtube.com') and \
        parsed_url.path == '/watch':
            
            # Parse the query string to get the 'v' parameter (video ID)
            video_id = parse_qs(parsed_url.query).get('v')
            
            if video_id:
                # Return the embeddable URL format
                return f"https://www.youtube.com/embed/{video_id[0]}"
                
        # Check if it's a shortened 'youtu.be' link
        if parsed_url.hostname == 'youtu.be' and parsed_url.path:
            # The video ID is the path itself (remove leading '/')
            video_id = parsed_url.path[1:]
            return f"https://www.youtube.com/embed/{video_id}"

        # If it's already an embed link, or not YouTube, return it (or None)
        # For now, we'll just handle the main cases.
        # You could add Vimeo, etc., here later.
        
        # A simple fallback (less robust)
        if 'embed' in video_url:
            return video_url
            
        return None # Or return video_url if you want to try embedding other things
    
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
        
        embed_url = get_youtube_embed_url(course['video_url']) if course else None
        return render_template('course_detail.html', course=course, username=user, is_admin=admin, embed_url=embed_url)

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
        
        video_url = request.form.get('video_url')  # New field for video URL

        # Insert into database
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO courses (title, description, video_url) VALUES (?, ?, ?)',
            (title, description, video_url)
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
        video_url = request.form.get('video_url')  # New field for video URL
        
        # Update in database
        conn = get_db_connection()
        conn.execute(
            'UPDATE courses SET title = ?, description = ?, video_url = ? WHERE id = ?',
            (title, description, video_url, course_id)
        )
        conn.commit()
        conn.close()
        
        # Redirect to course detail page (PRG pattern!)
        return redirect(f'/course/{course_id}')