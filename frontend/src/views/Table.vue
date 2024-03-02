<template>
  <link
    href="https://cdn.datatables.net/v/dt/dt-2.0.1/b-3.0.0/datatables.min.css"
    rel="stylesheet"
  />

  <script src="https://cdn.datatables.net/v/dt/dt-2.0.1/b-3.0.0/datatables.min.js"></script>
  <navbar />
  <div class="min-h-screen flex justify-center items-center p-4">
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in"
      :class="{ 'opacity-100': isAnimated }"
    >
      <div class="overflow-auto">
        <table id="myTable" class="display min-w-full">
          <thead>
            <tr>
              <th class="px-4 py-2">Name</th>
              <th class="px-4 py-2">Email</th>
              <th class="px-4 py-2">Type</th>
              <th class="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td class="px-4 py-2">
                {{ user.firstName }} {{ user.lastName }}
              </td>
              <td class="px-4 py-2">{{ user.email }}</td>
              <td class="px-4 py-2">{{ user.type }}</td>
              <td class="px-4 py-2">
                <button
                  @click="getuserid(user.id)"
                  class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                  Get User ID
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import DataTable from "datatables.net-dt";

import navbar from "@/components/NavBar.vue";

export default {
  name: "DataTableComponent",
  components: {
    navbar,
  },
  data() {
    return {
      isAnimated: false,
      users: [],
    };
  },

  methods: {
    getuserid(id) {
      alert(`user id: ${id}`);
    },

    fetchUsers() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/users`) // Adjust the URL as needed
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.users = data;
          this.$nextTick(() => {
            new DataTable("#myTable", {
              responsive: true,
            });
          });
        })
        .catch((error) => {
          console.error("There was a problem fetching the user data:", error);
        });
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchUsers();
  },
};
</script>

<style scoped>
/* Styles the scrollbar track (background) */
.overflow-auto::-webkit-scrollbar-track {
  background-color: #f0f0f0; /* Light grey background */
  border-radius: 10px; /* Rounded corners for the track */
}

/* Styles the scrollbar handle */
.overflow-auto::-webkit-scrollbar-thumb {
  background-color: #888; /* Darker grey handle */
  border-radius: 10px; /* Rounded corners for the handle */
}

/* Styles the scrollbar itself (width and height) */
.overflow-auto::-webkit-scrollbar {
  width: 8px; /* Width of the vertical scrollbar */
  height: 8px; /* Height of the horizontal scrollbar */
}

/* For Firefox */
.overflow-auto {
  scrollbar-width: thin; /* Makes scrollbar thinner */
  scrollbar-color: #888 #f0f0f0; /* Handle and track color */
}
</style>
