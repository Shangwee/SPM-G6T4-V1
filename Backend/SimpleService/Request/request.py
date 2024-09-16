import mysql.connector
from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection configuration
db_config = {
    'host': environ.get('DB_HOST'),
    'user': environ.get('DB_USER'),
    'password': environ.get('DB_PASSWORD'),
    'port': environ.get('DB_PORT'),
    'database': environ.get('DB_NAME')
}

# get all requests
@app.route('/requests', methods=['GET'])
def get_schedules():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT * FROM Request")
    cursor.execute(query)

    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(requests), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)