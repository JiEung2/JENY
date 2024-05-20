<template>
  <div>
    <h4 class="header">최근 개봉작</h4>
  </div>
  <div class="carousel-container">
    <button class="scroll-button left" @click="scrollLeft">←</button>
    <div class="movie-container" ref="movieContainer">
      <div class="movie-row" ref="movieRow">
        <div class="movie-card-wrapper" v-for="movie in movieStore.latedMovies" :key="movie.id">
          <MovieItemView :movie="movie" />
        </div>
      </div>
    </div>
    <button class="scroll-button right" @click="scrollRight">→</button>
  </div>
</template>

<script setup>
import MovieItemView from '@/views/MovieItemView.vue';
import { useMovieStore } from '@/stores/counter';
import { onMounted, ref } from 'vue';

const movieStore = useMovieStore();
const movieContainer = ref(null);

onMounted(() => {
  movieStore.getLatedMovieList();
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
  margin: 0 50px; /* Add margin to make space for the buttons */
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

/* Scrollbar styling */
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

/* Button styling */
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
</style>
