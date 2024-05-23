<template>
  <div class="card mb-3 movie-card">
    <div class="row g-0">
      <div class="col-md-2 d-flex align-items-center justify-content-center">
        <img v-if="user.image" :src="API_URL + user.image" class="img-fluid rounded-circle fixed-size" alt="...">
        <img v-else src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDBJhKc_AmFlxPGktgktgKpzusO8p6mryOtw&s" class="img-fluid rounded-circle fixed-size" alt="...">
      </div>
      <div class="col-md-10">
        <div @click="showUserProfile(user)" class="card-body d-flex flex-column justify-content-between">
          <div>
            <h5 class="card-title">{{ user.username }}</h5>
            <p class="card-text" v-if="user.introduce"><small class="text-muted">{{ user.introduce }}</small></p>
            <p class="card-text" v-else>아직 등록한 소개가 없습니다.</p>
            <p class="card-text" v-if="user.mbti">{{ user.mbti }}</p>
            <p class="card-text" v-else>아직 mbti를 등록하지 않았습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import router from '@/router';
import { useAccountStore } from '@/stores/account';

const accountStore = useAccountStore()
const API_URL = accountStore.API_URL
const props = defineProps({
  user: Object
})

const showUserProfile = (user_id) => {
  router.push({ name: 'MyPageView', params: { id: props.user.id } });
};

</script>

<style scoped>
.card-body {
  display: flex;
  flex-direction: column;
  gap: 5px;
  height: 100%;
}

.fixed-size {
  width: 100px; /* 원하는 너비로 고정 */
  height: 100px; /* 원하는 높이로 고정 */
  object-fit: cover; /* 이미지 비율 유지하며 크기에 맞게 조절 */
}

.movie-card:hover {
  box-shadow: 0 8px 16px #D00448;
}
</style>
