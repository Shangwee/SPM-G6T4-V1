<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import NavBar from './NavBar.vue';

// Define reactive variables to store the counts
const inOfficeCount = ref(null); // Set to null initially to show loading state
const wfhCount = ref(null); // Set to null initially to show loading state
const selectedDay = ref(new Date());

// Function to format the date as 'YYYY-MM-DD'
const formatDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// Get today's date
const today = formatDate(selectedDay.value);

// Function to count the number of people working from home and in the office
const countOfficeStatus = (schedules) => {
  console.log('Fetched Schedules:', schedules);

  if (!schedules || schedules.length === 0) {
    console.log('No schedules returned.');
    inOfficeCount.value = 0;
    wfhCount.value = 0;
    return;
  }

  // Count people in the office and WFH based on the data
  inOfficeCount.value = schedules.filter(schedule => !schedule.WorkFromHome).length;
  wfhCount.value = schedules.filter(schedule => schedule.WorkFromHome).length;

  console.log('In Office Count:', inOfficeCount.value);
  console.log('WFH Count:', wfhCount.value);
};

// Fetch the number of people in the office and working from home for the selected date
const fetchOfficeStatus = async () => {
  try {
    // Adjust the endpoint and parameters as needed for your backend
    const response = await axios.get(`http://localhost:5002/schedule/organisation`, {
      params: {
        start_date: formatDate(selectedDay.value),
        end_date: formatDate(selectedDay.value),
      }
    });
    console.log('API Response for Office/WFH:', response.data);

    if (response.data && response.data.length > 0) {
      countOfficeStatus(response.data); // Count WFH and office workers
    } else {
      console.log('No data found for the selected date.');
      inOfficeCount.value = 0;
      wfhCount.value = 0;
    }
  } catch (error) {
    console.error('Error fetching office status:', error);
    // Set the counts to 0 in case of an error
    inOfficeCount.value = 0;
    wfhCount.value = 0;
  }
};

// Watch for changes in selectedDay and refetch the data
watch(selectedDay, fetchOfficeStatus);

// Fetch data when the component is mounted
onMounted(fetchOfficeStatus);
</script>

<template>
  <NavBar></NavBar>
  <div class="container dashboard-container">
    <h2 class="text-center">Today's Office Status</h2>
    <!-- Show loading state when data is being fetched -->
    <div v-if="inOfficeCount === null || wfhCount === null">
      Loading data...
    </div>
    <!-- Show data once fetched -->
    <div v-else>
      <div class="status-card">
        <h3>In Office:</h3>
        <p class="count">{{ wfhCount }}</p> <!-- Dynamic count -->
      </div>
      <div class="status-card">
        <h3>Working from Home:</h3>
        <p class="count">{{ inOfficeCount }}</p> <!-- Dynamic count -->
      </div>
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
