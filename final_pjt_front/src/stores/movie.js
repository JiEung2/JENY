import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useAccountStore } from './account';

export const useMovieStore = defineStore('movie', () => {
  const popularMovies = ref([]);
  const latedMovies = ref([]);
  const API_URL = import.meta.env.VITE_API_URL;
  const youtubeKey = import.meta.env.VITE_YOUTUBE_API_KEY;
  const youtubeSrcs = ref([]);

  const accountStore = useAccountStore();

  const getPopularMovieList = function () {
    if (popularMovies.value.length === 0) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/popular/`,
        headers: {
          Authorization: `Bearer ${accountStore.token}`
        }
      })
        .then(response => {
          console.log(response);
          popularMovies.value = response.data;
          console.log(popularMovies.value);
        })
        .catch(error => {
          console.log(error);
        });
    }
  };

  const getLatedMovieList = function () {
    if (latedMovies.value.length === 0) {
      console.log(1)
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/late_release/`,
        headers: {
          Authorization: `Bearer ${accountStore.token}`
        }
      })
        .then(response => {
          console.log(response);
          latedMovies.value = response.data;
          console.log(latedMovies.value);
        })
        .then(() => {
          console.log(2)
          latedMovies.value.forEach((movie, index) => {
            const movieName = `${movie.title} 공식 예고편`;
            axios({
              method: 'get',
              url: 'https://www.googleapis.com/youtube/v3/search',
              params: {
                part: 'snippet',
                maxResults: 1,
                q: movieName,
                type: 'video',
                key: youtubeKey
              }
            })
            .then((response) => {
              if (response.data.items.length > 0) {
                const youtubeId = response.data.items[0].id.videoId;
                const youtubeData = {
                  src: `https://www.youtube.com/embed/${youtubeId}`,
                  thumbnail: `https://img.youtube.com/vi/${youtubeId}/0.jpg`,
                  title: movie.title,
                  release_date: movie.release_date,
                  id: index
                };
                youtubeSrcs.value.push(youtubeData);
              } else {
                console.log(`No YouTube video found for ${movie.title}`);
              }
            })
            .catch((error) => {
              console.error(`Failed to fetch YouTube video for ${movie.title}:`, error);
            });
          });
        })
        .catch(error => {
          console.log(error);
        });
    }
  };

  return { popularMovies, latedMovies, getPopularMovieList, getLatedMovieList, API_URL, youtubeKey, youtubeSrcs };
}, { persist: true });
