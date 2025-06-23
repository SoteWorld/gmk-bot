<template>
  <div class="products-view">
    <h1>Products</h1>
    <select v-model="selected" @change="loadProducts">
      <option disabled value="">Select category</option>
      <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
    </select>
    <ul>
      <li v-for="p in products" :key="p.id">
        <strong>{{ p.name }}</strong>
        <span v-if="p.expiration_date"> ({{ p.expiration_date }})</span>
        <div v-if="p.image"><img :src="p.image" alt="" width="100" /></div>
        <small v-if="p.ingredients">{{ p.ingredients }}</small>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchCategories, fetchProducts } from '../api'
import type { Product } from '../api'

const categories = ref<string[]>([])
const selected = ref('')
const products = ref<Product[]>([])

async function loadCategories() {
  categories.value = await fetchCategories()
  if (categories.value.length && !selected.value) {
    selected.value = categories.value[0]
    await loadProducts()
  }
}

async function loadProducts() {
  if (!selected.value) return
  products.value = await fetchProducts(selected.value)
}

onMounted(loadCategories)
</script>

<style scoped>
.products-view select {
  margin-bottom: 1rem;
}
.products-view img {
  display: block;
  margin: 0.5rem 0;
}
</style>