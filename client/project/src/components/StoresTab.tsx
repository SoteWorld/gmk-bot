import React, { useState, useEffect } from 'react';
import { MapPin, RefreshCw, AlertTriangle } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { useGeolocation } from '../hooks/useGeolocation';
import { Store, AppError } from '../types';
import StoreCard from './StoreCard';
import StoreMap from './StoreMap';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

const StoresTab: React.FC = () => {
  const [stores, setStores] = useState<Store[]>([]);
  const [selectedStore, setSelectedStore] = useState<Store | null>(null);
  const [error, setError] = useState<AppError | null>(null);
  const { location, error: locationError, loading: locationLoading } = useGeolocation();
  const { fetchStores, fetchAllStores, loading } = useApi();

  const loadStores = async () => {
    let result;
    
    if (location) {
      // Если есть геолокация, загружаем ближайшие магазины
      result = await fetchStores(location);
    } else {
      // Если нет геолокации, загружаем все магазины
      result = await fetchAllStores();
    }
    
    if (result.data) {
      setStores(result.data);
      setError(null);
    } else if (result.error) {
      setError(result.error);
    }
  };

  useEffect(() => {
    // Загружаем магазины независимо от наличия геолокации
    if (!locationLoading) {
      loadStores();
    }
  }, [location, locationLoading]);

  const handleShowRoute = (store: Store) => {
    if (!location) {
      setError({
        type: 'geolocation',
        message: 'Невозможно построить маршрут без доступа к вашему местоположению. Разрешите доступ к геолокации для построения маршрутов.'
      });
      return;
    }
    
    setSelectedStore(store);
    window.open(store.route_url, '_blank');
  };

  if (locationLoading) {
    return <LoadingSpinner message="Определение местоположения..." />;
  }

  if (loading) {
    return <LoadingSpinner message="Загрузка магазинов..." />;
  }

  if (error && error.type !== 'geolocation') {
    return (
      <ErrorMessage
        error={error}
        onRetry={loadStores}
      />
    );
  }

  if (stores.length === 0) {
    return (
      <div className="p-3">
        <div className="text-center py-12">
          <MapPin className="h-12 w-12 text-gray-300 mx-auto mb-3" />
          <h3 className="text-base font-medium text-gray-600 mb-1">Магазины не найдены</h3>
          <p className="text-gray-500 text-center text-sm mb-4">
            Не удалось загрузить список магазинов
          </p>
          <button
            onClick={loadStores}
            className="flex items-center space-x-1 bg-red-600 text-white px-3 py-2 rounded-lg hover:bg-red-700 transition-colors mx-auto text-sm"
          >
            <RefreshCw className="h-3 w-3" />
            <span>Обновить</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-3">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-gray-900">
          {location ? 'Ближайшие магазины' : 'Все магазины'}
        </h2>
        <button
          onClick={loadStores}
          disabled={loading}
          className="flex items-center space-x-1 text-red-600 hover:text-red-700 transition-colors text-sm"
        >
          <RefreshCw className={`h-3 w-3 ${loading ? 'animate-spin' : ''}`} />
          <span>Обновить</span>
        </button>
      </div>

      {/* Предупреждение о геолокации */}
      {locationError && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
          <div className="flex items-start space-x-2">
            <AlertTriangle className="h-4 w-4 text-yellow-600 mt-0.5 flex-shrink-0" />
            <div>
              <h3 className="font-medium text-yellow-800 text-sm mb-1">Геолокация недоступна</h3>
              <p className="text-xs text-yellow-700 leading-relaxed">
                Показаны все магазины. Для отображения расстояний и построения маршрутов разрешите доступ к местоположению.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Ошибка геолокации при попытке построить маршрут */}
      {error && error.type === 'geolocation' && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
          <div className="flex items-start space-x-2">
            <AlertTriangle className="h-4 w-4 text-red-600 mt-0.5 flex-shrink-0" />
            <div>
              <h3 className="font-medium text-red-800 text-sm mb-1">Невозможно построить маршрут</h3>
              <p className="text-xs text-red-700 leading-relaxed">{error.message}</p>
            </div>
          </div>
        </div>
      )}

      {/* Карта */}
      <div className="mb-4">
        <StoreMap 
          stores={stores} 
          userLocation={location} 
          selectedStore={selectedStore}
        />
      </div>
      
      {/* Список магазинов */}
      <div className="grid grid-cols-1 gap-3">
        {stores.map((store) => (
          <StoreCard 
            key={store.id} 
            store={store} 
            onShowRoute={location ? handleShowRoute : undefined}
            showDistance={!!location}
          />
        ))}
      </div>
    </div>
  );
};

export default StoresTab;