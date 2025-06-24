<template>
  <header class="header">
    <div class="header-container">
      <Beef class="header-icon" />
      <div class="header-text">
        <h1 class="header-title">Гомельский мясокомбинат</h1>
        <p class="header-subtitle">Качество, проверенное временем</p>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Beef } from 'lucide-vue-next'
</script>

<style scoped>
@reference utilities;
.header {
  @apply bg-red-700 text-white px-4 py-4 shadow-sm;
}

.header-container {
  @apply flex items-center justify-center space-x-2;
}

.header-icon {
  @apply h-6 w-6 text-white;
}

.header-text {
  @apply text-center;
}

.header-title {
  @apply text-base font-bold;
}

.header-subtitle {
  @apply text-red-100 text-xs;
}
</style>