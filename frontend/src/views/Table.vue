<template>
  <link
    rel="stylesheet"
    href="https://cdn.datatables.net/2.0.1/css/dataTables.dataTables.css"
  />

  <script src="https://cdn.datatables.net/2.0.1/js/dataTables.js"></script>

  <div>
    <table id="myTable" class="display">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import DataTable from "datatables.net-dt";

export default {
  name: "DataTableComponent",
  data() {
    return {
      users: [
        { id: 1, name: "John Doe", email: "john@example.com" },
        { id: 2, name: "Jane Doe", email: "jane@example.com" },
        // more users
      ],
    };
  },
  mounted() {
    this.initDataTable();
  },
  methods: {
    initDataTable() {
      new DataTable("#myTable", {
        responsive: true,
      });
    },
  },
};
</script>
