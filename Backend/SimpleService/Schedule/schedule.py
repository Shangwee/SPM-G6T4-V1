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

# Get all schedules
@app.route('/schedules', methods=['GET'])
def get_schedules():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT * FROM Schedule")
    cursor.execute(query)

    schedules = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(schedules), 200


@app.route('/get_own_schedule', methods=['GET'])
def get_own_schedule():
    # Extract the user ID from the query parameter (e.g., ?user_id=1)
    user_id = request.args.get('user_id') #TODO: Might need to change this later depending on how current user's staff_ID is retrieved

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Query to get schedules for the logged-in user
    query = "SELECT * FROM Schedule WHERE Staff_ID = %s"
    cursor.execute(query, (user_id,))

    # Fetch the schedules
    schedules = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return jsonify(schedules), 200

@app.route('/get_own_department_schedule', methods=['GET'])
def get_own_department_schedule():

    # Extract the user ID and department from the query parameters, might need to change later
    user_id = request.args.get('user_id')
    department = request.args.get('department')

    if not user_id or not department: #Error handling, will probably change later depending on how filtering is done
        return jsonify({'error': 'User ID and Department are required'}), 400

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Query to get schedules for the logged-in user and specific department
    query = "SELECT * FROM Schedule WHERE Staff_ID = %s AND Dept = %s"
    cursor.execute(query, (user_id, department))

    # Fetch the schedules
    schedules = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return jsonify(schedules), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)