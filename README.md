# TKA Learning Management System

A fully-featured Learning Management System built with Flask for managing and delivering educational video content. This project includes user authentication, progress tracking, video embedding, search functionality, and course categorization.

## Features

### Core Functionality
- 🔐 **User Authentication** - Secure registration and login with password hashing
- 👤 **User Registration** - New users can create accounts
- 🎓 **Progress Tracking** - Mark courses as complete and track learning progress
- 📹 **Video Embedding** - YouTube video integration with responsive players
- 🔍 **Search Functionality** - Search courses by title or description
- 🏷️ **Course Categories** - Organize courses into categories (Photography, Video Production, Design, etc.)
- 📊 **Category Filtering** - Filter courses by category with one click

### Admin Features
- ➕ **Add Courses** - Admin-only course creation
- ✏️ **Edit Courses** - Modify course details, videos, and categories
- 🗑️ **Delete Courses** - Remove courses with confirmation
- 🔒 **Admin Protection** - All admin actions require authentication

### User Experience
- 🎨 **Modern UI** - Clean, gradient-based design with CSS styling
- 📱 **Responsive Design** - Works on desktop and mobile
- 🎯 **Intuitive Navigation** - Easy-to-use interface with clear navigation
- 💬 **User Feedback** - Success/error messages for all actions
- 🔄 **Session Persistence** - Stay logged in across pages

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite with direct SQL queries
- **Templating:** Jinja2
- **Authentication:** Werkzeug password hashing
- **Session Management:** Flask sessions
- **Styling:** Custom CSS with gradient designs

## Project Structure

```
TKA_lms/
├── app.py                          # Main application entry point
├── helpers.py                      # Shared helper functions
├── routes/
│   ├── __init__.py                # Package initializer
│   ├── auth.py                    # Authentication routes
│   └── courses.py                 # Course management routes
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                  # Base template with navigation
│   ├── home.html                  # Home page
│   ├── login.html                 # Login form
│   ├── register.html              # Registration form
│   ├── courses.html               # Course listing with search/filter
│   ├── course_detail.html         # Individual course page
│   ├── add_course.html            # Add course form (admin)
│   └── edit_course.html           # Edit course form (admin)
├── static/
│   └── css/
│       └── style.css              # Main stylesheet
├── lms.db                         # SQLite database
├── init_db.py                     # Initial database setup
├── add_users_table.py             # Users table migration
├── add_video_url_column.py        # Video URL column migration
├── add_progress_tracking.py       # Progress tracking table migration
├── add_categories.py              # Categories column migration
├── make_admin.py                  # Set admin privileges
├── venv/                          # Virtual environment (not in git)
├── .gitignore                     # Git ignore file
└── README.md                      # Project documentation
```

## Database Schema

### users table
- `id` - INTEGER PRIMARY KEY AUTOINCREMENT
- `username` - TEXT UNIQUE NOT NULL
- `password_hash` - TEXT NOT NULL (hashed with werkzeug)
- `is_admin` - INTEGER DEFAULT 0 (1 for admin users)

### courses table
- `id` - INTEGER PRIMARY KEY AUTOINCREMENT
- `title` - TEXT NOT NULL
- `description` - TEXT NOT NULL
- `video_url` - TEXT (YouTube/Vimeo URL)
- `category` - TEXT DEFAULT 'General'

### course_progress table
- `id` - INTEGER PRIMARY KEY AUTOINCREMENT
- `user_id` - INTEGER NOT NULL (FK to users)
- `course_id` - INTEGER NOT NULL (FK to courses)
- `completed` - INTEGER DEFAULT 0 (0 or 1)
- `completed_at` - TIMESTAMP

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Justine-Njuguna/Flask_For_LMS.git
cd Flask_For_LMS
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install flask
```

### 4. Initialize the database
```bash
python init_db.py
python add_users_table.py
python add_video_url_column.py
python add_progress_tracking.py
python add_categories.py
python make_admin.py
```

### 5. Run the application
```bash
python app.py
```

### 6. Access the app
Open your browser and go to `http://127.0.0.1:5000/`

## Usage

### Default Admin Credentials
- **Username:** admin
- **Password:** password

**Note:** Change these credentials in production!

### Available Routes
- `/` - Home page
- `/login` - Login page
- `/register` - Create new account
- `/logout` - Logout (clears session)
- `/courses` - View all courses (with search and filter)
- `/courses?search=keyword` - Search courses
- `/courses?category=Photography` - Filter by category
- `/course/<id>` - View specific course details
- `/add-course` - Add new course (admin only)
- `/edit-course/<id>` - Edit course (admin only)
- `/delete-course/<id>` - Delete course (admin only, POST)
- `/toggle-complete/<id>` - Mark course complete/incomplete (POST)

## Features in Detail

### Authentication System
- Secure password hashing using Werkzeug's `generate_password_hash`
- Session-based login persistence
- User registration with duplicate username prevention
- Password confirmation validation
- Admin role management

### Course Management
- Dynamic course listing from database
- Video embedding with YouTube URL parsing
- Category-based organization
- Search functionality across title and description
- Admin-only CRUD operations with proper POST requests

### Progress Tracking
- Mark courses as complete/incomplete
- Track completion status per user
- Progress data persists across sessions
- Visual indicators for completed courses

### Search & Filter
- Real-time search through course titles and descriptions
- Category-based filtering
- Combined search + category filtering
- Results count display

### Video Integration
- Automatic YouTube URL parsing
- Support for standard (`youtube.com/watch`) and short (`youtu.be`) URLs
- Responsive 16:9 video player
- Graceful handling of missing videos

## Available Categories
- 📷 Photography
- 🎥 Video Production
- 🎨 Design
- 💻 Technology
- 💼 Business
- 📊 Marketing
- 📚 General

## Roadmap

### Next Up
- [ ] User dashboard with progress overview
- [ ] Related courses suggestions
- [ ] Breadcrumb navigation

### Planned Features
- [ ] Course reviews and ratings
- [ ] Enrollment system
- [ ] Course prerequisites
- [ ] Email notifications
- [ ] Certificate generation
- [ ] Course completion certificates
- [ ] Discussion forums per course
- [ ] Multiple video formats support
- [ ] Course playlists
- [ ] Learning paths

### Technical Improvements
- [ ] Migrate to SQLAlchemy ORM
- [ ] Add unit tests
- [ ] Environment variables for configuration
- [ ] Better error handling
- [ ] API endpoints (REST)
- [ ] React frontend (long-term)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Production deployment (Nginx, Gunicorn)

## Development Notes

- Always activate virtual environment before working: `source venv/bin/activate`
- Restart Flask after code changes: `Ctrl+C` then `python app.py`
- Database migrations are idempotent (safe to run multiple times)
- All passwords are hashed - never stored in plain text
- Admin actions use POST requests to prevent CSRF
- Follow PRG (Post-Redirect-Get) pattern for form submissions

## Security Features

✅ Password hashing with Werkzeug
✅ SQL injection prevention with parameterized queries
✅ Admin-only route protection
✅ Session-based authentication
✅ POST-only destructive operations
✅ CSRF confirmation dialogs

## Contributing

This is a learning project built to understand full-stack web development. Suggestions and improvements are welcome!

## Security Note

⚠️ **For Learning/Development Use Only** - This project uses basic security practices suitable for learning. For production deployment, implement:
- Environment variables for secrets (`.env` file)
- HTTPS/SSL certificates
- CSRF protection tokens
- Rate limiting on login attempts
- More robust session management
- Database connection pooling
- Input sanitization and validation
- Security headers
- Regular security audits

## License

MIT License - feel free to use this for your own learning projects.

## Author

Built by **Aeldra** as part of learning Flask and full-stack web development.

### Learning Journey
This project was built progressively over multiple sessions, adding features one at a time:
1. Basic Flask setup and routing
2. User authentication and sessions
3. Database integration with SQLite
4. Jinja2 templating and styling
5. Admin CRUD operations
6. Video embedding functionality
7. Progress tracking system
8. Search functionality
9. Course categorization and filtering

Each feature was implemented with proper security, error handling, and user experience in mind.

---

**Current Status:** Fully functional LMS with authentication, video courses, progress tracking, search, and categorization! 🎉

**Next Steps:** User dashboard, course reviews, and deployment preparation.