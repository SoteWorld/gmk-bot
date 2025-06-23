<template>
  <header class="bg-gradient-to-r from-red-600 to-red-700 text-white px-4 py-4 shadow-sm">
    <div class="flex items-center justify-center space-x-2">
      <Beef class="h-6 w-6" />
      <div class="text-center">
        <h1 class="text-lg font-bold">Гомельский мясокомбинат</h1>
        <p class="text-red-100 text-xs">Качество, проверенное временем</p>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Beef } from 'lucide-vue-next'
</script>

<style scoped></style>