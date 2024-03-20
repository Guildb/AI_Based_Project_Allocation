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
        :group-options="{ enabled: true }"
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
        <template v-slot:body="{ row, column, rowIndex }">
          <span v-if="column.field === 'expand'">
            <button @click="toggleExpand(rowIndex)">
              {{ expandedRows.includes(rowIndex) ? "Collapse" : "Expand" }}
            </button>
          </span>
          <span v-if="column.field === 'projectName'">
            {{ row.name }}
          </span>
          <span v-else-if="column.field === 'studentName'">
            {{ this.getStudentName(row.student_id) }}
          </span>
          <span v-else-if="column.field === 'tutorName'">
            {{ this.getTutorName(row.tutor_id) }}
          </span>
          <span v-else-if="column.field === 'alocated'">
            {{ row.alocated ? "Alocated" : "Not Alocated" }}
          </span>
          <span v-else-if="column.field === 'actions'">
            <button
              @click="editProject(row)"
              class="bg-green-700 hover:bg-green-500 text-white font-bold py-2 px-4 rounded"
            >
              Edit
            </button>
            <button
              class="w-full sm:w-auto bg-slate-700 hover:bg-red-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Delete
            </button>
          </span>
        </template>
        <template v-slot:group-row="{ row, groupIndex }">
          <tr v-if="expandedRows.includes(groupIndex)">
            <td colspan="100%">
              <!-- Your expanded row content here -->
              <div>Project Description {{ row.description }}</div>
              <div>Area: {{ this.getAreaName(row.area_id) }}</div>
              <div>
                Expertises: {{ this.getExpertiseNames(row.expertises) }}
              </div>
            </td>
          </tr>
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
        <div class="text-lg font-semibold">Editing Project</div>

        <div class="flex justify-center space-x-2">
          <button
            @click="saveProject()"
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
      editingProject: null,
      tutors: [],
      students: [],
      areas: [],
      expertises: [],
      projects: [],
      expandedRows: [],
      columns: [
        {
          label: "Expand",
          field: "expand",
          sortable: false,
          width: "100px",
        },
        { label: "Project Name", field: "projectName" },
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
      this.fetchAreas();
      this.fetchExpertises();
      this.fetchProjects();
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
      this.showModal = true;
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
      this.editingProject = null;
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
