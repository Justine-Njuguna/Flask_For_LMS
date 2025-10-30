"""Add course_progress table to track user completion."""

import sqlite3

DB_NAME = 'lms.db'

print(f"Connecting to database: {DB_NAME}")
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    # Create course_progress table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS course_progress (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER NOT NULL,
                       course_id INTEGER NOT NULL,
                       completed INTEGER DEFAULT 0,
                       completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (user_id) REFERENCES users(id),
                       FOREIGN KEY (course_id) REFERENCES courses(id),
                       UNIQUE(user_id, course_id)
                   )
                ''')
    print("✅ Success: 'course_progress' table created.")
except sqlite3.Error as e:
    print(f"❌ Error creating 'course_progress' table: {e}")

conn.commit()
conn.close()
print("Database connection closed.")
