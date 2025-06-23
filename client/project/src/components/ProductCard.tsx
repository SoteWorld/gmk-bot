import React from 'react';
import { Calendar, List } from 'lucide-react';
import { Product } from '../types';

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ru-RU');
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
      <div className="aspect-[4/3] bg-gray-100 overflow-hidden">
        <img
          src={product.image || 'https://images.pexels.com/photos/2611937/pexels-photo-2611937.jpeg'}
          alt={product.name}
          className="w-full h-full object-cover"
          onError={(e) => {
            (e.target as HTMLImageElement).src = 'https://images.pexels.com/photos/2611937/pexels-photo-2611937.jpeg';
          }}
        />
      </div>
      
      <div className="p-3">
        <h3 className="font-semibold text-base text-gray-900 mb-2 leading-tight">{product.name}</h3>
        
        {product.expiration_date && (
          <div className="flex items-center space-x-1 text-gray-600 mb-2">
            <Calendar className="h-3 w-3" />
            <span className="text-xs">Срок: {formatDate(product.expiration_date)}</span>
          </div>
        )}
        
        {product.ingredients && (
          <div className="flex items-start space-x-1 text-gray-600">
            <List className="h-3 w-3 mt-0.5 flex-shrink-0" />
            <span className="text-xs leading-relaxed line-clamp-2">{product.ingredients}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductCard;