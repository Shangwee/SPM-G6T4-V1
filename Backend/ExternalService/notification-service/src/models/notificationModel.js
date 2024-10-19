const pool = require('../config/db');

// Create a new notification in the database
async function createNotification(user_id, message, notification_type, request_id) {
    try {
        const query = `INSERT INTO notifications (user_id, message, notification_type, request_id) VALUES (?, ?, ?, ?)`;
        const values = [user_id, message, notification_type, request_id];
        const [result] = await pool.execute(query, values);
        
        return result.insertId; // Return the ID of the newly inserted notification
    } catch (error) {
        console.error('Error creating notification:', error);
        throw error;
    }
}

// Retrieve notifications for a specific user
async function getNotificationsByUserId(user_id) {
    try {
        const query = `SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC`;
        const values = [user_id];
        const [rows] = await pool.execute(query, values);

        return rows; // Return the list of notifications
    } catch (error) {
        console.error('Error fetching notifications for user:', error);
        throw error;
    }
}

// Mark a notification as read
async function markNotificationAsRead(notification_id) {
    try {
        const query = `UPDATE notifications SET is_read = TRUE WHERE id = ?`;
        const [result] = await pool.execute(query, [notification_id]);
        
        return result.affectedRows > 0; // Return true if the update was successful
    } catch (error) {
        console.error('Error marking notification as read:', error);
        throw error;
    }
}

// Retrieve a single notification by its ID
async function getNotificationById(notification_id) {
    try {
        const query = `SELECT * FROM notifications WHERE id = ?`;
        const [rows] = await pool.execute(query, [notification_id]);
        
        return rows[0]; // Return the notification object
    } catch (error) {
        console.error('Error fetching notification by ID:', error);
        throw error;
    }
}

// Mark all notifications as read for a specific user
async function markAllNotificationsAsRead(user_id) {
    try {
        const query = `UPDATE notifications SET is_read = TRUE WHERE user_id = ?`;
        await pool.execute(query, [user_id]);
    } catch (error) {
        console.error('Error marking all notifications as read:', error);
        throw error;
    }
}

// Count the number of unread notifications for a specific user
async function getNotificationCount(user_id) {
    try {
        const query = `SELECT COUNT(*) AS count FROM notifications WHERE user_id = ? AND is_read = FALSE`;
        const [rows] = await pool.execute(query, [user_id]);
        
        return rows[0].count; // Return the count of unread notifications
    } catch (error) {
        console.error('Error fetching unread notification count:', error);
        throw error;
    }
}

module.exports = {
    createNotification,
    getNotificationsByUserId,
    markNotificationAsRead,
    getNotificationById,
    markAllNotificationsAsRead,
    getNotificationCount
};
