<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center p-24">
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in p-1"
      :class="{ 'opacity-100': isAnimated }"
    >
      <vue-good-table
        :columns="columns"
        :rows="processedTutors"
        :pagination-options="{ enabled: true }"
        :search-options="{ enabled: true }"
        styleClass="vgt-table striped condensed"
        theme="nocturnal"
      >
        <template v-slot:table-row="props">
          <span v-if="props.column.field === 'fullName'">
            {{ props.row.fullName }}
          </span>
          <span v-else-if="props.column.field === 'email'">
            {{ props.row.email }}
          </span>
          <span v-else-if="props.column.field === 'type'">
            {{
              (
                typeList.find(
                  (typeItem) => typeItem.value === props.row.type
                ) || {}
              ).name || props.row.type
            }}
          </span>
          <span v-else-if="props.column.field === 'slots'">
            {{ props.row.slots }}
          </span>
          <span v-else-if="props.column.field === 'area'">
            {{ props.row.areaName }}
          </span>
          <span v-else-if="props.column.field === 'expertises'">
            {{ props.row.expertisesName }}
          </span>
          <span v-else-if="props.column.field === 'actions'">
            <button
              v-if="user.type === 'courseLeader' || user.type === 'admin'"
              @click="editUser(props.row)"
              class="w-full sm:w-auto bg-slate-700 hover:bg-green-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Edit
            </button>
            <button
              v-if="user.type === 'courseLeader' || user.type === 'admin'"
              @click="deleteUser(props.row)"
              class="w-full sm:w-auto bg-slate-700 hover:bg-red-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Delete
            </button>
          </span>
        </template>
      </vue-good-table>
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
            v-model="editingUser.area_id"
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
              v-for="expertise in filteredExpertises"
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
  name: "TutorsPage",
  components: {
    navbar,
    VueGoodTable,
  },
  data() {
    return {
      user: {},
      isAnimated: false,
      showModal: false,
      editingUser: null,
      users: [],
      areas: [],
      expertises: [],
      typeList: [
        { value: "student", name: "Student" },
        { value: "tutor", name: "Tutor" },
        { value: "courseLeader", name: "Course Leader" },
      ],
      columns: [
        { label: "Name", field: "fullName" },
        { label: "Email", field: "email" },
        { label: "Type", field: "type", tdClass: "text-center" },
        { label: "Slots", field: "slots", type: "number" },
        { label: "Area", field: "areaName" },
        { label: "Expertises", field: "expertiseNames" },
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
      return area ? area.name : "NaN";
    },
    editUser(user) {
      this.editingUser = { ...user, originalType: user.type };
      this.showModal = true;
      console.log(this.editingUser);
    },
    async saveUser() {
      const token = localStorage.getItem("token");
      try {
        const response = await fetch(
          `${process.env.VUE_APP_BACKEND_URL}/changeTutors`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ user: this.editingUser }),
          }
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        await response.json();
        this.cancelEdit();
        this.fetchUsers();
      } catch (error) {
        console.error("There was a problem editing the user:", error);
      }
    },
    cancelEdit() {
      this.showModal = false;
      this.editingUser = null;
    },
    deleteUser(user) {
      const token = localStorage.getItem("token");
      fetch(`${process.env.VUE_APP_BACKEND_URL}/deleteTutor`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ user: user }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(() => {
          this.fetchUsers();
        })
        .catch((error) => {
          console.error("There was a problem deleting the user:", error);
        });
    },
  },
  computed: {
    filteredExpertises() {
      // If an area is selected, filter expertises by the selected areaId
      if (this.editingUser.area_id) {
        return this.expertises.filter(
          (expertise) => expertise.area_id === this.editingUser.area_id
        );
      }
      // If no area is selected, return all expertises
      return this.expertises;
    },
    filteredTutors() {
      if (this.user.type === "admin") {
        return this.users;
      } else {
        return this.users.filter(
          (user) =>
            user.area_id === this.user.area_id ||
            user.area_id == null ||
            user.area_id === 0
        );
      }
    },
    processedTutors() {
      return this.filteredTutors.map((tutor) => ({
        ...tutor,
        fullName: `${tutor.firstName} ${tutor.lastName}`,
        areaName: tutor.area_id === 0 ? "NaN" : this.getAreaName(tutor.area_id),
        expertiseNames:
          tutor.expertises.length === 0
            ? "NaN"
            : this.getExpertiseNames(tutor.expertises),
      }));
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchAreas();
    this.fetchExpertises();
    this.fetchUsers();
    this.getUser();
  },
};
</script>
