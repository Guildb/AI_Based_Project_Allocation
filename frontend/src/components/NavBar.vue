<template>
  <div class="relative">
    <!-- Toggle Button -->
    <button
      @click="toggleSidebar"
      :class="[
        'fixed z-50 bg-slate-500 hover:bg-blue-700 bg-opacity-100 top-5 left-10 text-white font-bold py-2 px-4 rounded transition-all duration-300',
      ]"
    >
      <svg
        :class="showSidebar ? '' : 'rotate-180'"
        class="h-6 w-6 transform transition-transform duration-300"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 19l-7-7 7-7"
        />
      </svg>
    </button>

    <!-- Sidebar -->
    <div
      :class="[
        'fixed top-0 left-0 h-full bg-gray-200 bg-opacity-90 pt-20 p-6 z-40',
        showSidebar ? 'translate-x-0' : '-translate-x-full',
      ]"
      class="transition-transform duration-300 ease-in-out"
    >
      <ul class="space-y-4">
        <li>
          <router-link
            to="/dashboard"
            class="text-slate-700 hover:text-blue-500 font-semibold"
            >Dashboard</router-link
          >
        </li>
        <li>
          <router-link
            to="/students"
            class="text-slate-700 hover:text-blue-500 font-semibold"
            >Students</router-link
          >
        </li>
        <li>
          <router-link
            to="/tutors"
            class="text-slate-700 hover:text-blue-500 font-semibold"
            >Tutors</router-link
          >
        </li>
        <li>
          <router-link
            to="/areas"
            class="text-slate-700 hover:text-blue-500 font-semibold"
            >Areas</router-link
          >
        </li>
        <li>
          <router-link
            to="/expertises"
            class="text-slate-700 hover:text-blue-500 font-semibold"
            >Expertises</router-link
          >
        </li>
        <li>
          <router-link
            to="/projects"
            class="text-slate-700 hover:text-blue-500 font-semibold"
            >Projects</router-link
          >
        </li>
        <li>
          <button
            @click="logOut"
            class="bg-slate-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            LogOut
          </button>
        </li>
      </ul>
    </div>

    <!-- Overlay -->
    <div
      v-if="showSidebar"
      @click="toggleSidebar"
      class="fixed inset-0 bg-black bg-opacity-50 z-30"
    ></div>
  </div>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      showSidebar: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    },
    logOut() {
      localStorage.removeItem("token");
      this.$router.push("/");
    },
  },
};
</script>
