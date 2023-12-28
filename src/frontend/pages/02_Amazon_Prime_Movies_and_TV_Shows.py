import streamlit as st
import pandas as pd
import numpy as np
import git

repo_path = git.Repo('.', search_parent_directories=True).working_tree_dir
data_path = repo_path + '/data/raw/Amazon_Prime_Video_Movies_and_TV_Shows.csv'

# columns = ['Sl.No', 'Title', 'Description', 'Genres', 'Cast', 'Director',
#        'Production Country', 'Added On', 'Year', 'Text8', 'Duration(in Mins)',
#        'Season', 'Rating']

# filter movies by Genre, Director, Actor, Production Country, Year, Rating, etc.
# Assuming you have a DataFrame named 'df' with the Amazon Prime Video data
# Load data
df = pd.read_csv(data_path, encoding='ISO-8859-1')

# data preprocessing
# drop year where year is not available
df = df.dropna(subset=['Year'])
# convert year to int
df['Year'] = df['Year'].astype(int)

# Get unique values for the filters
unique_years = ['All'] + df['Year'].unique().tolist()

unique_genres = ['All'] + df['Genres'].unique().tolist()
unique_directors = ['All'] + df['Director'].unique().tolist()
unique_actors = ['All'] + df['Cast'].unique().tolist()
unique_countries = ['All'] + df['Production Country'].unique().tolist()
unique_ratings = ['All'] + df['Rating'].unique().tolist()

# Create filters in the sidebar with default value set to 'All'
selected_year = st.sidebar.selectbox('Year', unique_years, index=0)
selected_genre = st.sidebar.selectbox('Genre', unique_genres, index=0)
selected_director = st.sidebar.selectbox('Director', unique_directors, index=0)
selected_actor = st.sidebar.selectbox('Actor', unique_actors, index=0)
selected_country = st.sidebar.selectbox('Country', unique_countries, index=0)
selected_rating = st.sidebar.selectbox('Rating', unique_ratings, index=0)

# Filter the DataFrame based on the selected values

# If 'All' is selected in all filters, show the original DataFrame
if selected_year == 'All' and selected_genre == 'All' and selected_director == 'All' and selected_actor == 'All' and selected_country == 'All' and selected_rating == 'All':
    filtered_df = df
else:
    # Otherwise, filter the rows based on the selection
    filtered_df = df[
        ((df['Year'] == selected_year) | (selected_year == 'All')) &
        ((df['Genres'] == selected_genre) | (selected_genre == 'All')) &
        ((df['Director'] == selected_director) | (selected_director == 'All')) &
        ((df['Cast'] == selected_actor) | (selected_actor == 'All')) &
        ((df['Production Country'] == selected_country) | (selected_country == 'All')) &
        ((df['Rating'] == selected_rating) | (selected_rating == 'All'))
    ]

# Display the filtered DataFrame
st.title("Amazon Prime Video Movies and TV Shows")
st.write(filtered_df)