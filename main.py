from src.data_loader import load_data
from src.eda import dataset_summary , movie_analysis , rating_analysis , tag_analysis , link_analysis
from src.preprocessing import preprocess_tags , combine_tags , merge_movie_tag , create_feature
from src.content_based import build_tfidf , build_similarity , recommend
from src.collaborative import create_user_movie_matrix , build_collaborative_similarity ,collaborative_recommend
from src.popularity import build_popularity_model
from src.hybrid import hybrid_recommend , hybrid_recommend_rrf
from src.tmdb import get_movie_details,get_poster_url
from src.recommendation_engine import recommend_movies

import pandas as pd


movies, ratings , tags , links = load_data()

dataset_summary(movies,ratings,tags,links)

movie_analysis(movies,ratings)

rating_analysis(ratings)

tag_analysis(tags,movies)

link_analysis(links,movies)

tags = preprocess_tags(tags)

combined_tags = combine_tags(tags)

movies_data = merge_movie_tag(movies,combined_tags)

movies_data = create_feature(movies_data)

vectorizer, tfidf_matrix = build_tfidf(movies_data)

similarity_matrix = build_similarity(tfidf_matrix)

user_movie_matrix = create_user_movie_matrix(ratings)

collaborative_similarity = build_collaborative_similarity(user_movie_matrix)

content_df = recommend("Toy Story",movies_data,similarity_matrix)

collab_df = collaborative_recommend("Toy Story",movies_data,user_movie_matrix,collaborative_similarity)

popularity_df = build_popularity_model(ratings)

hybrid_df = hybrid_recommend(content_df,collab_df,popularity_df)

print(hybrid_df)

hybrid_df_rrf = hybrid_recommend_rrf(content_df,collab_df)

print(hybrid_df_rrf)


movies = movies.merge(links[["movieId","tmdbId"]],on="movieId",how="left")


hybrid_df = hybrid_df.merge(
    movies[["movieId", "tmdbId"]],
    on="movieId",
    how="left"
)

print("\n" + "=" * 70)
print("HYBRID RECOMMENDATIONS WITH TMDb")
print("=" * 70)

for index, row in hybrid_df.iterrows():

    try:
        movie = get_movie_details(row["tmdbId"])

        if movie is None:
            continue

        poster = get_poster_url(movie.get("poster_path"))

        print("Movie :", movie.get("title"))
        print("Rating:", movie.get("vote_average"))
        print("Release:", movie.get("release_date"))
        print("Poster :", poster)

        print("-" * 80)

    except Exception as e:
        print("Error:", row["title"])
        print(e)


tmdb_id = 862  # Toy Story

movie = get_movie_details(tmdb_id)

print("=" * 60)
print("MOVIE DETAILS")
print("=" * 60)

print("Title          :", movie["title"])
print("Overview       :", movie["overview"])
print("Release Date   :", movie["release_date"])
print("Rating         :", movie["vote_average"])
print("Poster URL     :", get_poster_url(movie["poster_path"]))


print(recommend_movies("Toy Story"))






