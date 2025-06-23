export interface Product {
  id: string
  name: string
  image?: string
  expiration_date?: string
  ingredients?: string
  category?: string
}

export interface StoreWithDistance {
  id: string
  name: string
  address: string
  opening_hours?: string
  phone?: string
  latitude?: number
  longitude?: number
  distance: number
  route_url?: string
}

export async function fetchCategories(): Promise<string[]> {
  const resp = await fetch('/api/products/categories')
  if (!resp.ok) throw new Error('Failed to fetch categories')
  return resp.json()
}

export async function fetchProducts(category: string): Promise<Product[]> {
  const resp = await fetch(`/api/products/category/${encodeURIComponent(category)}`)
  if (!resp.ok) throw new Error('Failed to fetch products')
  return resp.json()
}

export async function fetchNearbyStores(
  lat: number,
  lon: number,
  limit = 5,
): Promise<StoreWithDistance[]> {
  const url = `/api/stores/nearby?lat=${lat}&lon=${lon}&limit=${limit}`
  const resp = await fetch(url)
  if (!resp.ok) throw new Error('Failed to fetch stores')
  return resp.json()
}