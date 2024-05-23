<template>
  <div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel">
    <div class="carousel-inner mt-2">
      <div class="carousel-item" :class="{ active: index === 0 }" v-for="(movie, index) in movieStore.popularMovies" :key="index">
        <img v-if="movie.poster_path" :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" class="d-block mx-auto carousel-img" :alt="movie.title">
      </div>
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import { onMounted } from 'vue';

const movieStore = useMovieStore();

onMounted(() => {
  movieStore.getPopularMovieList();
});
</script>

<style scoped>
.carousel-img {
  max-width: 80%; /* 이미지의 최대 너비를 설정하여 크기 조정 */
  height: 500px; /* 이미지 비율을 유지하면서 높이를 자동으로 설정 */
}
</style>
