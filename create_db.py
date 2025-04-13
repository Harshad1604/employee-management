import sqlite3

# Connect to the SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('employee.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the 'employee' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    salary REAL NOT NULL
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")
