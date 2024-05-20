import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const popularMovies = ref([])
  const latedMovies = ref([])
  const API_URL = import.meta.env.VITE_API_URL
  const USER_TOKEN = import.meta.env.VITE_USER_TOKEN
  
  const getPopularMovieList = function() {
    if (popularMovies.value.length == 0){
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/popular/`,
        headers: {
          Authorization: `Bearer ${USER_TOKEN}`
        }
      }).then((response) => {
        console.log(response);
        popularMovies.value = response.data
        console.log(popularMovies.value);
      }).catch((error) => {
        console.log(error);
      });
    }
  }
  
  const getLatedMovieList = function() {
    if (latedMovies.value.length == 0){
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/late_release/`,
        headers: {
          Authorization: `Bearer ${USER_TOKEN}`
        }
      }).then((response) => {
        console.log(response);
        latedMovies.value = response.data
        console.log(latedMovies.value);
      }).catch((error) => {
        console.log(error);
      });
    }
  }

  return { popularMovies, latedMovies, getPopularMovieList, getLatedMovieList, API_URL, USER_TOKEN }
})

