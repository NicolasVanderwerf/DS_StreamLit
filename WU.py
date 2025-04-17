import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import re 

st.set_page_config(page_title="WU Directory", layout="wide")

st.title('Directory at Westminster University')
st.write("This is an enhanced alternative to the employee [directory](https://westminsteru.edu/campus-directory/index.html) at Westminster University." )
data = pd.read_csv('WU_directory.csv') 

filtered_data = data.copy()

department_list = data['Department'].unique().tolist()
department_list.insert(0, 'ALL')

department = st.selectbox(label = 'Choose one department from below:', options = department_list)
name = st.text_input("Enter Name", "")
use_regex = st.checkbox('Use Regex Search', value=False)
col1, col2, col3, col4 = st.columns([0.2,0.2,0.2,0.4])

with col1:
    st.text("Type of Role:") # add a text 
with col2:
    role_faculty = st.checkbox('Faculty', value=0)
with col3:
    role_staff = st.checkbox('Staff', value=0)


with col1:
    st.text("Type of Position:") # add a text 
with col2:
    assist_prof = st.checkbox('Assistant Professor', value=0)
with col3:
    assoc_prof = st.checkbox('Associate Professor', value=0)
with col4:
    prof = st.checkbox('Professor', value=0)

with col1:
    st.text("Contract:") # add a text 
with col2:
    ftime = st.checkbox('FULL-TIME', value=0)
with col3:
    ptime = st.checkbox('PART-TIME', value=0)

# Apply department filter
if department != 'ALL':
    filtered_data = filtered_data[filtered_data['Department'] == department]

if role_faculty:
    filtered_data = filtered_data[filtered_data['Role'] == 'Faculty']
if role_staff:
    filtered_data = filtered_data[filtered_data['Role'] == 'Staff']

if assist_prof:
    filtered_data = filtered_data[filtered_data['Position'] == 'Assistant Professor']
if assoc_prof:
    filtered_data = filtered_data[filtered_data['Position'] == 'Associate Professor']
if prof:
    filtered_data = filtered_data[filtered_data['Position'] == 'Professor']

if ftime:
    filtered_data = filtered_data[filtered_data['Contract'] == 'FULL-TIME']
if ptime:
    filtered_data = filtered_data[filtered_data['Contract'] == 'PART-TIME']

if name != "":
    if use_regex:
        filtered_data = filtered_data[filtered_data['Name'].str.contains(name, case=False, regex=True)]
    else:
        filtered_data = filtered_data[filtered_data['Name'].str.contains(name, case=False, regex=False)]



st.dataframe(filtered_data, hide_index=True)