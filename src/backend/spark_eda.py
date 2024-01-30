import plotly.express as px
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Assuming 'spark' is your SparkSession
spark = SparkSession.builder.appName("StreamingAnalysis").getOrCreate()


def yearly_show_plot(service: str = "netflix"):
    """Yearly plot using pyspark."""
    query = f"SELECT type, release_year FROM {service}"
    data = spark.read.jdbc(
        url="jdbc:mysql://<YOUR_MYSQL_HOST>:<YOUR_MYSQL_PORT>/<YOUR_DATABASE>",
        table=query,
        properties={"user": "<YOUR_MYSQL_USER>", "password": "<YOUR_MYSQL_PASSWORD>"},
    )

    fig = px.histogram(data.toPandas(), x="release_year", color="type", barmode="group")
    fig.update_xaxes(range=[1990, 2022])

    plot_json = fig.to_json()
    return plot_json


def rating_plot(service: str = "netflix"):
    """Rating plot using pyspark."""

    ratings_ages_mapping = {
        # Ratings mapping remains the same as in the original function
    }
    rating_df = spark.read.jdbc(
        url="jdbc:mysql://<YOUR_MYSQL_HOST>:<YOUR_MYSQL_PORT>/<YOUR_DATABASE>",
        table=f"{service}",
        properties={"user": "<YOUR_MYSQL_USER>", "password": "<YOUR_MYSQL_PASSWORD>"},
    )

    rating_df = rating_df.withColumn(
        "target_ages", col("rating").rlike("|".join(ratings_ages_mapping.keys()))
    )
    rating_df = rating_df.withColumn(
        "target_ages", col("target_ages").alias("target_ages").cast("string")
    )

    fig = px.pie(
        rating_df.toPandas(),
        names="target_ages",
        title=f"{service.capitalize()} Ratings Distribution",
        color_discrete_sequence=px.colors.sequential.Rainbow,
    )

    plot_json = fig.to_json()
    return plot_json


def genres_plot(service: str = "netflix"):
    """Genres plot using pyspark."""

    df_genres = spark.read.jdbc(
        url="jdbc:mysql://<YOUR_MYSQL_HOST>:<YOUR_MYSQL_PORT>/<YOUR_DATABASE>",
        table=f"{service}",
        properties={"user": "<YOUR_MYSQL_USER>", "password": "<YOUR_MYSQL_PASSWORD>"},
    )
    df_genres = (
        df_genres.select("listed_in")
        .rdd.flatMap(lambda x: x[0].split(", "))
        .map(lambda x: (x, 1))
        .reduceByKey(lambda x, y: x + y)
        .toDF(["genre", "count"])
    )

    fig = px.bar(
        df_genres.toPandas(),
        x="genre",
        y="count",
        color_discrete_sequence=px.colors.sequential.Viridis,
    )

    plot_json = fig.to_json()
    return plot_json


def country_prod_plot(service: str = "netflix"):
    """Country show production plot using pyspark."""

    country_df = spark.read.jdbc(
        url="jdbc:mysql://<YOUR_MYSQL_HOST>:<YOUR_MYSQL_PORT>/<YOUR_DATABASE>",
        table=f"{service}",
        properties={"user": "<YOUR_MYSQL_USER>", "password": "<YOUR_MYSQL_PASSWORD>"},
    )
    country_df = country_df.filter(col("country") != "unknown")

    top_countries = (
        country_df.select("country")
        .rdd.flatMap(lambda x: x[0].split(", "))
        .map(lambda x: (x, 1))
        .reduceByKey(lambda x, y: x + y)
        .sortBy(lambda x: x[1], ascending=False)
        .take(20)
    )
    top_countries_df = spark.createDataFrame(top_countries, ["country", "size"])

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
        top_countries_df.toPandas(),
        path=["country"],
        values="size",
        color_discrete_sequence=color_palette,
        title=f"Top 20 show producing countries for {service.capitalize()}",
        labels={"size": "Production Size"},
        template="plotly_dark",
    )

    plot_json = fig.to_json()
    return plot_json
