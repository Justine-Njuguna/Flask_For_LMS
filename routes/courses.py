"""Course-related routes."""

import sqlite3
from urllib.parse import urlparse, parse_qs
from flask import render_template, session, redirect, request, url_for
from helpers import is_admin, get_db_connection, get_user_id, is_course_completed




def register_course_routes(app):
    """Register course routes"""

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

    @app.route('/courses')
    def courses():
        """Courses page route"""

        search_query = request.args.get('search', '').strip()
        category_filter = request.args.get('category', '').strip()  # NEW!

        # Connect to database and fetch all courses
        conn = get_db_connection()

        # Build query based on filters
        if search_query and category_filter:
            # Both search and category
            courses_list = conn.execute(
                'SELECT * FROM courses WHERE (title LIKE ? OR description LIKE ?) AND category = ?',
                (f'%{search_query}%', f'%{search_query}%', category_filter)
            ).fetchall()
        elif search_query:
            # Just search
            courses_list = conn.execute(
                'SELECT * FROM courses WHERE title LIKE ? OR description LIKE ?',
                (f'%{search_query}%', f'%{search_query}%')
            ).fetchall()
        elif category_filter:
            # Just category filter
            courses_list = conn.execute(
                'SELECT * FROM courses WHERE category = ?',
                (category_filter,)
            ).fetchall()
        else:
            # Show all courses
            courses_list = conn.execute('SELECT * FROM courses').fetchall()

        conn.close()

        user = session.get('username')
        admin = is_admin()

        # Define the breadcrumbs
        breadcrumbs = [
            { "name": "Home", "url": "/" },
            { "name": "Courses", "url": None } # None for the active page
        ]

        return render_template('courses.html', courses=courses_list,
                            username=user, is_admin=admin, 
                            search_query=search_query,
                            category_filter=category_filter,
                            breadcrumbs=breadcrumbs)

    @app.route('/course/<int:course_id>')
    def course_details(course_id):
        """Course details page route"""
        conn = get_db_connection() 
        course = conn.execute(
            'SELECT * FROM courses WHERE id = ?', 
            (course_id,)
        ).fetchone()
        
        # Get related courses (same category, exclude current course, limit 4)
        related_courses = []
        if course and course['category']:
            related_courses = conn.execute(
                'SELECT * FROM courses WHERE category = ? AND id != ? LIMIT 4',
                (course['category'], course_id)
            ).fetchall()
        
        # --- THIS IS THE NEW LOGIC ---
        is_enrolled = False
        user_id = None
        user = session.get('username')
        if user:
            user_id = get_user_id(user)
            if user_id and course: # Check if user_id and course exist
                enrollment = conn.execute(
                    'SELECT id FROM enrollments WHERE user_id = ? AND course_id = ?',
                    (user_id, course_id)
                ).fetchone()
                if enrollment:
                    is_enrolled = True
        # --- END OF NEW LOGIC ---

        conn.close() # Close after ALL queries

        admin = is_admin()
        is_completed = False
        embed_url = None
        breadcrumbs = []  

        if course:
            if user_id: # We already have user_id
                is_completed = is_course_completed(user_id, course_id)
            
            embed_url = get_youtube_embed_url(course['video_url'])
            breadcrumbs = [
                { "name": "Home", "url": "/" },
                { "name": "Courses", "url": "/courses" },
                { "name": course['title'], "url": None }
            ]
        else:
            breadcrumbs = [
                { "name": "Home", "url": "/" },
                { "name": "Not Found", "url": None }
            ]

        return render_template('course_detail.html',
                               course=course,
                               username=user,
                               is_admin=admin,
                               embed_url=embed_url,
                               is_completed=is_completed,
                               breadcrumbs=breadcrumbs,
                               related_courses=related_courses,
                               is_enrolled=is_enrolled) # <-- Pass the new variable
    # Add course page (GET - show form)
    @app.route('/add-course')
    def add_course():
        """Add course page route - Admin only"""
        # Check if user is logged in
        if not is_admin():
            return redirect('/login')

        # Define breadcrumbs
        breadcrumbs = [
            { "name": "Home", "url": "/" },
            { "name": "Courses", "url": "/courses" },
            { "name": "Add Course", "url": None } # None for active page
        ]

        return render_template('add_course.html', breadcrumbs=breadcrumbs)

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
        category = request.form.get('category', 'General')  # Example of additional field

        # Insert into database
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO courses (title, description, video_url, category) VALUES (?, ?, ?, ?)',
            (title, description, video_url, category)
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

        # define breadcrumbs
        breadcrumbs = [
            { "name": "Home", "url": "/" },
            { "name": "Courses", "url": "/courses" },
            { "name": f"Edit {course['title']}", "url": None } # Dynamic name
        ]

        return render_template('edit_course.html', course=course, breadcrumbs=breadcrumbs)

    # Edit course submission (POST - update database)
    @app.route('/edit-course/<int:course_id>', methods=['POST'])
    def edit_course_submit(course_id):
        """Handle edit course form submission"""
        if not is_admin():
            return redirect('/login')

        title = request.form['title']
        description = request.form['description']
        video_url = request.form.get('video_url')  # New field for video URL
        category = request.form.get('category', 'General')  # Adding category field

        # Update in database
        conn = get_db_connection()
        conn.execute(
            'UPDATE courses SET title = ?, description = ?, video_url = ?, category = ? WHERE id = ?',
            (title, description, video_url, category, course_id)
        )
        conn.commit()
        conn.close()

        # Redirect to course detail page (PRG pattern!)
        return redirect(f'/course/{course_id}')

    # Route to enroll in a course
    @app.route('/enroll/<int:course_id>', methods=['POST'])
    def enroll_course(course_id):
        """Enroll the current user in a course."""
        if 'username' not in session:
            return redirect(url_for('login')) # use url_for for routes
        
        user_id = get_user_id(session['username'])
        if not user_id:
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        try:
            # Try to insert the new enrollment
            conn.execute(
                'INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)',
                (user_id, course_id)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            # This error fires if the UNIQUE constraint fails
            # (meaning)the user is already enrolled).
            # We can just ignore it.
            pass
        finally:
            conn.close()
            
        # Redirect back to the course page
        return redirect(url_for('course_details', course_id=course_id))
    # Mark course as complete/incomplete
    @app.route('/toggle-complete/<int:course_id>', methods=['POST'])
    def toggle_complete(course_id):
        """Toggle course completion status for current user"""
        if 'username' not in session:
            return redirect('/login')

        user_id = get_user_id(session['username'])
        if not user_id:
            return redirect('/login')

        conn = get_db_connection()

        # Check if progress record exists
        existing = conn.execute(
            'SELECT * FROM course_progress WHERE user_id = ? AND course_id = ?',
            (user_id, course_id)
        ).fetchone()

        if existing:
            # Toggle the completed status
            new_status = 0 if existing['completed'] == 1 else 1
            conn.execute(
                'UPDATE course_progress SET completed = ?,completed_at = CURRENT_TIMESTAMP WHERE user_id = ? AND course_id = ?',
                (new_status, user_id, course_id)
            )
        else:
            # Create new progress record (marked as complete)
            conn.execute(
                'INSERT INTO course_progress (user_id, course_id, completed) VALUES (?, ?, 1)',
                (user_id, course_id)
            )

        conn.commit()
        conn.close()

        return redirect(f'/course/{course_id}')

  #User Dashboard
    @app.route('/dashboard')
    def dashboard():
        """User dashboard showing progress"""
        if 'username' not in session:
            return redirect('/login')

        user_id = get_user_id(session['username'])
        if not user_id:
            return redirect('/login')

        conn = get_db_connection()

        # Get all courses
        all_courses = conn.execute('SELECT * FROM courses').fetchall()

        # Get completed courses
        # FIX 1: Set completed = 1
        # FIX 2: Select cp.completed_at so the template can use it
        completed = conn.execute(
            '''SELECT c.*, cp.completed_at
            FROM courses c
            JOIN course_progress cp ON c.id = cp.course_id
            WHERE cp.user_id = ? AND cp.completed = 1''',
            (user_id,)
        ).fetchall()

        # Get in-progress courses (not completed)
        # FIX 1: Set completed = 0
        in_progress = conn.execute(
            '''SELECT c.*
            FROM courses c
            JOIN course_progress cp ON c.id = cp.course_id
            WHERE cp.user_id = ? AND cp.completed = 0''',
            (user_id,)
        ).fetchall()

        conn.close()

        # Calculate stats
        total_courses = len(all_courses)
        completed_count = len(completed)
        in_progress_count = len(in_progress)
        completion_percentage = (completed_count / total_courses * 100) if total_courses > 0 else 0

        user = session.get('username')
        admin = is_admin()
        
        # Define the breadcrumbs
        breadcrumbs = [
            { "name": "Home", "url": "/" },
            { "name": "Dashboard", "url": None } # None for the active page
        ]

        return render_template('dashboard.html',
                               username=user,
                               is_admin=admin,
                               all_courses=all_courses,
                               completed=completed,
                               in_progress=in_progress,
                               total_courses=total_courses,
                               completed_count=completed_count,
                               in_progress_count=in_progress_count,
                               completion_percentage=completion_percentage,
                               breadcrumbs=breadcrumbs)