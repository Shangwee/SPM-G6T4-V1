<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { io } from 'socket.io-client';
import axios from "axios";
import NotificationToasterComponent from './NotificationToasterComponent.vue';

const router = useRouter();
const activeButton = ref(null);
const userRole = ref(null);
const staffID = ref(null);
const loading = ref(true); // Loading state
const notificationCount = ref(0); // Notification count badge
const socket = io('http://localhost:5005'); // Socket.io connection to the backend

// Fetch user role from backend
const fetchUserRole = async () => {
  try {
    staffID.value = JSON.parse(sessionStorage.getItem('staffID'));
    const response = await fetch(`http://localhost:5001/user/${staffID.value}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();
    userRole.value = data.Role;
  } catch (error) {
    console.error('Failed to fetch user role:', error);
  } finally {
    loading.value = false; // Set loading to false after fetching
  }
};

const fetchNotificationCount = async () => {
  try {
    const response = await axios.get(`http://localhost:5005/api/notifications/count/${staffID.value}`);
    console.log(response);
    notificationCount.value = response.data.count;
  } catch (error) {
    console.error('Failed to fetch notification count:', error);
  }
};

// Check if user logged in
const checkLoggedIn = () => {
  if (!staffID.value) {
    router.push('/login');
  }
};

const handleLogin = async () => {
  sessionStorage.clear();
  router.push('/login');
};

const handleOwnSchedule = () => {
  router.push('/ownschedule');
  activeButton.value = 'Own Schedule';
};

const handleTeamSchedule = () => {
  router.push('/teamschedule');
  activeButton.value = 'Team Schedule';
};

const handleArrangements = () => {
  router.push('/arrangements');
  activeButton.value = 'Arrangements';
};

const handleRequests = () => {
  router.push('/requests');
  activeButton.value = 'Requests';
};

const handleNotifications = () => {
  router.push('/notifications');
  activeButton.value = 'Notifications';
};

// Socket.io real-time notification listener
const setupSocketListeners = () => {
  socket.on('notification', (newNotificationCount) => {

    if (newNotificationCount.user_id === staffID.value) {
      // Increment the notification count when a new notification is received
      notificationCount.value += 1;
    }
  });
};

onMounted(() => {
  fetchUserRole();
  fetchNotificationCount();
  checkLoggedIn();
  setupSocketListeners();
});

// Clean up socket connection on component unmount
onBeforeUnmount(() => {
  socket.disconnect();
});

</script>

<template>
  <nav class="navbar navbar-expand-lg py-3 navbar-white bg-white border rounded-2 border-2 shadow-sm fixed-top">
    <div class="container">
      <router-link to="/" class="navbar-brand">
        <h3 class="text-primary">All-in-One</h3>
      </router-link>

      <button
        type="button"
        class="navbar-toggler"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div id="navbarSupportedContent" class="collapse navbar-collapse">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item btn nav-link navbar-btn-hover" :class="{ 'navbar-btn-active': activeButton === 'Own Schedule' }" @click="handleOwnSchedule">My Schedule</li>
          <li class="nav-item btn nav-link navbar-btn-hover" :class="{ 'navbar-btn-active': activeButton === 'Team Schedule' }" @click="handleTeamSchedule">Team Schedule</li>
          <li v-if="userRole === 2" class="nav-item btn nav-link navbar-btn-hover" :class="{ 'navbar-btn-active': activeButton === 'Arrangements' }" @click="handleArrangements">Arrangements</li>
          <li v-if="userRole === 3 || userRole === 1" class="nav-item btn nav-link navbar-btn-hover" :class="{ 'navbar-btn-active': activeButton === 'Requests' }" @click="handleRequests">Requests</li>
          <li class="nav-item btn ml-3 nav-link navbar-btn" @click="handleLogin">Logout</li>
          <li class="nav-item btn nav-link navbar-btn-hover position-relative" @click="handleNotifications">
            Notifications
            <span v-if="notificationCount > 0" class="badge bg-danger position-absolute top-0 start-100 translate-middle">
              {{ notificationCount }}
            </span>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <NotificationToasterComponent></NotificationToasterComponent>
</template>

<style scoped>
.nav-link.aria-current {
  background-color: #f5f5f5;
  border-bottom: 2px solid #000;
}
.nav-item {
  margin: 10px;
}

.navbar-btn-hover:hover,
.navbar-btn-active {
  background-color: #ffffff;
  color: rgb(0, 0, 0);
  font-weight: bold;
}
.navbar-btn:hover {
  background-color: #ffffff;
  color: red;
  font-weight: bold;
}

.navbar-nav {
  width: 100%;
  display: flex;
  justify-content: space-between;
}
.navbar-nav .nav-item {
  flex: 1;
  text-align: center;
}
.navbar-brand:hover {
  background-color: transparent; /* Change to the desired background color or none */
}

/* Style for notification badge */
.badge {
  font-size: 0.75rem;
  padding: 0.35em 0.5em;
}
</style>
