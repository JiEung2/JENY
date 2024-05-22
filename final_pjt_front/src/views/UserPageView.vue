<template>
  <div class="container mt-4">
    <div class="card mb-3 custom-card" style="max-width: 100%;">
      <div class="row g-0 align-items-center">
        <div class="col-md-2 d-flex flex-column align-items-center mt-3">
          <img v-if="user.image" :src="'http://127.0.0.1:8000' + user.image" class="img-fluid rounded-circle" alt="...">
          <img v-else src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDBJhKc_AmFlxPGktgktgKpzusO8p6mryOtw&s" class="img-fluid rounded-circle" alt="...">
          <div class="follow-info mt-3 mb-3">
            <p><small class="text-light me-3 ms-2">팔로워 수: {{ user.followers }}</small></p>
            <p><small class="text-light">팔로잉 수: {{ user.followings }}</small></p>
          </div>
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="text-light">{{ user.username }}</h5>
            <p v-if="user.introduce === ''"><small class="text-secondary">자기소개가 없습니다.</small></p>
            <p v-else><small class="text-secondary">간단한 소개: {{ user.introduce }}</small></p>

            <p class="card-text" v-if="user.mbti === ''"><small class="text-secondary">mbti가 존재하지 않습니다.</small></p>
            <p class="card-text" v-else><small class="text-secondary">mbti: {{ user.mbti }}</small></p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="container">
    <ThrowMovie />
    <CatchedMovie />
    <LikedMovie />
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/account'
import axios from 'axios';
import ThrowMovie from '@/views/ThrowMovie.vue';
import CatchedMovie from '@/views/CatchedMovie.vue';
import LikedMovie from '@/views/LikedMovie.vue'

const accountStore = useAccountStore()
const API_URL = accountStore.API_URL

const user = ref({
  username: '',
  followings: 0,
  followers: 0,
  introduce: '',
  mbti: '',
  image: '',
})

const getUserInfo = function() {
  axios({
    method:'get',
    url: `${API_URL}/accounts/user_profile/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
  .then((response) => {
    const tmp_user = response.data;
    if(tmp_user) {
      user.value = {
        username: tmp_user.username,
        followings: tmp_user.followings_count,
        followers: tmp_user.followers_count,
        introduce: tmp_user.introduce,
        mbti: tmp_user.mbti,
        image: tmp_user.image,
      }
    }
  })
  .catch((error) => {
    console.error(error)
  })
}

onMounted(() => {
  getUserInfo()
})
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

.form-control.bg-dark {
  background-color: #2c2c2e;
  border: 1px solid #3a3a3c; 
}

.btn-outline-light {
  color: #f5f5f5;
  border-color: #f5f5f5;
}

.btn-outline-light:hover {
  background-color: #f5f5f5;
  color: #1c1c1e;
}

.btn-primary {
  background-color: #e50914;
  border: none;
}

.btn-primary:hover {
  background-color: #f40612;
}

.text-danger {
  color: #e50914 !important; 
}
</style>
