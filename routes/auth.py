"""Authentication routes for the TKA Learning platform."""

from flask import request, session, redirect

def register_auth_routes(app):
    """Register authentication routes"""

    # Login page route - shows the form
    @app.route('/login')
    def login():
        """Login page route"""
        return '''
            <h1>Login to TKA Learning</h1>
            <form method="POST" action="/login">
                <div>
                    <label>Username:</label><br>
                    <input type="text" name="username" required>
                </div>
                <div>
                    <label>Password:</label><br>
                    <input type="password" name="password" required>
                </div>
                <br>
                <button type="submit">Login</button>
            </form>
            <br>
            <a href="/">Back to Home</a>
        '''

    # Handle login form submission
    @app.route('/login', methods=['POST'])
    def login_submit():
        """Handle login form submission"""
        username = request.form['username']
        password = request.form['password']

        # Simple check (in real app, check against database)
        if username == 'admin' and password == 'password':
            session['username'] = username  # Store username in session
            return redirect('/')  # Redirect to home page
        else:
            return '''
                <h1>Login Failed</h1>
                <p>Wrong username or password</p>
                <a href="/login">Try again</a>
            '''

    # Logout route
    @app.route('/logout')
    def logout():
        """Logout route"""
        session.pop('username', None)  # Remove username from session
        return redirect('/')
# End of routes/auth.py
