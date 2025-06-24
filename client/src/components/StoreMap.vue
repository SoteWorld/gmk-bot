<template>
    <div ref="mapRef" class="store-map" />
</template>

<script setup lang="ts">
import { onMounted, watch, ref } from 'vue'
import L from 'leaflet'
import type { StoreWithDistance as Store, StoreWithDistance } from '../api'

const props = defineProps<{
  stores: Store[]
  userLocation: { latitude: number; longitude: number } | null
  selectedStore?: Store | null
}>()

const mapRef = ref<HTMLDivElement | null>(null)
let map: L.Map | null = null

function initMap() {
  if (mapRef.value && !map) {
    map = L.map(mapRef.value).setView([53.9, 27.5], 11)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
    }).addTo(map)
  }
}

function updateMarkers() {
  if (!map) return
  map.eachLayer((layer: any) => {
    if (layer instanceof L.Marker) map!.removeLayer(layer)
  })
  if (props.userLocation) {
    const userIcon = L.divIcon({
      html: '<div class="user-location-dot"></div>',
      className: 'user-location-marker',
      iconSize: [12, 12],
      iconAnchor: [6, 6],
    })
    L.marker([props.userLocation.latitude, props.userLocation.longitude], { icon: userIcon })
      .bindPopup('Ваше местоположение')
      .addTo(map)
  }
  props.stores.forEach((store) => {
    const isSelected = props.selectedStore?.id === store.id
    const storeIcon = L.divIcon({
      html: `<div class="store-marker-dot ${isSelected ? 'store-marker-selected' : ''}">
                <div class="store-marker-dot-inner"></div>
              </div>`,
      className: 'store-marker',
      iconSize: [20, 20],
      iconAnchor: [10, 10],
    })
    L.marker([store.latitude!, store.longitude!], { icon: storeIcon })
      .bindPopup(
        `
        <div class="p-2 min-w-[200px]">
          <h3 class="font-semibold text-sm mb-1">${store.name}</h3>
          <p class="text-xs text-gray-600 mb-1">${store.address}</p>
          <p class="text-xs text-gray-600 mb-1">${store.opening_hours ?? ''}</p>
          ${props.userLocation ? `<p class="text-xs font-medium text-red-600">${store.distance.toFixed(1)} км</p>` : ''}
        </div>
      `
      )
      .addTo(map!)
  })
  if (props.stores.length > 0) {
    const group = new L.FeatureGroup()
    props.stores.forEach((store) => {
      group.addLayer(L.marker([store.latitude!, store.longitude!]))
    })
    if (props.userLocation) {
      group.addLayer(L.marker([props.userLocation.latitude, props.userLocation.longitude]))
    }
    map.fitBounds(group.getBounds().pad(0.1))
  }
}

onMounted(() => {
  initMap()
  updateMarkers()
})

watch(() => [props.stores, props.userLocation, props.selectedStore], updateMarkers, { deep: true })
</script>

<style scoped>
.store-map {
  width: 100%;
  height: 12rem; /* 48 */
  border-radius: 0.5rem; /* rounded-lg */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb; /* gray-200 */
}

.user-location-dot {
  background-color: #3b82f6; /* blue-500 */
  border-radius: 9999px;
  width: 0.75rem; /* w-3 */
  height: 0.75rem; /* h-3 */
  border: 2px solid #ffffff;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.store-marker-dot {
  background-color: #ef4444; /* red-500 */
  border-radius: 9999px;
  width: 1.25rem; /* w-5 */
  height: 1.25rem; /* h-5 */
  border: 2px solid #ffffff;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  justify-content: center;
}

.store-marker-selected {
  box-shadow: 0 0 0 2px #fca5a5;
}

.store-marker-dot-inner {
  background-color: #ffffff;
  border-radius: 9999px;
  width: 0.375rem; /* w-1.5 */
  height: 0.375rem; /* h-1.5 */
}

.user-location-marker {
  background: transparent !important;
  border: none !important;
}

.store-marker {
  background: transparent !important;
  border: none !important;
}

.leaflet-popup-content-wrapper {
  border-radius: 8px;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.leaflet-popup-tip {
  background-color: white;
}
</style>
