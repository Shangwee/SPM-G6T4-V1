<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import NavBar from './NavBar.vue';

const inOfficeCount = ref(null); 
const wfhCount = ref(null); 
const totalDeptCount = ref(null); 
const userDept = ref(''); 
const filteredStaffWorkingFromHome = ref([]); 
const today = ref(new Date()); 
const approvedWFHDates = ref([]); 
const pendingRequestCount = ref(0); 
const isLoadingWFH = ref(true); 
const isLoadingPendingRequests = ref(true); 
const isManagerOrHR = ref(false); 

const staffId = sessionStorage.getItem('staffID');

const formatDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const formatDateDisplay = (date) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString(undefined, options);
};

const todayFormattedDisplay = ref(formatDateDisplay(today.value));

const fetchUserDetails = async () => {
  try {
    const response = await axios.get(`http://localhost:5001/user/${staffId}`);
    if (response.data) {
      const { Dept, Role } = response.data;
      userDept.value = Dept;

      if (Role === 1 || Role === 3) {
        isManagerOrHR.value = true;
        fetchPendingRequests(); 
      }
      await fetchWFHCountForDepartment();
    }
  } catch (error) {
    console.error('Error fetching user details:', error);
  }
};

// Fetch the total department count for the logged-in user's department
const fetchTotalDeptCount = async () => {
  try {
    const response = await axios.get(`http://localhost:5001/users`, {
      params: { dept: userDept.value },
    });
    totalDeptCount.value = response.data.length || 0;
  } catch (error) {
    console.error('Error fetching total department count:', error);
    totalDeptCount.value = 0;
  }
};

// Fetch WFH schedules for the current day in the user's department
const fetchWFHCountForDepartment = async () => {
  try {
    const response = await axios.get(`http://localhost:6003/aggregateSchedule`, {
      params: {
        type: 'Dept',
        dept: userDept.value,
        start_date: formatDate(today.value),
        end_date: formatDate(today.value),
      },
    });

    const schedules = response.data || [];

    // Log the full structure of each schedule for debugging
    console.log('Detailed Schedules:', schedules);

    // Assuming 'Location' field indicates WFH or In Office
    // Update the filter based on the actual field name
    wfhCount.value = schedules.filter((schedule) => schedule.Location === 'WFH').length;

    // Correct the in-office count
    wfhCount.value = schedules.length - wfhCount.value;
    inOfficeCount.value = totalDeptCount.value - wfhCount.value;

    // Log counts to verify correctness
    console.log(`WFH Count: ${wfhCount.value}`);
    console.log(`In Office Count: ${inOfficeCount.value}`);
    
  } catch (error) {
    console.error('Error fetching WFH requests:', error);
    wfhCount.value = 0; // Default to 0 if an error occurs
    inOfficeCount.value = totalDeptCount.value || 0; // Assume all are in office if there's an error
  }
};

const fetchApprovedWFHDates = async () => {
  try {
    const response = await axios.get(`http://localhost:6001/flexibleArrangement/ownRequests/${staffId}`);
    const todayDate = new Date();
    todayDate.setHours(0, 0, 0, 0);

    approvedWFHDates.value = response.data
      .filter((schedule) => {
        const scheduleDate = new Date(schedule.Date);
        scheduleDate.setHours(0, 0, 0, 0);
        return schedule.Status === 1 && scheduleDate >= todayDate;
      })
      .map((schedule) => formatDateDisplay(new Date(schedule.Date)));
  } catch (error) {
    approvedWFHDates.value = [];
  } finally {
    isLoadingWFH.value = false;
  }
};

const fetchPendingRequests = async () => {
  try {
    const response = await axios.get(`http://localhost:6001/flexibleArrangement/approvalRequests/${staffId}`);
    pendingRequestCount.value = response.data.filter(request => request.Status === 0).length;
  } catch (error) {
    pendingRequestCount.value = 0;
  } finally {
    isLoadingPendingRequests.value = false;
  }
};

onMounted(async () => {
  await fetchUserDetails();
  await fetchTotalDeptCount(); // Fetch department count first
  await fetchWFHCountForDepartment(); // Then fetch WFH count and in-office count based on total
  await fetchApprovedWFHDates();
});
</script>

<template>
  <NavBar></NavBar>
  <div class="container dashboard-container">
    <h2 class="text-center">Today's Office Status</h2>
    <h5 class="text-center">{{ todayFormattedDisplay }}</h5>
    <h4 class="text-center mb-4 department-title">Department: {{ userDept }}</h4>
    
    <!-- Show loading state for office counts -->
    <div v-if="inOfficeCount === null || wfhCount === null" class="loading-placeholder">
      Loading data...
    </div>

    <div v-else class="status-cards">
      <div class="status-card">
        <h3>In Office</h3>
        <p class="count">{{ inOfficeCount }}</p>
      </div>
      <div class="status-card">
        <h3>WFH</h3>
        <p class="count">{{ wfhCount }}</p>
      </div>
    </div>

    <div class="wfh-container">
      <h3>Approved Work From Home Dates</h3>
      <div v-if="isLoadingWFH" class="loading-placeholder">Loading WFH dates...</div>
      <div v-else class="wfh-dates">
        <div v-for="(date, index) in approvedWFHDates" :key="index" class="wfh-date-card">{{ date }}</div>
        <div v-if="approvedWFHDates.length === 0" class="no-wfh-dates">No approved WFH dates found.</div>
      </div>
    </div>

    <div v-if="isManagerOrHR" class="pending-requests-container">
      <h3>Pending Work From Home Requests</h3>

      <!-- Loading state for pending requests -->
      <div v-if="isLoadingPendingRequests" class="loading-placeholder">
        Loading pending requests...
      </div>

      <!-- Show pending requests once loaded -->
      <div v-else>
        <div v-if="pendingRequestCount > 0" class="pending-requests">
          <p>There are {{ pendingRequestCount }} pending WFH requests waiting for your approval.</p>
        </div>
        <div v-else class="no-pending-requests">No pending WFH requests.</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

.container {
  font-family: 'Poppins', sans-serif;
}

.dashboard-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 30px;
  max-width: 600px;
  margin: 40px auto;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  margin-top: 100px;
  transition: all 0.3s ease-in-out;
}

.dashboard-container:hover {
  box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.2);
}

h2 {
  font-size: 1.8rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
}

h5 {
  font-size: 1.1rem;
  color: #666;
}

.department-title {
  font-size: 1.5rem;
  font-weight: 500;
  color: #3f51b5;
}

.status-cards {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.status-card {
  background-color: #fff;
  border-radius: 15px;
  padding: 30px;
  width: 100%;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.status-card:hover {
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

.status-card h3 {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 10px;
  font-weight: 500;
}

.status-card .count {
  font-size: 2.7rem;
  color: #3f51b5;
  font-weight: 600;
}

.wfh-container {
  margin-top: 30px;
}

.wfh-dates {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.wfh-date-card {
  background-color: #f9f9f9;
  padding: 15px;
  margin: 10px 0;
  width: 100%;
  max-width: 400px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s ease;
}

.wfh-date-card:hover {
  background-color: #e7f3ff;
}

.no-wfh-dates {
  font-size: 1rem;
  color: #999;
}

.pending-requests-container {
  margin-top: 40px;
}

.pending-requests {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.no-pending-requests {
  font-size: 1rem;
  color: #999;
}

.loading-placeholder {
  font-size: 1.2rem;
  color: #999;
  padding: 20px;
}

@media (min-width: 768px) {
  .status-card {
    padding: 30px 40px;
  }

  .status-card .count {
    font-size: 2.9rem;
  }
}
</style>
