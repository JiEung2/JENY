<template>
  <div class="movie-card-wrapper">
    <div class="card h-100 movie-card no-border">
      <img v-if="movie.poster_path" :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" class="card-img-top" :alt="movie.title">
      <div class="card-body" style="background-color: rgba(0, 0, 0, 1);">
        <p class="card-title text-white"><b>{{ movie.title }}</b></p>
        <p class="card-text text-white">{{ movie.release_data }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
defineProps({
  movie: Object
})

const router = useRouter()
// const goDetailPage = function(movieId){
//   router.push(`/${movieId}`)
// }
</script>

<style scoped>
.movie-card {
  width: 150px; /* 카드의 가로 너비를 150px로 설정 */
}

.movie-card-wrapper {
  flex: 0 0 auto; /* 카드가 가로로 정렬되도록 설정 */
  padding: 0.5rem;
}

.card-img-top {
  width: 100%; /* 이미지가 카드 너비에 맞도록 조정 */
  height: 220px; /* 이미지 높이 자동 조정 */
}

.card-body {
  padding: 0.5rem; /* 카드 본문 패딩 조정 */
  background-color: transparent;
}

.card-title {
  font-size: 1rem; /* 제목 글꼴 크기 조정 */
  word-wrap: break-word; /* 긴 단어가 줄바꿈되도록 설정 */
  white-space: normal; /* 텍스트가 자동으로 줄바꿈되도록 설정 */
  overflow-wrap: anywhere; /* 긴 단어가 줄바꿈되도록 설정 (브라우저 지원이 더 좋은 속성) */
}

.card-text {
  font-size: 0.875rem; /* 본문 글꼴 크기 조정 */
}

/* 테두리 제거 스타일 */
.no-border {
  border: none; /* 테두리 제거 */
  box-shadow: none; /* 그림자 제거 */
}
</style>
