<template>
  <div class="min-h-screen bg-gray-50 max-w-md mx-auto">
    <Header />
    <NavigationTabs />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import Header from './components/Header.vue'
import NavigationTabs from './components/NavigationTabs.vue'
</script>

<style scoped></style>
