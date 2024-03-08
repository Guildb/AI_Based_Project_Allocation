<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center p-4">
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in"
      :class="{ 'opacity-100': isAnimated }"
    >
      <button
        @click="toggleInput"
        class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
      >
        Add Area
      </button>
      <div class="overflow-auto">
        <table id="myTable" class="display min-w-full">
          <thead>
            <tr>
              <th class="px-4 py-2">Name</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="area in areas" :key="area.id">
              <td class="px-4 py-2">{{ area.name }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <transition name="fade">
    <div
      v-if="showInput"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center"
    >
      <div class="bg-white p-4 rounded-lg max-w-md w-full space-y-4">
        <div class="text-lg font-semibold">Add New Area</div>
        <input
          v-model="newName"
          placeholder="Area Name"
          class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
        />
        <div class="flex justify-center space-x-2">
          <button
            @click="addArea()"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Save
          </button>
          <button
            @click="
              showInput = false;
              newName = '';
              newAcronym = '';
              newArea = null;
            "
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
  name: "DataTableComponent",
  components: {
    navbar,
  },
  data() {
    return {
      isAnimated: false,
      areas: [],
      showInput: false,
      newName: "",
    };
  },

  methods: {
    addArea() {
      const areaName = this.newName.trim();
      if (!areaName) {
        alert("Area name cannot be empty.");
        return;
      }

      fetch(`${process.env.VUE_APP_BACKEND_URL}/addArea`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: areaName }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(() => {
          this.showAddArea = false;
          this.newAreaName = "";
          this.fetchAreas(); // Fetch areas again to update the list
        })
        .catch((error) => {
          console.error("There was a problem adding the area:", error);
        });
    },

    fetchAreas() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/areas`) // Adjust the URL as needed
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.areas = data;
          this.$nextTick(() => {
            new DataTable("#myTable", {
              responsive: true,
            });
          });
        })
        .catch((error) => {
          console.error("There was a problem fetching the areas data:", error);
        });
    },
    toggleInput() {
      this.showInput = !this.showInput;
      // Initialize data here if needed
      if (this.showInput) {
        // Reset the input field when opening the modal
        this.newName = "";
      }
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchAreas();
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
