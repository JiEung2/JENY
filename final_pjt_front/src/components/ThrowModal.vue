<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <button class="close-button" @click="closeModal">X</button>
      <div class="profiles">
        <div v-for="user in users" :key="user.username" class="profile" @click="throwMovie(user)">
          <img v-if="user.image" :src="API_URL + user.image" class="profile-image" alt="...">
          <img v-else src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDBJhKc_AmFlxPGktgktgKpzusO8p6mryOtw&s" class="profile-image" alt="...">
          <p>{{ user.username }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import { useAccountStore } from '@/stores/account';
import axios from 'axios';

const accountStore = useAccountStore()
const API_URL = accountStore.API_URL;
const props = defineProps({
  users: {
    type: Array,
    required: true
  },
  movie: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close']);

const throwMovie = (user) => {
  axios({
    method: 'post',
    url: `${API_URL}/api/v1/throw/${props.movie.id}/${user.username}/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    },
  })
  .then((response) => {
    console.log('보내기 성공');
    closeModal();
  })
  .catch((error) => {
    console.log(API_URL)
    console.log(error);
  });
};

const closeModal = () => {
  emit('close');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: rgba(0, 0, 0, 0.7);
  padding: 20px;
  border-radius: 10px;
  width: 80%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: white;
}

.profiles {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 5px;
  row-gap: 10px;
}

.profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.profile-image {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 5px;
}
</style>
