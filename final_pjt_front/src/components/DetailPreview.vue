<template>
  <div>
    <iframe ref="iframe" id="ytplayer" type="text/html" width="1100" height="500" :src="autoplaySrc" frameborder="0" allow="autoplay" allowfullscreen></iframe>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue';

const props = defineProps({
  src: Object
});

const autoplaySrc = computed(() => {
  if (!props.src || !props.src.src) {
    return '';
  }
  return `${props.src.src}?autoplay=1`;
});
</script>

<style scoped>
</style>
