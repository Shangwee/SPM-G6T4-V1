<script setup>

import Footer from './components/Footer.vue'
import NavBar from './components/NavBar.vue';
</script>

<template>
  <router-view></router-view>

  <img src="./assets/background.jpg" class="bottom-image">
  <Footer></Footer>

</template>

<style scoped>
.bottom-image {
  position: fixed;
  bottom: -75px;
  left: 150px;
  width: 75%; /* Ensures the image spans the entire width */
  z-index: -1; /* Ensures the image stays behind the content */
}

</style>