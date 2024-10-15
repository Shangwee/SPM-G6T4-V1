<template>
  <div class="notification-box">
    <div class="notification-header">
      <h3>Notifications</h3>
      <button class="mark-all-read" @click="markAllAsRead">Mark All as Read</button>
    </div>
    
    <ul class="notification-list">
      <li 
        v-for="notification in notifications" 
        :key="notification.id" 
        :class="{'unread': !notification.is_read}"
      >
        <div class="notification-content">
          <p>{{ notification.message }}</p>
        </div>
        <button class="dismiss-btn" @click="dismissNotification(notification.id)">Dismiss</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { io } from "socket.io-client";
import axios from "axios";

// Get Staff ID from session storage
const staffId = parseInt(sessionStorage.getItem('staffID'));

export default {
  data() {
    return {
      notifications: [],  // Array to store both fetched and real-time notifications
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

    // Connect to the WebSocket server for real-time notifications
    this.socket = io("http://localhost:3000");

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
    if (this.socket) {
      this.socket.disconnect();
    }
  },
  methods: {
    showNotificationToast(message) {
      alert(`New Notification: ${message}`);
    },
    // Dismiss a notification from the list
    dismissNotification(id) {
      this.notifications = this.notifications.filter(notification => notification.id !== id);
    },
    // Mark all notifications as read
    markAllAsRead() {
      this.notifications.forEach(notification => notification.is_read = true);
    },
    // Format the date to a readable format
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString();
    }
  }
};
</script>

<style scoped>
.notification-box {
  width: 300px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.notification-header {
  padding: 10px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-header h3 {
  margin: 0;
  font-size: 16px;
}

.mark-all-read {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.mark-all-read:hover {
  background-color: #0056b3;
}

.notification-list {
  list-style: none;
  margin: 0;
  padding: 0;
  max-height: 300px;
  overflow-y: auto;
}

.notification-list li {
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
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

.notification-content small {
  color: #888;
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
</style>
