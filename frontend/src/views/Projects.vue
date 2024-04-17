<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center p-24">
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in p-1"
      :class="{ 'opacity-100': isAnimated }"
    >
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
          <span v-else-if="props.column.field === 'tutorName'">
            {{ props.row.tutorName }}
          </span>
          <span v-else-if="props.column.field === 'alocated'">
            {{ props.row.alocated ? "Alocated" : "Not Alocated" }}
          </span>
          <span v-else-if="props.column.field === 'actions'">
            <button
              v-if="user.type === 'courseLeader' || user.type === 'admin'"
              @click="moreDetails(props.row)"
              class="w-full sm:w-auto bg-slate-700 hover:bg-blue-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              More Details
            </button>
            <button
              v-if="user.type === 'courseLeader' || user.type === 'admin'"
              @click="deleteProject(props.row.id)"
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
        <div v-if="editingProject">
          <div class="text-lg font-semibold">Edit Project</div>
          <div>
            New Tutor:
            <select
              v-model="newTutorId"
              class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
            >
              <option
                v-for="tutor in matched_tutors"
                :key="tutor.tutor_id"
                :value="tutor.tutor_id"
              >
                {{ getTutorName(tutor.tutor_id) }} With:
                {{ tutor.match_percentage * 100 }} %
              </option>
            </select>
          </div>
        </div>
        <div v-else>
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
        </div>

        <div
          class="flex flex-col sm:flex-row justify-center sm:space-x-2 space-y-2 sm:space-y-0"
        >
          <button
            v-if="!editingProject && inspectingProject.student_id && !findTutor"
            @click="findTutors()"
            class="w-full sm:w-auto bg-slate-700 hover:bg-green-700 flex-1 justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Find Tutor
          </button>
          <button
            v-if="findTutor"
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
      editingProject: false,
      showModal: false,
      findTutor: false,
      inspectingProject: null,
      newTutorId: null,
      matched_tutors: [],
      tutors: [],
      students: [],
      areas: [],
      user: {},
      expertises: [],
      projects: [],
      columns: [
        { label: "Project Name", field: "name" },
        { label: "Student Name", field: "studentName" },
        { label: "Tutor Name", field: "tutorName" },
        { label: "Alocated", field: "alocated", sortable: false },
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
      return area ? area.name : "NaN";
    },
    getStudentName(studentId) {
      const sName = this.students.find(
        (student) => student.student_id === studentId
      );
      return sName ? `${sName.firstName} ${sName.lastName}` : "NaN";
    },
    getTutorName(tutorId) {
      const tName = this.tutors.find((tutor) => tutor.tutor_id === tutorId);
      return tName ? `${tName.firstName} ${tName.lastName}` : "NaN";
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
    cancelEdit() {
      this.showModal = false;
      this.editingProject = false;
      this.findTutor = false;
      this.inspectingProject = null;
      this.newTutorId = null;
    },
    moreDetails(project) {
      this.inspectingProject = { ...project };
      this.showModal = true;
    },
    async findTutors() {
      this.findTutor = true;
      this.editingProject = true;
      this.newTutorId = this.inspectingProject.tutor_id;
      const token = localStorage.getItem("token");
      try {
        const response = await fetch(
          `${process.env.VUE_APP_BACKEND_URL}/findTutor`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              project: this.inspectingProject,
              tutors: this.tutors,
            }),
          }
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        this.matched_tutors = data.match_percentages;
      } catch (error) {
        console.error("There was a problem editing the project:", error);
      }
    },
    async saveProject() {
      if (this.newTutorId === this.inspectingProject.tutor_id) {
        this.cancelEdit();
      } else {
        this.inspectingProject.tutor_id = this.newTutorId;
        const token = localStorage.getItem("token");
        try {
          const response = await fetch(
            `${process.env.VUE_APP_BACKEND_URL}/saveNewTutor`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({
                project: this.inspectingProject,
              }),
            }
          );

          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          this.cancelEdit();
          this.fetchProjects();
        } catch (error) {
          console.error("There was a problem saving the project:", error);
        }
      }
    },
  },
  computed: {
    filteredProjects() {
      if (this.user.type === "admin") {
        return this.projects;
      } else {
        return this.projects.filter(
          (project) =>
            project.area_id === this.user.area_id ||
            project.area_id == null ||
            project.area_id === 0
        );
      }
    },
    processedProjects() {
      return this.filteredProjects.map((project) => ({
        ...project,
        studentName:
          project.student_id === 0 || !project.student_id
            ? "NaN"
            : this.getStudentName(project.student_id),
        tutorName:
          project.tutor_id === 0 || !project.tutor_id
            ? "NaN"
            : this.getTutorName(project.tutor_id),
      }));
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchData();
    this.getUser();
  },
};
</script>
