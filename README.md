# TKA Learning Management System

A simple, lightweight Learning Management System built with Flask for managing and delivering educational video content.

## Features

- 🔐 User authentication (login/logout with sessions)
- 📚 Dynamic course catalog
- 📝 Individual course detail pages
- 🎨 Clean, organized code structure
- 🚀 Easy to extend and customize

## Tech Stack

- **Backend:** Flask (Python)
- **Session Management:** Flask sessions
- **Styling:** HTML (React + Tailwind coming soon)

## Project Structure

```
TKA_lms/
├── app.py                 # Main application entry point
├── routes/
│   ├── __init__.py       # Package initializer
│   ├── auth.py           # Authentication routes (login/logout)
│   └── courses.py        # Course-related routes
├── venv/                 # Virtual environment (not in git)
└── .gitignore           # Git ignore file
```

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

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the app**
   Open your browser and go to `http://127.0.0.1:5000/`

## Usage

### Default Login Credentials
- **Username:** admin
- **Password:** password

### Available Routes
- `/` - Home page
- `/login` - Login page
- `/logout` - Logout
- `/courses` - View all courses
- `/course/<id>` - View specific course details

## Roadmap

- [ ] Add SQLite/MySQL database
- [ ] Implement user registration
- [ ] Add video embedding
- [ ] Track course progress
- [ ] Add quizzes and assessments
- [ ] Implement React frontend
- [ ] Add Tailwind CSS styling
- [ ] Certificate generation

## Contributing

This is a learning project, but suggestions and improvements are welcome!

## License

MIT License - feel free to use this for your own learning projects.

## Author

Built by Aeldra as part of learning Flask and full-stack development.

---

**Note:** This is a work in progress. More features coming soon!