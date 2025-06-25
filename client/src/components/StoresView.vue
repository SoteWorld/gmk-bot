<template>
  <div class="stores-view">
    <div class="stores-header">
      <h2 class="stores-title">{{ location ? 'Ближайшие магазины' : 'Все магазины' }}</h2>
      <button @click="loadStores" class="refresh-button">
        <RefreshCw :class="['refresh-icon', loading ? 'spin' : '']" />
        <span>Обновить</span>
      </button>
    </div>

    <div v-if="loading" class="loading-container">
      <Loader2 class="loader-icon" />
    </div>

    <div v-else>
      <div class="map-container">
        <StoreMap :stores="stores" :userLocation="location" :selectedStore="selectedStore" />
      </div>
      <div v-if="stores.length === 0" class="empty-text">Магазины не найдены</div>
      <div class="stores-grid">
        <StoreCard
          v-for="s in stores"
          :key="s.id"
          :store="s"
          :showDistance="!!location"
          :onShowRoute="location ? showRoute : undefined"
        />
      </div>
      <p v-if="error" class="error-text">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Loader2, RefreshCw } from 'lucide-vue-next'
import { fetchNearbyStores } from '../api'
import type { StoreWithDistance as Store } from '../api'
import StoreCard from './StoreCard.vue'
import StoreMap from './StoreMap.vue'

const stores = ref<Store[]>([])
const loading = ref(false)
const error = ref('')
const location = ref<{ latitude: number; longitude: number } | null>(null)
const selectedStore = ref<Store | null>(null)

async function loadStores() {
  if (!navigator.geolocation) {
    error.value = 'Геолокация не поддерживается.'
    return
  }
  loading.value = true
  error.value = ''
  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      try {
        const { latitude, longitude } = pos.coords
        location.value = { latitude, longitude }
        // Запрашиваем все магазины, чтобы показать их на карте
        stores.value = await fetchNearbyStores(latitude, longitude, 1000)
      } catch (e) {
        error.value = 'Не удалось загрузить список магазинов'
      } finally {
        loading.value = false
      }
    },
    () => {
      error.value = 'Невозможно получить местоположение'
      loading.value = false
    },
  )
}

function showRoute(store: Store) {
  selectedStore.value = store
  if (store.route_url) window.open(store.route_url, '_blank')
}

onMounted(loadStores)
</script>

<style scoped>
.stores-view {
  padding: 0.75rem;
}

.stores-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.stores-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827; /* gray-900 */
  margin-block-start: 0;
  margin-block-end: 0;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #dc2626; /* red-600 */
  font-size: 0.875rem;
  transition: color 0.3s;
  background: transparent;
  border: none;
}

.refresh-button:hover {
  color: #b91c1c; /* red-700 */
}

.refresh-icon {
  height: 0.75rem;
  width: 0.75rem;
}

.spin {
  animation: spin 1s linear infinite;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: 2rem 0;
}

.loader-icon {
  height: 1.5rem;
  width: 1.5rem;
  color: #dc2626; /* red-600 */
  animation: spin 1s linear infinite;
}

.map-container {
  margin-bottom: 1rem;
}

.empty-text {
  text-align: center;
  color: #4b5563; /* gray-600 */
}

.stores-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.error-text {
  color: #dc2626; /* red-600 */
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>