<template>
  <div class="stores-view">
    <h1>Nearby Stores</h1>
    <button @click="loadStores" :disabled="loading">
      {{ loading ? 'Loading...' : 'Load stores' }}
    </button>
    <ul>
      <li v-for="s in stores" :key="s.id">
        <strong>{{ s.name }}</strong> - {{ s.address }} ({{ s.distance.toFixed(2) }} km)
        <div v-if="s.route_url"><a :href="s.route_url" target="_blank">Route</a></div>
      </li>
    </ul>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { fetchNearbyStores } from '../api'
import type { StoreWithDistance } from '../api'

const stores = ref<StoreWithDistance[]>([])
const loading = ref(false)
const error = ref('')

async function loadStores() {
  if (!navigator.geolocation) {
    error.value = 'Geolocation is not supported.'
    return
  }
  loading.value = true
  error.value = ''
  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      try {
        const { latitude, longitude } = pos.coords
        stores.value = await fetchNearbyStores(latitude, longitude)
      } catch (e) {
        error.value = 'Failed to load stores'
      } finally {
        loading.value = false
      }
    },
    () => {
      error.value = 'Unable to get location'
      loading.value = false
    },
  )
}
</script>

<style scoped>
.stores-view button {
  margin-bottom: 1rem;
}
.error {
  color: red;
}
</style>