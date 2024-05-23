<template>
  <div class="movie-info">
    <h1>영화 상세정보</h1>
    <br>
    <img class="movie-poster" :src="'https://image.tmdb.org/t/p/w500' + movieDetail[0].poster_path" alt="movie_poster">
    <div class="movie-container">
      <img v-if="is_liked" @click="like" src="@/assets/like.png" alt="like" style="width: 50px;">
      <img @click="like" v-else src="@/assets/dislike.png" alt="dislike" style="width: 50px;">
      <img @click="fetchProfiles" src="@/assets/throw.png" alt="throw" style="width: 50px;"><br><br>
    </div>
    <div class="movie-details">
      <h2>{{ movieDetail[0].title }}</h2><br><br>
      <h4>줄거리</h4>
      <p v-if="movieDetail[0].overview" class="movie-summary">{{ movieDetail[0].overview }}</p>
      <p v-else class="movie-summary">등록된 줄거리가 없습니다.</p>
      <br>
      <h4>장르</h4>
      <p>{{ genres.join(', ') }}</p><br>
      <h4>평점</h4>
      <p>{{ movieDetail[0].vote_average }}</p><br>
      <h4>개봉일</h4>
      <p>{{ movieDetail[0].release_data }}</p><br>
    </div>
    <hr style="width: 100%; border: 1px solid white; margin: 20px 0;">
    <br>
    <br>
    <h2>리뷰</h2>
    
    <div>
      <div v-for="(comment, index) in movieComments" style="display: flex; justify-content: space-between; padding: 10px;" >
        <span>
          <a @click="showUserProfile(comment.user)" style="cursor: pointer; color: #007BFF;">{{ comment.userName }}</a>: {{ comment.content }}
        </span>
        <span>
          <a v-if="comment.user === userId" type="submit" style="padding-left: 5px; text-decoration: underline; color: gray;">수정</a>
          <a v-if="comment.user === userId" type="submit" style="padding-left: 5px; text-decoration: underline; color: gray;" @click="commentDelete(comment.id)">삭제</a>
        </span>
      </div>
    </div>

    <div style="padding: 50px;">
      <form @submit="handleSubmit">
      <input type="text" name="content" placeholder="댓글을 입력하세요." v-model="commentContent" style="width: 300px;">
      <button type="submit" value="작성"> 작성</button>
    </form>
    </div>
    <div>
      <WordCloud/>
    </div>

    <ThrowModal v-if="showModal" :users="profiles" :movie="movieDetail[0]" @close="closeModal" />
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import WordCloud from './WordCloud.vue';
import ThrowModal from '@/components/ThrowModal.vue';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useAccountStore } from '@/stores/account';
import { useRouter } from 'vue-router';

const props = defineProps({
  id: {
    type: String,
  },
  movieDetail: {
    type: Object,
  },
  movieComment: {
    type: Array,
  },
});

const router = useRouter();
const accountStore = useAccountStore()
const movieId = props.id
const genres = ref([])
const userId = ref([])
const userName = ref([])
const movieComments = ref([...props.movieComment])
const API_URL = import.meta.env.VITE_API_URL;
const USER_TOKEN = accountStore.token;

const commentContent = ref('');
const is_liked = ref(false);
const showModal = ref(false);
const profiles = ref([]);

const fetchComments = () => {
  axios({
    method: 'get',
    url: `http://127.0.0.1:8000/api/v1/movies/${movieId}/comments/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
    .then(response => {
      movieComments.value = response.data.map(comment => ({
        ...comment,
        userName: '' // 댓글 작성자의 이름을 담을 속성
      }));
      // 작성자의 이름을 가져오기 위해 fetchUserNames 함수 호출
      fetchUserNames(movieComments.value);
    })
    .catch(error => {
      console.log(error);
    });
};

const fetchUserNames = (comments) => {
  // 각 댓글의 작성자의 이름을 가져오는 비동기 함수
  comments.forEach(comment => {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/movies/getUserName/${comment.user}/`,
      headers: {
          Authorization: `Token ${accountStore.token}`
        }
    })
      .then(response => {
        // 댓글 작성자의 이름을 댓글 객체에 설정
        comment.userName = response.data;
      })
      .catch(error => {
        console.log(error)
      });
  });
};

const handleSubmit = (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  const content = formData.get('content');

  axios({
    method: 'post',
    url: `http://127.0.0.1:8000/api/v1/movies/${movieId}/comments/create/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    },
    data: { content }
  })
    .then(response => {
      commentContent.value = '';
      fetchComments();
    })
    .catch(error => {
      console.log(error);
    });
};

const commentDelete = (commentId) => {
  axios({
    method: 'delete',
    url: `http://127.0.0.1:8000/api/v1/movies/${movieId}/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
    .then(response => {
      fetchComments();
    })
    .catch(error => {
      console.log(error);
    });
};

const showUserProfile = (user_id) => {
  router.push({ name: 'MyPageView', params: { id: user_id } });
};

// 장르 가져오는 axios
axios({
  method: 'get',
  url: `http://127.0.0.1:8000/api/v1/movies/getMovieGenres/${movieId}/`,
  headers: {
    Authorization: `Token ${accountStore.token}`
  }
})
  .then(response => {
    genres.value = response.data;
  })
  .catch(error => {
    console.log(error);
  });

// userId 가져오는 axios
axios({
  method: 'get',
  url: 'http://127.0.0.1:8000/api/v1/movies/getUserId/',
  headers: {
    Authorization: `Token ${accountStore.token}`
  }
})
  .then(response => {
    userId.value = response.data;
  })
  .catch(error => {
    console.log(error);
  });

// 좋아요 기능 구현
const like = () => {
  axios({
    method: 'post',
    url: `${API_URL}/api/v1/movies/${movieId}/likes/`,
    headers: {
      Authorization: `Token ${USER_TOKEN}`
    }
  })
    .then(response => {
      is_liked.value = response.data.liked;
    })
    .catch(error => {
      console.log(error);
    });
};

// 좋아요 되어있는지 확인하는 기능 구현
const get_is_like = () => {
  axios({
    method: 'get',
    url: `${API_URL}/api/v1/movies/${movieId}/get_is_liked/`,
    headers: {
      Authorization: `Token ${USER_TOKEN}`
    }
  })
    .then(response => {
      is_liked.value = response.data.is_liked;
    })
    .catch(error => {
      console.log(error);
    });
};

const fetchProfiles = () => {
  axios({
    method: 'get',
    url: `${API_URL}/accounts/get_followings/`,  // 이 URL은 실제 API 엔드포인트로 변경되어야 합니다.
    headers: {
      Authorization: `Token ${USER_TOKEN}`
    }
  })
    .then(response => {
      profiles.value = response.data;
      showModal.value = true;
    })
    .catch(error => {
      console.log(error);
    });
};

const closeModal = () => {
  showModal.value = false;
};

onMounted(() => {
  fetchComments();
  get_is_like()
});
</script>


<style scoped>
.movie-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #1e1e1e;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: auto;
  margin: 0 auto;
}

.movie-poster {
  width: 400px;
  margin-bottom: 20px;
}

.movie-summary {
  padding: 0 20px;
  text-align: center;
  margin: 0 auto;
}

.movie-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  width: 100%;
  margin-bottom: 20px;
}

.movie-details {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.movie-details p {
  margin: 5px 20px;
}
</style>
