# TKA Learning Management System

A simple, lightweight Learning Management System built with Flask for managing and delivering educational video content.

## Features

- 🔐 User authentication with secure password hashing
- 👤 User registration system
- 📚 Dynamic course catalog from SQLite database
- 📝 Individual course detail pages
- 🎨 Clean Jinja2 templating
- 🔒 Session-based login persistence
- 🗄️ SQLite database for data persistence
- 🚀 Organized, modular code structure

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite with direct SQL queries
- **Templating:** Jinja2
- **Authentication:** Werkzeug password hashing
- **Session Management:** Flask sessions

## Project Structure

```
TKA_lms/
├── app.py                    # Main application entry point
├── routes/
│   ├── __init__.py          # Package initializer
│   ├── auth.py              # Authentication routes (login/register/logout)
│   └── courses.py           # Course-related routes
├── templates/               # Jinja2 HTML templates
│   ├── home.html           # Home page
│   ├── login.html          # Login form
│   ├── register.html       # Registration form
│   ├── courses.html        # Course listing
│   └── course_detail.html  # Course details page
├── lms.db                   # SQLite database
├── init_db.py              # Database initialization script
├── add_users_table.py      # Users table setup script
├── venv/                   # Virtual environment (not in git)
└── .gitignore              # Git ignore file
```

## Database Schema

### courses table
- `id` - INTEGER PRIMARY KEY
- `title` - TEXT NOT NULL
- `description` - TEXT NOT NULL

### users table
- `id` - INTEGER PRIMARY KEY AUTOINCREMENT
- `username` - TEXT UNIQUE NOT NULL
- `password_hash` - TEXT NOT NULL (hashed with werkzeug)

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Justine-Njuguna/Flask_For_LMS.git
   cd Flask_For_LMS
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   python add_users_table.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the app**
   Open your browser and go to `http://127.0.0.1:5000/`

## Usage

### Default Login Credentials
- **Username:** admin
- **Password:** password

Or create a new account using the registration page!

### Available Routes
- `/` - Home page (shows login status)
- `/login` - Login page
- `/register` - Create new account
- `/logout` - Logout (clears session)
- `/courses` - View all courses
- `/course/<id>` - View specific course details

## Features in Detail

### Authentication System
- Secure password hashing using Werkzeug
- Session-based login persistence
- User registration with validation
- Automatic duplicate username prevention
- Password confirmation on registration

### Course Management
- Dynamic course listing from database
- Individual course detail pages
- Easy to extend with new course features

### Template System
- Clean separation of HTML and Python code
- Reusable Jinja2 templates
- Dynamic content rendering
- Conditional displays based on login state

## Roadmap

- [x] SQLite database integration
- [x] User registration system
- [x] Jinja2 templating
- [x] Session-based authentication
- [x] Admin dashboard for adding courses
- [x] Video embedding in courses
- [ ] User progress tracking
- [ ] Quizzes and assessments
- [ ] Certificate generation
- [ ] Migrate to SQLAlchemy ORM
- [ ] Add CSS styling
- [ ] React frontend (long-term)
- [ ] REST API (long-term)

## Development Notes

- Always activate virtual environment before working: `source venv/bin/activate`
- Restart Flask after code changes (Ctrl+C then `python app.py`)
- Database file (`lms.db`) is created automatically on first run
- All passwords are hashed - never stored in plain text

## Contributing

This is a learning project, but suggestions and improvements are welcome!

## Security Note

⚠️ **For Learning Purposes Only** - This project uses a simple secret key and basic session management. For production use, implement:
- Environment variables for secrets
- HTTPS/SSL
- CSRF protection
- Rate limiting
- More robust session management

## License

MIT License - feel free to use this for your own learning projects.

## Author

Built by Aeldra as part of learning Flask and full-stack development.

---

**Current Status:** Fully functional with user authentication, database integration, and templating system! 🎉