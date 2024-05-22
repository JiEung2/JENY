<template>
  <div class="container">
    <DetailPreview />
    <br>
    <br>
    <DetailInfo :id="id" :movieDetail="movieDetail" :movieComment="movieComment"/>
  </div>

</template>


<script setup>
import DetailPreview from '@/components/DetailPreview.vue'
import DetailInfo from '@/components/DetailInfo.vue'
import axios from 'axios';

import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { defineProps } from 'vue';
import { useAccountStore } from '@/stores/account';

const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_API_URL
const USER_TOKEN = accountStore.token

const route = useRoute()
const movieDetail = ref([])
const movieComment = ref([])
const id = route.params.id

const props = defineProps({
  id: {
    type: String,
  },
})

axios({
    method: 'get',
    url: `${API_URL}/api/v1/movies/getMovieDetail/${id}`,
    headers: {
      Authorization: `Token ${USER_TOKEN}`
    }
  })
    .then(response => {
      movieDetail.value = response.data
    })
    .then(response => {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/${id}/comments/`,
        headers: {
          Authorization: `Token ${USER_TOKEN}`
        }
      })
        .then(response => {
          movieComment.value = response.data
        })
        .catch(error => {
          console.log(error)
        })
    })
    .catch(error => {
      console.log(error)
    })


</script>


<style scoped>
.container {
  text-align: center;
  color: white;
  background-color: #121212;
  padding: 20px;
}

.container .movie-poster {
  display: block;
  margin: 0 auto;
}

.container h1, .container h2, .container p {
  color: white;
}

.container h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
}

.container h2 {
  font-size: 2em;
  margin-bottom: 15px;
}

.container p {
  font-size: 1.2em;
  line-height: 1.6;
}

.container .movie-info {
  background-color: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.container .movie-comments {
  margin-top: 30px;
  padding: 20px;
  background-color: #1e1e1e;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
