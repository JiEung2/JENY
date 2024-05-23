<template>
  <div class="search-container">
    <form class="d-flex search-form" role="search" @submit.prevent="performSearch">
      <select v-model="searchType" class="form-select search-select">
        <option value="movie">영화</option>
        <option value="user">유저</option>
      </select>
      <input
        v-model="query"
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
    <SearchMovieItem v-if="searchType === 'movie'" v-for="movie in results" :key="movie.id" :movie="movie" />
    <SearchUserItem v-if="searchType === 'user'" v-for="user in results" :key="user.id" :user="user" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import SearchMovieItem from '@/components/SearchMovieItem.vue'
import { useAccountStore } from '@/stores/account';
import SearchUserItem from '@/components/SearchUserItem.vue'

const query = ref('')
const results = ref([])
const searchType = ref('movie') // 기본 검색 타입을 영화로 설정
const accountStore = useAccountStore()
const USER_TOKEN = accountStore.token
const API_URL = accountStore.API_URL

const search_movie = function() {
  const url = `${API_URL}/api/v1/movies/${encodeURIComponent(query.value)}/`
  axios({
    method: 'get',
    url: url,
    headers: {
      Authorization: `Token ${USER_TOKEN}`
    }
  })
  .then(response => {
    results.value = response.data
  })
  .catch(error => {
    console.error(error)
  })
}

const search_user = function() {
  const url = `${API_URL}/accounts/search_user/${encodeURIComponent(query.value)}/`
  axios({
    method: 'get',
    url: url,
    headers: {
      Authorization: `Token ${USER_TOKEN}`
    }
  })
  .then(response => {
    results.value = response.data
    console.log(results.value)
  })
  .catch(error => {
    console.error(error)
  })
}

const performSearch = function() {
  if (searchType.value === 'movie') {
    search_movie()
  } else if (searchType.value === 'user') {
    search_user()
  }
}

const clearSearch = function() {
  query.value = ''
  results.value = []
}

const handleInput = function() {
  if (query.value === '') {
    clearSearch()
  }
}

// watch 함수를 사용하여 searchType이 변경될 때 results를 초기화
watch(searchType, () => {
  clearSearch()
})
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

.search-select {
  border: none;
  border-radius: 30px 0 0 30px;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
}

.search-input {
  flex-grow: 1;
  border: none;
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
