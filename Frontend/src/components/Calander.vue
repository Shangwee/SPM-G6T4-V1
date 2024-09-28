<template>
  <div>
    <!-- Conditionally render the correct calendar view based on the user's role -->
    <div v-if="role === 1">
      <!-- Calendar view for Director -->
      <DirectorCalendarView />
    </div>

    <div v-else-if="role === 2">
      <!-- Calendar view for Staff -->
      <StaffCalendarView />
    </div>

    <div v-else-if="role === 3">
      <!-- Calendar view for Manager -->
      <ManagerCalendarView />
    </div>
  </div>
</template>

<script>
// Import the individual calendar view components for Director, Staff, and Manager
// Correctly import the components at the top of your file
import DirectorCalendarView from './DirectorCalendarView.vue'; // Adjust the path as needed
import StaffCalendarView from './StaffCalendarView.vue';
import ManagerCalendarView from './ManagerCalendarView.vue';


export default {
  components: {
    DirectorCalendarView,
    StaffCalendarView,
    ManagerCalendarView,
  },
  data() {
    return {
      role: null, // This will store the user's role (1 for Director, 2 for Staff, 3 for Manager)
    };
  },
  created() {
    this.getRoleFromSession(); // Fetch the user's role when the component is created
  },
  methods: {
    getRoleFromSession() {
      // Assuming the role is stored in sessionStorage after login
      const storedRole = sessionStorage.getItem('role'); // Example of how to get the role
      if (storedRole) {
        this.role = parseInt(storedRole); // Convert the string to an integer
      }
    },
  },
};
</script>

<style scoped>
/* Add any specific styles for the calendar view container here */
</style>