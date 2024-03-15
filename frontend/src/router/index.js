// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "HomePage",
    component: () => import("../views/MainPage.vue"),
  },
  {
    path: "/login",
    name: "LoginPage",
    component: () => import("../views/Login.vue"),
  },
  {
    path: "/signup",
    name: "SignupPage",
    component: () => import("../views/Signup.vue"),
  },
  {
    path: "/students",
    name: "StudentsPage",
    component: () => import("../views/Students.vue"),
  },
  {
    path: "/tutors",
    name: "TutorsPage",
    component: () => import("../views/Tutors.vue"),
  },
  {
    path: "/projects",
    name: "ProjectsPage",
    component: () => import("../views/Projects.vue"),
  },
  {
    path: "/areas",
    name: "AreasPage",
    component: () => import("../views/Areas.vue"),
  },
  {
    path: "/expertises",
    name: "ExpertisesPage",
    component: () => import("../views/Expertises.vue"),
  },
  {
    path: "/dashboard",
    name: "DashBoard",
    component: () => import("../views/Dashboard.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
