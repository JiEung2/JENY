<template>
  <div class="search-container">
    <form class="d-flex search-form" role="search" @submit.prevent="search_movie">
      <input
        v-model="movieName"
        class="form-control me-2 search-input"
        type="search"
        placeholder="검색어 입력"
        aria-label="Search"
        @input="handleInput"
      >
      <button class="btn btn-custom search-button" type="submit">Search</button>
    </form>
  </div>
  <div class="container mt-3">
    <SearchMovieItem v-for="movie in movies" :key="movie.id" :movie="movie" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import SearchMovieItem from '@/views/SearchMovieItem.vue'
import { useAccountStore } from '@/stores/account';

const movieName = ref('')
const movies = ref([])
const accountStore = useAccountStore()
const USER_TOKEN = accountStore.token

const search_movie = function() {
  const url = `http://127.0.0.1:8000/api/v1/movies/${encodeURIComponent(movieName.value)}`
  axios({
    method: 'get',
    url: url,
    headers: {
      Authorization: `Token ${USER_TOKEN}`
    }
  })
  .then(response => {
    movies.value = response.data
  })
  .catch(error => {
    console.error(error)
  })
}

const clearSearch = function() {
  movieName.value = ''
  movies.value = []
}

const handleInput = function() {
  if (movieName.value === '') {
    clearSearch()
  }
}
</script>

<style scoped>
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
  margin-top: 100px;
}

.search-form {
  width: 100%;
  max-width: 600px;
  background: #fff;
  border-radius: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;
}

.search-input {
  flex-grow: 1;
  border: none;
  border-radius: 30px 0 0 30px;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
}

.search-input:focus {
  outline: none;
  box-shadow: none;
}

.search-button {
  background-color: #F60556;
  color: white;
  border: none;
  border-radius: 0 30px 30px 0;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #D00448;
  color: #F0F0F0;
}
</style>
