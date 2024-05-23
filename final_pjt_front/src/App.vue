<template>
  <div>
    <nav class="navbar navbar-expand bg-body-tertiary bg-dark border-bottom" data-bs-theme="dark">
      <div class="container-fluid">
        <RouterLink to="/"><img src="@/assets/logo.png" alt="Logo" width="70" height="27" class="d-inline-block align-text-top"></RouterLink>
        <div class="collapse navbar-collapse d-flex justify-content-end align-items-center" id="navbarNav">
          <ul class="navbar-nav ms-auto d-flex align-items-center">
            <li class="nav-item ms-3">
              <RouterLink to="/" class="link text-white"><img src="@/assets/bell.png" alt="bell" height="27"></RouterLink>
            </li>
            <li class="nav-item ms-3">
              <RouterLink :to="{ name: 'SearchView' }" class="link text-white">검색</RouterLink>
            </li>
            <li class="nav-item ms-3" v-if="!accountStore.isLogin">
              <RouterLink :to="{ name: 'login' }" class="link text-white">로그인</RouterLink>
            </li>
            <li class="nav-item ms-3" v-if="!accountStore.isLogin">
              <RouterLink :to="{ name: 'signup' }" class="link text-white"><button type="button" class="btn btn-danger">회원가입</button></RouterLink>
            </li>
            <li class="nav-item ms-3" v-if="accountStore.isLogin">
              <button class="btn btn-link custom-link-btn" @click="goToMyPage">마이페이지</button>
            </li>
            <li class="nav-item ms-3" v-if="accountStore.isLogin">
              <button type="button" class="btn btn-danger" @click="logout">로그아웃</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <RouterView />
    <div v-if="showModal" class="modal fade custom-animation show fireworks" tabindex="-1" role="dialog" style="display: block;">
      <div class="modal-dialog modal-dialog-centered custom-modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modalData.message }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body d-flex justify-content-center align-items-center">
            <div class="card mb-3" style="max-width: 540px;">
              <div class="row g-0">
                <div class="col-md-4">
                  <img v-if="modalData.poster_path" :src="'https://image.tmdb.org/t/p/w500' + modalData.poster_path" class="img-fluid rounded-start movie-poster" :alt="modalData.title">
                </div>
                <div class="col-md-8">
                  <div class="card-body">
                    <h5 class="card-title">{{ modalData.title }}</h5>
                    <p class="card-text"><small class="text-muted">{{ modalData.release_data }}</small></p>
                    <p class="card-text"><small class="text-muted"><img class="star-icon" src="@/assets/star-icon.png" alt="">{{ modalData.vote_average }}</small></p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAccountStore } from '@/stores/account';
import { onMounted, ref } from 'vue';
import { useMovieStore } from '@/stores/counter';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter()
const movieStore = useMovieStore()
const accountStore = useAccountStore()

const showModal = ref(false)
const me = ref({
  id: '',
  username: '',
  followings: 0,
  followers: 0,
  introduce: '',
  mbti: '',
  image: '',
})
const modalData = ref({
  title: '',
  message: '',
  from_user: '',
  to_user: '',
  release_data: '',
  vote_average: '',
  poster_path: ''
})

const API_URL = accountStore.API_URL

const logout = async () => {
  try {
    await axios.post(`${API_URL}/accounts/logout/`, {}, {
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    });
    accountStore.logout();
    router.push({ name: 'home' });
  } catch (err) {
    console.log(err);
  }
}

const closeModal = () => {
  showModal.value = false;
}

const fetchThrownMovies = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/v1/thrown_movies/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    });
    const thrownMovie = response.data;
    if (thrownMovie) {
      const ThrownMovie = thrownMovie;
      modalData.value = {
        title: ThrownMovie.movie.title,
        message: `${ThrownMovie.from_user.username}님이 당신에게 '${ThrownMovie.movie.title}'를 던졌습니다.`,
        from_user: ThrownMovie.from_user.username,
        to_user: ThrownMovie.to_user.username,
        release_data: ThrownMovie.movie.release_data,
        vote_average: ThrownMovie.movie.vote_average,
        poster_path: ThrownMovie.movie.poster_path
      };
      showModal.value = true;
    }
  } catch (error) {
    console.error(error);
  }
}

const goToMyPage = () => {
  axios({
    method:'get',
    url: `${API_URL}/accounts/my_profile/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
  .then((response) => {
    const tmp_user = response.data;
    if(tmp_user) {
      me.value = {
        id: tmp_user.id, 
        username: tmp_user.username,
        followings: tmp_user.followings_count,
        followers: tmp_user.followers_count,
        introduce: tmp_user.introduce,
        mbti: tmp_user.mbti,
        image: tmp_user.image,
      }
    }
  })
  .then(() => {
    router.push({ 
    name: 'MyPageView', 
    params: {
      id: me.value.id,
    },
  })
  })
  .catch((error) => {
    console.error(error)
  })
}

const generateRandomStyle = () => {
  const size = `${Math.random() * 50 + 20}px`;
  const top = `${Math.random() * 100}vh`;
  const left = `${Math.random() * 100}vw`;
  const animationDelay = `${Math.random()}s`;
  const animationDuration = `${Math.random() * 0.5 + 1}s`;
  const colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#FF3387'];
  const backgroundColor = colors[Math.floor(Math.random() * colors.length)];
  return {
    width: size,
    height: size,
    top: top,
    left: left,
    backgroundColor: backgroundColor,
    animationDelay: animationDelay,
    animationDuration: animationDuration
  };
}

onMounted(() => {
  movieStore.getLatedMovieList();
  setInterval(fetchThrownMovies, 10000); // 20초마다 요청
});
</script>

<style scoped>
body {
  background-color: #000;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  font-family: 'YeongdeokSea';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2307-1@1.1/YeongdeokSea.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
  background-color: #141517 !important;
}

.link {
  text-decoration: none;
}

.star-icon {
  width: 15px;
  height: auto;
  margin-right: 5px;
}

.custom-modal-dialog {
  max-width: 600px; /* 모달의 최대 너비 조정 */
}

.modal-body {
  display: flex;
  justify-content: center;
  align-items: center;
}



.custom-link-btn {
    text-decoration: none; /* 밑줄 제거 */
    color: white; /* 기본 텍스트 색상 사용 */
    padding: 0; /* 기본 패딩 제거 */
    background: none; /* 배경색 제거 */
    border: none; /* 테두리 제거 */
}
.custom-link-btn:hover {
    text-decoration: none; /* 호버 시에도 밑줄 제거 */
}
/* .modal {
  animation:ball 1s ease-in Infinite Alternate;
}
@keyframes ball {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(300px);
  }
} */

@keyframes JamesBond {
  0% {
    transform: translateX(1000px);
  }
  80% {
    transform: translateX(0px);
  }
  90% {
    border-radius: 3px;
  }
  100% {
    border-radius: 3px;
  }
}

@keyframes modalContentFadeIn {
  0% {
    opacity: 0;
    top: -20px;
  }
  100% {
    opacity: 1;
    top: 0;
  }
}

@keyframes slowFade {
  0% {
    opacity: 1;
  }
  99.9% {
    opacity: 0;
    transform: scale(1);
  }
  100% {
    transform: scale(0);
  }
}

@keyframes fadeToRed {
  0% {
    box-shadow: inset 0 0 0 rgba(201, 24, 24, 0.8);
  }
  100% {
    box-shadow: inset 0 2000px 0 rgba(201, 24, 24, 0.8);
  }
}

@keyframes killShot {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(400px) rotate(45deg);
    opacity: 0;
  }
}

@keyframes modalContentFadeOut {
  0% {
    opacity: 1;
    top: 0;
  }
  100% {
    opacity: 0;
    top: -20px;
  }
}

.modal.custom-animation .modal-dialog {
  animation: JamesBond 1.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
}

.modal.custom-animation .modal-header h5,
.modal.custom-animation .modal-body p {
  opacity: 0;
  position: relative;
  animation: modalContentFadeIn 0.5s 1.4s linear forwards;
}

.modal.custom-animation.out {
  animation: slowFade 0.5s 1.5s linear forwards;
}

.modal.custom-animation.out .modal-dialog {
  animation: killShot 1s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
}

.modal.custom-animation.out .modal-header h5,
.modal.custom-animation.out .modal-body p {
  animation: modalContentFadeOut 0.5s 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
}
</style>
