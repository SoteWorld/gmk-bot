import React, { useState, useEffect } from 'react';
import { Package, RefreshCw } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { Product, AppError } from '../types';
import ProductCard from './ProductCard';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

const ProductsTab: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState<AppError | null>(null);
  const { fetchProducts, loading } = useApi();

  const loadProducts = async () => {
    const { data, error } = await fetchProducts();
    if (data) {
      setProducts(data);
      setError(null);
    } else if (error) {
      setError(error);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  if (loading) {
    return <LoadingSpinner message="Загрузка новых продуктов..." />;
  }

  if (error) {
    return (
      <ErrorMessage
        error={error}
        onRetry={loadProducts}
      />
    );
  }

  if (products.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 px-4">
        <Package className="h-12 w-12 text-gray-300 mb-3" />
        <h3 className="text-base font-medium text-gray-600 mb-1">Список пуст</h3>
        <p className="text-gray-500 text-center text-sm mb-4">
          В настоящее время нет новых продуктов
        </p>
        <button
          onClick={loadProducts}
          className="flex items-center space-x-1 bg-red-600 text-white px-3 py-2 rounded-lg hover:bg-red-700 transition-colors text-sm"
        >
          <RefreshCw className="h-3 w-3" />
          <span>Обновить</span>
        </button>
      </div>
    );
  }

  return (
    <div className="p-3">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-gray-900">Новые продукты</h2>
        <button
          onClick={loadProducts}
          disabled={loading}
          className="flex items-center space-x-1 text-red-600 hover:text-red-700 transition-colors text-sm"
        >
          <RefreshCw className={`h-3 w-3 ${loading ? 'animate-spin' : ''}`} />
          <span>Обновить</span>
        </button>
      </div>
      
      <div className="grid grid-cols-1 gap-3">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};

export default ProductsTab;