<template>
  <div class="favorites-page">

    <div v-if="isLoading" class="loader-container">
        <div class="spinner"></div>
    </div>

    <div class="bar-container">
        <div class="bar-list">
            <div v-for="bar in bars" :key="bar.id" class="bar-card">
                <div class="bar-images" style="display: flex; padding-right: 8px;" @click="openImageModal(bar.gallery)">
                    <img :src="bar.gallery?.[0]?.image_url || placeholder" alt="Bar Image" class="bar-img-main" @click="openGallery(bar)" />
                    <div style="margin-top: 8px;">
                        <img :src="bar.gallery?.[1]?.image_url || placeholder" alt="Bar Image" class="bar-img-sec" />
                        <img :src="bar.gallery?.[2]?.image_url || placeholder" alt="Bar Image" class="bar-img-sec" />
                    </div>
                </div>

                <div class="bar-info">
                    <div style="display: flex; justify-content: space-between;">
                        <h3 @click="goToBar(bar.id)" style="cursor: pointer">{{ bar.name }}</h3>
                        <div style="display: flex;">
                            <button class="favorite-btn" @click="toggleFavorite(bar)">
                                <img
                                    :src="bar.isFavorite ? 'https://i.imgur.com/TEyH0yT.png' : 'https://i.imgur.com/hOQA38l.png'"
                                    alt="favorite"
                                    style="width: 30px; height: 30px;"
                                />
                            </button>
                            <div class="rating">
                                <img src="https://i.imgur.com/qx5kdDU.png" alt="star" style="width: 18px; height: 18px; margin-top: 3px;" />
                                <div style="margin-left: 4px; margin-top: 3px;">{{ bar.rating ?? '—' }}</div>
                            </div>
                        </div>
                    </div>

                    <p class="bar-description">{{ bar.description }}</p>

                    <div class="cocktail-gallery" v-if="bar.cocktails?.length">
                        <div
                            class="cocktail-item"
                            v-for="(cocktail, index) in bar.cocktails.slice(0, 6)"
                            :key="cocktail.id"
                        >
                            <img :src="cocktail.gallery?.[0]?.image_url || placeholder2" alt="Cocktail" />
                            <div v-if="index === 5 && bar.cocktails.length > 6" class="cocktail-overlay">
                                +{{ bar.cocktails.length - 6 }}
                            </div>
                        </div>
                    </div>

                    <div class="tags">
                        <span v-for="tag in bar.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
                    </div>
                    <div class="footer">
                        <span>📍 {{ bar.address }}</span>
                        <span>📞 {{ bar.phone }}</span>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'

const bars = ref([])
const router = useRouter()

const showImageModal = ref(false)
const modalImages = ref([])

const placeholder = 'https://images.unsplash.com/photo-1597290282695-edc43d0e7129?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0'
const placeholder2 = 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0'

const isLoading = ref(true)

onMounted(async () => {
  try {
    // 1. Логин
    const params = new URLSearchParams()
    params.append('username', 'user')
    params.append('password', 'user')

    const loginRes = await axios.post('/api/auth/login', params)
    const token = loginRes.data.access_token
    localStorage.setItem('access_token', token)

    // 2. Авторизованный Axios
    const authAxios = axios.create({
      headers: { Authorization: `Bearer ${token}` }
    })

    // 3. Загружаем избранные бары
    const favoritesRes = await authAxios.get('/api/users/favorites/bars/')
    const favoriteBars = favoritesRes.data

    // 4. Для каждого бара подгружаем коктейли
    const barsWithDetails = await Promise.all(
        favoriteBars.map(async bar => {
        // список коктейлей у бара
        const cocktailsRes = await authAxios.get(`/api/bars/${bar.id}/cocktails/`)
        const cocktailsRaw = cocktailsRes.data

        // для каждого коктейля подгружаем его галерею
        const cocktailsWithGallery = await Promise.all(
            cocktailsRaw.map(async c => {
            try {
                const galRes = await authAxios.get(`/api/cocktails/${c.id}/gallery/`)
                return { ...c, gallery: galRes.data }
            } catch {
                return { ...c, gallery: [] }
            }
            })
        )

        return {
            ...bar,
            isFavorite: true,
            cocktails: cocktailsWithGallery
        }
        })
    )

    bars.value = barsWithDetails
  } catch (err) {
    console.error('Ошибка при загрузке избранных баров:', err)
  } finally {
    isLoading.value = false
  }
})

function toggleFavorite(bar) {
  const token = localStorage.getItem('access_token')
  if (!token) return

  const config = { headers: { Authorization: `Bearer ${token}` } }
  const url = `/api/bars/${bar.id}/favorites/`

  if (bar.isFavorite) {
    axios.delete(url, config)
      .then(() => { bar.isFavorite = false })
      .catch(console.error)
  } else {
    axios.post(url, null, config)
      .then(() => { bar.isFavorite = true })
      .catch(console.error)
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

function openGallery(bar) {
  // если у вас уже реализована модалка — подключите её здесь
}
</script>

<style scoped>
.favorites-page {
  color: #fefefe;
  display: flex; 
  justify-content: center; 
  background-color: #181818; 
  height: 100vh;
}
.title {
  font-size: 22px;
  margin-bottom: 16px;
}

/*  */
.bar-container {
  height: calc(100vh - 58px);
  margin-top: 8px;
  overflow-y: scroll;
  max-width: 352px;

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

.footer {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  font-size: 13px;
  opacity: 0.8;
  color: #FF7700;
}

/* Лоадер */
.loader-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #181818; /* фон под спиннером */
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
</style>
