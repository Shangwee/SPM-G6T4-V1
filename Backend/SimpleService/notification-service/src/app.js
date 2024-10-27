// Load environment variables from .env file
require('dotenv').config();

const express = require('express');
const http = require('http');
const bodyParser = require('body-parser');
const cors = require('cors');
const notificationRoutes = require('./routes/notificationRoutes');
const { initSocket } = require('./socket');

const app = express();
const server = http.createServer(app);

// Initialize Socket.io
initSocket(server);

// Middleware setup
app.use(bodyParser.json());

// Enable CORS
app.use(cors());

// API routes
app.use('/api/notifications', notificationRoutes);

// Start the server and pass `io` to the queue initializer after the server has started
const PORT = process.env.PORT || 5005;
server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});

module.exports = { app, server };