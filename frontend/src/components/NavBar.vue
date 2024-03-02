<template>
  <nav
    class="top-0 left-0 right-0 shadow-md p-6 bg-gray-200 bg-opacity-50 rounded-b-lg"
  >
    <ul class="flex justify-center space-x-4">
      <li>
        <router-link to="/" v-slot="{ isActive }">
          <a
            :class="[
              'text-slate-700 hover:text-blue-500 font-semibold',
              isActive ? 'text-blue-700' : '',
            ]"
            >Dashboard</a
          >
        </router-link>
      </li>
      <li>
        <router-link to="/table" v-slot="{ isActive }">
          <a
            :class="[
              'text-slate-700 hover:text-blue-500 font-semibold',
              isActive ? 'text-blue-700' : '',
            ]"
            >Table</a
          >
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
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
</style>
