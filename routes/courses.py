"""Course routes for the TKA Learning platform."""

def register_course_routes(app):
    """Register course routes"""

    # Create a list of course data - list of dictionaries
    courses_list = [
        {
            "id": 1,
            "title": "Introduction to Photography",
            "description": ("Learn the basics of photography, including "
            "composition, lighting, and camera settings.")
        },
        {
            "id": 2,
            "title": "Video Production Basics",
            "description": ("An introductory course on video production, covering "
            "filming techniques, editing, and more.")
        },
        {
            "id": 3,
            "title": "Advanced Canva Design",
            "description": ("Master advanced design techniques using Canva to create "
            "stunning graphics and presentations.")
        }
    ]

    # Courses list page
    @app.route('/courses')
    def courses():
        """Courses page route"""

        #start building the HTML response
        html = '<h1>AAvailable Courses</h1><ul>'
        # loop through the courses and add to the HTML
        for course in courses_list:
            html += f'''
                <li><a href="/course/{course["id"]}">
                {course["title"]}</a>:
                {course["description"]}</li>
        '''
        html += '</ul><a href="/">Back to Home</a>'
        return html

    # Individual course details
    @app.route('/course/<int:course_id>')
    def course_detail(course_id):
        """Course details page route"""
        # FInd the course with matching ID
        course = None
        for c in courses_list:
            if c['id'] == course_id:
                course = c
                break

        # if course found, show it, otherwise show error
        if course:
            return f'''
                <h1>{course["title"]}</h1>
                <p>{course["description"]}</p>
                <a href="/courses">Back to Courses</a> | <a href="/">Back to Home</a>
            '''
        else:
            return '''<h1>Course Not Found</h1>
                    <p>Sorry, we could not find the course you were looking for.</p>
                    <a href="/courses">Back to Courses</a>
                    '''
# End of routes/courses.py
