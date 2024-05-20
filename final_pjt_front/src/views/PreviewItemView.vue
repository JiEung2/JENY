<template>
  <div class="movie-card-wrapper">
    <div class="card h-100 movie-card no-border">
      <img v-if="src.thumbnail" :src="src.thumbnail" class="card-img-top" :data-bs-target="`#modal-${src.id}`" data-bs-toggle="modal">
      <div class="modal fade" :id="`modal-${src.id}`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl" style="max-width: 757px;">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="stopVideo"></button>
            </div>
            <div class="modal-body">
              <iframe ref="iframe" id="ytplayer" type="text/html" width="720" height="405" :src="src.src" frameborder="0" allowfullscreen></iframe>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';

const props = defineProps({
  src: Object
});

const iframe = ref(null);

const stopVideo = () => {
  iframe.value.src = '';
};

const resetVideoSrc = () => {
  iframe.value.src = props.src.src;
};

onMounted(() => {
  const modal = document.getElementById(`modal-${props.src.id}`);
  modal.addEventListener('hidden.bs.modal', resetVideoSrc);
});
</script>

<style scoped>
.movie-card {
  width: 200px; /* 카드의 가로 너비를 200px로 설정 */
}

.movie-card-wrapper {
  flex: 0 0 auto; /* 카드가 가로로 정렬되도록 설정 */
  padding: 0.5rem;
}

.card-img-top {
  width: 100%; /* 이미지가 카드 너비에 맞도록 조정 */
  height: 250px; /* 이미지 높이 자동 조정 */
}

.card-body {
  padding: 0.5rem; /* 카드 본문 패딩 조정 */
  background-color: transparent;
}

.card-title {
  font-size: 1rem; /* 제목 글꼴 크기 조정 */
  word-wrap: break-word; /* 긴 단어가 줄바꿈되도록 설정 */
  white-space: normal; /* 텍스트가 자동으로 줄바꿈되도록 설정 */
  overflow-wrap: anywhere; /* 긴 단어가 줄바꿈되도록 설정 (브라우저 지원이 더 좋은 속성) */
}

.card-text {
  font-size: 0.875rem; /* 본문 글꼴 크기 조정 */
}

/* 테두리 제거 스타일 */
.no-border {
  border: none; /* 테두리 제거 */
  box-shadow: none; /* 그림자 제거 */
}
</style>
