<script setup>
import NavBar from "./NavBar.vue";
</script>
<template>
  <NavBar></NavBar>

  <div class="container-fluid mt-5">
    <div class="row mt-5">
      <div class="chart">
        <div class="title">Rescheduled Flights</div>
      </div>
    </div>
    <div class="table-container">
      <table border="1">
        <thead>
          <tr>
            <th>Flight Number</th>
            <th>Origin</th>
            <th>Destination</th>
            <th>Date</th>
            <th>Scheduled Departure</th>
            <th>Departure</th>
            <th>Scheduled Arrival</th>
            <th>Arrival</th>
            <th>Flight Status</th>
            <th>Aircraft Type</th>
            <th>Crew ID (Cabin Crew)</th>
            <th>Distance (miles)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>SW1009</td>
            <td>SEA</td>
            <td>DEN</td>
            <td>2024-07-01</td>
            <td>2024-07-04</td>
            <td>09:15:00</td>
            <td>2024-07-07</td>
            <td>09:00</td>
            <td style="background-color: green">Rescheduled</td>
            <td>Boeing 737-700</td>
            <td>FA209, FA309</td>
            <td>1022</td>
          </tr>
          <tr>
            <td>SW1010</td>
            <td>GEG</td>
            <td>MDW</td>
            <td>2024-09-01</td>
            <td>2024-09-02</td>
            <td>09:15:00</td>
            <td>2024-09-05</td>
            <td>09:00</td>
            <td style="background-color: green">Rescheduled</td>
            <td>Boeing 737 MAX 8</td>
            <td>FA210, FA310</td>
            <td>1507</td>
          </tr>
          <tr>
            <td>SW1011</td>
            <td>ATL</td>
            <td>SFO</td>
            <td>2024-05-25</td>
            <td>2024-05-27</td>
            <td>09:15:00</td>
            <td>2024-05-30</td>
            <td>09:00</td>
            <td style="background-color: green">Rescheduled</td>
            <td>Boeing 737 MAX 7</td>
            <td>FA211, FA311</td>
            <td>2134</td>
          </tr>
          <tr>
            <td>SW1012</td>
            <td>AUS</td>
            <td>GEG</td>
            <td>2024-02-17</td>
            <td>2024-02-19</td>
            <td>09:15:00</td>
            <td>2024-02-22</td>
            <td>09:00</td>
            <td style="background-color: green">Rescheduled</td>
            <td>Boeing 737-800</td>
            <td>FA212, FA312</td>
            <td>1600</td>
          </tr>
          <tr>
            <td>SW1013</td>
            <td>JFK</td>
            <td>TPA</td>
            <td>2024-11-26</td>
            <td>2024-11-28</td>
            <td>09:15:00</td>
            <td>2024-11-30</td>
            <td>09:00</td>
            <td style="background-color: green">Rescheduled</td>
            <td>Boeing 737-800</td>
            <td>FA213, FA313</td>
            <td>1006</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "UpdatedFlightReassignment",
  data() {
    return {};
  },

  methods: {},
};
</script>

<style scoped>
.title {
  text-align: center;
  font-size: 30px;
  margin-bottom: 20px;
  font-weight: bold; /* Make title font bolder */
}

.container-fluid {
  max-width: 90%; /* Restrict maximum width to avoid overly wide table */
  margin: auto; 
  padding: 20px;

  border-radius: 10px; /* Rounded corners */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Soft shadow around the container */
}

table {
  width: 100%;
  background: white;
  border-collapse: collapse; /* Remove gaps between table cells */
  margin-top: 20px; /* Space between title and table */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for the table */
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
  border-radius: 5px; /* Rounded corners for buttons */
  font-size: 18px; /* Larger font-size for better readability */
  transition: background-color 0.3s ease; /* Smooth transition for mouse hover */
}

button:hover {
  background-color: #0056b3; /* Darker shade for hover effect */
}

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px; /* Rounded corners for popup */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); /* More pronounced shadow for popup */
}

.popup-content {
  text-align: center;
}

.popup button {
  margin-top: 10px;
}

/* Add additional styles here for other elements as needed */
</style>
