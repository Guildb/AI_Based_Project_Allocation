<template>
  <link
    rel="stylesheet"
    href="https://unicons.iconscout.com/release/v2.1.9/css/unicons.css"
  />

  <div class="min-h-screen flex items-center justify-center">
    <div
      class="w-2/3 flex min-h-screen max-w-screen-sm items-center justify-center transition-opacity duration-700 ease-in opacity-0 fade-bottom"
      :class="{ 'opacity-100': isAnimated }"
      @mouseenter="isAnimated = true"
    >
      <div class="relative bg-gray-200 bg-opacity-50 rounded-lg p-4 w-full">
        <router-link to="/" class="absolute top-0 right-0 m-4">
          <img
            src="@/assets/images/back.png"
            alt="Back to Home"
            class="h-8 w-8"
          />
          <!-- Adjust size with h-8 w-8 -->
        </router-link>
        <div>
          <h2
            class="mt-8 text-center text-4xl font-extrabold text-slate-700 tracking-tight"
          >
            Create Account
          </h2>
        </div>
        <form class="mt-8 space-y-6" @submit.prevent="signup">
          <input type="hidden" name="remember" value="true" />
          <div class="rounded-md -space-y-px">
            <div>
              <input
                id="firstName"
                name="firstName"
                type="text"
                v-model="firstName"
                autocomplete="firstName"
                required
                class="uil-user appearance-none rounded-full relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="First Name"
              />
              <input
                id="lastName"
                name="lastName"
                type="text"
                v-model="lastName"
                autocomplete="lastName"
                required
                class="appearance-none rounded-full relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Last Name"
              />
              <input
                id="email"
                name="email"
                type="email"
                v-model="email"
                autocomplete="email"
                required
                class="appearance-none rounded-full relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Email"
              />
              <input
                id="password"
                name="password"
                type="password"
                v-model="password"
                :class="{ 'border-red-500': passwordError }"
                @input="checkPasswords"
                autocomplete="current-password"
                required
                class="appearance-none rounded-full relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Password"
              />
              <input
                id="confirmpassword"
                name="confirmpassword"
                type="password"
                v-model="confirmPassword"
                :class="{ 'border-red-500': passwordError }"
                @input="checkPasswords"
                autocomplete="confirmpassword"
                required
                class="appearance-none rounded-full relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Confirm Password"
              />
              <span v-if="passwordError" class="text-red-500"
                >Passwords do not match.</span
              >
            </div>
          </div>

          <div
            class="flex flex-col sm:flex-row items-center justify-center space-y-2 sm:space-y-0 sm:space-x-2"
          >
            <button
              type="submit"
              class="w-full sm:w-auto bg-slate-700 hover:bg-green-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Create Account
            </button>
            <router-link
              to="/login"
              class="w-full sm:w-auto bg-slate-700 hover:bg-green-700 inline-flex items-center justify-center flex-1 py-2 px-4 border border-transparent text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Login
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignupPage",
  data() {
    return {
      password: "",
      confirmPassword: "",
      firstName: "",
      lastName: "",
      email: "",
      isAnimated: false,
      passwordError: false,
    };
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100); // Start the animation shortly after the component mounts
  },
  methods: {
    checkPasswords() {
      if (this.password !== this.confirmPassword) {
        this.passwordError = true;
      } else {
        this.passwordError = false;
      }
    },
    async signup() {
      if (this.passwordError) {
        alert("Please fix the errors before submitting.");
        return;
      }

      try {
        const response = await fetch(
          `${process.env.VUE_APP_BACKEND_URL}/signup`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              firstName: this.firstName,
              lastName: this.lastName,
              email: this.email,
              password: this.password,
            }),
          }
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.error || `HTTP error! Status: ${response.status}`
          );
        }

        console.log("Signup successful:", data);
        alert("Signup successful! Redirecting to login...");
        this.$router.push("/login");
      } catch (error) {
        console.error("Error during the signup:", error);
        alert(`Error during signup: ${error.message}`);
      }
    },
  },
};
</script>
