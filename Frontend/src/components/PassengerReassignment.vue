<script setup>
  import NavBar from "./NavBar.vue";
  import PassengerManagement from "./PassengerManagement.vue";
  import LiveChat from "./LiveChat.vue";
</script>

<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div>
      <NavBar></NavBar>

      <!-- Tabs -->
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a class="nav-link active" data-bs-toggle="tab" href="#passengerTab"
            >Passenger Management</a
          >
        </li>
        <li class="nav-item">
          <a class="nav-link" data-bs-toggle="tab" href="#liveChatTab"
            >Live Chat</a
          >
        </li>
      </ul>

      <!-- Tab content -->
      <div class="tab-content">
        <!-- Passenger Management Tab -->
        <div class="tab-pane fade show active" id="passengerTab">
          <PassengerManagement></PassengerManagement>
        </div>

        <!-- Live Chat Tab -->
        <div class="tab-pane fade" id="liveChatTab">
          <LiveChat></LiveChat>
        </div>
      </div>
    </div>
  </div>
</template>

<style></style>
