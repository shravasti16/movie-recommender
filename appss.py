import streamlit as st
import pickle
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Movie Recommender", layout="wide")

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #ff4b4b;
    margin-bottom: 10px;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #aaa;
    margin-bottom: 30px;
}
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 200px;
    font-size: 18px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #ff1c1c;
}
.movie-card {
    text-align: center;
    padding: 10px;
    border-radius: 15px;
    background-color: #161b22;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# ---------------- FETCH POSTER ---------------- #

API_KEY = "YOUR_API_KEY"


def fetch_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d62052c613279e83d79b827fce21d76e"
        data = requests.get(url, timeout=10, verify=False).json()

        poster_path = data.get('poster_path')
        rating = data.get('vote_average')

        # Poster
        if poster_path and poster_path != "":
            poster = "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            poster = "https://via.placeholder.com/500x750?text=No+Poster"

        # Rating
        if rating:
            rating = round(rating, 1)
        else:
            rating = "N/A"

        return poster, rating

    except:
        return "https://via.placeholder.com/500x750?text=Error", "N/A"


# ---------------- RECOMMEND ---------------- #
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,
                         key=lambda x: x[1])[1:6]

    names = []
    posters = []
    ratings = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        poster, rating = fetch_details(movie_id)

        names.append(movies.iloc[i[0]].title)
        posters.append(poster)
        ratings.append(rating)

        time.sleep(0.3)  # 👈 IMPORTANT FIX

    return names, posters, ratings


# ---------------- LOAD DATA ---------------- #
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------- UI ---------------- #
st.markdown('<div class="title">🎬 Movie Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find movies similar to your favorites 🍿</div>', unsafe_allow_html=True)

selected_movie = st.selectbox(
    "🔍 Choose a movie",
    movies['title'].values
)

# Center button
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    clicked = st.button("✨ Recommend")

# ---------------- RESULTS ---------------- #
if clicked:
    names, posters, ratings = recommend(selected_movie)

    st.markdown("## 🍿 Recommended for you")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(posters[i])
            st.markdown(f"**{names[i]}**")
            st.markdown(f"⭐ Rating: {ratings[i]}")
            st.markdown('</div>', unsafe_allow_html=True)

