<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-3">
    <div class="flex justify-between items-start mb-2">
      <h3 class="font-semibold text-base text-gray-900 flex-1 leading-tight">{{ store.name }}</h3>
      <div v-if="showDistance" class="flex items-center space-x-1 text-red-600 font-medium ml-2">
        <MapPin class="h-3 w-3" />
        <span class="text-xs">{{ store.distance.toFixed(1) }} км</span>
      </div>
    </div>

    <div class="space-y-1 mb-3">
      <div class="flex items-start space-x-1 text-gray-600">
        <MapPin class="h-3 w-3 mt-0.5 flex-shrink-0" />
        <span class="text-xs leading-relaxed">{{ store.address }}</span>
      </div>
      <div v-if="store.opening_hours" class="flex items-center space-x-1 text-gray-600">
        <Clock class="h-3 w-3" />
        <span class="text-xs">{{ store.opening_hours }}</span>
      </div>
      <div v-if="store.phone" class="flex items-center space-x-1 text-gray-600">
        <Phone class="h-3 w-3" />
        <button @click="handlePhoneClick" class="text-xs text-red-600 hover:text-red-700 transition-colors underline">
          {{ store.phone }}
        </button>
      </div>
    </div>

    <button v-if="onShowRoute" @click="onShowRoute(store)" class="w-full flex items-center justify-center space-x-1 bg-red-600 text-white py-2 px-3 rounded-lg hover:bg-red-700 transition-colors text-sm">
      <Navigation class="h-3 w-3" />
      <span>Построить маршрут</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { MapPin, Clock, Phone, Navigation } from 'lucide-vue-next'
import type { StoreWithDistance as Store } from '../api'

const props = defineProps<{ store: Store; onShowRoute?: (s: Store) => void; showDistance?: boolean }>()
const emit = defineEmits(['showRoute'])

const onShowRoute = props.onShowRoute
const showDistance = props.showDistance ?? true

function handlePhoneClick() {
  if (props.store.phone) window.open(`tel:${props.store.phone}`, '_self')
}
</script>

<style scoped></style>