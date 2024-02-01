import pandas as pd
import plotly.express as px

from src.backend.database.mysql.config import engine


def yearly_show_plot(service: str = "netflix"):
    """Generate a histogram of show releases over the years for a specified streaming service.

    Parameters:
    - service (str): The streaming service name. Default is "netflix".

    Returns:
    - str: JSON representation of the generated histogram.
    """
    query = f"SELECT type, release_year FROM {service}"
    data = pd.read_sql_query(query, con=engine)
    # Create the histogram using Plotly Express
    fig = px.histogram(data, x="release_year", color="type", barmode="group")
    fig.update_xaxes(range=[1990, 2022])
    # Convert the plot to JSON and return it
    plot_json = fig.to_json()
    return plot_json


def rating_plot(service: str = "netflix"):
    """Generate a pie chart showing the distribution of show ratings for a specified streaming
    service.

    Parameters:
    - service (str): The streaming service name. Default is "netflix".

    Returns:
    - str: JSON representation of the generated pie chart.
    """
    ratings_ages_mapping = {
        "G": "Kids",
        "TV-Y": "Kids",
        "TV-G": "Kids",
        "TV-PG": "Kids",
        "PG": "Kids",
        "TV-Y7": "Kids",
        "TV-Y7-FV": "Kids",
        "7+": "Kids",
        "TV-14": "Teens",
        "13+": "Teens",
        "PG-13": "Teens",
        "NC-17": "Adults",
        "18+": "Adults",
        "16+": "Adults",
        "16": "Adults",
        "AGES_16_": "Adults",
        "R": "Adults",
        "TV-MA": "Adults",
        "ALL": "All",
        "66 MIN": "All",
        "84 MIN": "All",
        "74 MIN": "All",
        "ALL_AGES": "All",
        "NOT_RATE": "Unrated",
        "UNRATED": "Unrated",
        "NR": "Unrated",
        "TV-NR": "Unrated",
        "UNKNOWN": "Unrated",
        "UR": "Unrated",
        # Add more ratings as needed
    }
    rating_df = pd.read_sql_query(f"SELECT rating from {service}", con=engine)

    rating_df["target_ages"] = rating_df["rating"].replace(ratings_ages_mapping)
    rating_df["target_ages"].unique()

    # Replace categories not present in ratings_ages with 'unknown'
    unknown_categories = set(rating_df["rating"].unique()) - set(ratings_ages_mapping.keys())
    rating_df["target_ages"] = rating_df["target_ages"].replace(unknown_categories, "Unrated")

    fig = px.pie(
        rating_df,
        names="target_ages",
        title=f"{service.capitalize()} Ratings Distribution",
        color_discrete_sequence=px.colors.sequential.Rainbow,
    )

    plot_json = fig.to_json()
    return plot_json


def genres_plot(service: str = "netflix"):
    """Generate a bar plot showing the distribution of genres for a specified streaming service.

    Parameters:
    - service (str): The streaming service name. Default is "netflix".

    Returns:
    - str: JSON representation of the generated bar plot.
    """
    df_genres = pd.read_sql_query(f"SELECT listed_in FROM {service}", con=engine)
    df_genres = df_genres["listed_in"].str.split(", ", expand=True).stack().value_counts()
    df_genres = pd.DataFrame(df_genres)
    df_genres.reset_index(inplace=True)
    df_genres.columns = ["genre", "count"]
    fig = px.bar(
        df_genres, x="genre", y="count", color_discrete_sequence=px.colors.sequential.Viridis
    )
    plot_json = fig.to_json()
    return plot_json


def country_prod_plot(service: str = "netflix"):
    """Generate a treemap showing the distribution of show production across countries for a
    specified streaming service.

    Parameters:
    - service (str): The streaming service name. Default is "netflix".

    Returns:
    - str: JSON representation of the generated treemap.
    """
    country_df = pd.read_sql_query(f"SELECT country FROM {service}", con=engine)

    # Remove rows where 'country' is 'unknown'
    country_df = country_df[country_df["country"] != "unknown"]

    # Split the 'country' column, stack, and count occurrences
    top_countries = (
        country_df["country"]
        .str.split(", ", expand=True)
        .stack()
        .value_counts()
        .head(20)
        .reset_index()
    )
    top_countries.columns = ["country", "size"]

    # Define color palette based on service
    if service == "netflix":
        color_palette = px.colors.sequential.Rainbow_r
    elif service == "amazon":
        color_palette = px.colors.sequential.Blues_r
    elif service == "disney":
        color_palette = px.colors.sequential.Blues
    else:
        color_palette = px.colors.sequential.Rainbow_r  # Default to Rainbow_r for unknown services

    # Create a treemap using Plotly Express
    fig = px.treemap(
        top_countries,
        path=["country"],
        values="size",
        color_discrete_sequence=color_palette,
        title=f"Top 20 show producing countries for {service.capitalize()}",
        labels={"size": "Production Size"},
        template="plotly_dark",
    )

    plot_json = fig.to_json()
    return plot_json
