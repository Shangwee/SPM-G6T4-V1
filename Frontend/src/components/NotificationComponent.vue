<template>
  <div class="container-fluid h-100 d-flex align-items-center">
    <div class="notification-box p-3 h-100">
      <div
        class="notification-header d-flex justify-content-between align-items-center pb-2 border-bottom"
      >
        <h3 class="h5 mb-0">Notifications</h3>
        <div class="d-flex">
          <button
        class="btn btn-secondary btn-sm me-2"
        @click="refreshNotifications"
        :disabled="loading"
          >
        Refresh
          </button>
          <button
        class="btn btn-primary btn-sm"
        @click="markAllAsRead"
        :disabled="notifications.length === 0"
          >
        Mark All as Read
          </button>
        </div>
      </div>

      <!-- Check if there are notifications -->
      <ul
        v-if="notifications.length > 0"
        class="notification-list list-unstyled mt-3"
      >
        <li
          v-for="notification in notifications"
          :key="notification.id"
          :class="{
            unread: !notification.is_read,
            'p-3 mb-2 border-bottom': true,
          }"
        >
          <div class="notification-content">
            <p class="mb-1">
              {{ notification.message }}
              <span class="text-muted"
                >({{ notification.notification_type }})</span
              >
            </p>
          </div>
          <button
            class="btn btn-link text-danger p-0"
            @click="dismissNotification(notification.id)"
          >
            Dismiss
          </button>
        </li>
      </ul>

      <li
        v-else
        class="text-center text-muted d-flex align-items-center justify-content-center"
        style="height: 100%; width: 100%"
      >
        No notifications available.
      </li>

      <!-- Load More Button -->
      <div v-if="hasMoreNotifications" class="text-center mt-3">
        <button
          class="btn btn-secondary"
          @click="loadMoreNotifications"
          :disabled="loading"
        >
          <span v-if="loading">Loading...</span>
          <span v-else>Load More</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { getSocket, disconnectSocket } from "../socket"; // Import the socket functions

// Get Staff ID from session storage
const staffId = parseInt(sessionStorage.getItem("staffID"));

const ACCOUNT_API = import.meta.env.VITE_ACCOUNT_API;
const SCHEDULE_API = import.meta.env.VITE_SCHEDULE_API;
const REQUEST_API = import.meta.env.VITE_REQUEST_API;
const MEETING_API = import.meta.env.VITE_MEETING_API;
const NOTIFICATION_API = import.meta.env.VITE_NOTIFICATION_API;
const FLEXIBLE_ARRANGEMENT_API = import.meta.env.VITE_FLEXIBLE_ARRANGEMENT_API;
const MANAGE_REQUEST_API = import.meta.env.VITE_MANAGE_REQUEST_API;
const SCHEDULE_AGGREGATION_API = import.meta.env.VITE_SCHEDULE_AGGREGATION_API;

export default {
  data() {
    return {
      notifications: [], // Array to store both fetched and real-time notifications
      page: 1, // Current page for pagination
      limit: 5, // Number of notifications per page
      count: 0, // Total count of notifications
      hasMoreNotifications: true, // To check if more notifications are available
      loading: false, // To track loading state
      socket: null, // Socket.IO instance
    };
  },
  async mounted() {
    // Fetch existing notifications from the backend API
    await this.fetchNotifications();

    // Get a singleton instance of the socket
    this.socket = getSocket();

    // Listen for real-time 'newNotification' events
    this.socket.on("notification", (data) => {
      // Add the new notification to the array if it matches the current staff ID
      if (data.user_id === staffId) {
        this.notifications.unshift(data); // Add the new notification to the top of the list
      }
    });
  },
  beforeDestroy() {
    // Disconnect the socket when the component is destroyed
    disconnectSocket();
  },
  methods: {
    async fetchNotifications() {
      // Set loading to true while fetching
      this.loading = true;
      try {
        const response = await axios.get(
          `${NOTIFICATION_API}/api/notifications/user/${staffId}?page=${this.page}&limit=${this.limit}`
        );
        const newNotifications = response.data;

        // Append new notifications to the current list
        this.notifications.push(...newNotifications);

        // Check if we have more notifications to load
        if (newNotifications.length < this.limit) {
          this.hasMoreNotifications = false; // Disable Load More if fewer than limit notifications are returned
        }

        // Increase the page number for the next fetch
        this.page += 1;
      } catch (error) {
        console.error("Error fetching notifications:", error);
      } finally {
        this.loading = false;
      }
    },
    async refreshNotifications() {
      location.reload(); // Reload the page to refresh notifications
    },
    async loadMoreNotifications() {
      // Load more notifications when Load More button is clicked
      await this.fetchNotifications();
    },
    dismissNotification(id) {
      try {
        axios.put(`${NOTIFICATION_API}/api/notifications/read/${id}`, {
          is_read: true,
        });
        const notification = this.notifications.find((n) => n.id === id);
        if (notification) notification.is_read = true;
      } catch (error) {
        console.error("Error dismissing notification:", error);
      }
    },
    markAllAsRead() {
      try {
        axios.put(
          `${NOTIFICATION_API}/api/notifications/read/all/${staffId}`
        );
        this.notifications.forEach(
          (notification) => (notification.is_read = true)
        );
      } catch (error) {
        console.error("Error marking all notifications as read:", error);
      }
    },
  },
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
  max-width: 900px;
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
</style>
