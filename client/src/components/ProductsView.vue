<template>
  <div class="products-view">
    <div class="products-header">
      <h2 class="products-title">Новые продукты</h2>
      <button @click="loadProducts" class="refresh-button">
        <RefreshCw :class="['refresh-icon', loading ? 'spin' : '']" />
        <span>Обновить</span>
      </button>
    </div>

    <div v-if="categories.length" class="categories-list">
      <button
        v-for="cat in categories"
        :key="cat"
        @click="selectCategory(cat)"
        class="category-button"
        :class="cat === selected ? 'category-active' : 'category-inactive'"
      >
        {{ categoryNames[cat] ?? cat }}
      </button>
    </div>

    <div v-if="loading" class="loading-container">
      <Loader2 class="loading-icon" />
      <span class="loading-text">
        <span>Данные загружаются...</span>
        <span>Обычно это длится не более 30 секунд. Ожидайте!</span>
      </span>
    </div>

    <div v-else>
      <div v-if="products.length === 0" class="empty-message">Список пуст</div>
      <div class="products-grid">
        <ProductCard v-for="p in products" :key="p.id" :product="p" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Loader2, RefreshCw } from 'lucide-vue-next'
import { fetchCategories, fetchProducts } from '../api'
import type { Product } from '../api'
import ProductCard from './ProductCard.vue'

const categoryNames: Record<string, string> = {
  fresh: 'Новинки',
  sausages: 'Сосиски и сардельки',
  smoked_meats: 'Копчености',
  boiled_sausage: 'Вареные колбасы',
  boiled_sausages: 'Вареные колбасы',
  'cooked-smoked_semi-smoked': 'В/К колбасы, полукопченые колбасы',
  semi_finished: 'Полуфабрикаты',
  dumplings: 'Пельмени',
  other: 'Прочие изделия',
  'raw-smoked_dry-cured': 'Сырокопченые, сыровяленые колбасы',
}

const categories = ref<string[]>([])
const selected = ref('')
const products = ref<Product[]>([])
const loading = ref(false)

async function loadCategories() {
  categories.value = await fetchCategories()
  if (categories.value.length && !selected.value) {
    selected.value = categories.value[0]
    await loadProducts()
  }
}

function selectCategory(cat: string) {
  if (cat === selected.value) return
  selected.value = cat
  loadProducts()
}

async function loadProducts() {
  if (!selected.value) return
  loading.value = true
  try {
    products.value = await fetchProducts(selected.value)
  } finally {
    loading.value = false
  }
}

onMounted(loadCategories)
</script>

<style scoped>
.products-view {
  padding: 0.75rem;
}

.products-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.products-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
  margin-block-start: 0;
  margin-block-end: 0;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #dc2626;
  font-size: 0.875rem;
  transition: color 0.2s;
  background: transparent;
  border: none;
}

.refresh-button:hover {
  color: #b91c1c;
}

.refresh-icon {
  width: 0.75rem;
  height: 0.75rem;
}

.categories-list {
  display: flex;
  overflow-x: auto;
  gap: 0.5rem;
  margin-bottom: 1rem;
  scrollbar-width: none; /* Hide scrollbar in Firefox */
  -ms-overflow-style: none; /* Hide scrollbar in IE and Edge */
}

.categories-list::-webkit-scrollbar {
  display: none; /* Hide scrollbar in Chrome, Safari, Opera */
}

.category-button {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  border-width: 1px;
  white-space: nowrap;
  font-size: 0.875rem;
  transition:
    color 0.2s,
    background-color 0.2s,
    border-color 0.2s;
}

.category-active {
  background-color: #dc2626;
  color: white;
  border-color: #dc2626;
}

.category-inactive {
  background-color: white;
  color: #4b5563;
  border-color: #d1d5db;
}

.category-inactive:hover {
  background-color: #fef2f2;
  color: #dc2626;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
}

.loading-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #dc2626;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 0.5rem;
  color: #4b5563;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-message {
  text-align: center;
  color: #4b5563;
}

.products-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
