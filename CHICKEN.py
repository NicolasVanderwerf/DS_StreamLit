import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import re 

st.set_page_config(page_title="WU Directory", layout="wide")

st.title('Directory at Westminster University')
st.write("This is an enhanced alternative to the employee [directory](https://westminsteru.edu/campus-directory/index.html) at Westminster University." )
data = pd.read_csv('./chicken_recipes.csv') 

def to_mins(x):
    h = re.search('(\d+) [hr|hrs]', x)
    m = re.search('(\d+) min', x)
    hrs = int(h.group(1)) if h else 0
    mins = int(m.group(1)) if m else 0
    return hrs * 60 + mins
data['Total Minutes'] = data['Total Time'].apply(to_mins)

filtered_data = data.copy()

st.sidebar.title("Filters")

# department = st.selectbox(label = 'Choose one department from below:', options = department_list)
name = st.sidebar.text_input("Enter Name", "")
use_regex = st.sidebar.checkbox('Use Regex Search', value=False)
col1, col2, col3, col4 = st.columns([0.2,0.2,0.2,0.4])

# calorieFilter = 0
calorieFilter = st.sidebar.slider(
    "Select a range of calorie values",
    0, 2000
)

timeFilter = st.sidebar.slider(
    "Select total cook time (mins)",
    0, 2000
)

# with col1:
#     st.text("Type of Role:") # add a text 
# with col2:
#     role_faculty = st.checkbox('Faculty', value=0)
# with col3:
#     role_staff = st.checkbox('Staff', value=0)


# with col1:
#     st.text("Type of Position:") # add a text 
# with col2:
#     assist_prof = st.checkbox('Assistant Professor', value=0)
# with col3:
#     assoc_prof = st.checkbox('Associate Professor', value=0)
# with col4:
#     prof = st.checkbox('Professor', value=0)

# with col1:
#     st.text("Contract:") # add a text 
# with col2:
#     ftime = st.checkbox('FULL-TIME', value=0)
# with col3:
#     ptime = st.checkbox('PART-TIME', value=0)

# Apply department filter
if calorieFilter != 0:
    filtered_data = filtered_data[filtered_data['Calorie'] < calorieFilter]

if timeFilter!= 0:
    filtered_data = filtered_data[filtered_data['Total Minutes'] < timeFilter]

# if role_faculty:
#     filtered_data = filtered_data[filtered_data['Role'] == 'Faculty']
# if role_staff:
#     filtered_data = filtered_data[filtered_data['Role'] == 'Staff']

# if assist_prof:
#     filtered_data = filtered_data[filtered_data['Position'] == 'Assistant Professor']
# if assoc_prof:
#     filtered_data = filtered_data[filtered_data['Position'] == 'Associate Professor']
# if prof:
#     filtered_data = filtered_data[filtered_data['Position'] == 'Professor']

# if ftime:
#     filtered_data = filtered_data[filtered_data['Contract'] == 'FULL-TIME']
# if ptime:
#     filtered_data = filtered_data[filtered_data['Contract'] == 'PART-TIME']

if name != "":
    if use_regex:
        filtered_data = filtered_data[filtered_data['Title'].str.contains(name, case=False, regex=True)]
    else:
        filtered_data = filtered_data[filtered_data['Title'].str.contains(name, case=False, regex=False)]

fig, ax = plt.subplots(figsize=(6,4))
ax.hist(filtered_data['Calorie'])
ax.set_title('Distribution of Calories')
ax.set_xlabel('Calories')
ax.set_ylabel('Frequency')

# Display the plot using Streamlit
# st.toast(calorieFilter)
# st.pyplot(fig, use_container_width=True)

plotRow = st.columns(3)
plotRow[0].container(height=300).pyplot(fig, use_container_width=True)


st.dataframe(filtered_data, hide_index=True, 
         column_config={"Link": st.column_config.LinkColumn(display_text="Link")})