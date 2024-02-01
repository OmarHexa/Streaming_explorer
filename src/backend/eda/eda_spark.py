import os

import plotly.express as px
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

# Load environment variables from .env file
load_dotenv()

# Get environment variables
DATABASE_URL = os.getenv("JDBC_URL")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

# Assuming 'spark' is your SparkSession
spark = SparkSession.builder.appName("StreamingAnalysis").getOrCreate()
# Define connection properties
my_properties = {"user": USER, "password": PASSWORD, "driver": "com.mysql.cj.jdbc.Driver"}


def yearly_show_plot(service: str = "netflix"):
    """Generate a histogram of show releases over the years for a specified streaming service.

    Parameters:
    - service (str): The streaming service name. Default is "netflix".

    Returns:
    - str: JSON representation of the generated histogram.
    """
    query = f"(SELECT type, release_year FROM {service}) AS newTable"
    data = spark.read.jdbc(
        url=DATABASE_URL,
        table=query,
        properties=my_properties,
    )

    fig = px.histogram(data.toPandas(), x="release_year", color="type", barmode="group")
    fig.update_xaxes(range=[1990, 2022])

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
    query = f"(SELECT rating FROM {service}) AS newTable"
    rating_df = spark.read.jdbc(
        url=DATABASE_URL,
        table=query,
        properties=my_properties,
    )

    # Define the UDF to handle the mapping
    get_target_ages_udf = F.udf(
        lambda rating: ratings_ages_mapping.get(rating, "Unrated"), StringType()
    )

    # Define the new column "target_ages" based on the mapping
    rating_df = rating_df.withColumn("target_ages", get_target_ages_udf(rating_df["rating"]))
    fig = px.pie(
        rating_df.toPandas(),
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

    query = f"(SELECT listed_in FROM {service}) AS newTable"
    df_genres = spark.read.jdbc(
        url=DATABASE_URL,
        table=query,
        properties=my_properties,
    )

    genre_counts = (
        df_genres.select(F.explode(F.split(F.col("listed_in"), ", ")).alias("genre"))
        .groupBy("genre")
        .count()
        .sort("count", ascending=False)
    )
    fig = px.bar(
        genre_counts.toPandas(),
        x="genre",
        y="count",
        color_discrete_sequence=px.colors.sequential.Viridis,
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

    query = f"(SELECT country FROM {service}) AS newTable"
    country_df = spark.read.jdbc(
        url=DATABASE_URL,
        table=query,
        properties=my_properties,
    )
    country_df = country_df.filter(F.col("country") != "unknown")

    top_countries = (
        country_df.withColumn("country", F.explode(F.split("country", ", ")))
        .groupBy("country")
        .count()
        .orderBy(F.desc("count"))
        .limit(20)
    )

    color_palette = (
        px.colors.sequential.Rainbow_r
        if service == "netflix"
        else px.colors.sequential.Blues_r
        if service == "amazon"
        else px.colors.sequential.Blues
        if service == "disney"
        else px.colors.sequential.Rainbow_r
    )

    fig = px.treemap(
        top_countries.toPandas(),
        path=["country"],
        values="count",
        color_discrete_sequence=color_palette,
        title=f"Top 20 show producing countries for {service.capitalize()}",
        labels={"count": "Production Size"},
        template="plotly_dark",
    )

    plot_json = fig.to_json()
    return plot_json
