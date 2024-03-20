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
    meta: { requiresAuth: true },
  },
  {
    path: "/tutors",
    name: "TutorsPage",
    component: () => import("../views/Tutors.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/projects",
    name: "ProjectsPage",
    component: () => import("../views/Projects.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/areas",
    name: "AreasPage",
    component: () => import("../views/Areas.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/expertises",
    name: "ExpertisesPage",
    component: () => import("../views/Expertises.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/dashboard",
    name: "DashBoard",
    component: () => import("../views/Dashboard.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem("token");

  // Check if the user is trying to access a page that requires authentication
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      // If the user is not logged in, redirect to the login page
      next({ path: "/" });
    } else {
      // If the user is logged in, proceed as normal
      next();
    }
  } else if (to.path === "/") {
    if (isLoggedIn) {
      // If the user is logged in and trying to access the home page, redirect to the dashboard
      next({ path: "/dashboard" });
    } else {
      // If the user is not logged in, allow them to see the home page
      next();
    }
  } else {
    next();
  }
});

export default router;
