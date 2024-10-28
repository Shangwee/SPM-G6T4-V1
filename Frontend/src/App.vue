<script setup>
import Footer from './components/Footer.vue';
</script>

<template>
  <div>
    <router-view></router-view>
    <img src="./assets/background.jpg" class="bottom-image" />
    <Footer></Footer>
  </div>
</template>

<style scoped>
.bottom-image {
  position: fixed;
  bottom: -75px;
  left: 50%; /* Centers the image horizontally */
  transform: translateX(-50%); /* Adjusts the position to truly center */
  width: 75%; /* Ensures the image spans most of the width */
  z-index: -1; /* Keeps the image behind the content */
}
</style>
