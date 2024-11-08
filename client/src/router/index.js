import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DeviceListView from "@/views/DeviceListView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
      {
      path: '/list',
      name: 'list',
      component: DeviceListView,
    },
  ],
})

export default router
