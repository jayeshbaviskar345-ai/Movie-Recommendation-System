import pandas as pd


def build_popularity_model(ratings):

    movie_stats = ratings.groupby("movieId").agg(
        average_rating=("rating", "mean"),
        number_of_ratings=("rating", "count")
    ).reset_index()

    C = movie_stats["average_rating"].mean()

    m = movie_stats["number_of_ratings"].quantile(0.90)

    movie_stats = movie_stats[
        movie_stats["number_of_ratings"] >= m
    ].copy()

    movie_stats["popularity_score"] = (
        (movie_stats["number_of_ratings"] /
        (movie_stats["number_of_ratings"] + m))
        * movie_stats["average_rating"]
    ) + (
        (m /
        (movie_stats["number_of_ratings"] + m))
        * C
    )

    return movie_stats[
        ["movieId", "popularity_score"]
    ]