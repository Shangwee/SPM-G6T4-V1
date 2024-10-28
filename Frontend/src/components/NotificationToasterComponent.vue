<template>
  <div class="h-100 d-flex align-items-center justify-content-center">
    <!-- Toast container for showing real-time alerts -->
    <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 1050;">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast align-items-center text-white bg-success border-0 show"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        style="display: flex; animation: fade-in-out 5s;"
      >
        <div class="d-flex">
          <div class="toast-body">
            {{ toast.message }}
          </div>
          <button
            type="button"
            class="btn-close btn-close-white me-2 m-auto"
            aria-label="Close"
            @click="removeToast(toast.id)"
          ></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { getSocket, disconnectSocket } from "../socket"; // Import the socket functions

const ACCOUNT_API = import.meta.env.VITE_ACCOUNT_API;
const SCHEDULE_API = import.meta.env.VITE_SCHEDULE_API;
const REQUEST_API = import.meta.env.VITE_REQUEST_API;
const MEETING_API = import.meta.env.VITE_MEETING_API;
const NOTIFICATION_API = import.meta.env.VITE_NOTIFICATION_API;
const FLEXIBLE_ARRANGEMENT_API = import.meta.env.VITE_FLEXIBLE_ARRANGEMENT_API;
const MANAGE_REQUEST_API = import.meta.env.VITE_MANAGE_REQUEST_API;
const SCHEDULE_AGGREGATION_API = import.meta.env.VITE_SCHEDULE_AGGREGATION_API;

// Get Staff ID from session storage
const staffId = parseInt(sessionStorage.getItem('staffID'));

export default {
  data() {
    return {
      notifications: [],  // Array to store both fetched and real-time notifications
      toasts: [],         // Array to store toast notifications
      socket: null        // Socket.IO instance
    };
  },
  async mounted() {
    // Fetch existing notifications from the backend API
    try {
      const response = await axios.get(`${NOTIFICATION_API}/api/notifications/user/` + staffId);
      this.notifications = response.data;
    } catch (error) {
      console.error("Error fetching notifications:", error);
    }

    // Get a singleton instance of the socket
    this.socket = getSocket();

    // Listen for real-time 'newNotification' events
    this.socket.on("notification", (data) => {
      // Add the new notification to the array if it matches the current staff ID
      if (data.user_id === staffId) {
        this.notifications.unshift(data);  // Add the new notification to the top of the list
        this.showNotificationToast(data.message);
      }
    });
  },
  beforeDestroy() {
    // Disconnect the socket when the component is destroyed
    disconnectSocket();
  },
  methods: {
    showNotificationToast(message) {
      const id = Date.now(); // Unique ID for the toast
      this.toasts.push({ id, message });

      // Automatically remove the toast after 5 seconds
      setTimeout(() => {
        this.removeToast(id);
      }, 5000);
    },
    removeToast(id) {
      this.toasts = this.toasts.filter(toast => toast.id !== id);
    },
  }
};
</script>

<style scoped>
.container-fluid {
  height: 100vh; /* Full height for the container */
}

.dismiss-btn {
  background-color: transparent;
  border: none;
  color: #ff6b6b;
  cursor: pointer;
}

.dismiss-btn:hover {
  color: #ff3b3b;
}

/* Fade-in and fade-out animation for toasts */
@keyframes fade-in-out {
  0% { opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { opacity: 0; }
}
</style>
