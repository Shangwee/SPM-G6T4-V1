<template>
  <NavBar></NavBar>
  <div>
    
    <div class="container mt-5 pt-5" style="padding-top: 100px;">
      <h3 class="text-center mb-4">Requests</h3>

      <!-- Filters for request status -->
      <div class="d-flex justify-content-center mb-4">
        <button @click="filterRequests('All')" class="btn btn-outline-primary mx-2">All</button>
        <button @click="filterRequests('Pending')" class="btn btn-outline-warning mx-2">Pending</button>
        <button @click="filterRequests('Approved')" class="btn btn-outline-success mx-2">Approved</button>
        <button @click="filterRequests('Rejected')" class="btn btn-outline-danger mx-2">Rejected</button>
      </div>

      <!-- Request List -->
      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead class="thead-dark">
            <tr>
              <th>Request ID</th>
              <th>Staff ID</th>
              <th>Request Date</th>
              <th>Status</th>
              <th class="text-center">Actions</th>
              <th v-if="hasUpdates" class="text-center">Previous Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in filteredRequests" :key="request.request_id">
              <td>{{ request.request_id }}</td>
              <td>{{ request.staff_id }}</td>
              <td>{{ request.date }}</td>
              <td>
                <span :class="statusBadgeClass(request.status)">{{ request.status }}</span>
              </td>
              <td class="text-center">
                <button v-if="request.status === 'Pending'" @click="updateStatus(request, 'Approved')" class="btn btn-success btn-sm mx-1">Approve</button>
                <button v-if="request.status === 'Pending'" @click="updateStatus(request, 'Rejected')" class="btn btn-danger btn-sm mx-1">Reject</button>
              </td>
              <td v-if="request.previous_date" class="text-center">{{ request.previous_date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import NavBar from './NavBar.vue';

// Dummy request data
const requests = ref([
  { request_id: 1, staff_id: 101, date: '2024-10-01', status: 'Pending', previous_date: null },
  { request_id: 2, staff_id: 102, date: '2024-10-03', status: 'Pending', previous_date: '2024-09-28' },
  { request_id: 3, staff_id: 103, date: '2024-10-04', status: 'Approved', previous_date: null },
  { request_id: 4, staff_id: 104, date: '2024-10-02', status: 'Rejected', previous_date: null },
]);

const filteredRequests = ref([...requests.value]);

const filterRequests = (status) => {
  if (status === 'All') {
    filteredRequests.value = requests.value;
  } else {
    filteredRequests.value = requests.value.filter(request => request.status === status);
  }
};

// Dynamically set the status badge classes
const statusBadgeClass = (status) => {
  if (status === 'Pending') return 'badge bg-warning text-dark';
  if (status === 'Approved') return 'badge bg-success';
  if (status === 'Rejected') return 'badge bg-danger';
};

const updateStatus = (request, newStatus) => {
  request.status = newStatus;
};
</script>

<style>
/* Additional styling to enhance appearance */
.container {
  margin-top: 80px;
}

.thead-dark {
  background-color: #343a40;
  color: white;
}

.table-hover tbody tr:hover {
  background-color: rgba(0, 123, 255, 0.1);
}

.badge {
  font-size: 0.9em;
  padding: 0.5em;
}

.btn {
  min-width: 100px;
}
</style>
