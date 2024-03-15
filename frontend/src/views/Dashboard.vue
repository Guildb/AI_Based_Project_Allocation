<template>
  <navbar />
  <div class="min-h-screen flex justify-center items-center">
    <div
      class="w-3/4 bg-gray-200 bg-opacity-50 rounded-lg shadow-lg p-4 transition-opacity duration-700 ease-in opacity-0"
      :class="{ 'opacity-100': isAnimated }"
    >
      <h1 class="text-4xl font-bold mb-4 text-slate-700">Welcome to my page</h1>
      <p class="text-lg mb-6 text-slate-700">
        This website is an AI-based project allocation, you will need to have an
        account in order to use this service.
      </p>
      <p class="text-lg mb-6 text-slate-700">
        If you do not have a project idea yet you will be able to see the
        projects proposed by the tutors
      </p>
      <button
        @click="addProject()"
        class="bg-green-700 hover:bg-green-500 text-white font-bold py-2 px-4 rounded"
      >
        Add Project
      </button>
    </div>
  </div>

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
            v-model="editingUser.areaId"
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
              v-for="expertise in expertises"
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
    };
  },
  methods: {
    addProject() {
      this.showModal = true;
    },
    saveProject() {
      this.showModal = false;
    },
    cancelEdit() {
      this.showModal = false;
    },
  },
  mounted() {
    setTimeout(() => {
      this.isAnimated = true;
    }, 100); // Start the animation shortly after the component mounts
  },
};
</script>
