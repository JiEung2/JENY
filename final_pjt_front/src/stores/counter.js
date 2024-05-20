import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const popularMovies = ref([])
  const TMDB_TOKEN = import.meta.env.VITE_TMDB_TOKEN
  
  const getPopularMovieList = function() {
    if (popularMovies.value.length == 0){
      axios({
        method: 'get',
        url: 'https://api.themoviedb.org/3/movie/popular?language=ko&page=1',
        headers: {
          accept: 'application/json',
          Authorization: `Bearer ${TMDB_TOKEN}`
        }
      }).then((response) => {
        // console.log(response.data);
        popularMovies.value = response.data.results
      }).catch((error) => {
        console.log(error);
      });
    }
  }
  
  return { popularMovies, getPopularMovieList }
})

