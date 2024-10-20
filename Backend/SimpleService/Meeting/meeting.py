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

# create meeting
@app.route('/meeting', methods=['POST'])
def create_meeting():
    data  = request.get_json()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    Created_By = data['Created_By']
    Date = data['Date']
    Title = data['Title']

    # ** validate date format
    if not validate_date(Date):
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD'}), 400
    
    try:
        query = ("INSERT INTO Meeting (Created_By, Date, Title) VALUES (%s, %s, %s)")
        values = ( Created_By, Date, Title)
        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Meeting created successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# retrieve meeting
@app.route('/meeting', methods=['GET'])
def get_meetings():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT * FROM Meeting where 1=1")

    Meeting_ID = request.args.get('Meeting_ID')
    Created_By = request.args.get('Created_By')
    Date = request.args.get('Date')

    if Meeting_ID:
        query += f" AND Meeting_ID = {Meeting_ID}"
    if Created_By:
        query += f" AND Created_By = {Created_By}"
    if Date:
        date_object = datetime.strptime(Date, "%Y-%m-%d")
        formatted_date = date_object.strftime("%Y-%m-%d")
        query += f" AND Date = '{formatted_date}'"

    values = ()

    cursor.execute(query, values)

    meetings = cursor.fetchall()

    if meetings != []:
        for m in meetings:
            query = ("SELECT * FROM MeetingStaffs WHERE Meeting_ID = %s")

            Meeting_ID = m["Meeting_ID"]

            values = (Meeting_ID,)

            cursor.execute(query, values)

            meetingstaffs = cursor.fetchall()

            m["meetingstaffs"] = meetingstaffs

    cursor.close()
    conn.close()

    return jsonify(meetings), 200

# retrieve meeting staffs
@app.route('/meetingstaffs/<int:Meeting_ID>', methods=['GET'])
def get_meetingstaffs(Meeting_ID):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT * FROM MeetingStaffs WHERE Meeting_ID = %s")
    values = (Meeting_ID,)

    cursor.execute(query, values)

    meetingstaffs = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(meetingstaffs), 200

# delete meeting
@app.route('/meeting/<int:Meeting_ID>', methods=['DELETE'])
def delete_meeting(Meeting_ID):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("DELETE FROM Meeting WHERE Meeting_ID = %s")
    values = (Meeting_ID,)

    cursor.execute(query, values)

    query = ("DELETE FROM MeetingStaffs WHERE Meeting_ID = %s")
    values = (Meeting_ID,)

    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'Meeting deleted successfully!'}), 200


# ** Utility function to validate date format
def validate_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
