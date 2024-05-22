<template>
	<div>
			<h1>MyPage</h1>
	</div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useAccountStore } from '@/stores/account';

const API_URL = import.meta.env.VITE_API_URL
const store = useAccountStore()
console.log(store.token)

axios({
  method: 'get',
    url: `${API_URL}/mypage/${user_id}`,
    headers: {
      Authorization: `Token ${store.token}`
    }
})
  .then(response => {
    console.log(response.data)
  })

</script>

<style scoped>

</style>