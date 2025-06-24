<template>
  <div class="p-3">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-bold text-gray-900">Новые продукты</h2>
      <button
        @click="loadProducts"
        class="flex items-center space-x-1 text-red-600 hover:text-red-700 transition-colors text-sm"
      >
        <RefreshCw :class="['h-3 w-3', loading ? 'animate-spin' : '']" />
        <span>Обновить</span>
      </button>
    </div>

    <div v-if="categories.length" class="flex overflow-x-auto space-x-2 mb-4">
      <button
        v-for="cat in categories"
        :key="cat"
        @click="selectCategory(cat)"
        class="px-3 py-1 rounded-full border whitespace-nowrap text-sm transition-colors"
        :class="cat === selected ? 'bg-red-600 text-white border-red-600' : 'bg-white text-gray-600 border-gray-300 hover:bg-red-50 hover:text-red-600'"
      >
        {{ categoryNames[cat] ?? cat }}
      </button>
    </div>

    <div v-if="loading" class="flex justify-center py-8">
      <Loader2 class="h-6 w-6 text-red-600 animate-spin" />
    </div>

    <div v-else>
      <div v-if="products.length === 0" class="text-center text-gray-600">Список пуст</div>
      <div class="grid grid-cols-1 gap-3">
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
  'raw-smoked_dry-cyred': 'Сырокопченые, сыровяленые колбасы',
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

<style scoped></style>