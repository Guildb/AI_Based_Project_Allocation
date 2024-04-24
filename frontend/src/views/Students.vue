<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center p-24">
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in p-1"
      :class="{ 'opacity-100': isAnimated }"
    >
    <h1 class="text-4xl font-bold mb-4 text-slate-700 p-4">Students</h1>
      <vue-good-table
        :columns="columns"
        :rows="processStudents"
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
          <span v-else-if="props.column.field === 'student_number'">
            {{ props.row.student_number }}
          </span>
          <span v-else-if="props.column.field === 'type'">
            <div v-if="editingUserId === props.row.id">
              <select
                v-model="props.row.newType"
                class="bg-gray-200 text-gray-700 py-1 px-2 rounded"
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
            <div v-else>
              {{
                (
                  typeList.find(
                    (typeItem) => typeItem.value === props.row.type
                  ) || {}
                ).name || props.row.type
              }}
            </div>
          </span>
          <span v-else-if="props.column.field === 'actions'">
            <button
              v-if="
                (user.type === 'courseLeader' || user.type === 'admin') &&
                editingUserId !== props.row.id
              "
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
            <div v-if="editingUserId === props.row.id">
              <button
                @click="changeUserType(props.row)"
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
          </span>
        </template>
      </vue-good-table>
    </div>
  </div>
</template>

<script>
import { VueGoodTable } from "vue-good-table-next";
import "vue-good-table-next/dist/vue-good-table-next.css";
import navbar from "@/components/NavBar.vue";

export default {
  name: "StudentsPage",
  components: {
    navbar,
    VueGoodTable,
  },
  data() {
    return {
      isAnimated: false,
      users: [],
      user: {},
      typeList: [
        { value: "student", name: "Student" },
        { value: "tutor", name: "Tutor" },
        { value: "courseLeader", name: "Course Leader" },
      ],
      editingUserId: null,
      editingUser: {},
      columns: [
        { label: "Name", field: "fullName" },
        { label: "Email", field: "email" },
        { label: "Student No.", field: "student_number" },
        { label: "Type", field: "type", tdClass: "text-center" },
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
    async changeUserType(user) {
      const token = localStorage.getItem("token");
      if (user.type !== user.newType) {
        try {
          const response = await fetch(
            `${process.env.VUE_APP_BACKEND_URL}/changeUserType`,
            {
              method: "POST",
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ id: user.id, newType: user.newType }),
            }
          );

          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          this.editingUserId = null;
          this.fetchUsers();
        } catch (error) {
          console.error("There was a problem updating the user type:", error);
        }
      } else {
        this.editingUserId = null;
        this.fetchUsers();
      }
    },
    fetchUsers() {
      fetch(`${process.env.VUE_APP_BACKEND_URL}/students`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.users = data.map((user) => ({
            ...user,
            showDropdown: false,
            newType: user.type,
          }));
        })
        .catch((error) => {
          console.error("There was a problem fetching the user data:", error);
        });
    },
    editUser(user) {
      if (this.editingUserId) {
        const originalUserDataIndex = this.users.findIndex(
          (user) => user.id === this.editingUserId
        );
        if (originalUserDataIndex !== -1) {
          this.users[originalUserDataIndex] = this.editingUser;
        }
      }
      this.editingUserId = user.id;
      this.editingUser = Object.assign({}, user);
    },
    cancelEdit() {
      if (this.editingUserId) {
        const originalUserDataIndex = this.users.findIndex(
          (user) => user.id === this.editingUserId
        );
        if (originalUserDataIndex !== -1) {
          this.users[originalUserDataIndex] = this.editingUser;
        }
      }
      this.editingUserId = null;
      this.editingUser = {};
    },
    deleteUser(user) {
      const token = localStorage.getItem("token");
      fetch(`${process.env.VUE_APP_BACKEND_URL}/deleteStudent`, {
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
    filteredStudents() {
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
    processStudents() {
      return this.filteredStudents.map((student) => ({
        ...student,
        fullName: `${student.firstName} ${student.lastName}`,
      }));
    },
  },

  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchUsers();
    this.getUser();
  },
};
</script>
