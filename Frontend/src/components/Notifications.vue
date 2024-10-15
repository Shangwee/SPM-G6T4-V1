<script setup>
import NavBar from "./NavBar.vue";
import NotificationComponent from "./NotificationComponent.vue";
</script>

<template>
    <div class="d-flex justify-content-center align-items-center vh-100">
      <div>
        <NavBar></NavBar>
        <div class="position-absolute top-0 end-0 p-3" style="margin-top: 80px;">
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