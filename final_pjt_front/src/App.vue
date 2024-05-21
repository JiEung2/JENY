<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAccountStore } from '@/stores/account';
import { onMounted } from 'vue';
import { useMovieStore } from '@/stores/counter';

const movieStore = useMovieStore()
const accountStore = useAccountStore()

onMounted(() => {
  movieStore.getLatedMovieList()
});

</script>

<template>
  <body>
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
            <li class="nav-item ms-3" v-if="accountStore.isLogin === false">
              <RouterLink :to="{ name: 'LogInView' }" class="link text-white" >로그인</RouterLink>
            </li>
            <li class="nav-item ms-3" v-if="accountStore.isLogin === false">
              <RouterLink :to="{ name: 'SignUpView' }" class="link text-white"><button type="button" class="btn btn-danger">회원가입</button></RouterLink>
            </li>
            <li class="nav-item ms-3">
              <RouterLink :to="{ name: 'LogInView' }" class="link text-white" v-if="accountStore.isLogin === true">마이페이지</RouterLink>
            </li>
            <li class="nav-item ms-3" v-if="accountStore.isLogin === true">
              <RouterLink :to="{ name: 'LogInView' }" class="link text-white" >로그아웃</RouterLink>

            </li>
          </ul>
        </div>
      </div>
    </nav>
    <RouterView />
  </body>
</template>

<style scoped>
  template{
    min-width: 500px;
  }
  .navbar{
    font-family: 'YeongdeokSea';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2307-1@1.1/YeongdeokSea.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
    background-color:#141517 !important;
  }

  .link{
    text-decoration: none;
  }

  body {
    background-color: #000; /* 검정색 배경색 설정 */
  }

  #app {
  min-height: 100vh; /* 뷰포트 전체 높이를 채우도록 설정 */
  display: flex;
  flex-direction: column;
  }
</style>
