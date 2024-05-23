<template>
  <div class="container mt-4">
    <div class="card mb-3 custom-card" style="max-width: 100%;">
      <div class="row g-0 align-items-center">
        <div class="d-flex flex-column align-items-center mt-3">
          <img v-if="user.image" :src="API_URL + user.image" class="img-fluid rounded-circle" alt="...">
          <img v-else src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDBJhKc_AmFlxPGktgktgKpzusO8p6mryOtw&s" class="img-fluid rounded-circle" alt="...">
          <div class="follow-info mt-3 mb-3">
            <p><small class="text-light me-3 ms-2">팔로워 수: {{ user.followers }}</small></p>
            <p><small class="text-light">팔로잉 수: {{ user.followings }}</small></p>
          </div>
          <div class="follow-info mt-1 mb-3" v-if="me.username !== user.username">
            <button v-if="is_followed" @click="follow" class="btn btn-unfollow">팔로우 취소</button>
            <button v-else @click="follow" class="btn btn-follow me-2">팔로우</button>
          </div>
          <div class="align-items-center">
            <div v-if="me.username === user.username">
              <MyInfo :user="me" @profile-updated="handleProfileUpdated" :defaultWords="defaultWords"/>
            </div>
            <div v-else>
              <UserInfo :user="user" :defaultWords="defaultWords"/>
            </div>
          </div>
        </div>
      </div>
    </div>
    <br>

    <div class="container" v-if="me.username === user.username">
      <ThrowMovie /><br><br>
      <hr style="width: 100%; border: 1px solid white; margin: 20px 0;">
      <CatchedMovie /><br><br>
      <hr style="width: 100%; border: 1px solid white; margin: 20px 0;">
    </div>
    <div class="container">
      <LikedMovie :likedMovies="likedMovies"/>
    </div>
  </div>
</template>


<script setup>
import { defineProps, ref, onMounted } from 'vue';
import { useAccountStore } from '@/stores/account';
import axios from 'axios';
import ThrowMovie from '@/views/ThrowMovie.vue';
import CatchedMovie from '@/views/CatchedMovie.vue';
import LikedMovie from '@/views/LikedMovie.vue';
import MyInfo from '@/components/MyInfo.vue';
import UserInfo from '@/components/UserInfo.vue';

const accountStore = useAccountStore();
const API_URL = accountStore.API_URL;
const likedMovies = ref([]);
const is_followed = ref(false);
const defaultWords = ref([]);

const props = defineProps({
  id: {
    type: Number,
    required: true
  },
});

const me = ref({
  username: '',
  followings: 0,
  followers: 0,
  introduce: '',
  mbti: '',
  image: '',
});

const user = ref({
  id: '',
  username: '',
  followings: 0,
  followers: 0,
  introduce: '',
  mbti: '',
  image: '',
});

const getMyInfo = function() {
  axios({
    method: 'get',
    url: `${API_URL}/accounts/my_profile/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
  .then((response) => {
    const tmp_user = response.data;
    if (tmp_user) {
      me.value = {
        username: tmp_user.username,
        followings: tmp_user.followings_count,
        followers: tmp_user.followers_count,
        introduce: tmp_user.introduce,
        mbti: tmp_user.mbti,
        image: tmp_user.image,
      };
    }
  })
  .catch((error) => {
    console.error(error);
  });
};

const getUserInfo = function() {
  axios({
    method: 'get',
    url: `${API_URL}/accounts/user_profile/${props.id}/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
  .then((response) => {
    const tmp_user = response.data;
    if (tmp_user) {
      user.value = {
        id: tmp_user.id,
        username: tmp_user.username,
        followings: tmp_user.followings_count,
        followers: tmp_user.followers_count,
        introduce: tmp_user.introduce,
        mbti: tmp_user.mbti,
        image: tmp_user.image,
      };
    }
    get_is_followed();
  }).then((response) => {
    axios({
      method:'get',
      url: `${API_URL}/api/v1/get_liked_movies/${user.value.username}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      },
    }).then((response) =>{
      console.log(response);
      likedMovies.value = response.data;
      console.log(likedMovies.value);
    }).catch ((error)=> {
      console.log(error);
    });
  })
  .then((response) => {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/get_liked_genres/${user.value.id}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
    .then(res => {
      defaultWords.value = res.data;
      console.log(defaultWords.value)
      console.log(1)
    })
    .catch(err => {
      console.log(err);
      hasError.value = true;
    });
  })
  .catch((error) => {
    console.log(props.id);
    console.error(error);
  });
};

const get_is_followed = function() {
  axios({
    method: 'get',
    url: `${API_URL}/accounts/is_followed/${user.value.id}/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    },
  })
  .then((response) => {
    is_followed.value = response.data.is_followed;
    console.log(1)
    console.log(is_followed.value)
  })
  .catch((error) => {
    console.log(error);
  });
};

const follow = function() {
  axios({
    method: 'post',
    url: `${API_URL}/accounts/follow/${user.value.id}/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    },
  })
  .then((response) => {
    console.log('팔로우/팔로우 취소 완료');
    is_followed.value = !is_followed.value;
    getUserInfo();
  })
  .catch((error) => {
    console.log(error);
  });
};

const handleProfileUpdated = (updated_info) => {
  user.value = { ...user.value, ...updated_info };
  me.value = { ...me.value, ...updated_info };
};

onMounted(() => {
  getMyInfo();
  getUserInfo();
});
</script>

<style scoped>
.custom-card {
  background-color: #1c1c1e; /* 어두운 배경색 */
  border: none; /* 테두리 제거 */
}

.text-light {
  color: #f5f5f5 !important; /* 밝은 텍스트 색상 */
}

.text-secondary {
  color: #a5a5a5 !important; /* 보조 텍스트 색상 */
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
  width: 150px; /* 이미지 너비 고정 */
  height: 150px; /* 이미지 높이 고정 */
  object-fit: cover; /* 이미지가 컨테이너를 채우도록 */
  border-radius: 50%; /* 원형 이미지 */
}

.card-body {
  font-size: 16px; /* 텍스트 크기 고정 */
  display: flex;
  flex-direction: column;
  justify-content: center; /* 카드 바디를 세로 가운데 정렬 */
  height: 100%; /* 부모 요소의 높이를 100%로 설정 */
}

.form-control.bg-dark {
  background-color: #2c2c2e; /* 어두운 입력 필드 배경색 */
  border: 1px solid #3a3a3c; /* 입력 필드 테두리 색상 */
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
  color: #e50914 !important; /* 넷플릭스 스타일의 빨간색 오류 메시지 */
}

.btn-follow, .btn-unfollow {
  background-color: #444; /* 중간 정도 어두운 배경색 */
  border: none;
  color: #f5f5f5; /* 밝은 텍스트 색상 */
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  border-radius: 0.25rem;
  transition: background-color 0.3s;
}

.btn-follow:hover, .btn-unfollow:hover {
  background-color: #555; /* 호버 시 약간 더 밝은 배경색 */
}


</style>
