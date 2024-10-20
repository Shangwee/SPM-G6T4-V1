const notificationModel = require('../models/notificationModel');
const { getIo } = require('../socket');

// Controller to add a new notification job to the queue
const createNotification = async (req, res) => {
    const { user_id, message, notification_type, request_id } = req.body;

    try {
        // Add the notification DB and Socket.io
        await notificationModel.createNotification(user_id, message, notification_type, request_id);

        // Emit real-time notification to connected clients using Socket.IO
        const io = getIo();
        io.emit('notification', { user_id, message, notification_type, request_id });
        res.status(200).json({ message: 'Notification created.' });
    } catch (error) {
        console.error('Error adding notification job to the queue:', error);
        res.status(500).json({ error: 'Failed to add notification to the queue.' });
    }
};

// Controller to get notifications for a specific user
const getUserNotifications = async (req, res) => {
    const userId = req.params.userId;
    let page = parseInt(req.query.page) || 1;
    let limit = parseInt(req.query.limit) || 5;
    
    try {
        // Fetch notifications from the database
        const notifications = await notificationModel.getNotificationsByUserId(userId, page, limit);
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

// Controller to mark all notifications as read for a specific user
const markAllAsRead = async (req, res) => {
    const userId = req.params.userId;

    try {
        // Mark all notifications as read in the database
        await notificationModel.markAllNotificationsAsRead(userId);
        res.status(200).json({ message: 'All notifications marked as read' });
    } catch (error) {
        console.error('Error marking all notifications as read:', error);
        res.status(500).json({ error: 'Failed to mark all notifications as read' });
    }
};

// controller to get notification count for a specific user
const getNotificationCount = async (req, res) => {
    const userId = req.params.userId;

    try {
        // Fetch notification count from the database
        const count = await notificationModel.getNotificationCount(userId);
        res.status(200).json({ count });
    } catch (error) {
        console.error('Error fetching notification count:', error);
        res.status(500).json({ error: 'Failed to fetch notification count' });
    }
};

module.exports = {
    createNotification,
    getUserNotifications,
    markAsRead,
    markAllAsRead,
    getNotificationCount,
};
