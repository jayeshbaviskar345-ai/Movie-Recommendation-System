import pandas as pd 

def preprocess_tags(tags):
    print("\n")
    print("="*60)
    print("Preprocessing Tags")
    print("="*60)

    tags["tag"] = tags["tag"].str.lower().str.strip()
    print("Tags Cleaned Successfully")
    print(tags.head())

    return tags

def combine_tags(tags):
    print("\n")
    print("="*60)
    print("Combining Tags")
    print("="*60)

    tags = tags.drop_duplicates(subset=["movieId","tag"])
    combined_tags = (tags.groupby("movieId")["tag"].apply(" ".join).reset_index())
    print("Tags Combined Successfully")
    print(combined_tags.head())

    return combined_tags

def merge_movie_tag(movies,combined_tags):
    print("\n")
    print("="*60)
    print("Merging Tags in Movies Data")
    print("="*60)

    movies_data = movies.merge(combined_tags,on="movieId",how="left")
    movies_data["tag"] = movies_data["tag"].fillna("No Tag")

    print("Movies Merge Successfully")
    print(movies_data.head())
    return movies_data

def create_feature(movies_data):
    print("\n")
    print("=" * 60)
    print("CREATING FEATURES")
    print("=" * 60)

    movies_data["genres"] = movies_data["genres"].str.replace("|"," ",regex=False)
    movies_data["title"] = movies_data["title"].str.replace(r"\s*\(\d{4}\)$", "", regex=True)

    movies_data["features"] = ( movies_data["genres"] + " " + movies_data["tag"])

    print(movies_data.head())

    return movies_data
