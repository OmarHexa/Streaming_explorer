import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database.config import engine


def recommend_similar_shows(input_title, top_n=3, platforms=("amazon", "disney", "netflix")):
    """Recommends similar shows from different platforms based on the input show title.

    Parameters:
    - input_title (str): The title of the show for which recommendations are sought.
    - top_n (int): Number of recommendations to retrieve for each platform. Default is 3.
    - platforms (tuple): Tuple of platform names to consider. Default is ("amazon", "disney", "netflix").

    Returns:
    dict: A dictionary containing recommendations for each platform. The keys are platform names, and
          the values are lists of dictionaries containing title and description of recommended shows.
          Returns None if the input show platform is not found.
    """
    result = {}
    all_platforms_data = {}

    # Read all platform data initially
    for platform in platforms:
        platform_data = pd.read_sql_query(f"SELECT description, title FROM {platform}", con=engine)
        platform_data["description"] = platform_data["description"].str.lower()
        all_platforms_data[platform] = platform_data

    # Find the platform of the input title
    input_show_platform = None

    for platform, platform_data in all_platforms_data.items():
        # Check if the input title exists in the current platform
        input_title_index = platform_data[platform_data["title"] == input_title].index

        if len(input_title_index) == 0:
            # Continue to the next platform if the title is not found
            continue

        input_title_index = input_title_index[0]
        input_description = platform_data.iloc[input_title_index]["description"]
        tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix_input = tfidf_vectorizer.fit_transform([input_description])

        top_similar_shows = find_similar_shows(
            platform_data, tfidf_vectorizer, tfidf_matrix_input, top_n + 1
        )
        result.setdefault(platform, [])
        for index, _ in top_similar_shows[1:]:
            result[platform].append(
                {
                    "title": platform_data.iloc[index]["title"],
                    "description": platform_data.iloc[index]["description"],
                }
            )
        input_show_platform = platform
        break
    # Return None if input_show_platform is not defined
    if input_show_platform is None:
        return None
    # suggest shows from other plateform
    for other_platform, other_platform_data in all_platforms_data.items():
        if other_platform != input_show_platform:
            top_similar_shows = find_similar_shows(
                other_platform_data, tfidf_vectorizer, tfidf_matrix_input, top_n
            )
            result.setdefault(other_platform, [])
            for index, _ in top_similar_shows:
                result[other_platform].append(
                    {
                        "title": other_platform_data.iloc[index]["title"],
                        "description": other_platform_data.iloc[index]["description"],
                    }
                )

    return result


def find_similar_shows(data, vectorizer, vectorizer_input, top_n):
    """Finds similar shows based on TF-IDF cosine similarity.

    Parameters:
    - data (pd.DataFrame): DataFrame containing show data.
    - vectorizer: TF-IDF vectorizer for transforming show descriptions.
    - vectorizer_input: TF-IDF matrix for the input show description.
    - top_n (int): Number of similar shows to retrieve.

    Returns:
    list: A list of tuples containing the index and cosine similarity score of similar shows.
    """
    tfidf_matrix_other = vectorizer.transform(data["description"])

    cosine_similarities = cosine_similarity(vectorizer_input, tfidf_matrix_other)
    del tfidf_matrix_other
    # Find top similar shows from the other platform
    similar_shows = list(enumerate(cosine_similarities[0]))
    similar_shows = sorted(similar_shows, key=lambda x: x[1], reverse=True)
    return similar_shows[:top_n]
