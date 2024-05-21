import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useMovieStore = defineStore('movie', () => {
  const popularMovies = ref([]);
  const latedMovies = ref([]);
  const API_URL = import.meta.env.VITE_API_URL;
  const USER_TOKEN = ref(import.meta.env.VITE_USER_TOKEN); // USER_TOKEN을 ref로 변경
  const youtubeKey = import.meta.env.VITE_YOUTUBE_API_KEY;
  const youtubeSrcs = ref([]);
  const youtubeCache = new Map(); // 캐시 추가

  const signUp = function (payload) {
    const { username, password1, password2 } = payload;

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then(res => {
        console.log('회원가입 완료!');
      })
      .catch(err => console.log(err));
  };

  const logIn = function (payload) {
    const { username, password } = payload;

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        console.log('로그인이 완료!');
        console.log(res.data);
        // USER_TOKEN.value = res.data.token;
      })
      .catch(err => console.log(err));
  };

  const getPopularMovieList = function () {
    if (popularMovies.value.length === 0) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/popular/`,
        headers: {
          Authorization: `Bearer ${USER_TOKEN.value}`
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
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/late_release/`,
        headers: {
          Authorization: `Bearer ${USER_TOKEN.value}`
        }
      })
        .then(response => {
          console.log(response);
          latedMovies.value = response.data;
          console.log(latedMovies.value);
        })
        .catch(error => {
          console.log(error);
        });
    }
  };

  const getMovieDetail = function (id) {
    if (movieDetail.value.length === 0) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/getMovieDetail/${id}`,
        headers: {
          Authorization: `Bearer ${USER_TOKEN.value}`
        }
      })
        .then(response => {
          movieDetail.value = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  }

  return { popularMovies, latedMovies, getPopularMovieList, getLatedMovieList, getMovieDetail, signUp, logIn, API_URL, USER_TOKEN, youtubeKey, youtubeSrcs };
}, { persist: true });
