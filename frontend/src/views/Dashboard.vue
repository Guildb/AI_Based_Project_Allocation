<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center">
    <div
      class="w-3/4 bg-gray-200 bg-opacity-50 rounded-lg shadow-lg p-4 transition-opacity duration-700 ease-in opacity-0"
      :class="{ 'opacity-100': isAnimated }"
    >
      <h1 class="text-4xl font-bold mb-4 text-slate-700">
        Welcome {{ user.firstName }} {{ user.lastName }}
      </h1>
      <button
        v-if="
          user.type !== 'student' || (user.type === 'student' && !user.project)
        "
        @click="addProject()"
        class="bg-slate-700 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
      >
        Add Project
      </button>

      <div class="p-4">
        <div class="max-w-4xl mx-auto">
          <div class="bg-white shadow-md rounded-lg overflow-hidden">
            <div class="p-4 md:p-6 lg:p-8">
              <h2 class="text-2xl font-semibold mb-4">Projects Details</h2>
              <div v-if="user.type !== 'student'"></div>
              <div
                class="grid grid-cols-1 sm:grid-cols-2 gap-4"
                v-if="user.projects"
              >
                <div v-for="project in user.projects" :key="project">
                  <div>
                    <h3 class="text-lg font-semibold">Project Name</h3>
                    <p>{{ user.project.name }}</p>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold">Student Name</h3>
                    <p>{{ getStudentName(user.project.student_id) }}</p>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold">Description</h3>
                    <p>{{ user.project.description }}</p>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold">Area</h3>
                    <p>{{ getAreaName(user.project.area_id) }}</p>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold">Expertises</h3>
                    <p>{{ getExpertiseNames(user.project.expertises) }}</p>
                  </div>
                </div>
              </div>
              <div
                class="grid grid-cols-1 sm:grid-cols-2 gap-4"
                v-if="user.project"
              >
                <div>
                  <div>
                    <h3 class="text-lg font-semibold">Project Name</h3>
                    <p>{{ user.project.name }}</p>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold">Tutor Name</h3>
                    <p>{{ getTutorName(user.project.tutor_id) }}</p>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold">Description</h3>
                    <p>{{ user.project.description }}</p>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold">Area</h3>
                    <p>{{ getAreaName(user.project.area_id) }}</p>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold">Expertises</h3>
                    <p>{{ getExpertiseNames(user.project.expertises) }}</p>
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
      v-if="showModal"
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
        <div v-if="(this.user.type = 'student')">
          Pre selected Tutor
          <select
            v-model="newProject.tutor_id"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          >
            <option v-for="tutor in tutors" :key="tutor.id" :value="tutor.id">
              {{ tutor.firstName }} {{ tutor.lastName }}
            </option>
          </select>
        </div>
        <div>
          Area
          <select
            v-model="newProject.area_id"
            class="bg-gray-200 text-gray-700 py-1 px-2 rounded w-full"
          >
            <option v-for="area in areas" :key="area.id" :value="area.id">
              {{ area.name }}
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
</template>

<script>
import navbar from "@/components/NavBar.vue";
export default {
  name: "DashBoard",
  components: {
    navbar,
  },
  data() {
    return {
      isAnimated: false,
      showModal: false,
      user: {},
      areas: [],
      expertises: [],
      tutors: [],
      students: [],
      newProject: {
        name: "",
        description: "",
        student_id: null,
        tutor_id: null,
        area_id: null,
        alocated: null,
        expertises: [],
      },
    };
  },
  methods: {
    addProject() {
      this.showModal = true;
    },
    saveProject() {
      console.log(this.newProject);
      if (this.user.type === "student") {
        this.newProject.student_id = this.user.student_id;
      } else {
        this.newProject.tutor_id = this.user.tutor_id;
      }
      if (!this.newProject.name.trim()) {
        alert("Projec name cannot be empty.");
        return;
      }
      if (!this.newProject.description.trim()) {
        alert("Projec description cannot be empty.");
        return;
      }
      if (!this.newProject.area_id) {
        alert("You need to select a area");
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
        body: JSON.stringify({ project: this.newProject }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(() => {
          this.showModal = false;
          window.location.reload();
        })
        .catch((error) => {
          console.error("There was a problem adding the project:", error);
        });
    },
    cancelEdit() {
      this.showModal = false;
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
          console.log(data);
          this.user = data;
          if (this.user.type === "student") {
            this.fetchTutors();
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
      return tName ? `${tName.firstName} ${tName.lastName}` : "Not Found";
    },
    getStudentName(studentId) {
      const sName = this.students.find(
        (student) => student.student_id === studentId
      );
      return sName ? `${sName.firstName} ${sName.lastName}` : "Not Found";
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
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.getInicialData();
  },
};
</script>
