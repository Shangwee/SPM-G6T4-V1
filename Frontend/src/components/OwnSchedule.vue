<script setup>
import { ref } from 'vue';
import NavBar from "./NavBar.vue";
import axios from 'axios'; // Import Axios

// Track selected date and form visibility
const selectedDay = ref(null);
const currentDate = ref(new Date());
const hoveredDay = ref(null); // To track the hovered date
const showForm = ref(false); // To track the visibility of the form
const dayToConfirm = ref(null); // Track the day being confirmed for work-from-home
const reason = ref(''); // Track the reason for working from home

const daysInMonth = ref([]);
const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

const getDaysInMonth = (year, month) => {
  const days = [];
  const firstDay = new Date(year, month, 1).getDay();
  const lastDate = new Date(year, month + 1, 0).getDate();

  // Fill in the empty days before the first day of the month
  for (let i = 0; i < firstDay; i++) {
    days.push('');
  }

  // Fill in the days of the month
  for (let day = 1; day <= lastDate; day++) {
    days.push(day);
  }

  return days;
};

// Update the calendar when the component is mounted
daysInMonth.value = getDaysInMonth(currentDate.value.getFullYear(), currentDate.value.getMonth());

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1);
  daysInMonth.value = getDaysInMonth(currentDate.value.getFullYear(), currentDate.value.getMonth());
  selectedDay.value = null; // Deselect the day when the month changes
};

const previousMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1);
  daysInMonth.value = getDaysInMonth(currentDate.value.getFullYear(), currentDate.value.getMonth());
  selectedDay.value = null; // Deselect the day when the month changes
};

const isToday = (day) => {
  const today = new Date();
  return (
    day === today.getDate() &&
    currentDate.value.getMonth() === today.getMonth() &&
    currentDate.value.getFullYear() === today.getFullYear()
  );
};

// Function to show the form when the plus button is clicked
const applyForWorkFromHome = (day) => {
  dayToConfirm.value = day; // Set the day to confirm
  showForm.value = true; // Show the WFH form
  reason.value = ''; // Clear the reason input
};

// Function to send the POST request
const confirmApplyWorkFromHome = async () => {
  const staffId = sessionStorage.getItem('staffID'); // Retrieve the staff ID

  if (!staffId) {
    alert('Error: Staff ID is missing');
    return;
  }

  if (reason.value.trim() !== '') {
    try {
      const response = await axios.post('http://localhost:6001/flexibleArrangement/createRequest', {
        staff_id: staffId,
        date: dayToConfirm.value,
        comments: reason.value, // Send reason for WFH
      });

      if (response.status === 200) {
        alert('Work-from-home application successful!');
        showForm.value = false; // Hide the form after confirmation
      } else {
        alert('Something went wrong, please try again.');
      }
    } catch (error) {
      console.error(error);
      alert('Error: Unable to apply for work from home.');
    }
  } else {
    alert('Please enter a reason for working from home.');
  }
};

const cancelWorkFromHome = () => {
  showForm.value = false; // Hide the form
};

</script>


<template>
  <div>
    <NavBar></NavBar>
    <div class="container-fluid">
      <div class="row text-center justify-content-center">
        <div class="col-12 header-container">
          <h3 class="mb-3">My Schedule</h3>
        </div>
        <!-- Flexbox Container for Side-by-Side Layout -->
        <div class="col-12 d-flex calendar-form-container">
          <div class="calendar-container">
            <div class="calendar card shadow-sm">
              <!-- Calendar Header -->
              <div class="calendar-header d-flex justify-content-between align-items-center p-3">
                <button class="btn btn-outline-primary" @click="previousMonth">
                  <i class="bi bi-arrow-left-circle"></i> Previous
                </button>
                <h4 class="m-0">{{ currentDate.toLocaleString('default', { month: 'long' }) }} {{ currentDate.getFullYear() }}</h4>
                <button class="btn btn-outline-primary" @click="nextMonth">
                  Next <i class="bi bi-arrow-right-circle"></i>
                </button>
              </div>

              <!-- Calendar Grid -->
              <div class="calendar-grid p-2">
                <div class="calendar-day fw-bold text-center" v-for="day in daysOfWeek" :key="day">{{ day }}</div>
                <div
                  v-for="(day, index) in daysInMonth"
                  :key="index"
                  class="calendar-cell text-center"
                  @mouseover="hoveredDay = day"
                  @mouseleave="hoveredDay = null"
                  :class="{
                    'empty-day': day === '',
                    'selected-day': day === selectedDay,
                    today: isToday(day),
                  }"
                >
                  <span v-if="day">{{ day }}</span>

                  <!-- "+" Button appears on hover -->
                  <button v-if="hoveredDay === day && day !== ''" class="apply-btn" @click.stop="applyForWorkFromHome(day)">+</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Inline WFH Form (Side by Side with Calendar) -->
          <div v-if="showForm" class="wfh-form">
            <h5>Apply for Work From Home</h5>
            <p>Date: {{ dayToConfirm }} {{ currentDate.toLocaleString('default', { month: 'long' }) }}</p>
            <div class="form-group">
              <label for="reason">Reason for WFH:</label>
              <input type="text" v-model="reason" id="reason" class="form-control" placeholder="Enter your reason" />
            </div>
            <div class="form-actions">
              <button class="btn btn-primary" @click="confirmApplyWorkFromHome">Confirm</button>
              <button class="btn btn-secondary" @click="cancelWorkFromHome">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header-container {
  margin-top: 20px;
  padding-bottom: 10px;
}

.calendar-form-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-top: 20px;
}

.calendar-container {
  flex: 3; /* Adjust the flex ratio of the calendar */
  max-width: 1000px;
  margin: 0 auto;
}
.wfh-form {
  flex: 1; /* This controls the form's proportion relative to the calendar */
  padding: 10px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  width: 100px; /* Adjust this value to change the form's width. You can try values like 70%, 50%, or set a fixed width (e.g., 300px) */
  margin-left: 20px; /* This adds space between the calendar and the form */
}

.calendar {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 10px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr); /* 7 columns for the 7 days of the week */
  gap: 1px;
  width: 100%;
}

.calendar-cell {
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #e0e0e0;
  cursor: pointer;
  transition: background-color 0.3s ease;
  background-color: white;
  position: relative;
}

.calendar-cell.selected-day {
  background-color: #e2e3e5;
  color: #495057;
  font-weight: bold;
  border-radius: 8px;
  border: 2px solid #495057;
}

.calendar-cell.today {
  background-color: #d1e7ff;
  color: #0d6efd;
  font-weight: bold;
  border-radius: 8px;
  border: 1px solid #0d6efd;
}

.calendar-cell:hover {
  background-color: #f8f9fa;
  transition: background-color 0.3s ease;
}

.apply-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: #0d6efd;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 10px;
  cursor: pointer;
}

.apply-btn:hover {
  background-color: #0d6efd;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ced4da;
}

.form-actions {
  display: flex;
  justify-content: space-around;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
}

.btn-primary {
  background-color: #0d6efd;
  color: white;
  border: none;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
}
</style>