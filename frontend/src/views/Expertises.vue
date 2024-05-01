<template>
  <navbar />
  <div
    class="min-h-screen flex justify-center items-center px-4 py-24 sm:px-24"
  >
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in p-1"
      :class="{ 'opacity-100': isAnimated }"
    >
      <h1 class="text-4xl font-bold mb-4 text-slate-700 p-4">Expertises</h1>
      <vue-good-table
        :columns="columns"
        :rows="filteredExpertises"
        :pagination-options="{ enabled: true }"
        :search-options="{ enabled: true }"
        styleClass="vgt-table striped condensed"
        theme="nocturnal"
      >
        <template v-slot:table-actions>
          <button
            v-if="user.type === 'courseLeader' || user.type === 'admin'"
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
              v-if="user.type === 'courseLeader' || user.type === 'admin'"
              @click="deleteExpertise(props.row.id)"
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
          v-if="user.type === 'admin'"
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
            @click="cancelEdit()"
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
      user: {},
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
    getUser() {
      const token = localStorage.getItem("token");

      fetch(`${process.env.VUE_APP_BACKEND_URL}/get_current_user`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ token: token }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          if (data.type === "student") {
            alert("Access denied!");
            this.$router.push("/dashboard");
          }
          this.user = data;
        })
        .catch((error) => {
          console.error("There was a problem fetching the user:", error);
        });
    },
    addExpertise() {
      const expertiseName = this.newName.trim();
      const expertiseAcronym = this.newAcronym.trim();
      let areaId = null;
      if (this.user.type !== "admin") {
        areaId = this.user.area_id;
      } else {
        areaId = this.newArea;
      }
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
          this.cancelEdit();
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
    cancelEdit() {
      this.showInput = false;
      this.newName = "";
      this.newAcronym = "";
      this.newArea = null;
    },
    findAreaName(areaId) {
      const area = this.areas.find((area) => area.id === areaId);
      return area ? area.name : "NaN";
    },
    deleteExpertise(expertise_id) {
      const token = localStorage.getItem("token");
      fetch(`${process.env.VUE_APP_BACKEND_URL}/deleteExpertise`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ expertise_id: expertise_id }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(() => {
          this.fetchExpertises();
        })
        .catch((error) => {
          console.error("There was a problem deleting the area:", error);
        });
    },
  },
  computed: {
    filteredExpertises() {
      if (this.user.type === "admin") {
        return this.expertises;
      } else {
        return this.expertises.filter(
          (expertise) => expertise.area_id === this.user.area_id
        );
      }
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchAreas();
    this.fetchExpertises();
    this.getUser();
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
