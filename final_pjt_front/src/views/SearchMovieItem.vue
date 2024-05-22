<template>
  <div class="card mb-3 movie-card">
    <div class="row g-0">
      <div class="col-md-2 d-flex align-items-center">
        <img v-if="movie.poster_path" :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" class="img-fluid rounded-start movie-poster" :alt="movie.title">
      </div>
      <div class="col-md-10">
        <div @click="goToDetailPage(movie)" class="card-body d-flex flex-column justify-content-between">
          <div>
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text"><small class="text-muted">{{ movie.release_data }}</small></p>
            <p class="card-text"><small class="text-muted"><img class="star-icon" src="@/assets/star-icon.png" alt="">{{ movie.vote_average }}</small></p>
          </div>
          <p class="card-text overview"><small class="text-muted">{{ movie.overview }}</small></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import router from '@/router';

const props = defineProps({
  movie: Object
})

const goToDetailPage = (movie) => {
  router.push({ 
    name: 'DetailView', 
    params: {
      id: movie.id,
    },
  })
}
</script>

<style scoped>
.card-body {
  display: flex;
  flex-direction: column;
  gap: 5px;
  height: 100%;
}

.star-icon {
  width: 15px;
  height: auto;
  margin-right: 5px;
}

.overview {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2; /* 두 줄로 제한 */
  overflow: hidden;
  text-overflow: ellipsis;
}

.movie-poster {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.movie-card {
  max-width: 100%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease-in-out;
}

.movie-card:hover {
  box-shadow: 0 8px 16px #D00448;
}
</style>