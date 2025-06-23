<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
    <div class="aspect-[4/3] bg-gray-100 overflow-hidden">
      <img
        :src="product.image || placeholder"
        :alt="product.name"
        class="w-full h-full object-cover"
        @error="onError"
      />
    </div>
    <div class="p-3">
      <h3 class="font-semibold text-base text-gray-900 mb-2 leading-tight">{{ product.name }}</h3>
      <div v-if="product.expiration_date" class="flex items-center space-x-1 text-gray-600 mb-2">
        <Calendar class="h-3 w-3" />
        <span class="text-xs">Срок: {{ formatDate(product.expiration_date) }}</span>
      </div>
      <div v-if="product.ingredients" class="flex items-start space-x-1 text-gray-600">
        <List class="h-3 w-3 mt-0.5 flex-shrink-0" />
        <span class="text-xs leading-relaxed line-clamp-2">{{ product.ingredients }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Calendar, List } from 'lucide-vue-next'
import type { Product } from '../api'

const props = defineProps<{ product: Product }>()
const placeholder = 'https://images.pexels.com/photos/2611937/pexels-photo-2611937.jpeg'

function onError(e: Event) {
  const target = e.target as HTMLImageElement
  target.src = placeholder
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU')
}
</script>

<style scoped></style>