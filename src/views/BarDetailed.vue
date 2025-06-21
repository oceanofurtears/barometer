<template>
    <div style="display: flex; justify-content: center; background-color: #181818; height: 100vh;">
        <!-- пока bar === null -->
        <div v-if="!bar" class="loader-container">
            <div class="spinner"></div>
        </div>

        <div v-else class="bar-detail">
            <button class="back-btn" @click="$router.back()">
                <img src="https://i.imgur.com/2fLvnSm.png" alt="back" class="btn-icon" style="margin-right: 0px;"/>
            </button>
            <div class="bar-card">
                <div class="bar-images" 
                    style="display: flex; 
                    padding-right: 8px;"
                    @click="openImageModal(bar.gallery)"
                >
                    <img :src="bar.gallery?.[0]?.image_url || placeholder" alt="Bar Image" class="bar-img-main" style="margin-right: 4px;"/>
                    <div style="margin-top: 8px;">
                        <img :src="bar.gallery?.[1]?.image_url || placeholder" alt="Bar Image" class="bar-img-sec" style="border-top-right-radius: 8px;"/>
                        <img :src="bar.gallery?.[2]?.image_url || placeholder" alt="Bar Image" class="bar-img-sec" style="border-bottom-right-radius: 8px;"/>
                    </div>
                </div>
                <div class="bar-info">
                    <div style="display: flex; justify-content: space-between;">
                        <h3 class="bar-name" @click="goToBar(bar.id)" style="cursor: pointer;">
                            {{ bar.name }}
                        </h3>
                        <div style="display: flex;">
                            <button class="favorite-btn" @click="toggleFavorite(bar)">
                                <img
                                    :src="bar.isFavorite ? 'https://i.imgur.com/TEyH0yT.png' : 'https://i.imgur.com/hOQA38l.png'"
                                    alt="favorite"
                                    class="btn-icon"
                                    style="width: 30px; height: 30px;"
                                />
                            </button>
                            <div class="rating">
                                <img src="https://i.imgur.com/qx5kdDU.png" alt="Настройки" class="btn-icon" style="width: 18px; height: 18px; margin-top: 0px;"/> 
                                <div style="margin-left: 4px; margin-top: 3px;">{{ bar.rating ?? '—' }}</div>
                            </div>
                        </div>
                        
                    </div>
                    <p class="bar-description" @click="goToBar(bar.id)" style="cursor: pointer;">
                        {{ bar.description }}
                    </p>

                    <div class="tags">
                        <span v-for="tag in bar.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
                    </div>

                    <div class="action-buttons">
                        <button class="btn-map" @click="showOnMap(bar)">
                            Показать на карте
                            <img src="https://i.imgur.com/PCYuXD9.png" alt="map" class="btn-icon-sec" />
                        </button>
                        <button class="btn-book" @click="bookTable(bar)">
                            Забронировать стол
                            <img src="https://i.imgur.com/Dh7WIsX.png" alt="book" class="btn-icon-sec" />
                        </button>
                    </div>

                    <div class="cocktail-section">
                        <div class="section-title">Барная карта</div>
                        <div class="cocktail-grid">
                            <div
                                v-for="cocktail in bar.cocktails"
                                :key="cocktail.id"
                                class="cocktail-card"
                                @click="goToCocktail(cocktail.id)"
                            >
                                <img
                                    :src="cocktail.gallery[0]?.image_url || placeholder2"
                                    alt="Cocktail image"
                                />
                                <h3>{{ cocktail.name }}</h3>
                                <p>{{ cocktail.description || cocktail.ingredients }}</p>
                            </div>
                        </div>
                    </div>

                    <div class="reviews-section">
                        <h2 class="section-title">Отзывы</h2>
                        <div class="reviews-list">
                            <div v-for="review in reviews" :key="review.id" class="review-card">
                                <div class="review-header">
                                    <span class="review-user">{{ review.username || 'User' }}</span>
                                    <div class="review-rating">
                                        <img src="https://i.imgur.com/qx5kdDU.png" alt="Настройки" class="btn-icon" style="width: 18px; height: 18px; margin-top: -1px; margin-right: 4px;"/> 
                                        {{ review.rating }}
                                    </div>
                                </div>
                                <p class="review-text">{{ review.text }}</p>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>

    <div
        v-if="showImageModal"
        class="image-modal-overlay"
        @click.self="closeImageModal"
    >
        <div class="image-modal-content">
            <button class="close-btn" @click="closeImageModal">×</button>

            <!-- Сетка Masonry -->
            <div class="masonry-gallery">
                <img
                    v-for="(img, i) in modalImages"
                    :key="i"
                    :src="img.image_url"
                    alt="Bar photo"
                />
            </div>
        </div>
    </div>

    <BottomNav />
</template>

<script setup>
import BottomNav from '@/components/BottomNav.vue'

import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter  } from 'vue-router'

const route = useRoute()
const router = useRouter()
const bar = ref(null)
const placeholder = 'https://images.unsplash.com/photo-1597290282695-edc43d0e7129?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YmFyfGVufDB8fDB8fHww'
const placeholder2 = 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y29ja3RhaWx8ZW58MHx8MHx8fDA%3D'

const reviews = ref([])
const users = ref([])

const modalImages = ref([])
const showImageModal = ref(false)

onMounted(async () => {
  const id = route.params.id
  try {
    // авторизация
    const params = new URLSearchParams()
    params.append('username', 'user')
    params.append('password', 'user')
    const loginRes = await axios.post('/api/auth/login', params)
    const token = loginRes.data.access_token

    const authAxios = axios.create({
      headers: { Authorization: `Bearer ${token}` }
    })

    // 1) основной объект бара
    const barRes = await authAxios.get(`/api/bars/${id}`)
    const barData = barRes.data

    // 2) галерея бара
    const galleryRes = await authAxios.get(`/api/bars/${id}/gallery/`)
    barData.gallery = galleryRes.data

    // 3) коктейли и их галереи
    const cocktailsRes = await authAxios.get(`/api/bars/${id}/cocktails/`)
    const rawCocktails = cocktailsRes.data
    barData.cocktails = await Promise.all(
      rawCocktails.map(async c => {
        const gal = await authAxios.get(`/api/cocktails/${c.id}/gallery`)
        return { ...c, gallery: gal.data }
      })
    )

    // 5) Отзывы бара
    const reviewsRes = await authAxios.get(`/api/bars/${id}/reviews/`)
    const rawReviews = reviewsRes.data

    // 6) Для каждого отзыва подтягиваем имя автора
    const reviewsWithUser = await Promise.all(
      rawReviews.map(async r => {
        try {
          const userRes = await authAxios.get(`/api/users/${r.user_id}`)
          return {
            ...r,
            username: userRes.data.username
          }
        } catch {
          return r // если по каким-то причинам не удалось — оставим user_id
        }
      })
    )

    bar.value = barData
    reviews.value = reviewsWithUser

  } catch (err) {
    console.error(err)
  }
})

function openImageModal(gallery) {
  modalImages.value = gallery.length ? gallery : [{ image_url: placeholder }]
  showImageModal.value = true
}

function closeImageModal() {
  showImageModal.value = false
}

function getUsername(review) {
  // возьмём заранее сохранённое имя, если есть
  return review.username || `User #${review.user_id}`
}

function showOnMap(bar) {
  console.log('Show on map', bar.address)
}

function bookTable(bar) {
  console.log('Book a table at', bar.name)
}

function goToCocktail(id) {
  router.push({ name: 'CocktailDetailed', params: { id } })
}

function toggleFavorite(bar) {
  const token = localStorage.getItem('access_token')
  if (!token) return

  const url = `/api/bars/${bar.id}/favorites/`
  const config = {
    headers: {
      Authorization: `Bearer ${token}`
    }
  }

  if (bar.isFavorite) {
    // удалить из избранного
    axios.delete(url, config)
      .then(() => {
        bar.isFavorite = false
      })
      .catch(err => console.error(err))
  } else {
    // добавить в избранное
    axios.post(url, null, config)
      .then(() => {
        bar.isFavorite = true
      })
      .catch(err => console.error(err))
  }
}
</script>

<style scoped>
.bar-detail {
  position: relative;
  padding: 16px;
  background: #181818;
  color: #fff;
  font-family: sans-serif;
  max-width: 352px;
  padding-top: 8px;
}
.back-btn {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 20;
  width: 40px;
  height: 40px;
  background: #2a2a2a;
  border: none;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 24px;
  cursor: pointer;
}
.btn-icon {
    width: 24px; 
    height: 24px; 
    object-fit: contain;
}
.bar-card {
  background: #2a2a2a;
  border-radius: 12px;
  overflow: hidden;
  user-select: none;
  cursor: default;
  text-align: left;
  margin-bottom: 24px;
  height: calc(100vh - 60px);
  overflow-y: scroll;
}
.bar-card::-webkit-scrollbar {
  height: 2px;
  width: 2px;
}
.bar-card::-webkit-scrollbar-track {
  background: transparent;
}
.bar-card::-webkit-scrollbar-thumb {
  background-color: #FF7700;
  border-radius: 4px;
}
.bar-images {
  display: flex;
  /* gap: 8px; */
}
.bar-img-main {
  /* width: 100%; */
  height: 180px;
  object-fit: cover;
  min-width: 232px;
  max-height: 135px;
  margin: 8px 8px;
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
  cursor: pointer;
}
.bar-img-sec {
    /* min-width: 117px; */
    width: 100%;
    height: 66px;
    cursor: pointer;
}
.bar-info {
  padding: 12px;
  padding-top: 0px;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.bar-name {
  font-size: 18px;
  margin: 0;
}
.icons {
  display: flex;
  align-items: center;
  gap: 12px;
}
.favorite-btn {
  background: transparent;
  border: none;
  cursor: pointer;
}
.favorite-icon {
  width: 24px;
  height: 24px;
}
.rating {
  display: flex;
  align-items: center;
  gap: 4px;
}
.rating-icon {
  width: 18px;
  height: 18px;
}
.bar-description {
  font-size: 14px;
  margin: 8px 0;
  color: #ccc;
}
.rating {
    display: flex;
    width: 54px;
    height: 24px;
    background-color: #333438;
    justify-content: center;
    border-radius: 6px;
}
.favorite-btn {
  background: transparent;
  border: none;
  color: gold;
  font-size: 24px;
  cursor: pointer;
  padding: 4px 0;
  height: 32px;
  /* line-height: 12px; */
  margin-right: 2px;
  margin-top: -8px;
}
.favorite-btn:hover {
  opacity: 0.8;
}
.tags {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    overflow-x: auto; 
    gap: 4px;
}
.tags::-webkit-scrollbar {
  height: 0px;
  width: 0px;
}
.tag {
  background: #333;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 14px;
  white-space: nowrap;
}
.action-buttons {
  display: flex;
  gap: 12px;
  margin: 4px 0;
}
.action-buttons button {
  flex: 1;
  display: inline-flex;
  height: 24px;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 10px;
  background: #FF7700;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.action-buttons button:hover {
  background: #e66f00;
}
.btn-icon-sec {
  width: 18px;
  height: 18px;
  object-fit: contain;
}

/* Коктейли */
.cocktail-section {
  margin-top: 12px;
}
.section-title {
  font-size: 14px;
  color: #fff;
  margin-bottom: 12px;
  font-weight: 600;
}

/* Грид с карточками коктейлей */
.cocktail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
}

/* Сама карточка */
.cocktail-card {
  background: #333438;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}
.cocktail-card:hover {
  transform: translateY(-4px);
}

/* Изображение */
.cocktail-card img {
  width: 100%;
  height: 100px;
  object-fit: cover;
}

/* Название */
.cocktail-card h3 {
  margin: 8px;
  font-size: 14px;
  color: #FF7700;
}

/* Описание */
.cocktail-card p {
  margin: 0 8px 8px;
  font-size: 12px;
  line-height: 1.3;
  color: #ccc;
}

/* Отзывы */
.reviews-section {
  margin-top: 12px;
}
.reviews-section .section-title {
  font-size: 18px;
  color: #fff;
  margin-bottom: 12px;
}

/* Список карточек отзывов */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Одна карточка отзыва */
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
  font-size: 16px;
}
.review-text {
  font-size: 14px;
  color: #ccc;
  line-height: 1.4;
  margin: 0;
}

/* Галерея */
.image-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}
.image-modal-content {
  position: relative;
  width: 370px;
  /* max-width: 900px; */
  max-height: 90%;
  background: #1e1e1e;
  border-radius: 12px;
  overflow: auto;
  padding: 16px;
}
.image-modal-content::-webkit-scrollbar {
  height: 2px;
  width: 2px;
}
.image-modal-content::-webkit-scrollbar-track {
  background: transparent;
}
.image-modal-content::-webkit-scrollbar-thumb {
  background-color: #FF7700;
  border-radius: 4px;
}
.close-btn {
  position: absolute;
  top: 12px;
  right: 16px;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 28px;
  cursor: pointer;
  z-index: 999;
}

.masonry-gallery {
  column-count: 2;
  column-gap: 8px;
}
.masonry-gallery img {
  display: block;
  width: 100%;
  margin-bottom: 8px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  cursor: pointer;
  transition: transform 0.2s;
}
.masonry-gallery img:hover {
  transform: scale(1.03);
  z-index: 2;
}

/* ЛОАДЕР */
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
  border: 4px solid rgba(255, 255, 255, 0.2);
  border-top-color: #FF7700;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>