import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '@/views/SearchView.vue'
import DetailView from '@/views/DetailView.vue'
import AccountView from '@/views/AccountView.vue'
import LogInComponent from '@/components/LogInComponent.vue'
import SignUpComponent from '@/components/SignUpComponent.vue'
import ProfileView from '@/views/ProfileView.vue'
import { useAccountStore } from '@/stores/account';  // Import the store

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

router.beforeEach((to, from, next) => {
  const accountStore = useAccountStore();
  
  if (!accountStore.isLogin && to.name !== 'login' && to.name !== 'signup' && to.name !== 'home') {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router;
