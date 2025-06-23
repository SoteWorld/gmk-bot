<template>
  <div class="flex bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
    <router-link
      to="/products"
      class="flex-1 flex items-center justify-center space-x-1 py-3 px-2 text-sm font-medium transition-colors"
      :class="isProducts ? 'text-red-600 border-b-2 border-red-600 bg-red-50' : 'text-gray-600 hover:text-red-600 hover:bg-gray-50'"
    >
      <PackageIcon class="h-4 w-4" />
      <span>Новые продукты</span>
    </router-link>
    <router-link
      to="/stores"
      class="flex-1 flex items-center justify-center space-x-1 py-3 px-2 text-sm font-medium transition-colors"
      :class="isStores ? 'text-red-600 border-b-2 border-red-600 bg-red-50' : 'text-gray-600 hover:text-red-600 hover:bg-gray-50'"
    >
      <MapPin class="h-4 w-4" />
      <span>Ближайшие магазины</span>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Package as PackageIcon, MapPin } from 'lucide-vue-next'

const route = useRoute()
const isProducts = computed(() => route.path === '/products')
const isStores = computed(() => route.path === '/stores')
</script>

<style scoped></style>