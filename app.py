import streamlit as st
from src.recommendation_engine import recommend_movies, movies_for_ui
from src.tmdb import get_movie_details, get_poster_url

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="🎬 AI Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

h1,h2,h3{
    color:white;
}

.movie-title{
    text-align:center;
    font-size:18px;
    font-weight:bold;
    min-height:60px;
}

.movie-card{
    background:#1E1E1E;
    padding:0;
    border-radius:15px;
    text-align:center;
    overflow:hidden;
}

.movie-card img{
    display:block;
    border:none !important;
    margin:0 !important;
}
.details-card{
    background:#1E1E1E;
    padding:20px;
    border-radius:20px;
}
            

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ---------------- #

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "selected_movie_details" not in st.session_state:
    st.session_state.selected_movie_details = None

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🎬 Movie Recommendation System")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### Algorithms

- 🎯 Content Based Filtering
- 👥 Collaborative Filtering
- ⚡ Hybrid Recommendation

### Dataset

- MovieLens
- TMDb API
""")

st.sidebar.markdown("---")

st.sidebar.success("Developed using Streamlit")

# ---------------- TITLE ---------------- #

st.title("🎬 AI Hybrid Movie Recommendation System")

st.write(
    "Select your favourite movie and discover similar movies instantly."
)

st.divider()

# ---------------- DROPDOWN ---------------- #

movie_list = sorted(
    movies_for_ui["title"].tolist()
)

selected_movie = st.selectbox(
    "🔍 Search for a Movie",
    options=movie_list,
    index=None,
    placeholder="Start typing a movie name..."
)

# ---------------- RECOMMEND ---------------- #

if selected_movie is None:
    st.info("👆 Search and select a movie to get recommendations.")
else:
    if st.button("🎬 Get Recommendations",type="primary",use_container_width=True):
        with st.spinner("Finding best recommendations..."):
            st.session_state.recommendations = recommend_movies(selected_movie)
            st.session_state.selected_movie_details = None


# ---------------- SHOW RECOMMENDATIONS ---------------- #

if st.session_state.recommendations is not None:

    recommendations = st.session_state.recommendations

    st.divider()

    st.subheader("🎬 Recommended Movies")

    cols = st.columns(5)

    for i, (_, row) in enumerate(recommendations.head(5).iterrows()):

        tmdb_id = row.get("tmdbId")

        if tmdb_id is None:
            continue

        movie = get_movie_details(tmdb_id)

        if movie is None:
            continue

        poster = get_poster_url(movie.get("poster_path"))

        with cols[i]:

            st.markdown('<div class="movie-card">', unsafe_allow_html=True)

            if poster:
                st.image(
                    poster,
                    use_container_width=True
                )
            else:
                st.image(
                    "https://via.placeholder.com/500x750?text=No+Poster",
                    use_container_width=True
                )

            st.markdown(
                f"""
                <div class="movie-title">
                {movie.get("title","Unknown")}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"⭐ **{movie.get('vote_average','N/A')}**"
            )

            st.markdown(
                f"📅 {movie.get('release_date','N/A')}"
            )

            score = row.get("final_score")

            if score is None:
                score = row.get("score")

            if score is not None:

                try:

                    st.write("### 🤖 Recommendation Score")

                    st.metric(
                        "Similarity",
                        f"{score:.3f}"
                    )

                except:
                    pass

            if st.button(
                "🎬 View Details",
                key=f"movie_{i}",
                use_container_width=True
            ):

                st.session_state.selected_movie_details = {

                    "movie": movie,

                    "poster": poster,

                    "score": score,

                    "tmdb_id": tmdb_id

                }

            st.markdown("</div>", unsafe_allow_html=True)


# ---------------- MOVIE DETAILS ---------------- #

if st.session_state.selected_movie_details is not None:

    details = st.session_state.selected_movie_details

    movie = details["movie"]

    st.divider()

    st.subheader("🎬 Movie Details")

    left, right = st.columns([1, 2])

    # ---------------- LEFT COLUMN ---------------- #

    with left:

        if details["poster"]:
            st.image(
                details["poster"],
                use_container_width=True
            )

    # ---------------- RIGHT COLUMN ---------------- #

    with right:

        st.title(movie.get("title", "Unknown Movie"))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "⭐ Rating",
                movie.get("vote_average", "N/A")
            )

        with col2:
            st.metric(
                "🔥 Popularity",
                round(movie.get("popularity", 0), 1)
            )

        with col3:
            st.metric(
                "🗳 Votes",
                movie.get("vote_count", "N/A")
            )

        st.markdown("---")

        info1, info2 = st.columns(2)

        with info1:

            st.write("### 📅 Release Date")

            st.write(
                movie.get("release_date", "N/A")
            )

            runtime = movie.get("runtime")

            if runtime:
                st.write("### ⏱ Runtime")
                st.write(f"{runtime} Minutes")

            language = movie.get("original_language")

            if language:
                st.write("### 🌍 Language")
                st.write(language.upper())

        with info2:

            genres = movie.get("genres")

            if genres:

                st.subheader("🎭 Genres")

                genre_html = """
                <div style="
                    display:flex;
                    flex-wrap:wrap;
                    gap:10px;
                ">
                """

            for genre in genres:
                genre_html += f"""
                <span style="
                    background:#3A3A3A;
                    color:white;
                    padding:8px 14px;
                    border-radius:8px;
                    font-weight:bold;
                    white-space:nowrap;
                    display:inline-block;
                ">
                    {genre["name"]}
                </span>
                """

            genre_html += "</div>"

            st.markdown(genre_html, unsafe_allow_html=True)
            status = movie.get("status")

            if status:
                st.write("### 📀 Status")
                st.write(status)

            release = movie.get("release_date")

            if release:
                year = release[:4]
                st.write("### 🎬 Year")
                st.write(year)

        st.markdown("---")

        tmdb_id = details.get("tmdb_id")

        if tmdb_id:
            tmdb_id = int(tmdb_id)

            tmdb_url = f"https://www.themoviedb.org/movie/{tmdb_id}"

            st.link_button(
                "🌐 View on TMDb",
                tmdb_url,
                use_container_width=True
                )

        st.subheader("📝 Overview")

        overview = movie.get("overview")

        if overview:

            st.markdown(
                f"""
                <div style="
                    background:#262730;
                    color:#FFFFFF;
                    padding:20px;
                    border-radius:12px;
                    line-height:1.8;
                    font-size:17px;
                    text-align:justify;
                ">
                    <p style="
                        color:#FFFFFF;
                        margin:0;
                    ">
                        {overview}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.warning("Overview not available.")

        st.markdown("---")

        financial1, financial2 = st.columns(2)

        budget = movie.get("budget")

        revenue = movie.get("revenue")

        with financial1:

            if budget and budget > 0:

                st.metric(
                    "💰 Budget",
                    f"${budget:,.0f}"
                )

        with financial2:

            if revenue and revenue > 0:

                st.metric(
                    "💵 Revenue",
                    f"${revenue:,.0f}"
                )