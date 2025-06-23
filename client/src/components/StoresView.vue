<template>
  <div class="p-3">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-bold text-gray-900">{{ location ? 'Ближайшие магазины' : 'Все магазины' }}</h2>
      <button @click="loadStores" class="flex items-center space-x-1 text-red-600 hover:text-red-700 transition-colors text-sm">
        <RefreshCw :class="['h-3 w-3', loading ? 'animate-spin' : '']" />
        <span>Обновить</span>
      </button>
    </div>

    <div v-if="loading" class="flex justify-center py-8">
      <Loader2 class="h-6 w-6 text-red-600 animate-spin" />
    </div>

    <div v-else>
      <div class="mb-4">
        <StoreMap :stores="stores" :userLocation="location" :selectedStore="selectedStore" />
      </div>
      <div v-if="stores.length === 0" class="text-center text-gray-600">Магазины не найдены</div>
      <div class="grid grid-cols-1 gap-3">
        <StoreCard
          v-for="s in stores"
          :key="s.id"
          :store="s"
          :showDistance="!!location"
          :onShowRoute="location ? showRoute : undefined"
        />
      </div>
      <p v-if="error" class="text-red-600 mt-2 text-sm">{{ error }}</p>
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
        stores.value = await fetchNearbyStores(latitude, longitude)
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

<style scoped></style>