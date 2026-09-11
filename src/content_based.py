from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def build_tfidf(movies_data):
    print("\n")
    print("=" * 60)
    print("BUILDING TF-IDF MODEL")
    print("=" * 60)

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(movies_data["features"])

    print("TF-IDF Matrix Shape :", tfidf_matrix.shape)

    return vectorizer , tfidf_matrix

def build_similarity(tfidf_matrix):

    print("\n")
    print("=" * 60)
    print("BUILDING COSINE SIMILARITY MATRIX")
    print("=" * 60)

    similarity_matrix = cosine_similarity(
        tfidf_matrix
    )

    print("Similarity Matrix Shape:",
          similarity_matrix.shape)

    return similarity_matrix

def recommend(movie_title, movies_data, similarity_matrix):

    print("Selected Movie:", movie_title)

    movie = movies_data[movies_data["title"] == movie_title]

    print(movie)

    if movie.empty:
        print("Movie not found!")
        return pd.DataFrame()

    movie_index = movie.index[0]

    similarity_score = similarity_matrix[movie_index]

    similar_movies = list(enumerate(similarity_score))

    similar_movies = sorted(
        similar_movies,
        key=lambda x: x[1],
        reverse=True
    )

    recommend_movies = similar_movies[1:101]

    recommendations = []

    for movie in recommend_movies:

        idx = movie[0]
        score = movie[1]

        recommendations.append({
            "movieId": movies_data.iloc[idx]["movieId"],
            "title": movies_data.iloc[idx]["title"],
            "score": score
        })

    return pd.DataFrame(recommendations)

        



