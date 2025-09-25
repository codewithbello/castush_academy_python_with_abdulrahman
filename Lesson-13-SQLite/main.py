"""
Resources and Links
https://realpython.com/python-sql-libraries/#understanding-the-database-schema
https://sqlitebrowser.org/dl/
https://www.w3schools.com/sql/
Vscode extension: install SQLite

C - Create  --> Insert 
R - Read    --> Select
U - Update  --> Insert/Where
D - Delete  --> Delete/ Drop
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
        return cursor
      
    except Error as e:
        print(f"The error '{e}' occurred")


#3 Reading Table
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = []
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
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


# Inserting Records


create_users_query = """
INSERT INTO users(name,age,gender, nationality)
VALUES 
('Ali','25','male','Nigeria'),
('Ahmad','20','male','Iran'),
('Abdulrahman','18','male','Nigeria'),
('Spongebob','12','male','UK');
"""


# execute_query(connection, create_users_query, operation='User Inserted') 

create_posts = """
INSERT INTO
  posts (title, description, user_id)
VALUES
  ("Happy", "I am feeling very happy today", 1),
  ("Hot Weather", "The weather is very hot today", 2),
  ("Help", "I need some help with my work", 2),
  ("Great News", "I am getting married", 1),
  ("Interesting Game", "It was a fantastic game of tennis", 4),
  ("Party", "Anyone up for a late-night party today?", 3);
"""

# execute_query(connection, create_posts, operation='Post Inserted')


create_comments = """
INSERT INTO
  comments (text, user_id, post_id)
VALUES
  ('Count me in', 1, 6),
  ('What sort of help?', 4, 3),
  ('Congrats buddy', 2, 4),
  ('I was rooting for Nadal though', 4, 5),
  ('Help with your thesis?', 2, 3),
  ('Many congratulations', 1, 4);
"""

create_likes = """
INSERT INTO
  likes (user_id, post_id)
VALUES
  (1, 6),
  (2, 3),
  (1, 5),
  (3, 4),
  (2, 4),
  (4, 2),
  (3, 6);
"""

# execute_query(connection, create_comments, operation="comment inserted")
# execute_query(connection, create_likes, operation="likes inserted")

# Selecting Record

get_all_users = "SELECT * FROM users"

users = execute_read_query(connection, get_all_users)

print("\n", "=========== USERS ===============")
for user in users:
    print(user[1])




print("\n", "=========== POST TITLE ===============")
select_posts = "SELECT * FROM posts"
posts = execute_read_query(connection, select_posts)

for post in posts:
    print(post[1])


# JOIN TABLE - Reading from Multiple tables

select_posts_comments_users = """
SELECT
  posts.description as post,
  text as comment,
  name
FROM
  posts
  INNER JOIN comments ON posts.id = comments.post_id
  INNER JOIN users ON users.id = comments.user_id
"""
print("\n", "=========== COMMENTS ===============")
posts_comments_users = execute_read_query(
    connection, select_posts_comments_users
)

for comment in posts_comments_users:
    print(comment)


# Print the column names
cursor = connection.cursor()
cursor.execute(select_posts_comments_users)
cursor.fetchall()

for desc in cursor.description:
    print(desc[0])


col_names = []


for desc in cursor.description:
   col_names.append(desc[0])


print(col_names)


# Using Where
select_post_likes = """
SELECT
  description as Post,
  COUNT(likes.id) as Likes
FROM
  likes,
  posts
WHERE
  posts.id = likes.post_id
GROUP BY
  likes.post_id
"""

post_likes = execute_read_query(connection, select_post_likes)


print("\n", "=============== LIKES ==================")
for post_like in post_likes:
    print(post_like)




# Get a single user

get_user_by_ID = "SELECT name FROM users WHERE id = 3"
# get_user_by_ID = "SELECT * FROM users WHERE id = 3"


user = execute_read_query(connection, get_user_by_ID)

print("\n")
print(user[0][0])


# Updating a Table


select_post_description = "SELECT description FROM posts WHERE id = 2"

post_description = execute_read_query(connection, select_post_description)

print("\n")
for description in post_description:
    print(description)


update_post_description = """
UPDATE
  posts
SET
  description = "The weather has become pleasant now"
WHERE
  id = 2
"""

execute_query(connection, update_post_description, operation="Post table update")

print("\n")
post_description = execute_read_query(connection, select_post_description)
for description in post_description:
    print(description)



# Delete a row

delete_a_user = "DELETE FROM users WHERE id = 4"
# execute_query(connection, delete_a_user, operation="delete a user")

# Deleting a Table
delete_table_query = """
DROP TABLE posts;
"""
# execute_query(connection, delete_table_query, operation='Post Table Deleted')


# Count

no_user_query = "SELECT COUNT(*) FROM users;"
no_of_users = execute_query(connection, no_user_query, operation="count users")
print(no_of_users.fetchone()[0])



gender_query = "SELECT COUNT(DISTINCT gender) FROM users;"
no_of_genders = execute_query(connection, gender_query, operation="count gender")
print(no_of_genders.fetchone())


user_order_query = "SELECT * FROM users ORDER BY name;"
ordered_users = execute_query(connection, user_order_query, operation="ordered_users")
print(ordered_users.fetchall())



users = post_description = execute_read_query(connection, user_order_query)
print(users)

for user in users:
    print(user[1])