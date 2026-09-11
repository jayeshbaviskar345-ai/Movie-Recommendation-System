import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def create_user_movie_matrix(ratings):

    user_movie_matrix = ratings.pivot_table(
        index="movieId",
        columns="userId",
        values="rating",
        fill_value=0
    )

    return user_movie_matrix

def build_collaborative_similarity(user_movie_matrix):

    print("\n")
    print("=" * 60)
    print("BUILDING COLLABORATIVE SIMILARITY")
    print("=" * 60)

    similarity_matrix = cosine_similarity(user_movie_matrix)
    print("Similarity Matrix Shape:", similarity_matrix.shape)

    return similarity_matrix

def collaborative_recommend(movie_title,movies_data,user_movie_matrix, collaborative_similarity):
    movie = movies_data[movies_data["title"] == movie_title]

    if movie.empty:
        print("Movie not Found!")
        return
    
    movie_id = movie.iloc[0]["movieId"]

    movie_index = user_movie_matrix.index.get_loc(movie_id)

    similarity_scores = collaborative_similarity[movie_index]

    similar_movies = list(enumerate(similarity_scores))

    similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

    recommended_movies = similar_movies[1:101]

    print("\nCollaborative Recommendations:\n")
    recommendations = []

    for movie in recommended_movies:

        row_index = movie[0]
        score = movie[1]

        recommended_movie_id = user_movie_matrix.index[row_index]

        title = movies_data[movies_data["movieId"] == recommended_movie_id]["title"].values[0]

        recommendations.append({"movieId": recommended_movie_id,"title": title,"score": score})

    return pd.DataFrame(recommendations)

        
