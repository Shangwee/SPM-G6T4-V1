const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.json());

require('dotenv').config();

const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME
});


db.connect((err) => {
  if (err) throw err;
  console.log('MySQL Connected...');
});

app.post('/api/login', (req, res) => {
  const { staffID, password } = req.body;

  const query = 'SELECT * FROM Employee WHERE Staff_ID = ?';
  db.query(query, [staffID], (err, result) => {
    if (err) return res.status(500).json({ message: 'Database error' });

    if (result.length === 0) {
      return res.status(401).json({ message: 'Staff ID not found' });
    }

    const staff = result[0];

    if (staff.Password !== password) {  // Case-sensitive for the column name
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    res.json({ message: 'Login successful', staffID: staff.Staff_ID });
  });
});

// Fetch user info route (no authentication)
app.get('/api/user', (req, res) => {
    const { staffID } = req.query; // Assuming staffid is provided as a query parameter
  
    if (!staffID) {
      return res.status(400).json({ message: 'Staff ID is required' });
    }
  
    const query = 'SELECT Staff_ID, Role FROM Employee WHERE Staff_ID = ?';
    db.query(query, [staffID], (err, result) => {
      if (err) return res.status(500).json({ message: 'Database error' });
  
      if (result.length === 0) {
        return res.status(404).json({ message: 'User not found' });
      }
  
      res.json(result[0]);
    });
  });

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
