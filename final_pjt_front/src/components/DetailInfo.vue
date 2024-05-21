<template>
  <div>
    <h1>DetailInfo</h1>
    <img :src="'https://image.tmdb.org/t/p/w500' + movieDetail[0].poster_path" alt="movie_poster">
    <h2>{{ movieDetail[0].title }}</h2>
    <p>줄거리 : {{ movieDetail[0].overview }}</p>
    <p>개봉일 : {{ movieDetail[0].release_data }}</p>
    <p>평점 : {{ movieDetail[0].vote_average }}</p>
    <p>장르 : {{ movieDetail[0].genre }}</p>
    <br>
    <br>
    <br>
    <h3>댓글</h3>
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
  }
})



</script>

<style scoped>

</style>