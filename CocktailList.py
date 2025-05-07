import streamlit as st
import pandas as pd
import numpy as np
import re 
import plotly.express as px

st.set_page_config(page_title="Cocktail List", layout="wide")

st.title('Cocktail List')
data = pd.read_csv('./recipes.csv') 
data = data.dropna(subset=['story']).query('story != ""')
def count_steps(steps_str):
    try:
        steps_str = steps_str.replace("'", "\"")
        import json
        steps_list = json.loads(steps_str)
        return len(steps_list)
    except:
        steps_raw = steps_str.strip('[]').split("', '")
        return len([step for step in steps_raw if step.strip("'")])

data['step_count'] = data['steps'].apply(count_steps)


filtered_data = data.copy()

st.sidebar.title("Filters")

name = st.sidebar.text_input("Enter Name", "")
use_regex = st.sidebar.checkbox('Use Regex Search', value=False)
col1, col2, col3, col4 = st.columns([0.2,0.2,0.2,0.4])

alc_list = data['primary_alcohol'].unique().tolist()
alc_list.insert(0, 'ALL')

prim_alc = st.sidebar.selectbox(label = 'Choose One Alcohol Type:', options = alc_list)

auth_list = data['author'].unique().tolist()
auth_list.insert(0, 'ALL')

author = st.sidebar.selectbox(label = 'Choose a Author:', options = auth_list)


reviewCountFilter = st.sidebar.slider(
    "Select a min number of reviews",
    0, 2000
)

if reviewCountFilter != 0:
    filtered_data = filtered_data[filtered_data['review_count'] > reviewCountFilter]

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

st.write("Cocktail Count: " + str(len(filtered_data)))

if len(event.selection['rows']):
    selected_row = event.selection['rows'][0]
    recipe = filtered_data.iloc[selected_row]
    
    st.header(recipe['title'])
    
    meta_col1, meta_col2 = st.columns(2)
    with meta_col1:
        st.write("**Author:** " + recipe['author'])
        st.write("**Primary Alcohol:** " + recipe['primary_alcohol'])
    with meta_col2:
        st.write("**Review Count:** " + str(recipe['review_count']))
    
    st.subheader("Ingredients")
    
    ingredients_str = recipe['ingredients']
    
    ingredients_str = ingredients_str.replace("'", "\"")
    
    try:
        import json
        ingredients_list = json.loads(ingredients_str)
        
        for item in ingredients_list:
            quantity = item.get('quantity', '')
            unit = item.get('unit', '')
            ingredient = item.get('ingredient', '')
            note = item.get('note', '')
            
            ingredient_line = f"• {quantity} {unit} {ingredient}"
            if note:
                ingredient_line += f" ({note})"
            
            st.write(ingredient_line)
    except:
        st.write(recipe['ingredients'])
    
    st.subheader("Instructions")
    
    steps_str = recipe['steps']
    steps_str = steps_str.replace("'", "\"")
    
    try:
        steps_list = json.loads(steps_str)
        for i, step in enumerate(steps_list, 1):
            if step.strip():
                st.write(f"{i}. {step.strip()}")
    except:
        steps_raw = recipe['steps'].strip('[]').split("', '")
        for i, step in enumerate(steps_raw, 1):
            clean_step = step.strip("'")
            if clean_step:
                st.write(f"{i}. {clean_step}")

    st.info("**Story Behind the Drink**\n" + recipe['story'])

else:
    st.subheader("Cocktail Insights")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        alcohol_counts = filtered_data['primary_alcohol'].value_counts().reset_index()
        alcohol_counts.columns = ['Alcohol Type', 'Count']
        
        fig1 = px.bar(
            alcohol_counts, 
            x='Alcohol Type', 
            y='Count',
            title='Cocktails by Primary Alcohol',
            color='Count',
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(xaxis_title='Primary Alcohol', yaxis_title='Number of Cocktails')
        st.plotly_chart(fig1, use_container_width=True)
    
    with chart_col2:
        fig2 = px.scatter(
            filtered_data, 
            x='step_count', 
            y='review_count',
            color='primary_alcohol',
            size='review_count',
            hover_data=['title'],
            title='Cocktail Complexity vs. Popularity',
            labels={
                'step_count': 'Number of Steps (Complexity)',
                'review_count': 'Number of Reviews (Popularity)'
            }
        )
        fig2.update_layout(legend_title_text='Primary Alcohol')
        st.plotly_chart(fig2, use_container_width=True)
