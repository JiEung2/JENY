<template>
  <h5 class="title text-white text-center mt-4">선호하는 장르</h5>
  <div v-if="!hasError && defaultWords" >
    <vue-word-cloud
      style="height: 240px; width: 320px;"
      :words="defaultWords"
      :color="([, weight]) => {
        if (weight > 10) return '#FF6B6B';
        if (weight > 7) return '#4ECDC4';
        if (weight > 4) return '#ffA500';
        if (weight > 2) return '#ffC0CB';
        return '#E2F0CB';                 
      }"
      font-family="Roboto">
    </vue-word-cloud>
  </div>
  <div v-else>
    <p v-if="hasError">
      <div class="title text-white">아직 좋아하는 영화가 없습니다.</div>
    </p>
  </div>
</template>

<script setup>
import axios from 'axios';
import VueWordCloud from 'vuewordcloud';

import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useAccountStore } from '@/stores/account'
import { defineProps } from 'vue';

const accountStore = useAccountStore()
const route = useRoute()
const id = route.params.id

const hasError = ref(false);

const props = defineProps({
  id: {
    type: Number,
  },
  defaultWords: Array
})

</script>

<style scoped>

</style>
