"""
Migration script to add the 'enrollments' table.
This table will track which users are enrolled in which courses.
"""
import sqlite3

DB_NAME = 'lms.db'

print(f"Connecting to database: {DB_NAME}")
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    # Create the new table
    # We will store the user_id and the course_id
    # We can also add a timestamp for when they enrolled
    cursor.execute("""
    CREATE TABLE enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (course_id) REFERENCES courses (id),
        UNIQUE(user_id, course_id)
    )
    """)
    print("✅ Success: 'enrollments' table created.")

except sqlite3.OperationalError as e:
    # This will error if the table already exists, which is fine.
    print(f"⚠️ Warning or Error: {e}")
    print("ℹ️  This may be because the 'enrollments' table already exists.")

conn.commit()
conn.close()
print("Database connection closed.")