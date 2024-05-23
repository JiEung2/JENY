<template>
  <div>
    <div class="card-body align-items-center">
      <h5 class="text-light">{{ user.username }}</h5>
      <p v-if="user.introduce === ''"><small class="text-secondary">자기소개를 작성해보세요</small></p>
      <p v-else><small class="text-secondary">간단한 소개: {{ user.introduce }}</small></p>

      <p class="card-text" v-if="user.mbti === ''"><small class="text-secondary">mbti를 등록해보세요.</small></p>
      <p class="card-text" v-else><small class="text-secondary">mbti: {{ user.mbti }}</small></p>
      
      <div class="word-cloud" style="padding-top: 30px 0 20px 0;">
        <UserWordCloud :defaultWords="defaultWords"/>
      </div>

      <div v-if="isEditing">
        <form @submit.prevent="updateProfile">
          <div class="mb-3">
            <label for="introduce" class="form-label text-light">자기소개</label>
            <textarea v-model="user.introduce" class="form-control bg-dark text-light" id="introduce" rows="3"></textarea>
          </div>
          <div class="mb-3">
            <label for="mbti" class="form-label text-light">MBTI</label>
            <input type="text" v-model="user.mbti" class="form-control bg-dark text-light" id="mbti">
          </div>
          <div class="mb-3">
            <label for="image" class="form-label text-light">프로필 이미지</label>
            <input type="file" @change="onFileChange" class="form-control bg-dark text-light" id="image">
          </div>
          <div class="text-center">
            <button type="submit" class="btn btn-primary">저장</button>
          </div>
        </form>
        <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
      </div>
      <button v-if="!isEditing" type="button" class="btn btn-outline-light mt-3" @click="editProfile">프로필 수정</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAccountStore } from '@/stores/account';
import axios from 'axios';
import UserWordCloud from '@/components/UserWordCloud.vue'

const accountStore = useAccountStore();
const API_URL = accountStore.API_URL;

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  defaultWords: Array
});

const emit = defineEmits(['profile-updated']);

const isEditing = ref(false)
const profileImage = ref(null)
const errorMessage = ref('')

const editProfile = () => {
  isEditing.value = true
}

const onFileChange = (event) => {
  profileImage.value = event.target.files[0]
}

const updateProfile = () => {
  errorMessage.value = ''; // 오류 메시지 초기화
  const formData = new FormData()
  formData.append('introduce', props.user.introduce)
  formData.append('mbti', props.user.mbti)
  if (profileImage.value) {
    formData.append('image', profileImage.value)
  }

  axios({
    method: 'put',
    url: `${API_URL}/accounts/update_profile/`,
    headers: {
      Authorization: `Token ${accountStore.token}`,
      'Content-Type': 'multipart/form-data'
    },
    data: formData
  })
  .then(response => {
    const updated_info = response.data
    isEditing.value = false
    props.user.introduce = updated_info.introduce
    props.user.mbti = updated_info.mbti
    props.user.image = updated_info.image
    // 부모 컴포넌트로 이벤트를 보냄
    emit('profile-updated', updated_info)
  })
  .catch(error => {
    if (error.response && error.response.data && error.response.data.message) {
      errorMessage.value = error.response.data.message;
    } else {
      errorMessage.value = '프로필 업데이트 중 오류가 발생했습니다.';
    }
    console.error(error)
  })
}
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

.text-danger {
  color: #e50914 !important; /* 넷플릭스 스타일의 빨간색 오류 메시지 */
}

.text-center {
  text-align: center;
}
</style>
