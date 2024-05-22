<template>
  <div v-if="!hasError && defaultWords.length > 0">
    <vue-word-cloud
      style="height: 480px; width: 640px;"
      :words="defaultWords"
      :color="([, weight]) => {
        if (weight > 450) return '#FF6B6B';
        if (weight > 300) return '#4ECDC4';
        if (weight > 150) return '#ffA500';
        if (weight > 100) return '#ffC0CB';
        if (weight > 50) return '#FF6B6B';
        return '#E2F0CB';                 
      }"
      font-family="Roboto">
    </vue-word-cloud>
  </div>
  <div v-else>
    <p v-if="hasError"></p>
  </div>
</template>

<script setup>
import axios from 'axios';
import VueWordCloud from 'vuewordcloud';

import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useAccountStore } from '@/stores/account'

// const USER_TOKEN = ref(import.meta.env.VITE_USER_TOKEN)
const accountStore = useAccountStore()
const route = useRoute()
const id = route.params.id

const defaultWords = ref([]);
const hasError = ref(false);

const getWordCloud = () => {
  axios({
    method: 'get',
    url: `http://127.0.0.1:8000/api/v1/movies/${id}/review/wordcloud/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
  .then(res => {
    defaultWords.value = res.data;
  })
  .catch(err => {
    console.log(err);
    hasError.value = true;
  });
};

onMounted(() => {
  getWordCloud();
});
</script>

<style scoped>

</style>
