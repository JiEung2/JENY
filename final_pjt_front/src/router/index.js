import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
// import SignUpView from '@/views/SignUpView.vue'
// import LogInView from '@/views/LogInView.vue'
import SearchView from '@/views/SearchView.vue'
import DetailView from '@/views/DetailView.vue'
import AccountView from '@/views/AccountView.vue'
import LogInComponent from '@/components/LogInComponent.vue'
import SignUpComponent from '@/components/SignUpComponent.vue'
import ProfileView from '@/views/ProfileView.vue'
import UserInfo from '@/components/UserInfo.vue'




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/account',
      component: AccountView,
      children: [
        { path: '', name: 'AccountView' },
        { path: 'login', name: 'login', component: LogInComponent },
        { path: 'signup', name: 'signup', component: SignUpComponent }
      ]
    },
    {
      path: '/detail/:id',
      name: 'DetailView',
      component: DetailView,
      props: true,
    },
    {
      path: '/search',
      name: 'SearchView',
      component: SearchView
    },
    {
      path: '/my_page/:id',
      name: 'MyPageView',
      component: ProfileView,
      props: true
    },
  ]
})



export default router
