"""
Resources and Links
https://realpython.com/python-sql-libraries/#understanding-the-database-schema
https://sqlitebrowser.org/dl/

Vscode extension: install SQLite
"""

import sqlite3
from sqlite3 import Error


#1 Connection to a database
def create_connection(path):
    try:
        connection = sqlite3.connect(path)
        print('Connection to SQLite DB successful 🚀')
    except Error as e:
        print(f"The error '{e}' occured")
    
    return connection


# -- Calling the create_connection function
try:  
  connection = create_connection('./Lesson-13-SQLite/database.db')
except Exception as e:
    print(f"Connecttion Error: {e}")

#2  Creating a Table
def execute_query(connection,query, operation):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print(f"{operation}: Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

"""
Schema
1. users: id, name, age, gender and nationality
2. posts: id, title, description, user_id(foriegn key)
3. comments: id, text, user_id (foriegn key), post_id (foriegn key)
4. likes: id, user_id (foriegn key), post_id (foriegn key)
"""


# SQL Query 
user_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    nationality TEXT
    )

"""

posts_table_query = """
CREATE TABLE IF NOT EXISTS posts(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  title TEXT NOT NULL, 
  description TEXT NOT NULL, 
  user_id INTEGER NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES users (id)
);
"""
comments_table_query = """
CREATE TABLE IF NOT EXISTS comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  text TEXT NOT NULL, 
  user_id INTEGER NOT NULL, 
  post_id INTEGER NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)
);
"""

likes_table_query = """
CREATE TABLE IF NOT EXISTS likes (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  user_id INTEGER NOT NULL, 
  post_id integer NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)
);
"""

execute_query(connection, user_table_query, operation='Create Table')  
execute_query(connection, posts_table_query, operation='Create Table')
execute_query(connection, comments_table_query, operation='Create Table')
execute_query(connection, likes_table_query, operation='Create Table')
