import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import NavigationTabs from './components/NavigationTabs';
import ProductsTab from './components/ProductsTab';
import StoresTab from './components/StoresTab';

declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        ready: () => void;
        expand: () => void;
        MainButton: {
          show: () => void;
          hide: () => void;
          setText: (text: string) => void;
          onClick: (callback: () => void) => void;
        };
        BackButton: {
          show: () => void;
          hide: () => void;
          onClick: (callback: () => void) => void;
        };
        themeParams: {
          bg_color?: string;
          text_color?: string;
          hint_color?: string;
          link_color?: string;
          button_color?: string;
          button_text_color?: string;
        };
      };
    };
  }
}

function App() {
  const [activeTab, setActiveTab] = useState<'products' | 'stores'>('products');

  useEffect(() => {
    // Initialize Telegram Web App
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready();
      tg.expand();
      
      // Apply Telegram theme
      const theme = tg.themeParams;
      if (theme.bg_color) {
        document.documentElement.style.setProperty('--tg-bg-color', theme.bg_color);
      }
      if (theme.text_color) {
        document.documentElement.style.setProperty('--tg-text-color', theme.text_color);
      }
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 max-w-md mx-auto">
      <Header />
      <NavigationTabs activeTab={activeTab} onTabChange={setActiveTab} />
      
      <main className="pb-4">
        {activeTab === 'products' ? <ProductsTab /> : <StoresTab />}
      </main>
    </div>
  );
}

export default App;