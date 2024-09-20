import mysql.connector
import requests
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

# Create new schedule (Create)
@app.route('/schedule', methods=['POST'])
def create_schedule():
    data = request.get_json()

    staff_id = data["staff_id"]
    request_id = data["request_id"]
    date = data["date"]

    if not staff_id or not request_id or not date:
        return jsonify({'error': 'Please provide all the required fields'}), 400
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Schedule (Staff_ID, Request_ID, Date)
            VALUES (%s, %s, %s)
        ''', (staff_id, request_id, date))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Schedule created successfully'}), 201
    except mysql.connector.IntegrityError:
        return jsonify({'message': 'Schedule already exists'}), 409


# Get all schedules (Read)
@app.route('/schedule', methods=['GET'])
def get_schedules():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT * FROM Schedule")
    cursor.execute(query)

    schedules = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(schedules), 200

# Delete schedule by schedule_id (Delete)
@app.route('/schedule/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM Schedule
        WHERE Schedule_ID = %s
    ''', (schedule_id,))

    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Schedule not found'}), 404

    return jsonify({'message': 'Schedule deleted successfully'}), 200


#Get schedule by staff_id
@app.route('/schedule/personal/<int:staff_id>', methods=['GET'])
def get_own_schedule(staff_id):
    
    # user_id = request.args.get('user_id') #TODO: Might need to change this later depending on how current user's staff_ID is retrieved
    user_id = staff_id 

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


# Get schedules by team
@app.route('/schedule/team/<string:team>', methods=['GET'])
def get_team_schedule(team):

    if not team:
        return jsonify({'error': 'Team is required'}), 400

    # Get staff IDs by team from accounts microservice
    staff_ids = get_staff_ids_by_team(team)
    if not staff_ids:
        return jsonify({'error': 'Unable to retrieve team information'}), 500

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Query the schedules for the staff in the specified team
    query = "SELECT * FROM Schedule WHERE Staff_ID IN (%s)" % ','.join(['%s'] * len(staff_ids))
    cursor.execute(query, tuple(staff_ids))

    schedules = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(schedules), 200


# Get schedules by department
@app.route('/schedule/dept/<string:department>', methods=['GET'])
def get_department_schedule(department):
    if not department:
        return jsonify({'error': 'Department is required'}), 400

    # Get staff IDs by department from accounts microservice
    staff_ids = get_staff_ids_by_department(department)
    if not staff_ids:
        return jsonify({'error': 'Unable to retrieve department information'}), 500

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Query the schedules for the staff in the specified department
    query = "SELECT * FROM Schedule WHERE Staff_ID IN (%s)" % ','.join(['%s'] * len(staff_ids))
    cursor.execute(query, tuple(staff_ids))

    schedules = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(schedules), 200



# TODO: Need to change it so that it calls the account microservice properly. 
 
# Function to get staff IDs by department from the accounts microservice
def get_staff_ids_by_department(department):
    try:
        # Call the account microservice to get staff by department
        response = requests.get(f"http://localhost:5001/users?dept={department}") #TODO: CHANGE THIS LATER ON WHEN DEPLOYING 
        response.raise_for_status()  # Will raise an HTTPError for bad responses

        # Parse the response JSON and extract staff IDs
        users = response.json()
        staff_ids = [user['Staff_ID'] for user in users]  # Extract staff IDs
        return staff_ids

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving staff IDs for department {department}: {e}")
        return None

# Function to get staff IDs by team from the accounts microservice
def get_staff_ids_by_team(team):
    try:
        # Call the account microservice to get staff by team (assuming position correlates with team)
        response = requests.get(f"http://localhost:5001/users?position={team}") #TODO: CHANGE THIS LATER ON WHEN DEPLOYING 
        response.raise_for_status()

        # Parse the response JSON and extract staff IDs
        users = response.json()
        staff_ids = [user['Staff_ID'] for user in users]  # Extract staff IDs
        return staff_ids

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving staff IDs for team {team}: {e}")
        return None



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)