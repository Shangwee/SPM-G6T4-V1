const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.json());

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'staffdb'
});

db.connect((err) => {
  if (err) throw err;
  console.log('MySQL Connected...');
});

app.post('/api/login', (req, res) => {
  const { staffid, password } = req.body;

  const query = 'SELECT * FROM staff WHERE staffid = ?';
  db.query(query, [staffid], (err, result) => {
    if (err) return res.status(500).json({ message: 'Database error' });

    if (result.length === 0) {
      return res.status(401).json({ message: 'Staff ID not found' });
    }

    const staff = result[0];

    if (staff.password !== password) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    res.json({ message: 'Login successful', staffid: staff.staffid });
  });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
