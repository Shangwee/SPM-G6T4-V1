<script setup>
import NavBar from "./NavBar.vue";
import Calander from "./Calander.vue";
</script>
<template>
  <div>
    <NavBar></NavBar>
    <br>
    <div class="container-fluid">
      <div class="row text-center justify-content-center">
        <div class="col-12">
          <h3 class="mb-3">My Schedule</h3> <!-- Remove bottom margin to bring closer to the button -->
        </div>
        <div class="col-12 col-md-8 calendar-wrapper">
          <Calander></Calander>
        </div>
      </div>
      <br>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showOriginalImage: true,
    };
  },

  methods: {
    
  },
  components: {
    Calander
  },  
};
</script>

<style scoped>
.title {
  text-align: center;
  font-size: 30px;
  margin-bottom: 20px;
  color: #333; /* Darker font color for better readability */
  font-weight: bold; /* Make title font bolder */
}
.chart img {
  max-width: 100%; /*Ensure the image does not exceed its container  */
  height: auto; /* Maintain aspect ratio */
  display: block; /* Remove any default inline styling */
  margin: 0 auto; /*  Center the image within its container  */
}

table {

  background: white;
  border-collapse: collapse; /* Remove gaps between table cells */
  margin-top: 20px; /* Space between title and table */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for the table */
  overflow-y: auto;

}
.table-responsive {
  overflow-y: auto; /* Enables vertical scrolling if content is taller than the container */
  max-height: 400px; /* Or whatever height you prefer */
}

th,
td {
  border: 1px solid #ddd; /* Lighter border color */
  padding: 12px 15px; /* More padding for table cells */
  text-align: left; /* Align text to the left */
  font-size: 18px; /* Slightly larger font-size for better readability */
}

th {
  background-color: #007bff; /* Use a solid color for header background */
  color: white; /* White text color for the header */
  text-transform: uppercase; /* Make header texts uppercase */
}

tr:nth-child(even) {
  background-color: #f2f2f2; /* Zebra striping for rows */
}

button {
  background-color: #007bff; /* Bootstrap primary color */
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 18px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.popup-content {
  text-align: center;
}

.popup button {
  margin-top: 10px;
}

.calendar-wrapper {
  max-width: 100%; /* Adjust the width here */
  margin: 0 auto;   /* Center the calendar */
  padding: 20px;    /* Add some padding around the calendar */
}

.container-fluid {
  margin-top: 100px;
}
.table-container {
  max-height: 600px; /* Set the maximum height of the container */
  max-width: 1700px;
  overflow-y: auto; /* Enable vertical scrolling */
}
</style>
