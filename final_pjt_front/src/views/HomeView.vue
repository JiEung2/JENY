<template>
  <CarouselView />
  <RecommendationMovieList />
  <PopularMovieListView />
  <LatedMovieList />
  <PreviewView />
  <LikeModal 
    v-if="showModal" 
    :movies="movies" 
    :showModal="showModal" 
    @close="showModal = false" 
    @confirm="handleConfirm" 
  />
</template>

<script setup>
import PopularMovieListView from '@/views/PopularMovieListView.vue';
import LatedMovieList from '@/views/LatedMovieList.vue';
import CarouselView from '@/views/CarouselView.vue';
import PreviewView from '@/views/PreviewView.vue';
import LikeModal from '@/components/LikeModal.vue';
import RecommendationMovieList from '@/components/RecommendationMovieList.vue';
import { useAccountStore } from '@/stores/account';
import axios from 'axios';
import { ref, onMounted } from 'vue';

const accountStore = useAccountStore()
const API_URL = accountStore.API_URL
const showModal = ref(false);
const movies = ref([]);

onMounted(() =>{
  get_popular_movies();
});

const get_popular_movies = function() {
  axios({
    method: 'get',
    url: `${API_URL}/api/v1/movies/popular_many/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
    .then((response) => {
      movies.value = response.data
      if(movies.value){
        showModal.value = true;
      }
    })
    .catch((error)=>{
      console.log(error)
    })
}

const handleConfirm = (selectedMovies) => {
  const movieIds = selectedMovies.map(movie => movie.id);
  axios({
    method: 'post',
    url: `${API_URL}/api/v1/movies/like_movies/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    },
    data: { movies: movieIds }
  })
    .then(() => {
      showModal.value = false;
    })
    .catch((error) => {
      console.error(error);
    });
};

</script>