const express = require('express');
const router = express.Router();
const notificationController = require('../controllers/notificationController');

// Route to create a new notification (add a job to Bull Queue)
router.post('/create', notificationController.createNotification);

// Route to get all notifications for a specific user
router.get('/user/:userId', notificationController.getUserNotifications);

// Route to mark a notification as read
router.put('/read/:notificationId', notificationController.markAsRead);

module.exports = router;
