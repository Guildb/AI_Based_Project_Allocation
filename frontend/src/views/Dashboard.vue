<template>
  <navbar />
  <div
    class="min-h-screen flex justify-center items-center px-4 py-24 sm:px-24"
  >
    <div
      class="w-full sm:w-3/4 bg-gray-200 bg-opacity-50 rounded-lg shadow-lg p-4 transition-opacity duration-700 ease-in opacity-0"
      :class="{ 'opacity-100': isAnimated }"
    >
      <div v-if="user.type === 'admin'">
        <h1 class="text-4xl font-bold mb-4 text-slate-700">Welcome admin</h1>
      </div>
      <div v-else>
        <h1 class="text-4xl font-bold mb-4 text-slate-700">
          Welcome {{ user.firstName }} {{ user.lastName }}
        </h1>
        <div
          class="flex flex-col sm:flex-row justify-center sm:space-x-2 space-y-2 sm:space-y-0"
        >
          <button
            v-if="user.type === 'student' && !user.student_id"
            @click="addStudentNumber()"
            class="bg-slate-700 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          >
            Add Student Number
          </button>
          <button
            v-if="
              user.type !== 'student' ||
              (user.type === 'student' && !user.project && user.student_id)
            "
            @click="addProject()"
            class="bg-slate-700 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Add Project
          </button>
          <button
            v-if="
              user.type === 'student' &&
              !user.project &&
              !availableProjects &&
              user.student_id
            "
            @click="this.availableProjects = true"
            class="bg-slate-700 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Available Projects
          </button>
          <button
            v-if="availableProjects && !user.project"
            @click="this.availableProjects = false"
            class="bg-slate-700 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
          >
            Close
          </button>
        </div>
        <div v-if="availableProjects && !user.project" class="pt-4">
          <vue-good-table
            :columns="studentColumns"
            :rows="processedProjects"
            :pagination-options="{ enabled: true }"
            :search-options="{ enabled: true }"
            styleClass="vgt-table striped condensed"
            theme="nocturnal"
          >
            <template v-slot:table-row="props">
              <span v-if="props.column.field === 'name'">
                {{ props.row.name }}
              </span>
              <span v-else-if="props.column.field === 'tutorName'">
                {{ props.row.tutorName }}
              </span>
              <span v-else-if="props.column.field === 'alocated'">
                {{ props.row.alocated ? "Alocated" : "Not Alocated" }}
              </span>
              <span v-else-if="props.column.field === 'actions'">
                <button
                  @click="moreDetails(props.row)"
                  class="w-full sm:w-auto bg-slate-700 hover:bg-blue-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  More Details
                </button>
                <button
                  @click="chooseProject(props.row.id)"
                  class="w-full sm:w-auto bg-slate-700 hover:bg-red-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Choose
                </button>
              </span>
            </template>
          </vue-good-table>
        </div>

        <div v-if="user.type !== 'student' && user.projects" class="pt-4">
          <vue-good-table
            :columns="columns"
            :rows="processedProjects"
            :pagination-options="{ enabled: true }"
            :search-options="{ enabled: true }"
            styleClass="vgt-table striped condensed"
            theme="nocturnal"
          >
            <template v-slot:table-row="props">
              <span v-if="props.column.field === 'name'">
                {{ props.row.name }}
              </span>
              <span v-else-if="props.column.field === 'studentName'">
                {{ props.row.studentName }}
              </span>
              <span v-else-if="props.column.field === 'alocated'">
                {{ props.row.alocated ? "Alocated" : "Not Alocated" }}
              </span>
              <span v-else-if="props.column.field === 'actions'">
                <button
                  @click="moreDetails(props.row)"
                  class="w-full sm:w-auto bg-slate-700 hover:bg-blue-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  More Details
                </button>
                <button
                  @click="deleteProject(props.row.id)"
                  class="w-full sm:w-auto bg-slate-700 hover:bg-red-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Delete
                </button>
              </span>
            </template>
          </vue-good-table>
        </div>

        <div v-if="user.type === 'student' && user.project">
          <div class="p-4">
            <div class="max-w-4xl mx-auto">
              <div class="bg-white shadow-md rounded-lg overflow-hidden">
                <h2 class="text-2xl font-semibold mb-4">Project Details</h2>
                <button
                  @click="editProject(user.project)"
                  class="w-full sm:w-auto bg-slate-700 hover:bg-blue-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Edit Project
                </button>
                <div class="p-4 md:p-6 lg:p-8">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <h3 class="text-lg font-semibold">Project Name</h3>
                      <p>{{ user.project.name }}</p>
                    </div>
                    <div>
                      <h3 class="text-lg font-semibold">Tutor Name</h3>
                      <p>{{ getTutorName(user.project.tutor_id) }}</p>
                    </div>
                  </div>
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <h3 class="text-lg font-semibold">Area</h3>
                      <p>{{ getAreaName(user.project.area_id) }}</p>
                    </div>
                    <div>
                      <h3 class="text-lg font-semibold">Expertises</h3>
                      <p>{{ getExpertiseNames(user.project.expertises) }}</p>
                    </div>
                  </div>
                  <div class="grid grid-cols-1">
                    <h3 class="text-lg font-semibold">Description</h3>
                    <p>{{ user.project.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <transition name="fade">
    <div
      v-if="addSNumberModal"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center p-4"
    >
      <div class="bg-white p-4 sm:p-6 rounded-lg max-w-md w-full space-y-4">
        <div class="text-lg font-semibold">Add new student number</div>
        <div>
          <input
            v-model="newSNumber"
            placeholder="StudentNumber"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          />
        </div>
        <div>
          Area
          <select
            v-model="newSareaId"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          >
            <option v-for="area in areas" :key="area.id" :value="area.id">
              {{ area.name }}
            </option>
          </select>
        </div>
        <div class="flex justify-center space-x-2">
          <button
            @click="saveSNumber()"
            class="w-full sm:w-auto bg-slate-700 hover:bg-green-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Save
          </button>
          <button
            @click="cancelSNumber()"
            class="w-full sm:w-auto bg-slate-700 hover:bg-red-700 inline-flex items-center justify-center flex-1 py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </transition>

  <transition name="fade">
    <div
      v-if="addProjectModal"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center p-4"
    >
      <div class="bg-white p-4 sm:p-6 rounded-lg max-w-md w-full space-y-4">
        <div class="text-lg font-semibold">Add a new Project</div>

        <!-- Example input for editing the user's name -->
        <div>
          <input
            v-model="newProject.name"
            placeholder="Project Name"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          />
        </div>
        <div>
          <textarea
            v-model="newProject.description"
            placeholder="Project Description"
            type="text"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          ></textarea>
        </div>
        <div v-if="user.type === 'student'">
          Pre selected Tutor
          <select
            v-model="newProject.tutor_id"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          >
            <option :key="null" :value="null">N/A</option>
            <option
              v-for="tutor in filteredTutors"
              :key="tutor.id"
              :value="tutor.id"
            >
              {{ tutor.firstName }} {{ tutor.lastName }}
            </option>
          </select>
        </div>
        <div class="max-h-48 overflow-y-auto border p-2">
          <span class="text-lg font-semibold">Expertises</span>
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
                v-model="newProject.expertises"
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
            @click="saveProject()"
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

  <transition name="fade">
    <div
      v-if="projectDetailsModal"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center p-4"
    >
      <div class="bg-white p-4 sm:p-6 rounded-lg max-w-md w-full space-y-4">
        <div class="text-lg font-semibold">Project Details</div>

        <div>
          <label class="block text-sm font-medium text-gray-700"
            >Project Name</label
          >
          <div
            class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 justify-center block w-full sm:text-sm border-gray-300 rounded-md"
          >
            {{ inspectingProject.name }}
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700"
            >Description</label
          >
          <div class="mt-1">
            <div
              class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 justify-center block w-full sm:text-sm border-gray-300 rounded-md"
            >
              {{ inspectingProject.description }}
            </div>
          </div>
        </div>
        <div v-if="this.user.type === 'student'">
          <label class="block text-sm font-medium text-gray-700"
            >Tutor Name</label
          >
          <div class="mt-1">
            <div
              class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 justify-center block w-full sm:text-sm border-gray-300 rounded-md"
            >
              {{ getTutorName(inspectingProject.tutor_id) }}
            </div>
          </div>
        </div>
        <div v-else>
          <label class="block text-sm font-medium text-gray-700"
            >Student Name</label
          >
          <div class="mt-1">
            <div
              class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 justify-center block w-full sm:text-sm border-gray-300 rounded-md"
            >
              {{ getStudentName(inspectingProject.student_id) }}
            </div>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Area</label>
          <div class="mt-1">
            <div
              class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 justify-center block w-full sm:text-sm border-gray-300 rounded-md"
            >
              {{ getAreaName(inspectingProject.area_id) }}
            </div>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700"
            >Expertises</label
          >
          <div class="mt-1">
            <div
              class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 justify-center block w-full sm:text-sm border-gray-300 rounded-md"
            >
              {{ getExpertiseNames(inspectingProject.expertises) }}
            </div>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700"
            >Alocated</label
          >
          <div class="mt-1">
            <div
              class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 justify-center block w-full sm:text-sm border-gray-300 rounded-md"
            >
              {{ inspectingProject.alocated ? "Alocated" : "Not Alocated" }}
            </div>
          </div>
        </div>

        <div class="flex justify-center space-x-2">
          <button
            v-if="this.user.type !== 'student'"
            @click="editProject(inspectingProject)"
            class="w-full sm:w-auto bg-slate-700 hover:bg-blue-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Edit Project
          </button>
          <button
            @click="closeDetails()"
            class="w-full sm:w-auto bg-slate-700 hover:bg-red-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </transition>

  <transition name="fade">
    <div
      v-if="changeDetails"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center p-4"
    >
      <div class="bg-white p-4 sm:p-6 rounded-lg max-w-md w-full space-y-4">
        <div class="text-lg font-semibold">Cahnge Details</div>

        <!-- Example input for editing the user's name -->
        <div>
          <input
            v-model="newProject.name"
            placeholder="Project Name"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          />
        </div>
        <div>
          <textarea
            v-model="newProject.description"
            placeholder="Project Description"
            type="text"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          ></textarea>
        </div>
        <div class="max-h-48 overflow-y-auto border p-2">
          <span class="text-lg font-semibold">Expertises</span>
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
                v-model="newProject.expertises"
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
            @click="saveChanges()"
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
  name: "DashBoard",
  components: {
    navbar,
    VueGoodTable,
  },
  data() {
    return {
      isAnimated: false,
      addProjectModal: false,
      addSNumberModal: false,
      projectDetailsModal: false,
      availableProjects: false,
      changeDetails: false,
      inspectingProject: null,
      newSNumber: "",
      newSareaId: null,
      user: {},
      areas: [],
      expertises: [],
      tutors: [],
      students: [],
      projects: [],
      newProject: {
        name: "",
        description: "",
        student_id: null,
        tutor_id: null,
        area_id: null,
        alocated: null,
        expertises: [],
      },
      studentColumns: [
        { label: "Project Name", field: "name" },
        { label: "Tutor Name", field: "tutorName" },
        { label: "Alocated", field: "alocated" },
        {
          label: "Actions",
          field: "actions",
          sortable: false,
          tdClass: "text-right",
        },
      ],
      columns: [
        { label: "Project Name", field: "name" },
        { label: "Student Name", field: "studentName" },
        { label: "Alocated", field: "alocated" },
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
    editProject(project) {
      this.newProject = { ...project };
      this.newProject.area_id = this.user.area_id;
      this.changeDetails = true;
    },
    moreDetails(project) {
      this.inspectingProject = { ...project };
      this.projectDetailsModal = true;
    },
    closeDetails() {
      this.inspectingProject = null;
      this.projectDetailsModal = false;
    },
    addProject() {
      this.addProjectModal = true;
      this.newProject.area_id = this.user.area_id;
    },
    saveProject() {
      if (this.user.type === "student") {
        this.newProject.student_id = this.user.student_id;
      } else {
        this.newProject.tutor_id = this.user.tutor_id;
      }
      if (!this.newProject.name.trim()) {
        alert("Project name cannot be empty.");
        return;
      }
      if (!this.newProject.description.trim()) {
        alert("Project description cannot be empty.");
        return;
      }
      if (!this.newProject.expertises.length > 0) {
        alert("You need to select the expertises");
        return;
      }
      const token = localStorage.getItem("token");
      fetch(`${process.env.VUE_APP_BACKEND_URL}/addProject`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          project: this.newProject,
          tutors: this.tutors,
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
          this.getUser();
        })
        .catch((error) => {
          console.error("There was a problem adding the project:", error);
        });
    },
    cancelEdit() {
      this.addProjectModal = false;
      this.changeDetails = false;
      this.newProject = {
        name: "",
        description: "",
        student_id: null,
        tutor_id: null,
        area_id: null,
        alocated: null,
        expertises: [],
      };
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
    fetchProjects() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/projects`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.projects = data;
        })
        .catch((error) => {
          console.error(
            "There was a problem fetching the projects data:",
            error
          );
        });
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
    fetchTutors() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/tutors`) // Adjust the URL as needed
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.tutors = data;
        })
        .catch((error) => {
          console.error("There was a problem fetching the tutors data:", error);
        });
    },
    fetchStudents() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/students`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.students = data;
        })
        .catch((error) => {
          console.error(
            "There was a problem fetching the students data:",
            error
          );
        });
    },
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
          this.user = data;
          if (this.user.type === "student") {
            this.fetchTutors();
            this.fetchProjects();
          } else {
            this.fetchStudents();
          }
        })
        .catch((error) => {
          console.error("There was a problem fetching the user:", error);
        });
    },
    getInicialData() {
      this.fetchAreas();
      this.fetchExpertises();
      this.getUser();
    },
    getTutorName(tutorId) {
      const tName = this.tutors.find((tutor) => tutor.tutor_id === tutorId);
      return tName ? `${tName.firstName} ${tName.lastName}` : "NaN";
    },
    getStudentName(studentId) {
      const sName = this.students.find(
        (student) => student.student_id === studentId
      );
      return sName ? `${sName.firstName} ${sName.lastName}` : "NaN";
    },
    addStudentNumber() {
      this.addSNumberModal = true;
      this.newSNumber = "";
    },
    saveSNumber() {
      const newSNumber = this.newSNumber.trim();
      const newSareaId = this.newSareaId;
      const token = localStorage.getItem("token");
      if (!newSNumber) {
        alert("Student Number is required");
        return;
      }
      if (!newSareaId) {
        alert("You need to select an Area");
        return;
      }
      fetch(`${process.env.VUE_APP_BACKEND_URL}/addStudentNumber`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sudent_number: newSNumber,
          user_id: this.user.id,
          area_id: newSareaId,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(() => {
          this.cancelSNumber();
          this.getInicialData();
        })
        .catch((error) => {
          console.error(
            "There was a problem adding the student number:",
            error
          );
        });
    },
    cancelSNumber() {
      this.addSNumberModal = false;
      this.newSNumber = "";
    },
    deleteProject(project_id) {
      const token = localStorage.getItem("token");
      fetch(`${process.env.VUE_APP_BACKEND_URL}/deleteProject`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ project_id: project_id }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(() => {
          this.fetchProjects();
        })
        .catch((error) => {
          console.error("There was a problem deleting the project:", error);
        });
    },
    chooseProject(project_id) {
      const token = localStorage.getItem("token");
      fetch(`${process.env.VUE_APP_BACKEND_URL}/chooseProject`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          project_id: project_id,
          student_id: this.user.student_id,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(() => {
          this.getInicialData();
        })
        .catch((error) => {
          console.error("There was a problem selecting this project:", error);
        });
    },
    saveChanges() {
      if (this.user.type === "student") {
        this.newProject.student_id = this.user.student_id;
      } else {
        this.newProject.tutor_id = this.user.tutor_id;
      }
      if (!this.newProject.name.trim()) {
        alert("Project name cannot be empty.");
        return;
      }
      if (!this.newProject.description.trim()) {
        alert("Project description cannot be empty.");
        return;
      }
      if (!this.newProject.expertises.length > 0) {
        alert("You need to select the expertises");
        return;
      }
      const token = localStorage.getItem("token");
      fetch(`${process.env.VUE_APP_BACKEND_URL}/saveProjectChanges`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          project: this.newProject,
          tutors: this.tutors,
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
          this.getUser();
          this.closeDetails();
        })
        .catch((error) => {
          console.error("There was a problem editing the project:", error);
        });
    },
  },
  computed: {
    filteredExpertises() {
      // If an area is selected, filter expertises by the selected areaId
      if (this.newProject.area_id) {
        return this.expertises.filter(
          (expertise) => expertise.area_id === this.newProject.area_id
        );
      }
      // If no area is selected, return all expertises
      return this.expertises;
    },
    filteredTutors() {
      // If an area is selected, filter tutors by the selected areaId
      if (this.newProject.area_id) {
        return this.tutors.filter(
          (tutor) =>
            tutor.area_id === this.newProject.area_id && tutor.slots > 0
        );
      }
      // If no area is selected, return all tutors
      return this.tutors;
    },
    processedProjects() {
      if (this.user.type === "student") {
        const filteredProjects = this.projects.filter(
          (project) =>
            !project.alocated &&
            project.area_id === this.user.area_id &&
            !project.student_id
        );
        return filteredProjects.map((project) => ({
          ...project,
          tutorName:
            project.tutor_id === 0 || !project.tutor_id
              ? "NaN"
              : this.getTutorName(project.tutor_id),
        }));
      } else {
        return this.user.projects.map((project) => ({
          ...project,
          studentName:
            project.student_id === 0 || !project.student_id
              ? "NaN"
              : this.getStudentName(project.student_id),
        }));
      }
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.getInicialData();
  },
};
</script>
