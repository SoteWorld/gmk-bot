<template>
  <div ref="mapRef" class="w-full h-48 rounded-lg shadow-sm border border-gray-200" />
</template>

<script setup lang="ts">
import { onMounted, watch, ref } from 'vue'
import L from 'leaflet'
import type { StoreWithDistance as Store, StoreWithDistance } from '../api'

const props = defineProps<{ stores: Store[]; userLocation: { latitude: number; longitude: number } | null; selectedStore?: Store | null }>()

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
      html: '<div class="bg-blue-500 rounded-full w-3 h-3 border-2 border-white shadow-md"></div>',
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
      html: `<div class="bg-red-500 rounded-full w-5 h-5 border-2 border-white shadow-md flex items-center justify-center ${isSelected ? 'ring-2 ring-red-300' : ''}">
                <div class="bg-white rounded-full w-1.5 h-1.5"></div>
              </div>`,
      className: 'store-marker',
      iconSize: [20, 20],
      iconAnchor: [10, 10],
    })
    L.marker([store.latitude!, store.longitude!], { icon: storeIcon })
      .bindPopup(`
        <div class="p-2 min-w-[200px]">
          <h3 class="font-semibold text-sm mb-1">${store.name}</h3>
          <p class="text-xs text-gray-600 mb-1">${store.address}</p>
          <p class="text-xs text-gray-600 mb-1">${store.opening_hours ?? ''}</p>
          ${props.userLocation ? `<p class="text-xs font-medium text-red-600">${store.distance.toFixed(1)} км</p>` : ''}
        </div>
      `)
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

<style scoped></style>