import os
import pickle
import streamlit as st
import requests
import pandas as pd
from requests.exceptions import ReadTimeout

def fetch_poster(movie_id, retries=3):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=5)  # Set a timeout of 5 seconds
            if response.status_code == 200:
                data = response.json()
                poster_path = data['poster_path']
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                st.error(f"Failed to fetch poster for movie ID {movie_id}. HTTP Status Code: {response.status_code}")
                return None
        except ReadTimeout:
            st.warning(f"Timeout occurred while fetching poster for movie ID {movie_id}. Retrying...")
    st.error(f"Failed to fetch poster for movie ID {movie_id} after {retries} retries.")
    return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movie_posters.append(poster_url)
            recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

# Check if the file exists
movie_dict_path = 'F:/movie_recommender_system/movie_recommender/movies_dict.pkl'
similarity_path = 'F:/movie_recommender_system/movie_recommender/similarity.pkl'

movies = None  # Initialize movies to None
similarity = None  # Initialize similarity to None

if not os.path.exists(movie_dict_path):
    st.error(f"File not found: {movie_dict_path}")
else:
    movies = pickle.load(open(movie_dict_path, 'rb'))

if not os.path.exists(similarity_path):
    st.error(f"File not found: {similarity_path}")
else:
    similarity = pickle.load(open(similarity_path, 'rb'))

if movies is not None and isinstance(movies, dict):
    movies = pd.DataFrame(movies)

if movies is not None:
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Recommend'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
else:
    st.error("Movies data is not loaded correctly.")
