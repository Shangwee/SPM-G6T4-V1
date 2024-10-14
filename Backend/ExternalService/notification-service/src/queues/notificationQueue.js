const Queue = require('bull');
const notificationModel = require('../models/notificationModel');
const { getIo } = require('../socket');

// Create a new Bull queue for notifications
const notificationQueue = new Queue('notificationQueue', {
    redis: {
        host: process.env.REDIS_HOST || 'redis',
        port: process.env.REDIS_PORT || 6379,
    },
});

// Process jobs in the notification queue
notificationQueue.process(async (job) => {
    const { user_id, message, notification_type, request_id } = job.data;

    try {
        // Call service to save the notification to the database
        await notificationModel.createNotification(user_id, message, notification_type, request_id);
        // Emit real-time notification to connected clients using Socket.IO
        const io = getIo();
        io.emit('notification', { user_id, message, notification_type, request_id });
    } catch (error) {
        console.error('Error processing notification job:', error);
        throw new Error('Job failed');
    }
});


// Optional: Handle queue events (completed, failed, etc.)
notificationQueue.on('completed', (job) => {
    console.log(`Job ${job.id} completed with result:`, job.data);
});

notificationQueue.on('failed', (job, error) => {
    console.error(`Job ${job.id} failed with error:`, error);
});

module.exports = notificationQueue;
