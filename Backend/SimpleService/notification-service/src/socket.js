// socket.js
const socketIo = require('socket.io');
let io;

function initSocket(server) {
    io = socketIo(server, {
        cors: {
            origin: '*', // Adjust this to match your frontend origin
            methods: ['GET', 'POST']
        }
    });

    io.on('connection', (socket) => {
        console.log('New client connected: ', socket.id);

        // Handle disconnection
        socket.on('disconnect', () => {
            console.log('Client disconnected: ', socket.id);
        });
    });

    return io;
}

function getIo() {
    if (!io) {
        throw new Error('Socket.io not initialized!');
    }
    return io;
}

module.exports = { initSocket, getIo };