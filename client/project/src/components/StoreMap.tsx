import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { Store, UserLocation } from '../types';

interface StoreMapProps {
  stores: Store[];
  userLocation: UserLocation | null;
  selectedStore?: Store | null;
}

const StoreMap: React.FC<StoreMapProps> = ({ stores, userLocation, selectedStore }) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);

  useEffect(() => {
    if (!mapRef.current) return;

    // Initialize map
    if (!mapInstanceRef.current) {
      mapInstanceRef.current = L.map(mapRef.current).setView([53.9, 27.5], 11);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(mapInstanceRef.current);
    }

    const map = mapInstanceRef.current;
    
    // Clear existing markers
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer);
      }
    });

    // Add user location marker if available
    if (userLocation) {
      const userIcon = L.divIcon({
        html: '<div class="bg-blue-500 rounded-full w-3 h-3 border-2 border-white shadow-md"></div>',
        className: 'user-location-marker',
        iconSize: [12, 12],
        iconAnchor: [6, 6]
      });

      L.marker([userLocation.latitude, userLocation.longitude], { icon: userIcon })
        .bindPopup('Ваше местоположение')
        .addTo(map);
    }

    // Add store markers
    stores.forEach((store) => {
      const isSelected = selectedStore?.id === store.id;
      
      const storeIcon = L.divIcon({
        html: `<div class="bg-red-500 rounded-full w-5 h-5 border-2 border-white shadow-md flex items-center justify-center ${isSelected ? 'ring-2 ring-red-300' : ''}">
                 <div class="bg-white rounded-full w-1.5 h-1.5"></div>
               </div>`,
        className: 'store-marker',
        iconSize: [20, 20],
        iconAnchor: [10, 10]
      });

      L.marker([store.latitude, store.longitude], { icon: storeIcon })
        .bindPopup(`
          <div class="p-2 min-w-[200px]">
            <h3 class="font-semibold text-sm mb-1">${store.name}</h3>
            <p class="text-xs text-gray-600 mb-1">${store.address}</p>
            <p class="text-xs text-gray-600 mb-1">${store.opening_hours}</p>
            ${userLocation ? `<p class="text-xs font-medium text-red-600">${store.distance.toFixed(1)} км</p>` : ''}
          </div>
        `)
        .addTo(map);
    });

    // Fit bounds to show all markers
    if (stores.length > 0) {
      const group = new L.FeatureGroup();
      
      stores.forEach((store) => {
        group.addLayer(L.marker([store.latitude, store.longitude]));
      });
      
      if (userLocation) {
        group.addLayer(L.marker([userLocation.latitude, userLocation.longitude]));
      }
      
      map.fitBounds(group.getBounds().pad(0.1));
    }

    return () => {
      // Don't remove map instance on cleanup to avoid re-initialization
    };
  }, [stores, userLocation, selectedStore]);

  return <div ref={mapRef} className="w-full h-48 rounded-lg shadow-sm border border-gray-200" />;
};

export default StoreMap;