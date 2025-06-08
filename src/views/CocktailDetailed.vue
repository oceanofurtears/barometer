<template>
  <!-- Лоадер на весь экран -->
  <div v-if="isLoading" class="loader-container">
    <div class="spinner"></div>
  </div>

  <!-- Контент коктейля -->
  <div v-else class="page-wrapper">
    <div class="card-wrapper">
        <div class="cocktail-card">
            <div class="images-three-wrapper">
                <button class="back-btn" @click="$router.back()">
                    <img src="https://i.imgur.com/2fLvnSm.png" alt="back" class="btn-icon" />
                </button>
                <div class="images-three">
                    <img
                        :src="gallery[0]?.image_url || placeholder2"
                        alt="Cocktail main"
                        class="img-main"
                    />
                    <div class="img-side-wrapper">
                        <img
                            :src="gallery[1]?.image_url || placeholder2"
                            alt="Cocktail side 1"
                            class="img-side img-side-top"
                        />
                        <img
                            :src="gallery[2]?.image_url || placeholder2"
                            alt="Cocktail side 2"
                            class="img-side img-side-bottom"
                        />
                    </div>
                </div>
            </div>
        
            <div class="header-row">
                <h1 class="cocktail-name">{{ cocktail.name }}</h1>
                <div class="rating">
                    <img
                        src="https://i.imgur.com/qx5kdDU.png"
                        alt="star"
                        class="rating-icon"
                    />
                    <span class="rating-value">
                        {{ cocktail.rating ?? '0' }}
                    </span>
                </div>
            </div>
            <p class="description">{{ cocktail.description }}</p>

            <ul class="ingredients-list">
                <li v-for="(ing, i) in ingredientsList" :key="i">
                    {{ ing }}
                </li>
            </ul>

            <h3 style="color: #FF7700; margin-bottom: 8px;">Рецепт</h3>
            <ul class="recipe-list">
                <li v-for="(line, i) in recipeLines" :key="i">{{ line }}</li>
            </ul>

            <div v-if="cocktail.video_url" class="video-wrapper">
                <iframe
                    class="cocktail-video"
                    :src="youtubeEmbedUrl"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                ></iframe>
            </div>

            <div v-if="reviews.length" class="reviews-section">
                <h3 style="color: #FF7700; margin-bottom: 8px;">Отзывы</h3>
                <div class="reviews-list">
                    <div v-for="r in reviews" :key="r.id" class="review-card">
                    <div class="review-header">
                        <span class="review-user">{{ r.username }}</span>
                        <span class="review-rating">
                        <img src="https://i.imgur.com/qx5kdDU.png" class="rating-icon" />
                        {{ r.rating }}
                        </span>
                    </div>
                    <p class="review-text">{{ r.text }}</p>
                    </div>
                </div>
            </div>

        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed  } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const cocktail = ref(null)
const gallery = ref([])
const isLoading = ref(true)
const reviews = ref([]) 
const users = ref([]) 

const placeholder2 = 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y29ja3RhaWx8ZW58MHx8MHx8fDA%3D'

const ingredientsList = computed(() => {
  if (!cocktail.value?.ingredients) return []
  return cocktail.value.ingredients
    .split(',')
    .map(i => i.trim())
    .filter(i => i.length)
    .map(i => i.charAt(0).toUpperCase() + i.slice(1))
})

const recipeLines = computed(() => {
  const text = cocktail.value?.recipe || ''
  return text
    .split(/\d+\.\s*/)
    .map(line => line.trim())
    .filter(line => line.length)
})

const youtubeEmbedUrl = computed(() => {
  if (!cocktail.value?.video_url) return ''
  const url = new URL(cocktail.value.video_url)
  let id = ''
  if (url.hostname.includes('youtu.be')) {
    id = url.pathname.slice(1)
  } else {
    id = url.searchParams.get('v')
  }
  return id
    ? `https://www.youtube.com/embed/${id}`
    : ''
})

onMounted(async () => {
  try {
    // 1) Авторизация
    const params = new URLSearchParams()
    params.append('username', 'user')
    params.append('password', 'user')
    const login = await axios.post('/api/auth/login', params)
    const token = login.data.access_token

    const authAxios = axios.create({
      headers: { Authorization: `Bearer ${token}` }
    })

    const id = route.params.id

    // 2) Данные коктейля
    const res = await authAxios.get(`/api/cocktails/${id}`)
    cocktail.value = res.data

    // 3) Галерея
    const gal = await authAxios.get(`/api/cocktails/${id}/gallery`)
    gallery.value = gal.data

    const revRes = await authAxios.get(`/api/cocktails/${id}/reviews`)
    const raw = revRes.data

    // 5) Для каждого отзыва подтягиваем имя пользователя
    const withUser = await Promise.all(
      raw.map(async r => {
        try {
          const userRes = await authAxios.get(`/api/users/${r.user_id}`)
          return {
            ...r,
            username: userRes.data.username || 'User'
          }
        } catch {
          return {
            ...r,
            username: 'User'
          }
        }
      })
    )
    reviews.value = withUser

  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
/* Фон страницы */
.page-wrapper {
  background: #181818;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

/* Центрированный контейнер */
.card-wrapper {
  width: 100%;
  max-width: 352px;
  margin-top: 8px;
}

/* Лоадер */
.loader-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #181818;
}
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255,255,255,0.2);
  border-top-color: #FF7700;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

.back-btn {
  position: absolute;
  top: -8px;
  left: -8px;
  z-index: 10;
  width: 36px;
  height: 36px;
  background: #2a2a2a;
  border: none;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.btn-icon {
    width: 24px; 
    height: 24px; 
    object-fit: contain;
}
.images {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.images img {
  flex: 1;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
}

.cocktail-card {
  background: #2a2a2a;
  border-radius: 12px;
  padding: 12px;
  color: #fff;
  text-align: left;
  max-height: calc(100vh - 40px);
  overflow-y: scroll;
}
.cocktail-card::-webkit-scrollbar {
  height: 2px;
  width: 2px;
}
.cocktail-card::-webkit-scrollbar-track {
  background: transparent;
}
.cocktail-card::-webkit-scrollbar-thumb {
  background-color: #FF7700;
  border-radius: 4px;
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

/* Заголовок коктейля */
.cocktail-name {
  font-size: 20px;
  margin: 0;
  color: #FF7700;
}

/* Блок рейтинга */
.rating {
  display: flex;
  align-items: center;
  gap: 4px;
  width: 54px;
  height: 24px;
  background-color: #333438;
  border-radius: 6px;
  justify-content: center;
}


/* Иконка звезды */
.rating-icon {
  width: 18px;
  height: 18px;
  margin-right: 2px;
}

/* Само значение рейтинга */
.rating-value {
  font-size: 14px;
  color: #fefefe;
  line-height: 1;
}

.description {
  font-size: 14px;
  line-height: 1.4;
  margin: 0 0 12px;
  color: #ccc;
}

.section-subtitle {
  font-size: 16px;
  margin: 12px 0 8px;
  color: #FF7700;
}

.images-three-wrapper {
  position: relative;
}
.images-three {
  display: flex;
  gap: 4px;
  margin-bottom: 16px;
}
.img-main {
  flex: 2;
  height: 180px;
  object-fit: cover;
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
}
.img-side-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.img-side {
  width: 100%;
  height: 86px;
  object-fit: cover;
}
.img-side-top {
  border-top-right-radius: 8px;
}
.img-side-bottom {
  border-bottom-right-radius: 8px;
}

/* Ингредиенты */
.ingredients-list {
  list-style: none;
  margin: 0 0 16px;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 16px;
  row-gap: 4px;          /* <-- уменьшили расстояние между строками */
}

.ingredients-list li {
  position: relative;
  margin: 0;             /* отменили внешние отступы */
  padding-left: 12px;    /* место под буллет */
  font-size: 12px;
  line-height: 1.2;      /* <-- пошуще строки друг к другу */
  color: #fff;
}

.ingredients-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.3em;
  width: 6px;
  height: 6px;
  background: #FF7700;
  border-radius: 50%;
}

/* Рецепт */
.recipe-list {
  list-style: none;
  margin: 0 0 16px;
  padding: 0;
}
.recipe-list li {
  position: relative;
  margin: 4px 0;
  padding-left: 12px;
  font-size: 14px;
  line-height: 1.3;
  color: #fff;
}
.recipe-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.5em;
  width: 6px;
  height: 6px;
  background: #FF7700;
  border-radius: 50%;
}

/* видео */
.video-wrapper {
  margin: 16px 0;
  width: 100%;
  /* сохраняем соотношение сторон 16:9 */
  position: relative;
  padding-top: 56.25%;
}
.cocktail-video {
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
  background: #000;
}

/* Отзывы */
.reviews-section {
  margin-top: 24px;
}
.reviews-section .section-title {
  font-size: 18px;
  color: #fff;
  margin-bottom: 12px;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.review-card {
  background: #333438;
  border-radius: 8px;
  padding: 12px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.review-user {
  font-weight: bold;
  color: #FF7700;
}

.review-rating {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #fff;
}

.rating-icon {
  width: 18px;
  height: 18px;
}

.review-text {
  font-size: 14px;
  color: #ccc;
  line-height: 1.4;
  margin: 0;
}
</style>