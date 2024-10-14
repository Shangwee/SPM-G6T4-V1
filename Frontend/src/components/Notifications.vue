<script setup>
import NavBar from "./NavBar.vue";
import NotificationComponent from "./NotificationComponent.vue";
</script>

<template>
    <div class="d-flex justify-content-center align-items-center vh-100">
      <div>
        <NavBar></NavBar>
        <div class="container mt-5 pt-5">
          <h3 class="text-center" style="margin-top: -200px;">Notifications</h3>
          <NotificationComponent></NotificationComponent>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  data() {
    return {

    };
  },

  methods: {
    
  },
  components: {
    NavBar,
    NotificationComponent
  },  
};
</script>

<style>
</style>