export interface Product {
  id: string;
  name: string;
  image: string;
  expiration_date?: string;
  ingredients?: string;
}

export interface Store {
  id: string;
  name: string;
  address: string;
  opening_hours: string;
  phone: string;
  latitude: number;
  longitude: number;
  distance: number;
  route_url: string;
}

export interface UserLocation {
  latitude: number;
  longitude: number;
}

export interface AppError {
  type: 'geolocation' | 'network' | 'products' | 'stores';
  message: string;
}