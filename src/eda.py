import pandas as pd

def dataset_summary(movies,ratings,tags,links):
    print("-"*60)
    print("Dataset Summary")
    print("-"*60)

    print(f"Movies Dataset Shape : {movies.shape}")
    print(f"Ratings Dataset Shape : {ratings.shape}")
    print(f"Tags Dataset Shape    : {tags.shape}")
    print(f"Links Dataset Shape   : {links.shape}")

    print("\nUnique Movies :", movies["movieId"].nunique())

    print("Unique Users :", ratings["userId"].nunique())

    print("Unique Genres :", movies["genres"].nunique())

    print("Unique Tags :", tags["tag"].nunique())

    print("\n")
    print("=" * 60)
    print("MISSING VALUES")
    print("=" * 60)

    print("\nMovies")
    print(movies.isnull().sum())

    print("\nRatings")
    print(ratings.isnull().sum())

    print("\nTags")
    print(tags.isnull().sum())

    print("\nLinks")
    print(links.isnull().sum())

    print("\n")
    print("=" * 60)
    print("DUPLICATES")
    print("=" * 60)

    print("Movies :", movies.duplicated().sum())

    print("Ratings :", ratings.duplicated().sum())

    print("Tags :", tags.duplicated().sum())

    print("Links :", links.duplicated().sum())

def movie_analysis(movies,ratings):
    print("\n")
    print("=" * 60)
    print("MOVIE ANALYSIS")
    print("=" * 60)

    print(f"Total Movies : {movies['movieId'].nunique()}")

    genres = movies["genres"].str.split("|")
    genres = genres.explode()
    print(f"Total Genres:{genres.nunique()}")
    print(sorted(genres.unique()))


    print("\n")
    print("Most Common Genre")
    genre_count = genres.value_counts()

    print(genre_count.head(10))


   
    movies["year"] = movies["title"].str.extract(r"\((\d{4})\)")
    

    print("\n")
    print("Most Movies Released")
    print(movies["year"].value_counts().head(10))

def rating_analysis(ratings):
    print("\n")
    print("=" * 60)
    print("RATING ANALYSIS")
    print("=" * 60)

    print(f"Total Ratings : {len(ratings)}")
    print(f"Unique Users : {ratings['userId'].nunique()}")
    print(f"Average Rating : {ratings['rating'].mean():.2f}")
    print(f"Highest Rating : {ratings['rating'].max()}")
    print(f"Lowest Rating : {ratings['rating'].min()}")
    print("\nUnique Rating Values")
    print(sorted(ratings["rating"].unique()))
    print("\nRating Distribution")
    print(ratings["rating"].value_counts().sort_index())

    user_activity = ratings["userId"].value_counts()
    print("\nTop 10 Most Active Users")

    print(user_activity.head(10))

def tag_analysis(tags,movies):

    print("\n")
    print("=" * 60)
    print("TAG ANALYSIS")
    print("=" * 60)
    tags["tag"] = tags["tag"].str.lower().str.strip()

    print(f"Total Tags : {len(tags)}")
    print(f"Unique Tags : {tags['tag'].nunique()}")
    print("\nTop 20 Most Common Tags")
    print(tags["tag"].value_counts().head(20))
    movie_tag_count = tags["movieId"].value_counts()

    print("\nMovies With Most Tags")
    print(movie_tag_count.head(10))

    movie_tag_count = tags["movieId"].value_counts().head(10)
    top_movies = movies[
    movies["movieId"].isin(movie_tag_count.index)]

    print(top_movies[["movieId", "title"]])

    avg_tags = tags.groupby("movieId").size().mean()

    print(f"\nAverage Tags Per Movie : {avg_tags:.2f}")

    longest_tag = tags.loc[
    tags["tag"].str.len().idxmax()]

    print("\nLongest Tag")

    print(longest_tag["tag"])

def link_analysis(links,movies):
    print("\n")
    print("=" * 60)
    print("LINK ANALYSIS")
    print("=" * 60)


    print(f"Total Links : {len(links)}")

    print("\nMissing Values")
    print(links.isnull().sum())

    missing_movie_ids = links.loc[links["tmdbId"].isnull(),"movieId"]

    print(movies.loc[movies["movieId"].isin( missing_movie_ids),["movieId", "title"]])
