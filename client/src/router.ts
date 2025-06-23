import { createRouter, createWebHistory } from 'vue-router'
import ProductsView from './components/ProductsView.vue'
import StoresView from './components/StoresView.vue'

const routes = [
  { path: '/', redirect: '/products' },
  { path: '/products', component: ProductsView },
  { path: '/stores', component: StoresView },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})