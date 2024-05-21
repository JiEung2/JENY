<template>
  <div>
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
import { useRoute, useRouter } from 'vue-router';
import { defineProps } from 'vue';
import { onMounted, ref } from 'vue';
import { useMovieStore } from '@/stores/counter';

const API_URL = import.meta.env.VITE_API_URL;
const USER_TOKEN = ref(import.meta.env.VITE_USER_TOKEN); // USER_TOKEN을 ref로 변경

const route = useRoute()
const movieStore = useMovieStore()
const movieDetail = ref([])
const movieComment = ref([])

const props = defineProps({
  id: {
    type: String,
  },
})

const id = route.params.id

axios({
    method: 'get',
    url: `${API_URL}/api/v1/movies/getMovieDetail/${id}`,
    headers: {
      Authorization: `Bearer ${USER_TOKEN.value}`
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
          Authorization: `Bearer ${USER_TOKEN.value}`
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

</style>