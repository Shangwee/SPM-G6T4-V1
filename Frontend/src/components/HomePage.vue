<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import NavBar from './NavBar.vue';

// Define reactive variables to store the counts
const inOfficeCount = ref(null); // Set to null initially to show loading state
const wfhCount = ref(null); // Set to null initially to show loading state
const totalDeptCount = ref(null); // Total number of employees in the department
const userDept = ref(''); // Store user department
const filteredStaffWorkingFromHome = ref([]); // Staff working from home
const today = ref(new Date()); // Hold today's date
const approvedWFHDates = ref([]); // Store the dates the user has applied for WFH with their status
const isLoadingWFH = ref(true); // Loading state for WFH dates

// Get staff ID from session storage (assuming staffID is stored in session)
const staffId = sessionStorage.getItem('staffID');

// Function to format the date as 'YYYY-MM-DD'
const formatDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// Function to display today's date in a readable format (e.g., "October 25, 2024")
const formatDateDisplay = (date) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString(undefined, options);
};

// Get today's date in formatted string for display
const todayFormattedDisplay = ref(formatDateDisplay(today.value));

// Fetch the user's department
const fetchUserDepartment = async () => {
  try {
    const response = await axios.get(`http://localhost:5001/user/${staffId}`);
    if (response.data && response.data.Dept) {
      userDept.value = response.data.Dept;
      console.log('User department:', userDept.value);
      await fetchWFHCountForDepartment(); // Fetch the WFH count after getting the department
    } else {
      console.log('Department not found for the user.');
    }
  } catch (error) {
    console.error('Error fetching user department:', error);
  }
};

// Fetch the total number of employees in the user's department
const fetchTotalDeptCount = async () => {
  try {
    const response = await axios.get(`http://localhost:5001/users`, {
      params: { dept: userDept.value }
    });
    totalDeptCount.value = response.data.length;
    console.log('Total department count:', totalDeptCount.value);
  } catch (error) {
    console.error('Error fetching total department count:', error);
    totalDeptCount.value = 0;
  }
};

// Fetch the approved WFH requests for the selected day in the department
const fetchWFHCountForDepartment = async () => {
  try {
    // Fetch total department count
    await fetchTotalDeptCount();

    // Fetch WFH requests for the user's department on the selected day
    const response = await axios.get(`http://localhost:6003/aggregateSchedule`, {
      params: {
        type: 'Dept',
        dept: userDept.value,
        start_date: formatDate(today.value),
        end_date: formatDate(today.value)
      }
    });
    console.log('WFH Requests API Response:', response.data); // Debugging the response

    // Filter the staff working from home
    filteredStaffWorkingFromHome.value = response.data.filter(
      (schedule) => schedule.Location === 'WFH'
    );

    // Set WFH count
    wfhCount.value = filteredStaffWorkingFromHome.value.length;

    // Calculate in-office count
    inOfficeCount.value = (totalDeptCount.value || 0) - wfhCount.value;

    console.log('WFH Count:', wfhCount.value);
    console.log('In Office Count:', inOfficeCount.value);
  } catch (error) {
    console.error('Error fetching WFH requests:', error);
    wfhCount.value = 0;
    inOfficeCount.value = totalDeptCount.value || 0; // If there's an error, assume all are in the office
  }
};

// Fetch the approved WFH dates for the logged-in user
const fetchApprovedWFHDates = async () => {
  try {
    const response = await axios.get(`http://localhost:6001/flexibleArrangement/ownRequests/${staffId}`);
    console.log('Approved WFH Dates API Response:', response.data); // Debugging the response

    // Get today's date for comparison
    const todayDate = new Date();
    todayDate.setHours(0, 0, 0, 0); // Reset hours to midnight to compare only the date part

    // Ensure the response contains dates and filter out past dates
    approvedWFHDates.value = response.data
      .filter((schedule) => {
        const scheduleDate = new Date(schedule.Date);
        scheduleDate.setHours(0, 0, 0, 0); // Reset hours to midnight
        return schedule.Status === 1 && scheduleDate >= todayDate; // Only future or today's approved WFH requests
      })
      .map((schedule) => formatDateDisplay(new Date(schedule.Date))); // Format the date for display

    console.log('Approved WFH Dates (Filtered):', approvedWFHDates.value);
  } catch (error) {
    console.error('Error fetching approved WFH dates:', error);
    approvedWFHDates.value = [];
  } finally {
    isLoadingWFH.value = false; // Set loading to false once data is fetched
  }
};

// Fetch data when the component is mounted
onMounted(async () => {
  await fetchUserDepartment(); // First fetch the user department
  await fetchApprovedWFHDates(); // Fetch WFH dates after fetching department info
});
</script>

<template>
  <NavBar></NavBar>
  <div class="container dashboard-container">
    <h2 class="text-center">Today's Office Status</h2>
    <!-- Display today's date -->
    <h5 class="text-center">{{ todayFormattedDisplay }}</h5>
    
    <!-- Display the department -->
    <h4 class="text-center mb-4">Department: {{ userDept }}</h4>
    
    <!-- Show loading state when data is being fetched -->
    <div v-if="inOfficeCount === null || wfhCount === null">
      Loading data...
    </div>
    <!-- Show data once fetched -->
    <div v-else>
      <div class="status-card">
        <h3>In Office:</h3>
        <p class="count">{{ inOfficeCount }}</p> <!-- Dynamic count -->
      </div>
      <div class="status-card">
        <h3>Working from Home:</h3>
        <p class="count">{{ wfhCount }}</p> <!-- Dynamic count -->
      </div>
    </div>

    <!-- Approved WFH Dates Section -->
    <div class="wfh-container">
      <h3>Approved Work From Home Dates</h3>
      
      <!-- Loading state for WFH dates -->
      <div v-if="isLoadingWFH">
        Loading WFH dates...
      </div>

      <!-- Show WFH dates once loaded -->
      <ul v-else>
        <li v-for="(date, index) in approvedWFHDates" :key="index">
          {{ date }}
        </li>
        <li v-if="approvedWFHDates.length === 0">No approved WFH dates found.</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

.container {
  font-family: 'Poppins', sans-serif;
}

/* Centering and ensuring the container isn't too wide */
.dashboard-container {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  padding: 30px;
  max-width: 600px; /* Restricting the width for better appearance */
  margin: 40px auto; /* Centering the container */
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.1);
  text-align: center; /* Ensure everything is centered inside */
  padding-top: 100px;
}

.dashboard h2 {
  font-size: 1.8rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
}

.status-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
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
  font-size: 2.5rem;
  color: #3f51b5;
  font-weight: 600;
}

.wfh-container {
  margin-top: 20px;
  padding: 10px;
}

ul {
  list-style-type: none;
  padding: 0;
}

ul li {
  background-color: #f9f9f9;
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

ul li:nth-child(odd) {
  background-color: #f1f1f1;
}

ul li:nth-child(even) {
  background-color: #e7e7e7;
}

@media (min-width: 768px) {
  .status-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 30px;
  }

  .status-card h3 {
    font-size: 1.2rem;
  }

  .status-card .count {
    font-size: 2.7rem;
  }
}
</style>
