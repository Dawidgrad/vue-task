import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import ArticlesPage from 'pages/ArticlesPage.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: ArticlesPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;