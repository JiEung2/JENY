<template>
  <div>
    <div class="card-body">
      <h5 class="text-light">{{ props.user.username }}</h5>
      <p v-if="props.user.introduce === ''"><small class="text-secondary">자기소개가 없습니다.</small></p>
      <p v-else><small class="text-secondary">간단한 소개: {{ props.user.introduce }}</small></p>

      <p class="card-text" v-if="props.user.mbti === ''"><small class="text-secondary">mbti가 존재하지 않습니다.</small></p>
      <p class="card-text" v-else><small class="text-secondary">mbti: {{ props.user.mbti }}</small></p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, onMounted, watch } from 'vue';
import { useAccountStore } from '@/stores/account';

const accountStore = useAccountStore();
const API_URL = accountStore.API_URL;

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
});

</script>

<style scoped>
.custom-card {
  background-color: #1c1c1e; /* 어두운 배경색 */
  border: none;
}

.text-light {
  color: #f5f5f5 !important;
}

.text-secondary {
  color: #a5a5a5 !important;
}

.follow-info {
  display: flex;
  gap: 5px; /* 요소 간의 간격 최소화 */
  padding-top: 1px; /* 이미지와 텍스트 사이의 간격 조절 */
}

.follow-info p {
  margin: 0;
}

.img-fluid {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
}

.card-body {
  font-size: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}
</style>
