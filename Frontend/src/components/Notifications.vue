<script setup>
import NavBar from "./NavBar.vue";
import NotificationComponent from "./NotificationComponent.vue";
</script>

<template>
    <div class="d-flex justify-content-center align-items-center vh-100">
      <div>
        <NavBar></NavBar>
        <div class="flex-grow-1 w-100">
        <!-- Increase the size of NotificationComponent to fill height -->
          <NotificationComponent class="notification-component h-100"></NotificationComponent>
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

<style scoped>
.notification-component {
  width: 100%;            /* Take the full width of the parent container */
  max-width: 900px;        /* Limit the maximum width */
  min-height: 100vh;       /* Ensure it covers the full viewport height */
  padding: 20px;           /* Add some padding */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Ensure content is well distributed */
}
</style>
