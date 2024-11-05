import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}?api_key=055634e334960f00e5f7fd1d3c4bb9a8&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']  # Corrected 'poster_path'


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))  # Fetch movie poster from API
    return recommended_movies, recommended_movies_posters


# Load movie data and similarity scores
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("FilmScout")
Selected_Movie_Name = st.selectbox("Choose a movie to get recommendations:", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(Selected_Movie_Name)
    col1, col2, col3, col4, col5 = st.columns(5)  # Updated to st.columns
    columns = [col1, col2, col3, col4, col5]

    for idx, col in enumerate(columns):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
