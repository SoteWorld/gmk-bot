import { useState, useCallback } from 'react';
import { Product, Store, UserLocation, AppError } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export const useApi = () => {
  const [loading, setLoading] = useState(false);

  const fetchProducts = useCallback(async (): Promise<{ data: Product[] | null; error: AppError | null }> => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/products/new`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return { data, error: null };
    } catch (err) {
      return {
        data: null,
        error: {
          type: 'products',
          message: 'Не удалось загрузить список продуктов. Проверьте интернет-соединение.'
        }
      };
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchStores = useCallback(async (location: UserLocation): Promise<{ data: Store[] | null; error: AppError | null }> => {
    setLoading(true);
    try {
      const response = await fetch(
        `${API_BASE_URL}/stores/nearby?lat=${location.latitude}&lon=${location.longitude}`
      );
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return { data, error: null };
    } catch (err) {
      return {
        data: null,
        error: {
          type: 'stores',
          message: 'Не удалось загрузить список магазинов. Проверьте интернет-соединение.'
        }
      };
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchAllStores = useCallback(async (): Promise<{ data: Store[] | null; error: AppError | null }> => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/stores/all`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return { data, error: null };
    } catch (err) {
      return {
        data: null,
        error: {
          type: 'stores',
          message: 'Не удалось загрузить список магазинов. Проверьте интернет-соединение.'
        }
      };
    } finally {
      setLoading(false);
    }
  }, []);

  return { fetchProducts, fetchStores, fetchAllStores, loading };
};