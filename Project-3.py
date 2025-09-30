import sqlite3
from sqlite3 import Error
import streamlit as st
import uuid6
from datetime import datetime
import pandas as pd

# Resources
#1 https://pypi.org/


#Modules to Install
# python -m pip install uuid6


def generateID():
    id = None
    try:
        id = uuid6.uuid6()
        id = str(id)
    except Exception as e:
         print(f"An error occured due to {e}")
    return id


# Connection to Database function
def connect_to_db (path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Database connected succesfully 🚀")
    except Error as error:
        print(f"An error occured due to {error}")
    return connection


# Connect to database
connection = connect_to_db("employee.db")


def execute_query (connection,query, data=None):
    cursor = connection.cursor()

    try:
        if data:
            cursor = cursor.execute(query, data)
        else:
            cursor = cursor.execute(query)
        connection.commit()

    except Error as e:
        print(f"An error occured due to {e}")

    return cursor


# Create a table
create_staff_table_query = """
CREATE TABLE IF NOT EXISTS staff (
staff_id VARCHAR(32) PRIMARY KEY,
name VARCHAR(255),
gender VARCHAR(6),
age INTEGER,
marital_status VARCHAR(7),
department VARCHAR(255),
created_at DATETIME
)
"""

cursor = execute_query (connection,create_staff_table_query)
print(cursor.executemany)

st.title("Staff :orange[Profile]")

with st.form("my_form",clear_on_submit=True):
    isFormData = False
    name = st.text_input(label="Name", placeholder="Ali Ahmad")
    gender = st.selectbox(label="Gender",options=("Female", "Male") )
    age = st.number_input(label="Age")
    marital_status = st.selectbox(label="Marital Status",options=("Married", "Single") )
    department = st.selectbox(label="Department",options=("Account", "IT", "HR", "Cybersecurity") )

    if (name and gender and age >0 and marital_status and department):
        isFormData = True
        

    
    submit = st.form_submit_button("Submit")
    if submit and isFormData:
        staff_id = generateID()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_staff_data_query = """
        INSERT INTO staff (staff_id, name, gender,age,marital_status,department,created_at)
        VALUES (?,?,?,?,?,?,?);
        """

        cursor = execute_query(connection, insert_staff_data_query,data=(staff_id,name,gender,age,marital_status,department,created_at))

        print(cursor.lastrowid)

      
        st.success("Staff profile created successfully")
        st.balloons()

st.title("Staff List")
st.dataframe(pd.read_sql_query("SELECT * FROM staff", connection ))

