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
                                <img src="https://i.imgur.com/qx5kdDU.png" alt="Настройки" class="btn-icon" style="width: 18px; height: 18px; margin-top: 3px;"/> 
                                <div style="margin-left: 4px; margin-top: 3px;">{{ bar.rating ?? '—' }}</div>
                            </div>
                        </div>
                        
                    </div>
                    <p class="bar-description" @click="goToBar(bar.id)" style="cursor: pointer;">
                        {{ bar.description }}
                    </p>

                    <!-- Горизонтальная галерея коктейлей -->
                    <!-- <div class="cocktail-gallery" v-if="bar.cocktails?.length">
                        <div class="cocktail-item" v-for="(cocktail, index) in bar.cocktails.slice(0, 6)" :key="cocktail.id">
                            <img :src="cocktail.gallery?.[0]?.image_url || placeholder2" alt="Cocktail" />
                            <div
                            v-if="index === 5 && bar.cocktails.length > 6"
                            class="cocktail-overlay"
                            >
                            +{{ bar.cocktails.length - 6 }}
                            </div>
                        </div>
                    </div> -->

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
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const bar = ref(null)
const placeholder2 = 'https://via.placeholder.com/200?text=Cocktail'

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

    bar.value = barData
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
</script>

<style scoped>
.bar-detail {
  position: relative;
  padding: 16px;
  background: #181818;
  color: #fff;
  font-family: sans-serif;
  max-width: 352px;
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
  height: calc(100vh - 24px);
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
.footer {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  font-size: 13px;
  opacity: 0.8;
  color: #FF7700;
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