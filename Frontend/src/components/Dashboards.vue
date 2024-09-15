<script setup>
import NavBar from "./NavBar.vue";
import Weather from "./Weather.vue";
import Flight from "./Flight.vue";
</script>

<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <NavBar></NavBar>
    <div class="container">
      <!-- Tabs -->
      <ul class="nav nav-tabs nav-fill">
        <li class="nav-item">
          <a class="nav-link active" data-bs-toggle="tab" href="#weatherTab"
            >Weather Analysis</a
          >
        </li>
        <li class="nav-item">
          <a class="nav-link" data-bs-toggle="tab" href="#flightTab"
            >Flight Operations Analysis</a
          >
        </li>
      </ul>

      <div class="tab-content">
        <div class="tab-pane fade show active" id="weatherTab">
          <Weather></Weather>
        </div>
        <div class="tab-pane fade" id="flightTab">
          <Flight></Flight>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px; /* Adjust the maximum width as needed */
  max-height: 700px;
  overflow-y: auto;
  margin-top: 100px;
  
}

.nav-link {
  padding: 0.5rem 1rem; /* Adjust padding to make tabs more compact */
}

.tab-content {
  margin-top: 1rem; /* Add margin between tabs and content */
  
  
}

</style>
