import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useAccountStore = defineStore('account', () => {
  const API_URL = import.meta.env.VITE_API_URL;
  const token = ref(null);

  const isLogin = computed(() => {
    if (token.value === null){
      return false
    } else{
      return true
    }
  })

  const logout = ()=> {
    token.value = null
    localStorage.removeItem('token');
  }

  return { API_URL, token, isLogin, logout };
}, { persist: true });
