<template>
  <div>
    <h4 class="header">나만의 추천 영화</h4>
  </div>
  <div class="carousel-container">
    <button class="scroll-button left" @click="scrollLeft">←</button>
    <div class="movie-container" ref="movieContainer">
      <div class="movie-row">
        <div
          @click="goToDetailPage(movie)" 
          class="movie-card-wrapper" 
          v-for="movie in recommended_movies" 
          :key="movie.id">
          <MovieItemView :movie="movie" />
        </div>
      </div>
    </div>
    <button class="scroll-button right" @click="scrollRight">→</button>
  </div>
</template>

<script setup>
import MovieItemView from '@/views/MovieItemView.vue';
import { useAccountStore } from '@/stores/account';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const accountStore = useAccountStore();
const movieContainer = ref(null);
const router = useRouter()
const API_URL = accountStore.API_URL
const recommended_movies = ref([])

const getRecommendationMovie = function (){
  axios({
    method: 'get',
    url: `${API_URL}/api/v1/movies/recommend/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
      }
    })
      .then(response => {
        console.log(response);
        recommended_movies.value = response.data;
        console.log(recommended_movies.value);
      })
      .catch(error => {
        console.log(error);
    });
}

onMounted(() => {
  getRecommendationMovie()
});

const scrollLeft = () => {
  movieContainer.value.scrollBy({
    left: -500,
    behavior: 'smooth',
  });
};

const scrollRight = () => {
  movieContainer.value.scrollBy({
    left: 500,
    behavior: 'smooth',
  });
};

const goToDetailPage = (movie) => {
  router.push({ 
    name: 'DetailView', 
    params: {
      id: movie.id,
    },
  })
}
</script>

<style scoped>
.header {
  margin-top: 20px;
  margin-left: 5rem; /* 오른쪽으로 더 이동하도록 마진 추가 */
  color: white; /* 글씨가 흐리지 않도록 검은색 지정 */
  font-family: "Noto Sans KR", sans-serif; /* 폰트 패밀리 설정 */
  font-weight: 600; /* 폰트 굵기 설정 */
}

.carousel-container {
  position: relative;
  display: flex;
  align-items: center;
}

.movie-container {
  overflow: hidden;
  overflow-x: auto;
  white-space: nowrap;
  padding: 1rem;
  margin: 0 50px; /* 버튼을 위한 공간 확보 */
}

.movie-row {
  display: flex;
}

.movie-card-wrapper {
  flex: 0 0 auto;
  margin-right: 1rem;
}

.movie-card {
  width: 250px;
  height: 375px; /* 영화 카드 높이 설정 */
}

/* 스크롤바 스타일링 */
.movie-container::-webkit-scrollbar {
  height: 10px;
}

.movie-container::-webkit-scrollbar-thumb {
  background-color: dimgrey;
  border-radius: 10px;
}

.movie-container::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}

.movie-container::-webkit-scrollbar-track {
  background: black;
}

/* 버튼 스타일링 */
.scroll-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 50px; /* 버튼 너비 */
  height: 375px; /* 영화 카드 높이와 맞추기 */
  cursor: pointer;
  z-index: 10;
  font-size: 1.5rem;
}

.scroll-button.left {
  left: 0;
}

.scroll-button.right {
  right: 0;
}

.scroll-button:hover {
  background-color: rgba(0, 0, 0, 0.7);
}

.movie-card-wrapper {
  flex: 0 0 auto;
  margin-right: 1rem;
  transition: transform 0.3s ease;
  cursor: pointer; /* 마우스를 클릭 가능한 포인터 모양으로 설정 */
}

.movie-card-wrapper:hover {
  transform: scale(1.05); /* 마우스 호버 시 크기 1.1배로 확대 */
}

</style>
