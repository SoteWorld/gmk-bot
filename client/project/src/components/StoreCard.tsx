import React from 'react';
import { MapPin, Clock, Phone, Navigation } from 'lucide-react';
import { Store } from '../types';

interface StoreCardProps {
  store: Store;
  onShowRoute?: (store: Store) => void;
  showDistance?: boolean;
}

const StoreCard: React.FC<StoreCardProps> = ({ store, onShowRoute, showDistance = true }) => {
  const handlePhoneClick = (phone: string) => {
    window.open(`tel:${phone}`, '_self');
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-3">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-base text-gray-900 flex-1 leading-tight">{store.name}</h3>
        {showDistance && (
          <div className="flex items-center space-x-1 text-red-600 font-medium ml-2">
            <MapPin className="h-3 w-3" />
            <span className="text-xs">{store.distance.toFixed(1)} км</span>
          </div>
        )}
      </div>
      
      <div className="space-y-1 mb-3">
        <div className="flex items-start space-x-1 text-gray-600">
          <MapPin className="h-3 w-3 mt-0.5 flex-shrink-0" />
          <span className="text-xs leading-relaxed">{store.address}</span>
        </div>
        
        <div className="flex items-center space-x-1 text-gray-600">
          <Clock className="h-3 w-3" />
          <span className="text-xs">{store.opening_hours}</span>
        </div>
        
        <div className="flex items-center space-x-1 text-gray-600">
          <Phone className="h-3 w-3" />
          <button
            onClick={() => handlePhoneClick(store.phone)}
            className="text-xs text-red-600 hover:text-red-700 transition-colors underline"
          >
            {store.phone}
          </button>
        </div>
      </div>
      
      {onShowRoute && (
        <button
          onClick={() => onShowRoute(store)}
          className="w-full flex items-center justify-center space-x-1 bg-red-600 text-white py-2 px-3 rounded-lg hover:bg-red-700 transition-colors text-sm"
        >
          <Navigation className="h-3 w-3" />
          <span>Построить маршрут</span>
        </button>
      )}
    </div>
  );
};

export default StoreCard;