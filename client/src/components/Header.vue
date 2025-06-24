<template>
  <header class="bg-red-700 text-white px-4 py-4 shadow-sm">
    <div class="flex items-center justify-center space-x-2">
      <Beef class="h-6 w-6 text-white" />
      <div class="text-center">
        <h1 class="text-base font-bold">Гомельский мясокомбинат</h1>
        <p class="text-red-100 text-xs">Качество, проверенное временем</p>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Beef } from 'lucide-vue-next'
</script>

<style scoped>
header {
  background-color: #b91c1c; /* red-700 */
  color: white;
  padding: 1rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.text-red-100 {
  color: #fee2e2;
}
.text-xs {
  font-size: 0.75rem;
}
.text-base {
  font-size: 1rem;
}
.font-bold {
  font-weight: 700;
}
.flex {
  display: flex;
}
.items-center {
  align-items: center;
}
.justify-center {
  justify-content: center;
}
.space-x-2 > :not([hidden]) ~ :not([hidden]) {
  margin-left: 0.5rem;
}
.h-6 {
  height: 1.5rem;
}
.w-6 {
  width: 1.5rem;
}
.text-center {
  text-align: center;
}
</style>
