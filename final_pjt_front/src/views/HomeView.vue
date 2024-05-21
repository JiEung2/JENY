<template>
  <CarouselView />
  <PopularMovieListView />
  <LatedMovieList />
  <PreviewView />
</template>

<script setup>
import PopularMovieListView from '@/views/PopularMovieListView.vue';
import LatedMovieList from '@/views/LatedMovieList.vue';
import CarouselView from '@/views/CarouselView.vue';
import PreviewView from '@/views/PreviewView.vue';
</script>