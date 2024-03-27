<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center p-4">
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in p-1"
      :class="{ 'opacity-100': isAnimated }"
    >
      <vue-good-table
        :columns="columns"
        :rows="expertises"
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
            Add Expertise
          </button>
        </template>
        <template v-slot:table-row="props">
          <span v-if="props.column.field === 'name'">
            {{ props.row.name }}
          </span>
          <span v-else-if="props.column.field === 'acronym'">
            {{ props.row.acronyms }}
          </span>
          <span v-else-if="props.column.field === 'area'">
            {{ findAreaName(props.row.area_id) }}
          </span>
          <span v-else-if="props.column.field === 'actions'">
            <button
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
        <div class="text-lg font-semibold">Add New Expertise</div>
        <input
          v-model="newName"
          placeholder="Expertise Name"
          class="bg-gray-200 text-gray-700 py-1 px-2 rounded"
        />
        <input
          v-model="newAcronym"
          placeholder="Expertise Acronym"
          class="bg-gray-200 text-gray-700 py-1 px-2 rounded"
        />

        <select
          v-model="newArea"
          class="bg-gray-200 text-gray-700 py-1 px-2 rounded"
        >
          <option disabled value="">Select an Expertise Area</option>
          <option v-for="area in areas" :key="area.id" :value="area.id">
            {{ area.name }}
          </option>
        </select>
        <div class="flex justify-center space-x-2">
          <button
            @click="addExpertise()"
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
  name: "ExpertisesPage",
  components: {
    navbar,
    VueGoodTable,
  },
  data() {
    return {
      isAnimated: false,
      expertises: [],
      areas: [],
      showInput: false,
      newName: "",
      newAcronym: "",
      newArea: null,
      columns: [
        { label: "Name", field: "name" },
        { label: "Acronym", field: "acronym" },
        { label: "Area", field: "area" },
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
    addExpertise() {
      const expertiseName = this.newName.trim();
      const expertiseAcronym = this.newAcronym.trim();
      const areaId = this.newArea;
      const token = localStorage.getItem("token");
      if (!expertiseName) {
        alert("Expertise name is required.");
        return;
      } else if (!expertiseAcronym) {
        alert("Expertise acronym is required.");
        return;
      } else if (!areaId && areaId !== 0) {
        alert("Area ID is required.");
        return;
      }
      fetch(`${process.env.VUE_APP_BACKEND_URL}/addExpertise`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: expertiseName,
          acronym: expertiseAcronym,
          area_id: areaId,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(() => {
          this.showInput = false;
          this.newName = "";
          this.newAcronym = "";
          this.newArea = null;
          this.fetchExpertises();
        })
        .catch((error) => {
          console.error("There was a problem adding the area:", error);
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
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.expertises = data;
        })
        .catch((error) => {
          console.error(
            "There was a problem fetching the expertises data:",
            error
          );
        });
    },
    toggleInput() {
      this.showInput = !this.showInput;
      // Initialize data here if needed
      if (this.showInput) {
        // Reset the input field when opening the modal
        this.newName = "";
        this.newAcronym = "";
        this.newArea = null;
      }
    },
    findAreaName(areaId) {
      const area = this.areas.find((area) => area.id === areaId);
      return area ? area.name : "Unknown Area";
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchAreas();
    this.fetchExpertises();
  },
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>