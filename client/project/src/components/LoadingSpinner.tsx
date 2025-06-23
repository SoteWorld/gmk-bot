import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  message?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ message = 'Загрузка...' }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <Loader2 className="h-6 w-6 text-red-600 animate-spin mb-3" />
      <p className="text-gray-600 text-center text-sm">{message}</p>
    </div>
  );
};

export default LoadingSpinner;