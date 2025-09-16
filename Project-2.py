# https://streamlit.io/
# https://docs.streamlit.io/develop/api-reference
# https://streamlit.io/playground
# run using: streamlit run Project-2.py
# https://sqlitebrowser.org/dl/

import streamlit as st
import pandas as pd
from helper import regFunc, getFunc, db

st.title("Online Registration")

name = st.text_input("Fullname", "")
age = st.number_input("How old are you")
gender = st.selectbox(
    "Gender",
    ("Male", "Female"),
)
maritalStatus = st.selectbox(
    "Marital Status",
    ("Married", "Single"),
)
email = st.text_input("Enter your email", "")
phone = st.text_input("Enter your phone", "")
occupation = st.text_input("Enter your occupation", "")

if st.button("Submit", type="primary"):
    if name and age and email and phone and occupation and maritalStatus and gender:
        response = regFunc(name, age, email, phone, occupation,maritalStatus, gender)
        st.success(f"{response['status']}: {response['msg']}", icon="✅")
        st.balloons()

    else:
        st.error("All fields are required.", icon="🚨")


# User registration table      
data = pd.DataFrame(db)
if len(db)>0:
    st.dataframe(data)





    
