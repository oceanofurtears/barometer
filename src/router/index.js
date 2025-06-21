import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import MainPage from '../views/MainPage.vue'
import BarDetailed from '../views/BarDetailed.vue'
import CocktailDetailed from '@/views/CocktailDetailed.vue'
import FavouritesPage from '@/views/FavouritesPage.vue'

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
  },
  {
    path: '/cocktails/:id',
    name: 'CocktailDetailed',
    component: CocktailDetailed,
    props: true
  },
  {
    path: '/favorites',
    name: 'FavouritesPage',
    component: () => import('@/views/FavouritesPage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
