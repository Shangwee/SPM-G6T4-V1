const notificationQueue = require('../queues/notificationQueue');
const notificationModel = require('../models/notificationModel');

// Controller to add a new notification job to the queue
const createNotification = async (req, res) => {
    const { user_id, message, notification_type, request_id } = req.body;

    try {
        // Add a job to the Bull Queue
        await notificationQueue.add({
            user_id,
            message,
            notification_type,
            request_id
        });
        res.status(200).json({ message: 'Notification job added to the queue.' });
    } catch (error) {
        console.error('Error adding notification job to the queue:', error);
        res.status(500).json({ error: 'Failed to add notification to the queue.' });
    }
};

// Controller to get notifications for a specific user
const getUserNotifications = async (req, res) => {
    const userId = req.params.userId;

    try {
        // Fetch notifications from the database
        const notifications = await notificationModel.getNotificationsByUserId(userId);
        res.status(200).json(notifications);
    } catch (error) {
        console.error('Error fetching notifications:', error);
        res.status(500).json({ error: 'Failed to fetch notifications' });
    }
};

// Controller to mark a notification as read
const markAsRead = async (req, res) => {
    const notificationId = req.params.notificationId;

    try {
        // Mark the notification as read in the database
        const success = await notificationModel.markNotificationAsRead(notificationId);

        if (success) {
            res.status(200).json({ message: 'Notification marked as read' });
        } else {
            res.status(404).json({ error: 'Notification not found' });
        }
    } catch (error) {
        console.error('Error marking notification as read:', error);
        res.status(500).json({ error: 'Failed to mark notification as read' });
    }
};

module.exports = {
    createNotification,
    getUserNotifications,
    markAsRead,
};
