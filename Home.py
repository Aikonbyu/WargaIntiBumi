import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
import altair as alt

url1: str = 'https://docs.google.com/spreadsheets/d/1RiWBMTJ3NZkloRhQnjImCG0XT7LMraNMOzzePrB_Zug/edit?usp=sharing'
conn1: GSheetsConnection = st.experimental_connection('stunting', type=GSheetsConnection)

df: pd.DataFrame = conn1.read(spreadsheet=url1, worksheet=0)

# st.dataframe(df)
st.title('Stunting in Children Under 5 Years Old')
st.header('What is Stunting?')
st.write('**Stunting** is a condition in which a child is too short for his or her age. Stunting is the result of chronic or recurrent malnutrition, usually combined with frequent infections. Stunting has long-term consequences for children, such as poor cognitive development, low school performance, low adult wages, and lost productivity.')
st.subheader('What is the cause of Stunting?')
st.write('**Stunting** is caused by a long-term lack of nutrients and/or frequent infections. Poor nutrition before birth and in the first two years of life is most often the cause. Stunting is irreversible after the age of two, and has lifelong consequences for health, education and productivity.')
st.subheader('Why is Stunting important?')
st.write('**Stunting** is a key indicator of child well-being and development. It is also a major indicator of human capital and sustainable development. Stunting is a sign of multiple deprivations of a child’s rights to adequate nutrition, health and care. Stunting is a major public health problem that affects children’s physical and cognitive development, their educational performance, their future earnings, and their overall health. Stunting is also a major contributor to child mortality. Stunting is a major public health problem that affects children’s physical and cognitive development, their educational performance, their future earnings, and their overall health. Stunting is also a major contributor to child mortality.')


st.header('Percentage of Stunting from 2000 to 2020')
selected_country = st.selectbox('Select The Country', df['Country and areas'].unique())
if selected_country:
    st.subheader(f'{selected_country} Stunting Chart')
    filtered_data = df[df['Country and areas'] == selected_country]
    tahun_columns = [str(year) for year in range(2000, 2021)]
    melted_data = filtered_data.melt(id_vars=['Estimate'], value_vars=tahun_columns, var_name='Year', value_name='Percentage')
    pivoted_data = melted_data.pivot_table(index=['Year'], columns='Estimate', values='Percentage')
    st._arrow_line_chart(pivoted_data)

st.write('From chart above, we can see that stunting percentage in The Earth is decreasing from 2000 to 2020. It means that the world is getting better in terms of stunting. But, there are still many countries that have high stunting percentage. ')
st.header('Top 10 Lowest and Highest Stunting Percentage Countries')

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.horizontal = False

col1, col2 = st.columns(2)

with col1:
    selected_type = st.radio('Choose The Type', ["Lowest", "Highest"])

with col2:
    selected_year = st.selectbox('Choose Year', tahun_columns)



if selected_year:
    st.subheader(f'Top 10 {selected_type} Stunting Percentage in {selected_year}')
    if selected_type == "Lowest":
        top_10_countries = df[['Country and areas', selected_year, 'Estimate']].copy()
        top_10_countries = top_10_countries[top_10_countries['Estimate'] == 'Point Estimate']
        top_10_countries = top_10_countries.sort_values(by=selected_year, ascending=False).tail(10)
        # st.dataframe(top_10_countries)
        chart = (
            alt.Chart(top_10_countries).mark_bar().encode(\
                x=alt.X(selected_year),
                y=alt.Y('Country and areas', sort='x'),
            )
        )
        st.altair_chart(chart, use_container_width=True)
    elif selected_type == "Highest":
        top_10_countries = df[['Country and areas', selected_year, 'Estimate']].copy()
        top_10_countries = top_10_countries[top_10_countries['Estimate'] == 'Point Estimate']
        top_10_countries = top_10_countries.sort_values(by=selected_year, ascending=False).head(10)
        # st.dataframe(top_10_countries)
        chart = (
            alt.Chart(top_10_countries).mark_bar().encode(
                x=alt.X(selected_year),
                y=alt.Y('Country and areas', sort='-x'),
            )
        )
        st.altair_chart(chart, use_container_width=True)

st.write('From chart above, we can see that on 2020, the highest stunting percentage is in Burundi with 56.1%. That means, we need to keep improving our world to reduce stunting percentage. But, why stunting hard to reduce?')
st.image('./stunting.jpg', caption='The Cycle of Stunting', use_column_width=True)
st.write('From the picture above, we can see that stunting is a cycle. It means that stunting is a complex problem. It is not only about nutrition, but also about health, education, and many more. So, we need to solve this problem together.')

st.divider()
