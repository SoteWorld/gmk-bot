import React from 'react';
import { Beef } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-gradient-to-r from-red-600 to-red-700 text-white px-4 py-4 shadow-sm">
      <div className="flex items-center justify-center space-x-2">
        <Beef className="h-6 w-6" />
        <div className="text-center">
          <h1 className="text-lg font-bold">Гомельский мясокомбинат</h1>
          <p className="text-red-100 text-xs">Качество, проверенное временем</p>
        </div>
      </div>
    </header>
  );
};

export default Header;