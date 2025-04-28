import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import re 

st.set_page_config(page_title="Cocktail List", layout="wide")

st.title('Cocktail List')
data = pd.read_csv('./recipes.csv') 
data = data.dropna(subset=['story']).query('story != ""')


filtered_data = data.copy()

st.sidebar.title("Filters")

# department = st.selectbox(label = 'Choose one department from below:', options = department_list)
name = st.sidebar.text_input("Enter Name", "")
use_regex = st.sidebar.checkbox('Use Regex Search', value=False)
col1, col2, col3, col4 = st.columns([0.2,0.2,0.2,0.4])

alc_list = data['primary_alcohol'].unique().tolist()
alc_list.insert(0, 'ALL')

prim_alc = st.sidebar.selectbox(label = 'Choose One Alcohol Type:', options = alc_list)

auth_list = data['author'].unique().tolist()
auth_list.insert(0, 'ALL')

author = st.sidebar.selectbox(label = 'Choose a Author:', options = auth_list)

# calorieFilter = 0
reviewCountFilter = st.sidebar.slider(
    "Select a min number of reviews",
    0, 2000
)

timeFilter = st.sidebar.slider(
    "Select total cook time (mins)",
    0, 2000
)

# Apply department filter
if reviewCountFilter != 0:
    filtered_data = filtered_data[filtered_data['review_count'] > reviewCountFilter]

# if timeFilter!= 0:
#     filtered_data = filtered_data[filtered_data['Total Minutes'] < timeFilter]

if prim_alc != 'ALL':
    filtered_data = filtered_data[filtered_data['primary_alcohol'] == prim_alc]

if author != 'ALL':
    filtered_data = filtered_data[filtered_data['author'] == author]


if name != "":
    if use_regex:
        filtered_data = filtered_data[filtered_data['title'].str.contains(name, case=False, regex=True)]
    else:
        filtered_data = filtered_data[filtered_data['title'].str.contains(name, case=False, regex=False)]


event = st.dataframe(
    filtered_data,
    on_select='rerun',
    selection_mode='single-row',
    hide_index=True, 
    column_config={"url": st.column_config.LinkColumn(display_text="Link")}
)

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]
    recipe = filtered_data.iloc[selected_row]
    
    # Display title in large format
    st.header(recipe['title'])
    
    # Create columns for metadata
    meta_col1, meta_col2 = st.columns(2)
    with meta_col1:
        st.write("**Author:** " + recipe['author'])
        st.write("**Primary Alcohol:** " + recipe['primary_alcohol'])
    with meta_col2:
        st.write("**Review Count:** " + str(recipe['review_count']))
    
    # Display story in a highlighted box
    
    # Display ingredients in a clean list
    st.subheader("Ingredients")
    ingredients_list = recipe['ingredients'].split('\n')
    for ingredient in ingredients_list:
        st.write("• " + ingredient.strip())
    
    # Display steps in a numbered list
    st.subheader("Instructions")
    steps_list = recipe['steps'].split('\n')
    for i, step in enumerate(steps_list, 1):
        if step.strip():  # Only display non-empty steps
            st.write(f"{i}. {step.strip()}")

    st.info("**Story Behind the Drink**\n" + recipe['story'])

fig, ax = plt.subplots(figsize=(6,4))
ax.hist(filtered_data['review_count'])
ax.set_title('Distribution of reviews')
ax.set_xlabel('Reviews')
ax.set_ylabel('Frequency')

# Display the plot using Streamlit
# st.toast(calorieFilter)
# st.pyplot(fig, use_container_width=True)

plotRow = st.columns(3)
plotRow[0].container(height=300).pyplot(fig, use_container_width=True)