"""Add users table to existing database."""
import sqlite3
from werkzeug.security import generate_password_hash

# Connect to existing database
conn = sqlite3.connect('lms.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')

# Add the admin user with hashed password
admin_password = generate_password_hash('password')
cursor.execute(
    'INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)',
    ('admin', admin_password)
)

# Save and close
conn.commit()
conn.close()

print("✅ Users table created!")
print("👤 Admin user added (username: admin, password: password)")
