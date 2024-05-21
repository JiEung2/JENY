<template>
  <div>
    <h4 class="header">예고편</h4>
  </div>
  <div class="carousel-container">
    <button class="scroll-button left" @click="scrollLeft">←</button>
    <div class="movie-container" ref="movieContainer">
      <div class="movie-row" ref="movieRow">
        <div class="movie-card-wrapper" v-for="src in movieStore.youtubeSrcs" :key="src.src">
          <PreviewItemView :src="src" />
        </div>
      </div>
    </div>
    <button class="scroll-button right" @click="scrollRight">→</button>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/counter';
import { onMounted, ref } from 'vue';
import PreviewItemView from './PreviewItemView.vue';

const movieStore = useMovieStore();
const movieContainer = ref(null);

const scrollLeft = () => {
  movieContainer.value.scrollBy({
    left: -500,
    behavior: 'smooth',
  });
};

const scrollRight = () => {
  movieContainer.value.scrollBy({
    left: 500,
    behavior: 'smooth',
  });
};
</script>

<style scoped>
.header {
  margin-top: 20px;
  margin-left: 5rem;
  color: white;
  font-family: "Noto Sans KR", sans-serif;
  font-weight: 600;
}

.carousel-container {
  position: relative;
  display: flex;
  align-items: center;
}

.movie-container {
  overflow: hidden;
  overflow-x: auto;
  white-space: nowrap;
  padding: 1rem;
  margin: 0 50px;
}

.movie-row {
  display: flex;
}

.movie-card-wrapper {
  flex: 0 0 auto;
  margin-right: 1rem;
}

.movie-card {
  width: 250px;
  height: 375px;
}

.movie-container::-webkit-scrollbar {
  height: 10px;
}

.movie-container::-webkit-scrollbar-thumb {
  background-color: dimgrey;
  border-radius: 10px;
}

.movie-container::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}

.movie-container::-webkit-scrollbar-track {
  background: black;
}

.scroll-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 50px;
  height: 250px;
  cursor: pointer;
  z-index: 10;
  font-size: 1.5rem;
}

.scroll-button.left {
  left: 0;
}

.scroll-button.right {
  right: 0;
}

.scroll-button:hover {
  background-color: rgba(0, 0, 0, 0.7);
}
</style>
