<template>
  <div class="store-card">
    <div class="store-card-header">
      <h3 class="store-card-name">{{ store.name }}</h3>
      <div v-if="showDistance" class="store-card-distance">
        <MapPin class="store-card-distance-icon" />
        <span class="store-card-distance-text">{{ store.distance.toFixed(1) }} км</span>
      </div>
    </div>

    <div class="store-card-details">
      <div class="store-card-address">
        <MapPin class="store-card-address-icon" />
        <span class="store-card-address-text">{{ store.address }}</span>
      </div>
      <div v-if="store.opening_hours" class="store-card-hours">
        <Clock class="store-card-hours-icon" />
        <span class="store-card-hours-text">{{ store.opening_hours }}</span>
      </div>
      <div v-if="store.phone" class="store-card-phone">
        <Phone class="store-card-phone-icon" />
        <button @click="handlePhoneClick" class="store-card-phone-text">
          {{ store.phone }}
        </button>
      </div>
    </div>

    <button v-if="onShowRoute" @click="onShowRoute(store)" class="store-card-route-button">
      <Navigation class="store-card-route-icon" />
      <span>Построить маршрут</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { MapPin, Clock, Phone, Navigation } from 'lucide-vue-next'
import type { StoreWithDistance as Store } from '../api'

const props = defineProps<{
  store: Store
  onShowRoute?: (s: Store) => void
  showDistance?: boolean
}>()
const emit = defineEmits(['showRoute'])

const onShowRoute = props.onShowRoute
const showDistance = props.showDistance ?? true

function handlePhoneClick() {
  if (props.store.phone) window.open(`tel:${props.store.phone}`, '_self')
}
</script>

<style scoped>
.store-card {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  border: 1px solid #f3f4f6;
  padding: 0.75rem;
}

.store-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.store-card-name {
  font-weight: 600;
  font-size: 1rem;
  color: #111827;
  flex: 1 1 0;
  line-height: 1.25;
  margin-block-start: 0.1rem;
  margin-block-end: 0.1rem;
}

.store-card-distance {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #dc2626;
  font-weight: 500;
  margin-left: 0.5rem;
}

.store-card-distance-icon,
.store-card-address-icon,
.store-card-hours-icon,
.store-card-phone-icon,
.store-card-route-icon {
  width: 0.75rem;
  height: 0.75rem;
}

.store-card-address-icon {
  margin-top: 0.125rem;
  flex-shrink: 0;
}

.store-card-distance-text,
.store-card-address-text,
.store-card-hours-text,
.store-card-phone-text {
  font-size: 0.75rem;
}

.store-card-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.75rem;
}

.store-card-address {
  display: flex;
  align-items: flex-start;
  gap: 0.25rem;
  color: #4b5563;
}

.store-card-address-text {
  line-height: 1.625;
}

.store-card-hours,
.store-card-phone {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #4b5563;
}

.store-card-phone-text {
  color: #dc2626;
  text-decoration: underline;
  transition: color 0.2s;
  background: transparent;
  border: none;
}

.store-card-phone-text:hover {
  color: #b91c1c;
}

.store-card-route-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  background-color: #dc2626;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.store-card-route-button:hover {
  background-color: #b91c1c;
}
</style>
