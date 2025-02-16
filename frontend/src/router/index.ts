import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    component: () => import('../components/AuthReg.vue'),
  },
  {
    path: '/base',
    component: () => import('../components/Mainpage.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;