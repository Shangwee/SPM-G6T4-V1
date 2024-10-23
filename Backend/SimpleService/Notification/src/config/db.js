const mysql = require('mysql2/promise');

// Create a pool of connections to the MySQL database
const pool = mysql.createPool({
    host: process.env.DB_HOST || 'spmg6t4.duckdns.org',
    user: process.env.DB_USER || 'remote',
    password: process.env.DB_PASSWORD || 'P@ssw0rd',
    database: process.env.DB_NAME || 'notifications',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

module.exports = pool;
