<template>
  <div class="product-card">
    <div class="product-card-image">
      <img
        :src="product.image || placeholder"
        :alt="product.name"
        class="product-card-img"
        @error="onError"
      />
    </div>
    <div class="product-card-content">
      <h3 class="product-card-name">{{ product.name }}</h3>
      <div v-if="product.expiration_date" class="product-card-expiration">
        <Calendar class="product-card-expiration-icon" />
        <span class="product-card-expiration-text">Срок годности: {{ product.expiration_date}}</span>
      </div>
      <div v-if="product.ingredients" class="product-card-ingredients">
        <List class="product-card-ingredients-icon" />
        <span class="product-card-ingredients-text line-clamp-2">{{ product.ingredients }}</span>
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
</script>

<style scoped>
.product-card {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  border: 1px solid #f3f4f6;
  overflow: hidden;
}

.product-card-image {
  aspect-ratio: 4 / 3;
  background-color: #f3f4f6;
  overflow: hidden;
}

.product-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-card-content {
  padding: 0.75rem;
}

.product-card-name {
  font-weight: 600;
  font-size: 1rem;
  color: #111827;
  margin-bottom: 0.5rem;
  line-height: 1.25;
}

.product-card-expiration,
.product-card-ingredients {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #4b5563;
  font-size: 0.75rem;
  margin-bottom: 0.5rem;
}

.product-card-ingredients {
  align-items: flex-start;
}

.product-card-expiration-icon,
.product-card-ingredients-icon {
  width: 0.75rem;
  height: 0.75rem;
}

.product-card-ingredients-icon {
  margin-top: 0.125rem;
  flex-shrink: 0;
}

.product-card-expiration-text,
.product-card-ingredients-text {
  font-size: 0.75rem;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
