import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import MainPage from '../views/MainPage.vue'
import BarDetailed from '../views/BarDetailed.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: MainPage
  },
  {
    path: '/bars/:id',
    name: 'BarDetailed',
    component: BarDetailed,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
