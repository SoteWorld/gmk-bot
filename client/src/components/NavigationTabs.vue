<template>
  <div class="nav-tabs">
    <router-link to="/products" class="nav-tab" :class="isProducts ? 'tab-active' : 'tab-inactive'">
      <PackageIcon class="tab-icon" />
      <span>Новые продукты</span>
    </router-link>
    <router-link to="/stores" class="nav-tab" :class="isStores ? 'tab-active' : 'tab-inactive'">
      <MapPin class="tab-icon" />
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

<style scoped>
.nav-tabs {
  display: flex;
  background-color: #ffffff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 1001;
}

.nav-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.75rem 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  text-align: center;
  border-bottom: 2px solid transparent;
  text-decoration: none;
  transition:
    color 0.2s,
    background-color 0.2s;
}

.tab-icon {
  width: 1rem;
  height: 1rem;
}

.tab-active {
  color: #dc2626;
  border-bottom-color: #dc2626;
  background-color: #fef2f2;
}

.tab-inactive {
  color: #4b5563;
}

.tab-inactive:hover {
  color: #dc2626;
  background-color: #f9fafb;
}
</style>
