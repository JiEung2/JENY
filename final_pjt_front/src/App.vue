<script setup>
import { RouterLink, RouterView } from 'vue-router'
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
            <RouterLink :to="{ name: 'LogInView' }" class="link text-white">로그인</RouterLink>
          </li>
          <li class="nav-item ms-3">
            <RouterLink :to="{ name: 'SignUpView' }" class="link text-white"><button type="button" class="btn btn-danger">회원가입</button></RouterLink>
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
    background-color:#141517 !important;
  }

  .link{
    text-decoration: none;
  }

  body {
    background-color: #000; /* 검정색 배경색 설정 */
  }

</style>
