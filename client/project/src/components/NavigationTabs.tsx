import React from 'react';
import { Package, MapPin } from 'lucide-react';

interface NavigationTabsProps {
  activeTab: 'products' | 'stores';
  onTabChange: (tab: 'products' | 'stores') => void;
}

const NavigationTabs: React.FC<NavigationTabsProps> = ({ activeTab, onTabChange }) => {
  return (
    <div className="flex bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
      <button
        onClick={() => onTabChange('products')}
        className={`flex-1 flex items-center justify-center space-x-1 py-3 px-2 text-sm font-medium transition-colors ${
          activeTab === 'products'
            ? 'text-red-600 border-b-2 border-red-600 bg-red-50'
            : 'text-gray-600 hover:text-red-600 hover:bg-gray-50'
        }`}
      >
        <Package className="h-4 w-4" />
        <span>Новые продукты</span>
      </button>
      <button
        onClick={() => onTabChange('stores')}
        className={`flex-1 flex items-center justify-center space-x-1 py-3 px-2 text-sm font-medium transition-colors ${
          activeTab === 'stores'
            ? 'text-red-600 border-b-2 border-red-600 bg-red-50'
            : 'text-gray-600 hover:text-red-600 hover:bg-gray-50'
        }`}
      >
        <MapPin className="h-4 w-4" />
        <span>Ближайшие магазины</span>
      </button>
    </div>
  );
};

export default NavigationTabs;