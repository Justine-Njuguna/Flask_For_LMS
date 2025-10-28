"""Add is_admin column to users table and make admin user an admin."""
import sqlite3

conn = sqlite3.connect('lms.db')
cursor = conn.cursor()

# Add is_admin column (defaults to 0/False)
try:
    cursor.execute('ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0')
    print("✅ Added is_admin column to users table")
except sqlite3.OperationalError:
    print("⚠️ is_admin column already exists")

# Make 'admin' user an admin
cursor.execute("UPDATE users SET is_admin = 1 WHERE username = 'admin'")
conn.commit()

print("✅ Admin user now has admin privileges")
print("ℹ️ All other users are regular users (is_admin = 0)")

conn.close()