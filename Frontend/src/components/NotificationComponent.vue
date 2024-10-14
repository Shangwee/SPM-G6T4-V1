<template>
    <div>
      <ul>
        <li v-for="notification in notifications" :key="notification.id">
          {{ notification.message }} ({{ notification.notification_type }})
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
        // Add the new notification to the array
        // check user id against the user id in the notification
        if (data.user_id === staffId) {
            this.notifications.push(data);
            // Optionally, display a toast notification for the new message
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
      }
    }
  };
  </script>
  
  <style scoped>
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    background-color: #f1f1f1;
    margin: 5px 0;
    padding: 10px;
    border-radius: 4px;
  }
  </style>
  