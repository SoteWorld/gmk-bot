import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';
import { AppError } from '../types';

interface ErrorMessageProps {
  error: AppError;
  onRetry?: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ error, onRetry }) => {
  const getErrorStyle = () => {
    switch (error.type) {
      case 'geolocation':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'network':
        return 'bg-red-50 border-red-200 text-red-800';
      default:
        return 'bg-red-50 border-red-200 text-red-800';
    }
  };

  return (
    <div className="p-3">
      <div className={`border rounded-lg p-3 ${getErrorStyle()}`}>
        <div className="flex items-start space-x-2">
          <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
          <div className="flex-1">
            <h3 className="font-medium mb-1 text-sm">Произошла ошибка</h3>
            <p className="text-xs leading-relaxed">{error.message}</p>
            {onRetry && (
              <button
                onClick={onRetry}
                className="flex items-center space-x-1 mt-2 text-xs font-medium hover:underline"
              >
                <RefreshCw className="h-3 w-3" />
                <span>Попробовать снова</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;