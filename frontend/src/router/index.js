// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Main",
    component: () => import("../views/MainPage.vue"),
  },
  {
    path: "/signinup",
    name: "sSgnInUp",
    component: () => import("../views/SignInUp.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
