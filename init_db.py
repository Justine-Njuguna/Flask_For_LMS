"""Database initialization script, run once to set up the database."""

import sqlite3

# Connect to database (creates file if it doesn't exist)
conn = sqlite3.connect('lms.db')
cursor = conn.cursor()

# Create courses table
cursor.execute('''
               CREATE TABLE IF NOT EXISTS courses (
                   id INTEGER PRIMARY KEY,
                   title TEXT NOT NULL,
                   description TEXT NOT NULL
               )
               ''')

# Insert initial course data
courses = [
    (1, "Introduction to Photography", 
     "Learn the basics of photography, including composition, lighting, and camera settings."),
    (2, "Video Production Basics", 
     "An introductory course on video production, covering filming techniques, editing, and more."),
    (3, "Advanced Canva Design", 
     "Master advanced design techniques using Canva to create stunning graphics and presentations."),
    (4, "Robotics for beginners", 
     "Get started with robotics, learning about basic concepts."),
    (5, "Introduction to Machine Learning", 
     "Understand the fundamentals of machine learning, including algorithms and applications."),
]

cursor.executemany('INSERT INTO courses (id, title, description) VALUES (?, ?, ?)', courses)

# Save changes and close
conn.commit()
conn.close()

print("Database created and initialized with course data.")
print("Inserted 4 courses into the database")
