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

  const validStores = props.stores.filter((s) => s.latitude != null && s.longitude != null)

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

  validStores.forEach((store) => {
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
          <div class="flex justify-between items-center mb-1">
            <h3 class="font-semibold text-sm">${store.name}</h3>
            ${props.userLocation ? `<div class="popup-distance">
              <svg class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0" />
                <circle cx="12" cy="10" r="3" />
              </svg>
              <span>${store.distance.toFixed(1)} км</span>
            </div>` : ''}
          </div>
          <div class="popup-details">
            <div class="popup-line address">
              <svg class="popup-icon mt-[2px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0" />
                <circle cx="12" cy="10" r="3" />
              </svg>
              <span class="text-xs">${store.address}</span>
            </div>
            ${store.opening_hours ? `<div class="popup-line">
              <svg class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
              <span class="text-xs">${store.opening_hours}</span>
            </div>` : ''}
            ${store.phone ? `<div class="popup-line">
              <svg class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384" />
              </svg>
              <a href="tel:${store.phone}" class="text-xs text-red-600 underline">${store.phone}</a>
            </div>` : ''}
          </div>
          ${store.route_url ? `<a href="${store.route_url}" target="_blank" class="popup-route-button">
            <svg class="popup-icon" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="3 11 22 2 13 21 11 13 3 11" />
            </svg>
            <span>Построить маршрут</span>
          </a>` : ''}
        </div>
      `
      )
      .addTo(map!)
  })
  const group = new L.FeatureGroup()
  validStores.forEach((store) => {
    group.addLayer(L.marker([store.latitude!, store.longitude!]))
  })
  if (props.userLocation) {
    group.addLayer(L.marker([props.userLocation.latitude, props.userLocation.longitude]))
  }

  if (group.getLayers().length > 0) {
    map.fitBounds(group.getBounds().pad(0.1))
  } else if (props.userLocation) {
    map.setView([props.userLocation.latitude, props.userLocation.longitude], 13)
  } else {
    map.setView([53.9, 27.5], 11)
  }
}

onMounted(() => {
  initMap()
  updateMarkers()
})

watch(() => [props.stores, props.userLocation, props.selectedStore], updateMarkers, { deep: true })
</script>

<style>
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
  border-radius: 0.25rem; /* square with slight rounding */
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
  border-radius: 0.25rem; /* square with slight rounding */
  transform: rotate(-45deg);
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

.popup-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.popup-line {
  display: flex;
  gap: 0.25rem;
  color: #4b5563;
  align-items: center;
}

.popup-line.address {
  align-items: flex-start;
}

.popup-icon {
  width: 0.75rem;
  height: 0.75rem;
  flex-shrink: 0;
}

.popup-distance {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #dc2626;
  font-weight: 500;
  font-size: 0.75rem;
}

.popup-route-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  background-color: #dc2626;
  color: #ffffff !important;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.popup-route-button svg {
  fill: currentColor;
  stroke: currentColor;
}


.popup-route-button:hover {
  background-color: #b91c1c;
}
</style>
