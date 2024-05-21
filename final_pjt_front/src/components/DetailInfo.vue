<template>
  <div class="movie-info">
    <h1>영화 상세정보</h1>
    <br>
    <img class="movie-poster" :src="'https://image.tmdb.org/t/p/w500' + movieDetail[0].poster_path" alt="movie_poster">
    <div class="button-container">
      <img src="@/assets/dislike.png" alt="dislike" style="width: 50px;">
      <img src="@/assets/like.png" alt="like" style="width: 50px;">
      <img src="@/assets/throw.png" alt="throw" style="width: 50px;"><br><br>
    </div>
    <div class="movie-details">
      <h2>{{ movieDetail[0].title }}</h2><br>
      <p v-if="movieDetail[0].overview" class="movie-summary">{{ movieDetail[0].overview }}</p>
      <p v-else class="movie-summary">등록된 줄거리가 없습니다.</p>
      <br>
      <p>장르 : {{ movieDetail[0].genre }}</p><br>
      <p>평점 : {{ movieDetail[0].vote_average }}</p><br>
      <p>개봉일 : {{ movieDetail[0].release_data }}</p><br>
    </div>
    <br>
    <br>
    <br>
    <h3>리뷰</h3>
    <div v-for="(comment, index) in movieComment">
      {{ index + 1 }}. {{ comment.content }}
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  id: {
    type: String,
  },
  movieDetail: {
    type: Object,
  },
  movieComment: {
    type: Object,
  },
});
</script>

<style scoped>
.movie-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #1e1e1e;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: auto; /* Adjust width as needed */
  margin: 0 auto; /* 좌우 여백 자동 설정으로 가운데 정렬 */
}


.movie-poster {
  width: 400px; /* Adjust width based on your poster size */
  margin-bottom: 20px;
}

.movie-summary {
  padding: 0 20px; /* 좌우 20px의 안쪽 여백 적용 */
  text-align: center; /* 텍스트를 가운데 정렬 */
  margin: 0 auto; /* 가운데 정렬을 위해 좌우 여백을 자동 설정 */
}



.button-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  width: 100%;
  margin-bottom: 20px;
}

.movie-details {
  display: flex;
  flex-direction: column;
  width: 100%; /* Expands to fill remaining space */
}

.movie-details p {
  margin: 5px 20px; /* Adjust left and right margin as needed */
}
</style>
