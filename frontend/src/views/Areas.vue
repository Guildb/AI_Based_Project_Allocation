<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center p-4">
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in p-1"
      :class="{ 'opacity-100': isAnimated }"
    >
      <vue-good-table
        :columns="columns"
        :rows="areas"
        :pagination-options="{ enabled: true }"
        :search-options="{ enabled: true }"
        styleClass="vgt-table striped condensed"
        theme="nocturnal"
      >
        <template v-slot:table-actions>
          <button
            @click="toggleInput"
            class="w-full sm:w-auto bg-slate-700 hover:bg-green-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Add Area
          </button>
        </template>
        <template v-slot:table-row="props">
          <span v-if="props.column.field === 'name'">
            {{ props.row.name }}
          </span>
          <span v-else-if="props.column.field === 'actions'">
            <button
              @click="deleteArea(props.row.id)"
              class="w-full sm:w-auto bg-slate-700 hover:bg-red-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Delete
            </button>
          </span>
        </template>
      </vue-good-table>
    </div>
  </div>

  <transition name="fade">
    <div
      v-if="showInput"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center p-4"
    >
      <div class="bg-white p-4 sm:p-6 rounded-lg max-w-md w-full space-y-4">
        <div class="text-lg font-semibold">Add New Area</div>
        <input
          v-model="newName"
          placeholder="Area Name"
          class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
        />
        <div class="flex justify-center space-x-2">
          <button
            @click="addArea()"
            class="w-full sm:w-auto bg-slate-700 hover:bg-green-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
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
            class="w-full sm:w-auto bg-slate-700 hover:bg-red-700 inline-flex items-center justify-center flex-1 py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { VueGoodTable } from "vue-good-table-next";
import "vue-good-table-next/dist/vue-good-table-next.css";
import navbar from "@/components/NavBar.vue";

export default {
  name: "AreasPage",
  components: {
    navbar,
    VueGoodTable,
  },
  data() {
    return {
      isAnimated: false,
      areas: [],
      showInput: false,
      newName: "",
      columns: [
        { label: "Name", field: "name" },
        {
          label: "Actions",
          field: "actions",
          sortable: false,
          tdClass: "text-right",
        },
      ],
    };
  },

  methods: {
    addArea() {
      const areaName = this.newName.trim();
      const token = localStorage.getItem("token");
      if (!areaName) {
        alert("Area name cannot be empty.");
        return;
      }

      fetch(`${process.env.VUE_APP_BACKEND_URL}/addArea`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
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
          this.fetchAreas();
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
    deleteArea(area_id) {
      const token = localStorage.getItem("token");
      fetch(`${process.env.VUE_APP_BACKEND_URL}/deleteArea`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ area_id: area_id }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(() => {
          this.fetchAreas();
        })
        .catch((error) => {
          console.error("There was a problem deleting the area:", error);
        });
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
