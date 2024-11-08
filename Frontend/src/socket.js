import { io } from "socket.io-client";
const NOTIFICATION_API = import.meta.env.VITE_NOTIFICATION_API;
let socket = null;

export const getSocket = () => {
  // Check if the socket instance already exists
  if (!socket) {
    // If not, create a new socket connection
    socket = io(`${NOTIFICATION_API}`, {
      // Optionally add connection options
      reconnectionAttempts: 5, // Set max reconnection attempts
      transports: ["websocket"], // Force WebSocket only
    });
  }
  return socket;
};

export const disconnectSocket = () => {
  if (socket) {
    socket.disconnect();
    socket = null; // Clear the socket instance after disconnecting
  }
};
