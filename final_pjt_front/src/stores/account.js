import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import axios from 'axios';

export const useAccountStore = defineStore('account', () => {
  const API_URL = import.meta.env.VITE_API_URL;
  const token = ref(null);
  const router = useRouter()

  const isLogin = computed(() => {
    if (token.value === null){
      return false
    } else{
      return true
    }
  })

  const signUp = function (payload) {
    const { username, password1, password2 } = payload;

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then(res => {
        console.log('회원가입 완료!');
        const password = password1
        logIn({username, password})
      })
      .catch(err => console.log(err));
  };

  const logIn = function (payload) {
    const { username, password } = payload;

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        console.log('로그인이 완료!');
        console.log(res.data.key);
        token.value = res.data.key;
        router.push({name : 'home'})
      })
      .catch(err => console.log(err));
  };

  

  return { signUp, logIn, API_URL, token, isLogin };
}, { persist: true });
