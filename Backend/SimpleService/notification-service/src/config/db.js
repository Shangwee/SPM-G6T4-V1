const mysql = require('mysql2/promise');

// Create a pool of connections to the MySQL database
const pool = mysql.createPool({
    host: process.env.DB_HOST || 'notifications_db',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || 'root',
    database: process.env.DB_NAME || 'notifications_db',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

module.exports = pool;
