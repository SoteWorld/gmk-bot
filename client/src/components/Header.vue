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
.header {
  background-color: #b91c1c; /* red-700 */
  color: white;
  padding: 1rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.header-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
.header-icon {
  height: 1.5rem;
  width: 1.5rem;
  text-align: center;
}

.header-title {
  font-size: 1rem;
  font-weight: 700;
}

.header-subtitle {
  color: #fee2e2;
  font-size: 0.75rem;
}

.header-title {
  font-size: 1rem;
  font-weight: 700;
}

.header-subtitle {
  color: #fee2e2;
  font-size: 0.75rem;
}
</style>
