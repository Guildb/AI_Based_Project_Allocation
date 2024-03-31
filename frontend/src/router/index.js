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
  const token = localStorage.getItem("token");

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token) {
      // No token, redirect to login
      next({ path: "/" });
    } else {
      // Verify token before proceeding
      verifyToken(token)
        .then(() => {
          next();
        })
        .catch(() => {
          // Token verification failed, redirect to login
          next({ path: "/" });
        });
    }
  } else if (to.path === "/" && token) {
    // For home path, redirect to dashboard if token exists and is valid
    verifyToken(token)
      .then(() => {
        next({ path: "/dashboard" });
      })
      .catch(() => {
        next();
      });
  } else {
    // For all other cases, allow navigation
    next();
  }
});

function verifyToken(token) {
  return new Promise((resolve, reject) => {
    fetch(`${process.env.VUE_APP_BACKEND_URL}/verify_token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message === "Token is valid") {
          resolve();
        } else {
          localStorage.removeItem("token");
          reject(new Error("Token validation failed!"));
        }
      })
      .catch((error) => {
        localStorage.removeItem("token");
        console.error("There was a problem verifying the token:", error);
        reject(error);
      });
  });
}

export default router;
