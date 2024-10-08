import mysql.connector
from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS
from datetime import datetime

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

# Utility function to validate date format
def validate_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Utility function to apply date filters to a query
def apply_date_filters(query, parameters, start_date, end_date):
    if start_date and end_date:
        query += " AND Date BETWEEN %s AND %s"
        parameters += (start_date, end_date)
    elif start_date:
        query += " AND Date >= %s"
        parameters += (start_date,)
    elif end_date:
        query += " AND Date <= %s"
        parameters += (end_date,)
    return query, parameters

# Reusable function to execute a query and return the results
def execute_query(query, parameters=()):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, parameters)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Get all schedules with optional date filtering
@app.route('/schedule/organisation', methods=['GET'])
def get_schedules():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # staff_ids = request.args.getlist('staff_ids')

    # Validate dates if provided
    if (start_date and not validate_date(start_date)) or (end_date and not validate_date(end_date)):
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400

    query = "SELECT * FROM Schedule WHERE 1=1"

    # Filter by staff IDs if provided #TODO: NOT WORKING PROPERLY, fix later
    # if staff_ids:
    #     query += " AND Staff_ID IN (%s)" % ','.join(['%s'] * len(staff_ids))
    #     parameters = tuple(staff_ids)
    # else:
    #     parameters = ()

    # Apply date filters
    query, parameters = apply_date_filters(query, parameters, start_date, end_date)

    # Execute query and return results
    schedules = execute_query(query, parameters)
    return jsonify(schedules), 200


# Get schedule by staff_id with optional date filtering
@app.route('/schedule/personal/<int:staff_id>', methods=['GET'])
def get_own_schedule(staff_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if (start_date and not validate_date(start_date)) or (end_date and not validate_date(end_date)):
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400

    query = "SELECT * FROM Schedule WHERE Staff_ID = %s"
    parameters = (staff_id,)
    query, parameters = apply_date_filters(query, parameters, start_date, end_date)

    schedules = execute_query(query, parameters)
    return jsonify(schedules), 200


# Get schedules by department based on passed staff IDs (updated)
@app.route('/schedule/dept', methods=['GET'])
def get_department_schedule():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    staff_ids = request.args.getlist('staff_ids')  # Passed in as a list of staff IDs

    if not staff_ids:
        return jsonify({'error': 'No staff IDs provided'}), 400

    if (start_date and not validate_date(start_date)) or (end_date and not validate_date(end_date)):
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400

    query = "SELECT * FROM Schedule WHERE Staff_ID IN (%s)" % ','.join(['%s'] * len(staff_ids))
    parameters = tuple(staff_ids)
    query, parameters = apply_date_filters(query, parameters, start_date, end_date)

    schedules = execute_query(query, parameters)
    return jsonify(schedules), 200


# Get schedules by team based on passed staff IDs (updated)
@app.route('/schedule/team', methods=['GET'])
def get_team_schedule():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    staff_ids = request.args.getlist('staff_ids')  # Passed in as a list of staff IDs

    if not staff_ids:
        return jsonify({'error': 'No staff IDs provided'}), 400

    if (start_date and not validate_date(start_date)) or (end_date and not validate_date(end_date)):
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400

    query = "SELECT * FROM Schedule WHERE Staff_ID IN (%s)" % ','.join(['%s'] * len(staff_ids))
    parameters = tuple(staff_ids)
    query, parameters = apply_date_filters(query, parameters, start_date, end_date)

    schedules = execute_query(query, parameters)
    return jsonify(schedules), 200


# Function to check if staff_id and request_id exist in the database
def check_staff_request_exists(staff_id, request_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Schedule WHERE Staff_ID = %s AND Request_ID = %s''', (staff_id, request_id))
    
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
