<script setup>
import NavBar from "./NavBar.vue";
// Import your icons or metrics component here if necessary
</script>

<template>
  <NavBar></NavBar>
  <div id="app" class="container dashboard-container shadow-lg">
    <div class="dashboard">
      <h2>Today's Office Status</h2>
      <div class="status-card">
        <h3>In Office:</h3>
        <p class="count" id="inOfficeCount">12</p> <!-- Example count; replace with dynamic data -->
      </div>
      <div class="status-card">
        <h3>Working from Home:</h3>
        <p class="count" id="wfhCount">8</p> <!-- Example count; replace with dynamic data -->
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

.container {
  margin-top: 100px;
  padding: 2rem;
  font-family: 'Poppins', sans-serif;
}

.dashboard-container {
  background: rgba(255, 255, 255, 0.9); /* Lightly transparent background */
  border-radius: 15px;
  padding: 30px;
  max-width: 800px;
  margin: 100px auto;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.1);
}

.dashboard {
  text-align: center;
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
  color: #3f51b5; /* Muted blue color for emphasis */
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
