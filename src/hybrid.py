import pandas as pd 


def hybrid_recommend(content_df,collab_df,popularity_df):
    print("\n")
    print("=" * 60)
    print("HYBRID RECOMMENDATION")
    print("=" * 60)

    content_df["score"] = (content_df["score"] /content_df["score"].max())

    collab_df["score"] = (collab_df["score"] /collab_df["score"].max())


    content_df = content_df.rename(columns={"score":"content_score"})

    collab_df = collab_df.rename(columns={"score":"collab_score"})

    hybrid = pd.merge(content_df,collab_df,on=["movieId","title"],how="outer")
    hybrid = hybrid.merge(popularity_df,on="movieId",how="left")


    hybrid["content_score"] = hybrid["content_score"].fillna(0)
    hybrid["collab_score"] = hybrid["collab_score"].fillna(0)
    hybrid["popularity_score"] = hybrid["popularity_score"].fillna(0)

    if hybrid["popularity_score"].max() > 0:
        hybrid["popularity_score"] /= hybrid["popularity_score"].max()

    content_weight = 0.4
    collab_weight = 0.4
    popularity_weight = 0.2

    hybrid["final_score"] = (
    content_weight * hybrid["content_score"] +
    collab_weight * hybrid["collab_score"] +
    popularity_weight * hybrid["popularity_score"])

    hybrid = hybrid.sort_values(
        by="final_score",
        ascending=False)

    return hybrid.head(10)


def hybrid_recommend_rrf(content_df, collab_df):

    print("\n")
    print("=" * 60)
    print("HYBRID RECOMMENDATION (RRF)")
    print("=" * 60)

    
    content_df = content_df.copy()
    collab_df = collab_df.copy()

    
    content_df["content_rank"] = range(1, len(content_df) + 1)
    collab_df["collab_rank"] = range(1, len(collab_df) + 1)

   
    content_df = content_df[
        ["movieId", "title", "content_rank"]
    ]

    collab_df = collab_df[
        ["movieId", "title", "collab_rank"]
    ]

    
    hybrid = pd.merge(
        content_df,
        collab_df,
        on=["movieId", "title"],
        how="outer"
    )

    
    hybrid["content_rank"] = hybrid["content_rank"].fillna(1000)
    hybrid["collab_rank"] = hybrid["collab_rank"].fillna(1000)

    
    k = 60

    
    hybrid["content_rrf"] = (
        1 / (k + hybrid["content_rank"])
    )

    hybrid["collab_rrf"] = (
        1 / (k + hybrid["collab_rank"])
    )

    
    hybrid["final_score"] = (
        hybrid["content_rrf"] +
        hybrid["collab_rrf"]
    )

    
    hybrid = hybrid.sort_values(
        by="final_score",
        ascending=False
    )

    return hybrid.head(10)

