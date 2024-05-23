<template>
  <div class="movie-info">
    <h1>영화 상세정보</h1>
    <br>
    <img class="movie-poster" :src="'https://image.tmdb.org/t/p/w500' + movieDetail[0].poster_path" alt="movie_poster">
    <div class="movie-container">
      <img v-if="is_liked" @click="like" src="@/assets/like.png" alt="like" style="width: 50px;">
      <img @click="like" v-else src="@/assets/dislike.png" alt="dislike" style="width: 50px;">
      <img @click="fetchProfiles" src="@/assets/throw.png" alt="throw" style="width: 60px;"><br><br>
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
      <div v-for="(comment, index) in visibleComments" :key="index" style="display: flex; align-items: center; padding: 10px;">
        <div style="margin-right: 10px;">
          <img v-if="comment.userName['image']" :src="API_URL + comment.userName['image']" class="img-fluid rounded-circle" alt="..." @click="showUserProfile(comment.user)" style="cursor: pointer; width: 50px; height: 50px;">
          <img v-else src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDBJhKc_AmFlxPGktgktgKpzusO8p6mryOtw&s" class="img-fluid rounded-circle" alt="..." style="width: 50px; height: 50px;">
        </div>
        <div style="flex-grow: 1; text-align: left;">
          <div>
            <a @click="showUserProfile(comment.user)" style="cursor: pointer; color: #007BFF;">{{ comment.userName['username'] }} </a>
          </div>
          <div>
            <span v-if="!comment.isEditing">{{ comment.content }}</span>
            <input v-else v-model="comment.editContent" style="width: 300px;">
          </div>
        </div>
        <div>
          <a v-if="comment.user === userId && !comment.isEditing" @click="editComment(comment)" style="padding-left: 5px; text-decoration: underline; color: gray;">수정</a>
          <a v-if="comment.user === userId && !comment.isEditing" @click="commentDelete(comment.id)" style="padding-left: 5px; text-decoration: underline; color: gray;">삭제</a>
          <a v-if="comment.isEditing" @click="updateComment(comment)" style="padding-left: 5px; text-decoration: underline; color: gray;">저장</a>
          <a v-if="comment.isEditing" @click="cancelEdit(comment)" style="padding-left: 5px; text-decoration: underline; color: gray;">취소</a>
        </div>
      </div>
      <button class="btn btn-secondary" v-if="visibleComments.length < movieComments.length" @click="loadMoreComments" style="margin: 20px; padding: 10px 20px;">더보기</button>
    </div>


    <div style="padding: 50px;">
      <form @submit="handleSubmit" class="form-inline">
        <input type="text" class="form-control" id="basic-url" aria-describedby="basic-addon3 basic-addon4" name="content" placeholder="댓글을 입력하세요." v-model="commentContent" style="width: 300px; display: inline-block; margin-right: 10px;">
        <button type="submit" class="btn btn-primary" value="작성" style="display: inline-block;">작성</button>
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
const movieComments = ref(props.movieComment.map(comment => ({ ...comment, isEditing: false, editContent: comment.content })))
const visibleComments = ref(movieComments.value.slice(0, 10));
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
        isEditing: false,
        editContent: comment.content,
        userName: '' // 댓글 작성자의 이름을 담을 속성
      }));
      visibleComments.value = movieComments.value.slice(0, 10);
      fetchUserNames(movieComments.value);
    })
    .catch(error => {
      console.log(error);
    });
};

const fetchUserNames = (comments) => {
  comments.forEach(comment => {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/movies/getUserName/${comment.user}/`,
      headers: {
          Authorization: `Token ${accountStore.token}`
        }
    })
      .then(response => {
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
    url: `${API_URL}/accounts/get_followings/`,  
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

const editComment = (comment) => {
  comment.isEditing = true;
};

const updateComment = (comment) => {
  axios({
    method: 'put',
    url: `http://127.0.0.1:8000/api/v1/movies/${movieId}/comments/${comment.id}/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    },
    data: { content: comment.editContent }
  })
    .then(response => {
      comment.isEditing = false;
      fetchComments();
    })
    .catch(error => {
      console.log(error);
    });
};

const cancelEdit = (comment) => {
  comment.isEditing = false;
  comment.editContent = comment.content;
};

const loadMoreComments = () => {
  const nextIndex = visibleComments.value.length;
  visibleComments.value = movieComments.value.slice(0, nextIndex + 10);
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

.img-fluid {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 50%;
}

.form-inline {
  display: flex;
  align-items: center;
}

</style>
