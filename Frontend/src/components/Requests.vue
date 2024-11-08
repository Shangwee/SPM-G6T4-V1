<template>
  <div>
    <div class="container mt-3 pt-5">
      <div class="d-flex justify-content-center mb-4">
        <button
          @click="filterRequests('All')"
          class="btn btn-outline-primary mx-2"
        >
          All
        </button>
        <button
          @click="filterRequests('Pending')"
          class="btn btn-outline-warning mx-2"
        >
          Pending
        </button>
        <button
          @click="filterRequests('Approved')"
          class="btn btn-outline-success mx-2"
        >
          Approved
        </button>
        <button
          @click="filterRequests('Rejected')"
          class="btn btn-outline-danger mx-2"
        >
          Rejected
        </button>
      </div>

      <!-- Limit the height of the table and enable scrolling -->
      <div class="table-responsive" style="max-height: 400px; overflow-y: auto">
        <table class="table table-striped table-hover">
          <thead class="thead-dark">
            <tr>
              <th>Request ID</th>
              <th>Employee ID</th>
              <th>Employee Name</th>
              <th>Request Date</th>
              <th>Reason</th>
              <th>Status</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in filteredRequests" :key="request.Request_ID">
              <td>{{ request.Request_ID }}</td>
              <td>{{ request.Employee_ID }}</td>
              <td>{{ request.Staff_FName }} {{ request.Staff_LName }}</td>
              <td>{{ request.Date }}</td>
              <td>{{ request.Reason }}</td>
              <td>
                <span :class="statusBadgeClass(request.Status)">{{
                  getStatusText(request.Status)
                }}</span>
              </td>
              <td class="text-center">
                <button
                  v-if="request.Status === 0"
                  @click="updateStatus(request.Request_ID, 1)"
                  class="btn btn-success btn-sm mx-1"
                >
                  Approve
                </button>
                <button
                  v-if="request.Status === 0"
                  @click="updateStatus(request.Request_ID, 2)"
                  class="btn btn-danger btn-sm mx-1"
                >
                  Reject
                </button>
                <button
                  v-if="canWithdraw(request.Date) && request.Status === 1"
                  @click="withdrawRequest(request.Request_ID)"
                  class="btn btn-warning btn-sm mx-1"
                >
                  Withdraw
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const ACCOUNT_API = import.meta.env.VITE_ACCOUNT_API;
const SCHEDULE_API = import.meta.env.VITE_SCHEDULE_API;
const REQUEST_API = import.meta.env.VITE_REQUEST_API;
const MEETING_API = import.meta.env.VITE_MEETING_API;
const NOTIFICATION_API = import.meta.env.VITE_NOTIFICATION_API;
const FLEXIBLE_ARRANGEMENT_API = import.meta.env.VITE_FLEXIBLE_ARRANGEMENT_API;
const MANAGE_REQUEST_API = import.meta.env.VITE_MANAGE_REQUEST_API;
const SCHEDULE_AGGREGATION_API = import.meta.env.VITE_SCHEDULE_AGGREGATION_API;

const requests = ref([]);
const filteredRequests = ref([]);

// Get Staff ID from session storage
const staffId = sessionStorage.getItem("staffID");

// Fetch requests for the approver using the Flask API
const fetchRequests = async () => {
  try {
    const response = await axios.get(
      `${FLEXIBLE_ARRANGEMENT_API}/flexibleArrangement/approvalRequests/${staffId}`
    );
    requests.value = response.data;
    filterRequests("All"); // Set initial filter to show all requests
  } catch (error) {
    console.error("Error fetching requests:", error);
  }
};

onMounted(() => {
  fetchRequests();
});

// Convert numeric status to text label
const getStatusText = (status) => {
  if (status === 0) return "Pending";
  if (status === 1) return "Approved";
  if (status === 2) return "Rejected";
  return "Unknown"; // Fallback for unexpected values
};

// Filter requests based on status
const filterRequests = (status) => {
  if (status === "All") {
    filteredRequests.value = requests.value;
  } else {
    filteredRequests.value = requests.value.filter(
      (request) => getStatusText(request.Status) === status
    );
  }
};

// Assign badge class based on status
const statusBadgeClass = (status) => {
  if (status === 0) return "badge bg-warning text-dark"; // Pending
  if (status === 1) return "badge bg-success"; // Approved
  if (status === 2) return "badge bg-danger"; // Rejected
  return "badge bg-secondary"; // Unknown status
};

// Update status of a request using the Flask API
const updateStatus = async (requestId, newStatus) => {
  try {
    const url =
      newStatus === 1
        ? `${MANAGE_REQUEST_API}/manageRequest/accept` // Accept the request
        : `${MANAGE_REQUEST_API}/manageRequest/reject`; // Reject the request

    const response = await axios.post(url, {
      staff_id: parseInt(staffId),
      request_id: requestId,
    });

    if (response.status === 200) {
      await fetchRequests(); // Refresh the requests after updating
    } else {
      console.error("Error updating status:", response.data.error);
    }
  } catch (error) {
    console.error("Error updating status:", error);
  }
};

const withdrawRequest = async (requestId) => {
  try {
    const staffId = sessionStorage.getItem("staffID");

    const response = await axios.post(
      `${MANAGE_REQUEST_API}/manageRequest/withdraw`,
      {
        staff_id: parseInt(staffId),
        request_id: requestId,
      }
    );

    if (response.status === 200) {
      await fetchRequests(); // Refresh the request list
      console.log("Request withdrawn successfully");
    } else {
      alert(response.data.error);
      console.error("Error withdrawing request:", response.data.error);
    }
  } catch (error) {
    console.error("Error withdrawing request:", error);
  }
};

const canWithdraw = (requestDate) => {
  const requestDateObject = new Date(requestDate);
  const now = new Date();
  const diffInMilliseconds = requestDateObject - now;
  const diffInHours = diffInMilliseconds / (1000 * 60 * 60);
  return diffInHours >= 24;
};
</script>

<style>
/* Adjust margin-top for the container to avoid affecting navbar */
.container {
  margin-top: 0px; /* Adjust this value as needed */
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

/* Add max-height and make the table scrollable */
.table-responsive {
  max-height: 400px; /* You can adjust this height as needed */
  overflow-y: auto;
}
</style>
