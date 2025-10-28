"""
    Migration script to add a 'video_url' column to the 'courses' table.
"""
import sqlite3

DB_NAME = 'lms.db'

print(f"Connecting to database: {DB_NAME}")
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    # Add the new column
    # TEXT is used tso we can store any URL.
    cursor.execute("ALTER TABLE courses ADD COLUMN video_url TEXT")
    print("✅ Success: 'video_url' column added to 'courses' table.")
except sqlite3.OperationalError as e:
    # THis will error if the column already exists, which is fine.
    print(f"⚠️ Warning: Could not add 'video_url' column. It may already exist. Error: {e}")
    print("ℹ️  This may be because the 'video_url' column already exists.")
    
conn.commit()
conn.close()
print("Database connection closed.")