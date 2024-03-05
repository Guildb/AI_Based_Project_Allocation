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
              <th class="px-4 py-2">Slots</th>
              <th class="px-4 py-2">Area</th>
              <th class="px-4 py-2">Expertises</th>
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
                <div v-if="editingUserId === user.id">
                  <input
                    v-model="user.slots"
                    type="number"
                    class="bg-gray-200 text-gray-700 py-1 px-2 rounded"
                  />
                </div>
                <div v-else>
                  {{ user.slots }}
                </div>
              </td>
              <td class="px-4 py-2">
                <div v-if="editingUserId === user.id">
                  <select
                    v-model="user.areaId"
                    class="bg-gray-200 text-gray-700 py-1 px-2 rounded"
                  >
                    <option
                      v-for="area in areas"
                      :key="area.id"
                      :value="area.id"
                    >
                      {{ area.name }}
                    </option>
                  </select>
                </div>
                <div v-else>
                  {{ user.areaName }}
                </div>
              </td>
              <td class="px-4 py-2">
                <div v-if="editingUserId === user.id">
                  <select
                    v-model="user.expertises"
                    multiple
                    class="bg-gray-200 text-gray-700 py-1 px-2 rounded"
                  >
                    <option
                      v-for="expertise in expertises"
                      :key="expertise.id"
                      :value="expertise.id"
                    >
                      {{ expertise.name }}
                    </option>
                  </select>
                </div>
                <div v-else>
                  {{ getExpertiseNames(user.expertises) }}
                </div>
              </td>
              <td class="px-4 py-2">
                <button
                  v-if="editingUserId !== user.id"
                  @click="editUser(user)"
                  class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                  Edit
                </button>
                <div v-if="editingUserId === user.id">
                  <button
                    @click="saveUser(user)"
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  >
                    Save
                  </button>
                  <button
                    @click="cancelEdit()"
                    class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                  >
                    Cancel
                  </button>
                </div>
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
      areas: [],
      expertises: [],
      editingUserId: null,
    };
  },

  methods: {
    getuserid(id) {
      alert(`user id: ${id}`);
    },

    fetchUsers() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/tutors`) // Adjust the URL as needed
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
    fetchAreas() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/areas`)
        .then((response) => response.json())
        .then((data) => (this.areas = data))
        .catch((error) => console.error("Error fetching areas:", error));
      console.log(this.areas);
    },
    fetchExpertises() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/expertises`)
        .then((response) => response.json())
        .then((data) => (this.expertises = data))
        .catch((error) => console.error("Error fetching expertises:", error));
      console.log(this.expertises);
    },
    getExpertiseNames(expertiseIds) {
      return this.expertises
        .filter((expertise) => expertiseIds.includes(expertise.id))
        .map((expertise) => expertise.name)
        .join(", "); // Combines all names into a string, separated by commas
    },
    editUser(user) {
      if (this.editingUserId) {
        const originalUserDataIndex = this.users.findIndex(
          (user) => user.id === this.editingUserId
        );
        if (originalUserDataIndex !== -1) {
          this.users[originalUserDataIndex] = this.editingUser;
        }
      }
      this.editingUserId = user.id;
      this.editingUser = Object.assign({}, user);
    },
    async saveUser(user) {
      console.log(user);
      // Implement saving logic, potentially sending a request to your backend
      // After saving, clear editingUserId
      this.editingUserId = null;
      this.editingUser = {};
    },
    cancelEdit() {
      if (this.editingUserId) {
        const originalUserDataIndex = this.users.findIndex(
          (user) => user.id === this.editingUserId
        );
        if (originalUserDataIndex !== -1) {
          this.users[originalUserDataIndex] = this.editingUser;
        }
      }
      this.editingUserId = null;
      this.editingUser = {};
      this.fetchUsers();
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchUsers();
    this.fetchAreas();
    this.fetchExpertises();
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
