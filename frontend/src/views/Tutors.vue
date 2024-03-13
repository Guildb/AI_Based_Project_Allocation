<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center p-4">
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in p-1"
      :class="{ 'opacity-100': isAnimated }"
    >
      <div>
        <table id="myTable" width="100%">
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
              <td class="px-4 py-2">{{ user.slots }}</td>
              <td class="px-4 py-2">
                {{ user.areaId === 0 ? "NaN" : getAreaName(user.areaId) }}
              </td>
              <td class="px-4 py-2">
                {{
                  user.expertises.length === 0
                    ? "NaN"
                    : getExpertiseNames(user.expertises)
                }}
              </td>
              <td class="px-4 py-2">
                <button
                  @click="editUser(user)"
                  class="bg-green-700 hover:bg-green-500 text-white font-bold py-2 px-4 rounded"
                >
                  Edit
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- User Editing Modal -->
  <transition name="fade">
    <div
      v-if="showModal"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center p-4"
    >
      <div class="bg-white p-4 sm:p-6 rounded-lg max-w-md w-full space-y-4">
        <div class="text-lg font-semibold">Edit User</div>

        <!-- Example input for editing the user's name -->
        <div>
          Type:
          <select
            v-model="editingUser.type"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          >
            <option
              v-for="typeItem in typeList"
              :key="typeItem.value"
              :value="typeItem.value"
            >
              {{ typeItem.name }}
            </option>
          </select>
        </div>
        <div>
          Slots:
          <input
            v-model="editingUser.slots"
            type="number"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          />
        </div>
        <div>
          Area:
          <select
            v-model="editingUser.areaId"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          >
            <option v-for="area in areas" :key="area.id" :value="area.id">
              {{ area.name }}
            </option>
          </select>
        </div>

        <div class="max-h-48 overflow-y-auto border p-2">
          <span class="text-lg font-semibold">Expertises:</span>
          <div>
            <div
              v-for="expertise in expertises"
              :key="expertise.id"
              class="flex items-center my-1"
            >
              <input
                type="checkbox"
                :value="expertise.id"
                :id="'expertise-' + expertise.id"
                v-model="editingUser.expertises"
                class="form-checkbox h-5 w-5 text-blue-600"
              />
              <label :for="'expertise-' + expertise.id" class="ml-2 text-sm">
                {{ expertise.name }}
              </label>
            </div>
          </div>
        </div>

        <div class="flex justify-center space-x-2">
          <button
            @click="saveUser()"
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
      </div>
    </div>
  </transition>
</template>

<script>
import DataTable from "datatables.net-dt";

import navbar from "@/components/NavBar.vue";

export default {
  name: "TutorPage",
  components: {
    navbar,
  },
  data() {
    return {
      isAnimated: false,
      users: [],
      areas: [],
      expertises: [],
      typeList: [
        { value: "student", name: "Student" },
        { value: "tutor", name: "Tutor" },
        { value: "courseLeader", name: "Course Leader" },
      ],
      editingUserId: null,
      showModal: false,
      editingUser: null,
    };
  },

  methods: {
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
              scrollX: true,
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
    },
    fetchExpertises() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/expertises`)
        .then((response) => response.json())
        .then((data) => (this.expertises = data))
        .catch((error) => console.error("Error fetching expertises:", error));
    },
    getExpertiseNames(expertiseIds) {
      return this.expertises
        .filter((expertise) => expertiseIds.includes(expertise.id))
        .map((expertise) => expertise.acronyms)
        .join(", "); // Combines all names into a string, separated by commas
    },
    getAreaName(areaId) {
      const area = this.areas.find((area) => area.id === areaId);
      return area ? area.name : "Not Found";
    },
    editUser(user) {
      this.editingUser = { ...user }; // Make a copy of the user to edit
      this.showModal = true;
    },
    async saveUser() {
      try {
        console.log(this.editingUser);
        const response = await fetch(
          `${process.env.VUE_APP_BACKEND_URL}/changeTutors`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ user: this.editingUser }),
          }
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        await response.json();
        this.editingUserId = null;
        this.editingUser = {};
        window.location.reload();
      } catch (error) {
        console.error("There was a problem editing the user:", error);
      }
    },
    cancelEdit() {
      this.showModal = false;
      this.editingUser = null;
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchAreas();
    this.fetchExpertises();
    this.fetchUsers();
  },
};
</script>

<style scoped></style>
