"""Add category column to courses table"""
import sqlite3

DB_NAME = 'lms.db'

print(f"Connecting to database: {DB_NAME}")
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    # Add category column
    cursor.execute("ALTER TABLE courses ADD COLUMN category TEXT DEFAULT 'General'")
    print("✅ Success: 'category' column added to 'courses' table.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Warning: Could not add 'category' column. It may already exist. Error: {e}")

conn.commit()
conn.close()
print("Database connection closed.")
