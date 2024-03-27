<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center p-4">
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in p-1"
      :class="{ 'opacity-100': isAnimated }"
    >
      <vue-good-table
        :columns="columns"
        :rows="projects"
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
            Add Project
          </button>
        </template>
        <template v-slot:table-row="props">
          <span v-if="props.column.field === 'name'">
            {{ props.row.name }}
          </span>
          <span v-else-if="props.column.field === 'studentName'">
            {{
              props.row.student_id
                ? getStudentName(props.row.student_id)
                : "No student"
            }}
          </span>
          <span v-else-if="props.column.field === 'tutorName'">
            {{
              props.row.tutor_id ? getTutorName(props.row.tutor_id) : "No Tutor"
            }}
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
      v-if="showModal"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center p-4"
    >
      <div class="bg-white p-4 sm:p-6 rounded-lg max-w-md w-full space-y-4">
        <div class="text-lg font-semibold">
          {{ editingProject ? "Edit Project" : "Project Details" }}
        </div>

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
        <div>
          <label class="block text-sm font-medium text-gray-700"
            >Student Name</label
          >
          <div class="mt-1">
            <div
              class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 justify-center block w-full sm:text-sm border-gray-300 rounded-md"
            >
              {{ this.getStudentName(inspectingProject.student_id) }}
            </div>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700"
            >Tutor Name</label
          >
          <div class="mt-1">
            <div
              class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
            >
              {{ this.getTutorName(inspectingProject.tutor_id) }}
            </div>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Area</label>
          <div class="mt-1">
            <div
              class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 justify-center block w-full sm:text-sm border-gray-300 rounded-md"
            >
              {{ this.getAreaName(inspectingProject.area_id) }}
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
              {{ this.getExpertiseNames(inspectingProject.expertises) }}
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
            v-if="!editingProject"
            @click="editingProject = true"
            class="w-full sm:w-auto bg-slate-700 hover:bg-blue-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Edit
          </button>
          <button
            v-if="editingProject"
            @click="saveProject()"
            class="w-full sm:w-auto bg-slate-700 hover:bg-blue-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Save
          </button>
          <button
            @click="cancelEdit()"
            class="w-full sm:w-auto bg-slate-700 hover:bg-red-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
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
  name: "ProjectsPage",
  components: {
    navbar,
    VueGoodTable,
  },
  data() {
    return {
      isAnimated: false,
      showModal: false,
      editingProject: false,
      inspectingProject: null,
      tutors: [],
      students: [],
      areas: [],
      expertises: [],
      projects: [],
      columns: [
        { label: "Project Name", field: "name" },
        { label: "Student Name", field: "studentName" },
        { label: "Tutor Name", field: "tutorName" },
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
    fetchTutors() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/tutors`)
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
    getStudentName(studentId) {
      const sName = this.students.find(
        (student) => student.student_id === studentId
      );
      return sName ? `${sName.firstName} ${sName.lastName}` : "Not Found";
    },
    getTutorName(tutorId) {
      const tName = this.tutors.find((tutor) => tutor.tutor_id === tutorId);
      return tName ? `${tName.firstName} ${tName.lastName}` : "Not Found";
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
    fetchData() {
      this.fetchProjects();
      this.fetchAreas();
      this.fetchExpertises();
      this.fetchTutors();
      this.fetchStudents();
    },
    toggleExpand(rowIndex) {
      const index = this.expandedRows.indexOf(rowIndex);
      if (index > -1) {
        this.expandedRows.splice(index, 1); // Collapse row
      } else {
        this.expandedRows.push(rowIndex); // Expand row
      }
    },
    editProject(project) {
      this.editingProject = { ...project };
    },
    async saveProject() {
      try {
        console.log(this.editingProject);
        const response = await fetch(
          `${process.env.VUE_APP_BACKEND_URL}/changeProject`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ user: this.editingProject }),
          }
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        await response.json();
        this.cancelEdit();
        this.fetchProjects();
      } catch (error) {
        console.error("There was a problem editing the project:", error);
      }
    },
    cancelEdit() {
      this.showModal = false;
      this.editingProject = false;
      this.inspectingProject = null;
    },
    moreDetails(project) {
      this.inspectingProject = { ...project };
      this.showModal = true;
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchData();
  },
};
</script>
