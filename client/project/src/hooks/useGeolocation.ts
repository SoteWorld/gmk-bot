import { useState, useEffect } from 'react';
import { UserLocation, AppError } from '../types';

export const useGeolocation = () => {
  const [location, setLocation] = useState<UserLocation | null>(null);
  const [error, setError] = useState<AppError | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!navigator.geolocation) {
      setError({
        type: 'geolocation',
        message: 'Геолокация не поддерживается вашим устройством'
      });
      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        });
        setLoading(false);
      },
      (err) => {
        let message = 'Не удалось получить местоположение';
        
        switch (err.code) {
          case err.PERMISSION_DENIED:
            message = 'Доступ к геолокации запрещен. Разрешите доступ к местоположению для полного функционала.';
            break;
          case err.POSITION_UNAVAILABLE:
            message = 'Информация о местоположении недоступна';
            break;
          case err.TIMEOUT:
            message = 'Истекло время ожидания запроса местоположения';
            break;
        }
        
        setError({
          type: 'geolocation',
          message
        });
        setLoading(false);
      },
      { 
        enableHighAccuracy: true, 
        timeout: 10000, 
        maximumAge: 300000 
      }
    );
  }, []);

  return { location, error, loading };
};