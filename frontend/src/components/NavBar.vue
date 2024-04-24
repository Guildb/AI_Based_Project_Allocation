<template>
  <nav
    class="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600"
  >
    <div
      class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4"
    >
      <router-link
        to="/dashboard"
        class="flex items-center space-x-3 rtl:space-x-reverse"
      >
        <span
          class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white"
          >Project Allocation</span
        >
      </router-link>
      <div class="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
        <button
          @click="toggleMenu"
          type="button"
          class="toggle-button inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
          aria-controls="navbar-sticky"
          aria-expanded="false"
        >
          <span class="sr-only">Open main menu</span>
          <svg
            class="w-5 h-5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 17 14"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M1 1h15M1 7h15M1 13h15"
            />
          </svg>
        </button>
      </div>
      <div
        :class="[
          !isMenuOpen ? 'hidden' : 'flex',
          'items-center',
          'justify-between',
          'w-full',
          'md:flex',
          'md:w-auto',
          'md:order-1',
        ]"
        id="navbar-sticky"
      >
        <ul
          class="flex flex-col w-full p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700"
        >
          <li>
            <router-link
              to="/dashboard"
              class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
              active-class="text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500"
              aria-current="page"
              >Dashboard</router-link
            >
          </li>
          <li>
            <router-link
              v-if="this.user.type !== 'student'"
              to="/students"
              class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
              active-class="text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500"
              aria-current="page"
              >Students</router-link
            >
          </li>
          <li>
            <router-link
              v-if="this.user.type !== 'student'"
              to="/tutors"
              class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
              active-class="text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500"
              aria-current="page"
              >Tutors</router-link
            >
          </li>
          <li>
            <router-link
              v-if="this.user.type !== 'student'"
              to="/areas"
              class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
              active-class="text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500"
              aria-current="page"
              >Areas</router-link
            >
          </li>
          <li>
            <router-link
              v-if="this.user.type !== 'student'"
              to="/expertises"
              class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
              active-class="text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500"
              aria-current="page"
              >Expertises</router-link
            >
          </li>
          <li>
            <router-link
              v-if="this.user.type !== 'student'"
              to="/projects"
              class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
              active-class="text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500"
              aria-current="page"
              >Projects</router-link
            >
          </li>
          <li>
            <button
              @click="logOut"
              class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
              active-class="text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500"
              aria-current="page"
            >
              LogOut
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      isMenuOpen: false,
      user: {},
    };
  },
  methods: {
    getUser() {
      const token = localStorage.getItem("token");

      fetch(`${process.env.VUE_APP_BACKEND_URL}/get_current_user`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ token: token }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.user = data;
        })
        .catch((error) => {
          console.error("There was a problem fetching the user:", error);
        });
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen; // Toggle the state
    },
    logOut() {
      localStorage.removeItem("token");
      this.$router.push("/");
    },
  },
  mounted() {
    this.getUser();
  },
};
</script>
<style scoped>
/* Custom animation for sliding down */
@keyframes slideDown {
  from {
    transform: translateY(-100%);
  }
  to {
    transform: translateY(0);
  }
}
nav {
  animation: slideDown 0.5s ease-out forwards;
}
@media (max-width: 849px) {
  #navbar-sticky {
    display: none; /* Hide by default when under 850px */
  }
}
@media (max-width: 849px) {
  .toggle-button {
    display: block !important;  /* Important to override any other hidden classes */
  }
}
</style>
