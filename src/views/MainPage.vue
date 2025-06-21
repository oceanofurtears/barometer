<template>
    <div style="display: flex; justify-content: center; background-color: #181818; height: 100vh;">
        <div v-if="isLoading" class="loader-container">
            <div class="spinner"></div>
        </div>

        <div v-else class="home">
            <!-- Поиск и фильтры -->
            <div class="search-bar">
                <div style="display: flex;">
                    <input
                        v-model="searchQuery"
                        type="text"
                        placeholder="Что пробуем сегодня?"
                        class="search-input"
                    />
                    <div class="actions">
                        <button @click="showTagModal = true"><img src="https://i.imgur.com/JLIDEUd.png" alt="Настройки" class="btn-icon"/></button>
                        <button @click="showMapModal = true"><img src="https://i.imgur.com/81BknL0.png" alt="Настройки" class="btn-icon"/></button>
                    </div>
                </div>
                <!-- Селектор города -->
                <div class="city-selector">
                    <div @click="toggleCityDropdown" style="display: flex;">
                        <img src="https://i.imgur.com/9WAJRUL.png" alt="Настройки" class="btn-icon" style="height: 18px; margin-top: 0px;"/>
                        <strong style="margin-top: 2px;">{{ selectedCity }}</strong>
                    </div>
                    <div v-if="showCityDropdown" class="city-dropdown">
                        <div
                        v-for="city in cities"
                        :key="city"
                        class="city-option"
                        @click="selectCity(city)"
                        >
                        {{ city }}
                        </div>
                    </div>
                </div>
                <div class="filters">
                    <span v-for="tag in selectedTags" :key="tag" class="tag">{{ tag }}</span>
                </div>
            </div>

            <!-- Список баров -->
            <div class="bar-container">
                <div class="bar-list">
                    <div v-for="bar in filteredBars" :key="bar.id" class="bar-card">
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
                                        <img src="https://i.imgur.com/qx5kdDU.png" alt="Настройки" class="btn-icon" style="width: 18px; height: 18px; margin-top: 3px;"/> 
                                        <div style="margin-left: 4px; margin-top: 3px;">{{ bar.rating ?? '—' }}</div>
                                    </div>
                                </div>
                                
                            </div>
                            <p class="bar-description" @click="goToBar(bar.id)" style="cursor: pointer;">
                                {{ bar.description }}
                            </p>

                            <!-- Горизонтальная галерея коктейлей -->
                            <div class="cocktail-gallery" v-if="bar.cocktails?.length">
                                <div class="cocktail-item" v-for="(cocktail, index) in bar.cocktails.slice(0, 6)" :key="cocktail.id">
                                    <img :src="cocktail.gallery?.[0]?.image_url || placeholder2" alt="Cocktail" />
                                    <!-- Если последний видимый элемент и есть ещё -->
                                    <div
                                    v-if="index === 5 && bar.cocktails.length > 6"
                                    class="cocktail-overlay"
                                    >
                                    +{{ bar.cocktails.length - 6 }}
                                    </div>
                                </div>
                            </div>

                            <div class="tags">
                                <span v-for="tag in bar.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
                            </div>
                            <div class="footer">
                                <span class="address">📍 {{ bar.address }}</span>
                                <span class="phone">📞 {{ bar.phone }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div> 
    </div>

    <!-- Модалка тегов -->
    <div v-if="showTagModal" class="modal-overlay" @click.self="showTagModal = false">
      <div class="modal">
        <h3>Выберите теги</h3>
        <div class="checkboxes">
          <label v-for="tag in allTags" :key="tag" style="display: relative;">
            <input type="checkbox" :value="tag" v-model="selectedTags" />
            {{ tag }}
          </label>
        </div>
        <button @click="showTagModal = false">Применить</button>
      </div>
    </div>

    <!-- Модалка карты -->
    <div v-if="showMapModal" class="map-modal" @click.self="showMapModal = false">
      <div class="map-content">
        <h2>Здесь будет карта :)</h2>
        <!-- <button @click="showMapModal = false">Закрыть</button> -->
      </div>
    </div>

    <!-- Попап галереии -->
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

import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const bars = ref([])
const searchQuery = ref('')
const favoriteIds = ref([])
const selectedTags = ref([])
const allTags = ['вино', 'живая музыка', 'диджей', 'пиво', 'авторское', 
                'уют', 'вечеринки', 'тишина', 'свидание', 'для компании', 
                'шумно', 'караоке']

const cities = ['Ростов-на-Дону', 'Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск']
const selectedCity = ref(cities[0])
const showCityDropdown = ref(false)

const showTagModal = ref(false)
const showMapModal = ref(false)

const showImageModal = ref(false)
const modalImages = ref([])

const placeholder = 'https://images.unsplash.com/photo-1597290282695-edc43d0e7129?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YmFyfGVufDB8fDB8fHww'
const placeholder2 = 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y29ja3RhaWx8ZW58MHx8MHx8fDA%3D'

const isLoading = ref(true)

onMounted(async () => {
  try {
    // — логин, получение токена и создание authAxios (то, что у тебя уже есть) —
    const params = new URLSearchParams()
    params.append('username', 'user')
    params.append('password', 'user')
    const loginRes = await axios.post('/api/auth/login', params)
    const token = loginRes.data.access_token
    localStorage.setItem('access_token', token)

    const authAxios = axios.create({
      headers: { Authorization: `Bearer ${token}` }
    })

    // список id избранных баров
    const favRes = await authAxios.get('/api/users/favorites/bars/')
    const favoriteIds = favRes.data.map(b => b.id)

    // получаем сами бары
    const barsRes = await authAxios.get('/api/bars/')
    const barsData = barsRes.data

    const barsWithCocktails = await Promise.all(
      barsData.map(async bar => {
        // коктейли бара
        const cocktailsRes = await authAxios.get(`/api/bars/${bar.id}/cocktails/`)
        const rawCocktails = cocktailsRes.data

        // для каждого коктейля галерея
        const cocktailsWithGallery = await Promise.all(
          rawCocktails.map(async cocktail => {
            const galRes = await authAxios.get(
              `/api/cocktails/${cocktail.id}/gallery`
            )
            return {
              ...cocktail,
              gallery: galRes.data
            }
          })
        )

        return {
          ...bar,
          isFavorite: favoriteIds.includes(bar.id),
          cocktails: cocktailsWithGallery
        }
      })
    )

    bars.value = barsWithCocktails
  } catch (err) {
    console.error('Ошибка при загрузке данных:', err)
  } finally {
    isLoading.value = false
  }
})

const filteredBars = computed(() => {
  return bars.value.filter(bar => {
    const matchesSearch = bar.name.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesTags = selectedTags.value.length === 0 || selectedTags.value.every(tag =>
      bar.tags?.some(t => t.name === tag)
    )

    return matchesSearch && matchesTags
  })
})

function toggleCityDropdown() {
    showCityDropdown.value = !showCityDropdown.value
}

function selectCity (city) {
    selectedCity.value = city
    showCityDropdown.value = false
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

function openImageModal(gallery) {
  modalImages.value = gallery.length ? gallery : [{ image_url: placeholder }]
  showImageModal.value = true
}

function closeImageModal() {
  showImageModal.value = false
}

function goToBar(id) {
  router.push({ name: 'BarDetailed', params: { id } })
}
</script>

<style scoped>
.home {
  padding: 16px;
  background: #181818;
  color: #fff;
  font-family: sans-serif;
  max-width: 352px;
}
.search-bar {
  margin-bottom: 0px;
}
.search-input {
  width: 100%;
  height: 16px;
  padding: 8px;
  padding-right: 8px;
  border-radius: 8px;
  border: none;
  font-size: 16px;
  background-color: #222222;
  color: #858585;
}
.actions {
  display: flex;
  gap: 8px;
  padding-left: 8px;
}
.actions button {
  background: #222222;
  width: 32px;
  height: 32px;
  color: white;
  padding: 4px 4px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.btn-icon {
    width: 24px; 
    height: 24px; 
    object-fit: contain;
}
.filters {
  margin-top: 4px;
  margin-bottom: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;

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
.bar-container {
    height: calc(100vh - 142px);
    overflow-y: scroll;
}
.bar-container::-webkit-scrollbar {
  height: 2px;
  width: 2px;
}
.bar-container::-webkit-scrollbar-track {
  background: transparent;
}
.bar-container::-webkit-scrollbar-thumb {
  background-color: #FF7700;
  border-radius: 4px;
}
.bar-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.bar-card {
  background: #222222;
  border-radius: 12px;
  overflow: hidden;
  height: 344px !important;
  text-align: left;
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
.bar-info h3 {
  margin: 0;
  font-size: 18px;
}
.bar-info p {
  font-size: 14px;
  margin: 8px 0;
}
.bar-description {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
    text-overflow: ellipsis;
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

/* лента коктейлей */
.cocktail-gallery {
  display: flex;
  overflow-x: auto;
  gap: 7.5px;
  margin-top: 12px;
  padding-bottom: 4px;
  scrollbar-width: none;
}
.cocktail-gallery::-webkit-scrollbar {
  display: none;
}
.cocktail-item {
  position: relative;
  flex: 0 0 auto;
  width: 48px;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
}
.cocktail-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.cocktail-overlay {
  position: absolute;
  top: 0;
  right: 0;
  background: orange;
  color: white;
  font-size: 12px;
  font-weight: bold;
  padding: 2px 6px;
  border-bottom-left-radius: 8px;
}

.footer {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  font-size: 13px;
  opacity: 0.8;
  color: #FF7700;
}

/* Выбор города */
.city-selector {
  margin: 6px 0;
  height: 24px;
  color: #ccc;
  cursor: pointer;
  position: relative;
  font-size: 15px;
  text-align: left;
}
.city-dropdown {
  position: absolute;
  background: #2c2c2c;
  border: 1px solid #444;
  border-radius: 8px;
  margin-top: 4px;
  z-index: 5;
  width: max-content;
}
.city-option {
  padding: 8px 12px;
  cursor: pointer;
}
.city-option:hover {
  background: #444;
}

/* МОДАЛКИ */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}
.modal {
  background: #2c2c2c;
  padding: 24px;
  border-radius: 12px;
  width: 300px;
  color: #fefefe;
}
.checkboxes {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
}
.modal button {
  padding: 8px 12px;
  background: #444;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
}

.map-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 20;
  display: flex;
  justify-content: center;
  align-items: center;
}
.map-content {
  background: #1e1e1e;
  padding: 32px;
  border-radius: 16px;
  color: white;
  text-align: center;
  width: 90%;
  max-width: 500px;
}

/* Попап фото */
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
  border: 4px solid rgba(255,255,255,0.2);
  border-top-color: #FF7700;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>