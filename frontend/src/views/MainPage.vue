<template>
  <div class="min-h-screen flex justify-center items-center p-4 sm:p-24">
    <div
      class="w-full sm:w-3/4 bg-gray-200 bg-opacity-50 rounded-lg shadow-lg p-4 transition-opacity duration-700 ease-in opacity-0"
      :class="{ 'opacity-100': isAnimated }"
    >
      <h1
        class="text-2xl sm:text-4xl font-bold mb-4 text-center text-slate-700"
      >
        Welcome to my page
      </h1>
      <p class="text-base sm:text-lg mb-6 text-center text-slate-700">
        This website is an AI-based project allocation, you will need to have an
        account in order to use this service.
      </p>
      <p class="text-base sm:text-lg mb-6 text-center text-slate-700">
        If you do not have a project idea yet you will be able to see the
        projects proposed by the tutors.
      </p>
      <div
        class="text-center flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 mt-6"
      >
        <router-link
          to="/login"
          class="bg-slate-700 hover:bg-green-700 text-white font-bold py-2 px-4 rounded inline-block mx-2 sm:w-1/2"
          >Sign in</router-link
        >
        <router-link
          to="/signup"
          class="bg-slate-700 hover:bg-green-700 text-white font-bold py-2 px-4 rounded inline-block mx-2 sm:w-1/2"
          >Create Account</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  components: {},
  data() {
    return {
      isAnimated: false,
    };
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100); // Start the animation shortly after the component mounts
  },
};
</script>

<style scoped>
/* Additional styles if needed */
</style>
