<template>
  <nav class="bottom-nav">
    <button @click="$router.push('/')" class="nav-btn" :class="{ active: isHome }">
      <img src="https://i.imgur.com/4RNJbNx.png" alt="Домой" class="nav-icon" />
    </button>

    <button @click="$router.push('/favorites')" class="nav-btn" :class="{ active: isFavorites }">
      <img src="https://i.imgur.com/m3rAbob.png" alt="Избранное" class="nav-icon" />
    </button>

    <button class="nav-btn">
      <img src="https://i.imgur.com/L6Ug3Ro.png" alt="Профиль" class="nav-icon" />
    </button>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const isHome = route.path === '/'
const isFavorites = route.path === '/favorites'
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: calc(50% - 184px);
  max-width: 352px;
  width: 352px;
  height: 32px;
  background: #2a2a2a;
  display: flex;
  justify-content: space-around;
  align-items: center;
  border-top-left-radius: 24px;
  border-top-right-radius: 24px;
  z-index: 100;
  padding: 8px;
}

.nav-btn {
  background: none;
  border: none;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  height: 100%;
  cursor: pointer;
  transition: opacity 0.2s;
}

.nav-btn.active .nav-icon {
  filter: invert(51%) sepia(94%) saturate(750%) hue-rotate(2deg) brightness(102%) contrast(106%);
}

.nav-icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
}
</style>