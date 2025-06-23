<template>
  <div>
    <nav>
      <router-link to="/products">Products</router-link> |
      <router-link to="/stores">Stores</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
nav {
  margin-bottom: 1rem;
}
nav a {
  margin-right: 0.5rem;
}
</style>