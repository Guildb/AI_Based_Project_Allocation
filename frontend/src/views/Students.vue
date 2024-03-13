<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center p-4">
    <div
      class="w-full max-w-4xl bg-gray-200 bg-opacity-50 rounded-lg shadow-lg transition-opacity duration-700 ease-in p-1"
      :class="{ 'opacity-100': isAnimated }"
    >
      <div>
        <table id="myTable" width="100%">
          <thead>
            <tr>
              <th class="px-4 py-2">Name</th>
              <th class="px-4 py-2">Email</th>
              <th class="px-4 py-2">Student No.</th>
              <th class="px-4 py-2">Type</th>
              <th class="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td class="px-4 py-2">
                {{ user.firstName }} {{ user.lastName }}
              </td>
              <td class="px-4 py-2">{{ user.email }}</td>
              <td class="px-4 py-2">{{ user.student_number }}</td>
              <td class="px-4 py-2">
                <div v-if="editingUserId === user.id">
                  <select
                    v-model="user.newType"
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
                  {{ user.type }}
                </div>
              </td>
              <td class="px-4 py-2">
                <button
                  v-if="editingUserId !== user.id"
                  @click="editUser(user)"
                  class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                  Edit
                </button>
                <div v-if="editingUserId === user.id">
                  <button
                    @click="changeUserType(user)"
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
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import DataTable from "datatables.net-dt";
import navbar from "@/components/NavBar.vue";

export default {
  name: "StudentsPage",
  components: {
    navbar,
  },
  data() {
    return {
      isAnimated: false,
      users: [],
      typeList: [
        { value: "student", name: "Student" },
        { value: "tutor", name: "Tutor" },
        { value: "courseLeader", name: "Course Leader" },
      ],
      editingUserId: null,
    };
  },

  methods: {
    async changeUserType(user) {
      try {
        const response = await fetch(
          `${process.env.VUE_APP_BACKEND_URL}/changeUserType`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ id: user.id, newType: user.newType }),
          }
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        this.editingUserId = null;
        window.location.reload();
      } catch (error) {
        console.error("There was a problem updating the user type:", error);
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
          this.$nextTick(() => {
            new DataTable("#myTable", {
              responsive: true,
              scrollX: true,
            });
          });
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
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100);
    this.fetchUsers();
  },
};
</script>
