<template>
  <div v-if="showModal" class="modal fade show d-block" tabindex="-1" role="dialog" aria-hidden="true" style="background-color: rgba(0,0,0, 0.5);">
    <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content" style="background-color: rgba(0,0,0, 0.8);">
        <div class="modal-header" style="border-bottom: none; position: relative;">
          <h5 class="modal-title text-white" style="width: 100%;">당신의 취향인 영화를 선택해주세요</h5>
          <button type="button" class="close text-white" aria-label="Close" @click="closeModal" style="background-color: rgba(0,0,0,0.8); position: absolute; top: 15px; right: 15px;">
            <span aria-hidden="true">&times;</span>
          </button>
          <div class="text-white" style="position: absolute; top: 15px; left: 50%; transform: translateX(-50%);">
            {{ selectedMovies.length }} / 10
          </div>
        </div>
        <div class="modal-body">
          <div class="container">
            <div class="row">
              <div v-for="movie in movies" :key="movie.id" class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
                <div class="card movie-card" :class="{ 'border-success selected': selectedMovies.includes(movie) }" @click="toggleSelectMovie(movie)" style="background-color: rgba(255, 255, 255, 0.1);">
                  <img v-if="movie.poster_path" :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" class="card-img-top" :alt="movie.title">
                  <div class="card-body" style="background-color: rgba(0, 0, 0, 0.1);">
                    <p class="card-title text-white"><b>{{ movie.title }}</b></p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="fixed-bottom d-flex justify-content-between p-3">
          <button type="button" class="btn btn-secondary mr-2" @click="closeModal">Close</button>
          <button type="button" class="btn btn-primary" @click="confirmSelection">Confirm</button>
          <button type="button" class="btn btn-link text-white" @click="noSee">일주일동안 보지 않음</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useAccountStore } from '@/stores/account';

export default {
  props: {
    movies: Array,
    showModal: Boolean,
  },
  data() {
    return {
      selectedMovies: [],
    };
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    toggleSelectMovie(movie) {
      if (this.selectedMovies.includes(movie)) {
        this.selectedMovies = this.selectedMovies.filter(selected => selected !== movie);
      } else if (this.selectedMovies.length < 10) {
        this.selectedMovies.push(movie);
      }
    },
    confirmSelection() {
      this.$emit('confirm', this.selectedMovies);
      this.selectedMovies = [];
    },
    async noSee() {
      const accountStore = useAccountStore();
      const API_URL = accountStore.API_URL;
      try {
        await axios.get(`${API_URL}/api/v1/movies/popular_many/no_see/`, {
          headers: {
            Authorization: `Token ${accountStore.token}`
          }
        });
        this.closeModal();
      } catch (error) {
        console.error(error);
      }
    }
  },
};
</script>

<style>
.modal-backdrop {
  display: none;
}

.fixed-bottom {
  position: fixed;
  bottom: 0;
  right: 0;
  width: auto;
  background-color: rgba(0, 0, 0, 0.8); /* To make sure buttons are visible */
}

.close {
  background-color: rgba(0, 0, 0, 0.8);
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.5rem;
  line-height: 1;
  padding: 0.5rem 0.75rem;
}

.movie-card {
  transition: transform 0.3s;
}

.movie-card.selected {
  transform: scale(1.05);
}
</style>
