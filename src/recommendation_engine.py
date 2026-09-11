from src.data_loader import load_data
from src.preprocessing import (
    preprocess_tags,
    combine_tags,
    merge_movie_tag,
    create_feature
)
from src.content_based import (
    build_tfidf,
    build_similarity,
    recommend
)
from src.collaborative import (
    create_user_movie_matrix,
    build_collaborative_similarity,
    collaborative_recommend
)
from src.popularity import build_popularity_model
from src.hybrid import hybrid_recommend


# Load everything only once
movies, ratings, tags, links = load_data()

movies = movies.merge(
    links[["movieId", "tmdbId"]],
    on="movieId",
    how="left"
)

tags = preprocess_tags(tags)

combined_tags = combine_tags(tags)

movies_data = merge_movie_tag(movies, combined_tags)

movies_data = create_feature(movies_data)

vectorizer, tfidf_matrix = build_tfidf(movies_data)

similarity_matrix = build_similarity(tfidf_matrix)

user_movie_matrix = create_user_movie_matrix(ratings)

collaborative_similarity = build_collaborative_similarity(user_movie_matrix)

popularity_df = build_popularity_model(ratings)


def recommend_movies(movie_name):

    content_df = recommend(
        movie_name,
        movies_data,
        similarity_matrix
    )

    collab_df = collaborative_recommend(
        movie_name,
        movies_data,
        user_movie_matrix,
        collaborative_similarity
    )

    hybrid_df = hybrid_recommend(
        content_df,
        collab_df,
        popularity_df
    )
    hybrid_df = hybrid_df.merge(
        movies[["movieId", "tmdbId"]],
        on="movieId",
        how="left"
    )

    return hybrid_df

movies_for_ui = movies_data

 