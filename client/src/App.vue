<template>
  <div class="tg-viewport min-h-screen bg-gray-50 max-w-md mx-auto">
    <Header />
    <NavigationTabs />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import Header from './components/Header.vue'
import NavigationTabs from './components/NavigationTabs.vue'

// Force light theme regardless of Telegram settings
function applyTheme() {
  const root = document.documentElement
  root.style.setProperty('--tg-bg-color', '#ffffff')
  root.style.setProperty('--tg-text-color', '#000000')
}

onMounted(() => {
  applyTheme()
})
</script>

<style>
/* Telegram Web App integration */
:root {
  --tg-bg-color: #ffffff;
  --tg-text-color: #000000;
}

body {
  margin: 0;
  padding: 0;
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell',
    'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--tg-bg-color);
  color: var(--tg-text-color);
  overflow-x: hidden;
}

/* Mobile-first design */
#app {
  max-width: 100vw;
  overflow-x: hidden;
}

/* Touch optimization for mobile */
button,
a {
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}

/* Smooth transitions */
* {
  transition-property:
    color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow,
    transform, filter, backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Custom scrollbar for webkit browsers */
::-webkit-scrollbar {
  width: 4px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #b1b1b1;
  border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
  background: #8f8f8f;
}

/* Image loading placeholder */
img {
  background-color: #f3f4f6;
}

/* Ensure proper mobile viewport */
@media screen and (max-width: 480px) {
  body {
    font-size: 14px;
  }

  .text-xs {
    font-size: 0.75rem;
  }

  .text-sm {
    font-size: 0.875rem;
  }
}

/* Telegram Mini App specific styles */
.tg-viewport {
  height: 100dvh; /* Dynamic viewport height for mobile browsers */
  overflow-y: scroll; /* Keep scrollbar over content to avoid layout shift */
}

/* Prevent horizontal scroll */
html,
body {
  overflow-x: hidden;
  width: 100%;
}

/* Optimize for touch devices */
@media (hover: none) and (pointer: coarse) {
  button:hover {
    transform: none;
  }

  .hover\:shadow-lg:hover {
    box-shadow:
      0 4px 6px -1px rgba(0, 0, 0, 0.1),
      0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
}
</style>
