import streamlit as st
import pandas as pd
import numpy as np
import git

repo_path = git.Repo('.', search_parent_directories=True).working_tree_dir
data_path = repo_path + '/data/raw/disney_plus_shows.csv'

columns = ['imdb_id', 'title', 'plot', 'type', 'rated', 'year', 'released_at',
       'added_at', 'runtime', 'genre', 'director', 'writer', 'actors',
       'language', 'country', 'awards', 'metascore', 'imdb_rating',
       'imdb_votes']

# Assuming you have a DataFrame named 'df' with the Disney+ data
# Load data
df = pd.read_csv(data_path)

# get rid of extra characters in year column


# convert year column to int


# drop rows if imdb_id and title are both null
df = df.dropna(subset=['imdb_id', 'title'])

# create imdb links
def make_clickable(url, name):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)

df['imdb_link'] = df.apply(lambda row: make_clickable('https://www.imdb.com/title/' + str(row['imdb_id']), str(row['imdb_id'])), axis=1)


# Get unique values for the filters
unique_years = ['All'] + df['year'].unique().tolist()
unique_genres = ['All'] + df['genre'].unique().tolist()
unique_directors = ['All'] + df['director'].unique().tolist()
unique_actors = ['All'] + df['actors'].unique().tolist()
unique_countries = ['All'] + df['country'].unique().tolist()
unique_ratings = ['All'] + df['imdb_rating'].unique().tolist()

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
        ((df['year'] == selected_year) | (selected_year == 'All')) &
        ((df['genre'] == selected_genre) | (selected_genre == 'All')) &
        ((df['director'] == selected_director) | (selected_director == 'All')) &
        ((df['actors'] == selected_actor) | (selected_actor == 'All')) &
        ((df['country'] == selected_country) | (selected_country == 'All')) &
        ((df['imdb_rating'] == selected_rating) | (selected_rating == 'All'))
    ]

# Display the filtered DataFrame
st.title("Disney+ Shows")
st.markdown(filtered_df[['imdb_link', 'title', 'year', 'genre', 'director', 'actors', 'country', 'imdb_rating']].to_html(escape=False), unsafe_allow_html=True)
