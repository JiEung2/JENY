<template>
  <div class="container">
    <DetailPreview :src="youtubeSrc"/>
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
const movieName = ref('')
const youtubeSrc = ref('')
const youtubeKey = import.meta.env.VITE_YOUTUBE_API_KEY
const props = defineProps({
  id: {
    type: String,
  },
})

axios({
    method: 'get',
    url: `${API_URL}/api/v1/movies/getMovieDetail/${id}`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
    .then(response => {
      movieDetail.value = response.data
      movieName.value = movieDetail.value[0].title + ' 공식 예고편'
      console.log(movieName.value)
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
    .then(response => {
      get_youtube_src()
    })
    .catch(error => {
      console.log(error)
    })

const get_youtube_src = function() {
  axios({
    method: 'get',
    url: 'https://www.googleapis.com/youtube/v3/search',
    params: {
      part: 'snippet',
      maxResults: 1,
      q: movieName.value,
      type: 'video',
      key: youtubeKey
    }
  })
  .then((response) => {
    if (response.data.items.length > 0) {
      console.log(response.data.items[0].id.videoId);
      const youtubeId = response.data.items[0].id.videoId;
      const youtubeData = {
        src: `https://www.youtube.com/embed/${youtubeId}`,
        thumbnail: `https://img.youtube.com/vi/${youtubeId}/0.jpg`,
        title: movieName.value,
      };
      youtubeSrc.value=youtubeData;
    } else {
      console.log(`No YouTube video found for ${movieName.value}`);
    }
  })
  .catch((error) => {
    console.error(`Failed to fetch YouTube video for ${movieName.value}:`, error);
  });
}

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
