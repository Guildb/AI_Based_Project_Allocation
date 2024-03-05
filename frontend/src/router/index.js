// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Main",
    component: () => import("../views/MainPage.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/Login.vue"),
  },
  {
    path: "/signup",
    name: "Signup",
    component: () => import("../views/Signup.vue"),
  },
  {
    path: "/students",
    name: "Students",
    component: () => import("../views/Students.vue"),
  },
  {
    path: "/tutors",
    name: "Tutors",
    component: () => import("../views/Tutors.vue"),
  },
  {
    path: "/projects",
    name: "Projects",
    component: () => import("../views/Projects.vue"),
  },
  {
    path: "/areas",
    name: "Areas",
    component: () => import("../views/Areas.vue"),
  },
  {
    path: "/expertises",
    name: "Expertises",
    component: () => import("../views/Expertises.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
