<template>
  <div class="center-wrap">
    <div class="section text-center">
      <h4 class="mb-4 pb-3">Sign Up</h4>
      <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
      <form @submit.prevent="signUp">
        <div class="form-group">
          <input type="text" class="form-style" placeholder="Your Username" id="signup-username" v-model.trim="signupUsername" autocomplete="off">
          <i class="input-icon uil uil-user"></i>
        </div>  
        <div class="form-group mt-2">
          <input type="password" class="form-style" placeholder="Your Password" id="signup-password1" v-model.trim="signupPassword1" autocomplete="off">
          <i class="input-icon uil uil-lock-alt"></i>
        </div>  
        <div class="form-group mt-2">
          <input type="password" class="form-style" placeholder="Confirm Password" id="signup-password2" v-model.trim="signupPassword2" autocomplete="off">
          <i class="input-icon uil uil-lock-alt"></i>
        </div>
        <input type="submit" class="btn mt-4" value="SignUp">
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'
import axios from 'axios';
import { useRouter } from 'vue-router';


const router = useRouter()
const signupUsername = ref(null)
const signupPassword1 = ref(null)
const signupPassword2 = ref(null)
const errorMessage = ref('')
const store = useAccountStore()

const API_URL = store.API_URL

const signUp = function () {
  const username = signupUsername.value
  const password1 = signupPassword1.value
  const password2 = signupPassword2.value

  axios.post(`${API_URL}/accounts/signup/`, { username, password1, password2 })
    .then(res => {
      console.log('회원가입 완료!');
      const password = password1
      logIn({ username, password })
    })
    .catch(error => {
      if (error.response && error.response.data) {
        if (error.response.data.username) {
          errorMessage.value = error.response.data.username[0];
        } else if (error.response.data.password1) {
          errorMessage.value = error.response.data.password1[0];
        } else if (error.response.data.non_field_errors) {
          errorMessage.value = error.response.data.non_field_errors[0];
        } else {
          errorMessage.value = '회원가입 중 오류가 발생했습니다.';
        }
      } else {
        errorMessage.value = '서버와 연결할 수 없습니다.';
      }
      console.log(error);
    });
};

const logIn = function (payload) {
  const { username, password } = payload
  axios({
    method: 'post',
    url: `${API_URL}/accounts/login/`,
    data: {
      username, password
    }
  })
    .then(res => {
      store.token = res.data.key;
      router.push({name : 'home'})
    })
    .catch(err => {
      console.log(err)
    });
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Poppins:400,500,600,700,800,900');

body {
  font-family: 'Poppins', sans-serif;
  font-weight: 300;
  font-size: 15px;
  line-height: 1.7;
  color: #ffffff;
  background-color: #1f2029;
  overflow-x: hidden;
}

a {
  cursor: pointer;
  transition: all 200ms linear;
}

a:hover {
  text-decoration: none;
}

.link {
  color: #ffffff;
}

.link:hover {
  color: #ffeba7;
}

p {
  font-weight: 500;
  font-size: 14px;
  line-height: 1.7;
}

h4 {
  font-weight: 600;
  color: #ffffff;
}

h6 span {
  padding: 0 20px;
  text-transform: uppercase;
  font-weight: 700;
  color: #ffffff;
}

.section {
  position: relative;
  width: 100%;
  display: block;
}

.full-height {
  min-height: 100vh;
}

[type="checkbox"]:checked,
[type="checkbox"]:not(:checked) {
  position: absolute;
  left: -9999px;
}

.checkbox:checked + label,
.checkbox:not(:checked) + label {
  position: relative;
  display: block;
  text-align: center;
  width: 60px;
  height: 16px;
  border-radius: 8px;
  padding: 0;
  margin: 10px auto;
  cursor: pointer;
  background-color: #ffeba7;
}

.checkbox:checked + label:before,
.checkbox:not(:checked) + label:before {
  position: absolute;
  display: block;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: #ffeba7;
  background-color: #102770;
  font-family: 'unicons';
  content: '\eb4f';
  z-index: 20;
  top: -10px;
  left: -10px;
  line-height: 36px;
  text-align: center;
  font-size: 24px;
  transition: all 0.5s ease;
}

.checkbox:checked + label:before {
  transform: translateX(44px) rotate(-270deg);
}

.card-3d-wrap {
  position: relative;
  width: 440px;
  max-width: 100%;
  height: 400px;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  perspective: 800px;
  margin-top: 60px;
}

.card-3d-wrapper {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  transition: all 600ms ease-out;
}

.card-front,
.card-back {
  width: 100%;
  height: 100%;
  background-color: #2a2b38;
  background-image: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/1462889/pat.svg');
  background-position: bottom center;
  background-repeat: no-repeat;
  background-size: 300%;
  position: absolute;
  border-radius: 6px;
  left: 0;
  top: 0;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  -webkit-backface-visibility: hidden;
  -moz-backface-visibility: hidden;
  -o-backface-visibility: hidden;
  backface-visibility: hidden;
}

.card-back {
  transform: rotateY(180deg);
}

.checkbox:checked ~ .card-3d-wrap .card-3d-wrapper {
  transform: rotateY(180deg);
}

.center-wrap {
  position: absolute;
  width: 100%;
  padding: 0 35px;
  top: 50%;
  left: 0;
  transform: translate3d(0, -50%, 35px) perspective(100px);
  z-index: 20;
  display: block;
}

.form-group {
  position: relative;
  display: block;
  margin: 0;
  padding: 0;
}

.form-style {
  padding: 13px 20px;
  padding-left: 55px;
  height: 48px;
  width: 100%;
  font-weight: 500;
  border-radius: 4px;
  font-size: 14px;
  line-height: 22px;
  letter-spacing: 0.5px;
  outline: none;
  color: #ffffff;
  background-color: #1f2029;
  border: none;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
  box-shadow: 0 4px 8px 0 rgba(21, 21, 21, .2);
}

.form-style:focus,
.form-style:active {
  border: none;
  outline: none;
  box-shadow: 0 4px 8px 0 rgba(21, 21, 21, .2);
}

.form-style::placeholder {
  color: #ffffff;
  opacity: 0.7;
}

.input-icon {
  position: absolute;
  top: 0;
  left: 18px;
  height: 48px;
  font-size: 24px;
  line-height: 48px;
  text-align: left;
  color: #ffeba7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:-ms-input-placeholder {
  color: #ffffff;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input::-moz-placeholder {
  color: #ffffff;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:-moz-placeholder {
  color: #ffffff;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input::-webkit-input-placeholder {
  color: #ffffff;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus:-ms-input-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus::-moz-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus:-moz-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus::-webkit-input-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.btn {
  border-radius: 4px;
  height: 44px;
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
  padding: 0 30px;
  letter-spacing: 1px;
  display: -webkit-inline-flex;
  display: -ms-inline-flexbox;
  display: inline-flex;
  -webkit-align-items: center;
  -moz-align-items: center;
  -ms-align-items: center;
  align-items: center;
  -webkit-justify-content: center;
  -moz-justify-content: center;
  -ms-justify-content: center;
  justify-content: center;
  -ms-flex-pack: center;
  text-align: center;
  border: none;
  background-color: #ffeba7;
  color: #102770;
  box-shadow: 0 8px 24px 0 rgba(255, 235, 167, .2);
}

.btn:active,
.btn:focus {
  background-color: #102770;
  color: #ffeba7;
  box-shadow: 0 8px 24px 0 rgba(16, 39, 112, .2);
}

.btn:hover {
  background-color: #102770;
  color: #ffeba7;
  box-shadow: 0 8px 24px 0 rgba(16, 39, 112, .2);
}

.logo {
  position: absolute;
  top: 30px;
  right: 30px;
  display: block;
  z-index: 100;
  transition: all 250ms linear;
}

.logo img {
  height: 26px;
  width: auto;
  display: block;
}
</style>