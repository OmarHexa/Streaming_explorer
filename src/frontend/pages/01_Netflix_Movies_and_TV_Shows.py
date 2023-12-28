import streamlit as st
import pandas as pd
import numpy as np
import git

repo_path = git.Repo('.', search_parent_directories=True).working_tree_dir
data_path = repo_path + '/data/raw/netflix_titles.csv'

# filter movies by year, genre, director, actor, country, rating, etc.
# Assuming you have a DataFrame named 'df' with the Netflix data
# Load data
df = pd.read_csv(data_path)

# Get unique values for the filters
unique_years = ['All'] + df['release_year'].unique().tolist()
unique_genres = ['All'] + df['listed_in'].unique().tolist()
unique_directors = ['All'] + df['director'].unique().tolist()
unique_actors = ['All'] + df['cast'].unique().tolist()
unique_countries = ['All'] + df['country'].unique().tolist()
unique_ratings = ['All'] + df['rating'].unique().tolist()

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
        ((df['release_year'] == selected_year) | (selected_year == 'All')) &
        ((df['listed_in'] == selected_genre) | (selected_genre == 'All')) &
        ((df['director'] == selected_director) | (selected_director == 'All')) &
        ((df['cast'] == selected_actor) | (selected_actor == 'All')) &
        ((df['country'] == selected_country) | (selected_country == 'All')) &
        ((df['rating'] == selected_rating) | (selected_rating == 'All'))
    ]

# Display the filtered DataFrame
st.title("Netflix Movies and TV Shows")
st.write(filtered_df)