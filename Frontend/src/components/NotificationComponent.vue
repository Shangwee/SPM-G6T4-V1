<template>
  <div class="container-fluid h-100 d-flex align-items-center justify-content-center">
    <div class="notification-box p-3">
      <div class="notification-header d-flex justify-content-between align-items-center pb-2 border-bottom">
        <h3 class="h5 mb-0">Notifications</h3>
        <button class="btn btn-primary btn-sm" @click="markAllAsRead" :disabled="notifications.length === 0">
          Mark All as Read
        </button>
      </div>
      
      <!-- Check if there are notifications -->
      <ul class="notification-list list-unstyled mt-3">
        <li 
          v-if="notifications.length === 0" 
          class="text-center text-muted d-flex align-items-center justify-content-center"
          style="height: 100%; width: 100%; /* Adjust width to screen */"
        >
          No notifications available.
        </li>
        <li 
          v-for="notification in notifications" 
          :key="notification.id" 
          :class="{'unread': !notification.is_read, 'p-3 mb-2 border-bottom': true}"
        >
          <div class="notification-content">
            <p class="mb-1">{{ notification.message }} <span class="text-muted">({{ notification.notification_type }})</span></p>
          </div>
          <button class="btn btn-link text-danger p-0" @click="dismissNotification(notification.id)">Dismiss</button>
        </li>
      </ul>
    </div>

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
      const response = await axios.get("http://localhost:3000/api/notifications/user/" + staffId);
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
    dismissNotification(id) {
      try {
        axios.put(`http://localhost:3000/api/notifications/read/${id}`, { is_read: true });
        const notification = this.notifications.find(n => n.id === id);
        if (notification) notification.is_read = true;
      } catch (error) {
        console.error("Error dismissing notification:", error);
      }
    },
    markAllAsRead() {
      try {
        axios.put(`http://localhost:3000/api/notifications/read/all/${staffId}`);
        this.notifications.forEach(notification => notification.is_read = true);
      } catch (error) {
        console.error("Error marking all notifications as read:", error);
      }
    }
  }
};
</script>

<style scoped>
.container-fluid {
  height: 100vh; /* Full height for the container */
}

.notification-box {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* Set a fixed width for consistent size */
  max-width: 800px;
  width: 100%; /* Adjust width to screen */
}

.notification-header {
  padding: 10px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between; /* Space between title and button */
  align-items: center; /* Align items vertically */
  flex-wrap: wrap; /* Allow wrapping to avoid overlap */
}

.notification-header h3 {
  margin: 0;
  font-size: 16px;
}

.notification-header button {
  margin-left: 10px; /* Add margin to give some space between text and button */
}

.notification-list {
  list-style: none;
  margin: 0;
  padding: 0;
  min-height: 200px;
  max-height: 300px;
  overflow-y: auto; /* Ensure scrolling when content exceeds max height */
}

.notification-list li {
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd; /* Adds a bottom border to each notification */
}

.notification-list li.unread {
  background-color: #eef4fb;
}

.notification-content {
  display: flex;
  flex-direction: column;
}

.notification-content p {
  margin: 0;
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
