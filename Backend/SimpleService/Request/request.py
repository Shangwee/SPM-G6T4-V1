import mysql.connector
from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS
import datetime

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


# ** get all requests (add filters)
@app.route('/request', methods=['GET'])
def get_request():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT Request_ID, Employee_ID, Approver_ID, Date, Comments, Status FROM Request where 1=1")

    # ** Extract the parameters from the query string
    Employee_ID = request.args.get('Employee_ID')
    Approver_ID = request.args.get('Approver_ID')
    Status = request.args.get('Status')

    # ** pagination parameters
    page = request.args.get('page')
    page_size = request.args.get('page_size')


    if Employee_ID:
        query += " AND Employee_ID = {Employee_ID}"
    if Approver_ID:
        query += " AND Approver_ID = {Approver_ID}"
    if Status:
        query += " AND Status = {Status}"
    
    if page and page_size:
        offset = (int(page) - 1) * int(page_size)
        query += f" LIMIT {page_size} OFFSET {offset}"

    cursor.execute(query)

    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(requests), 200

# ** get all requests by employee id (add filters)
@app.route('/request/employee/<int:Employee_ID>', methods=['GET'])
def get_request_by_employee_id(Employee_ID):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT Request_ID, Employee_ID, Approver_ID, Date, Comments, Status FROM Request WHERE Employee_ID = %s")
    values = (Employee_ID,)

     # ** Extract the parameters from the query string
    Status = request.args.get('Status')

    if Status:
        query += f" AND Status = {Status}"

    # ** pagination parameters
    page = request.args.get('page')
    page_size = request.args.get('page_size')

    if page and page_size:
        offset = (int(page) - 1) * int(page_size)
        query += f" LIMIT {page_size} OFFSET {offset}"

    cursor.execute(query, values)

    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(requests), 200

# ** get all requests by approver id (add filters)
@app.route('/request/approver/<int:Approver_ID>', methods=['GET'])
def get_request_by_approver_id(Approver_ID):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT Request_ID, Employee_ID, Approver_ID, Date, Comments, Status FROM Request WHERE Approver_ID = %s")
    values = (Approver_ID,)

    # ** Extract the parameters from the query string
    Employee_ID = request.args.get('Employee_ID')
    Status = request.args.get('Status')

    if Employee_ID:
        query += f" AND Employee_ID = {Employee_ID}"
    if Status:
        query += f" AND Status = {Status}"

    # ** pagination parameters
    page = request.args.get('page')
    page_size = request.args.get('page_size')

    if page and page_size:
        offset = (int(page) - 1) * int(page_size)
        query += f" LIMIT {page_size} OFFSET {offset}"


    cursor.execute(query, values)

    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(requests), 200

# ** get request by id (add filters)
@app.route('/request/<int:Request_ID>', methods=['GET'])
def get_request_by_id(Request_ID):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT Request_ID, Employee_ID, Approver_ID, Date, Comments, Status FROM Request WHERE Request_ID = %s")
    values = (Request_ID,)

    cursor.execute(query, values)

    request = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify(request), 200


# ** create a request
@app.route('/request/create/', methods=['POST'])
def create_request():
    data  = request.get_json()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    Employee_ID = data['Employee_ID']
    Approver_ID = data['Approver_ID']
    Comments = data['Comments']
    Status = 0
    Date = data['Date']

    # ** check if the request already exists
    check_exist = check_if_request_exists_by_employee_id_date(Employee_ID, Date)

    if check_exist:
        return jsonify({'message': 'Request already exists'}), 409

    try:
        query = ("INSERT INTO Request (Employee_ID, Approver_ID, Date, Comments, Status) VALUES (%s, %s, %s, %s, %s)")
        values = (Employee_ID, Approver_ID, Date, Comments, Status)
        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Request created successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# ** update a request status
@app.route('/request/update/<int:Request_ID>', methods=['PUT'])
def update_request(Request_ID):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    Status = request.args.get('Status')

    try:
        query = ("UPDATE Request SET Status = %s WHERE Request_ID = %s")
        values = (Status, Request_ID)

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Request updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ** delete a request by id
@app.route('/request/delete/<int:Request_ID>', methods=['DELETE'])
def delete_request(Request_ID):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("DELETE FROM Request WHERE Request_ID = %s")
    values = (Request_ID,)

    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'Request deleted successfully!'}), 200


# ** check if request exists by employee id and date
def check_if_request_exists_by_employee_id_date(employee_id, date):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT * FROM Request WHERE Employee_ID = %s AND Date = %s")
    values = (employee_id, date)
    cursor.execute(query, values)

    request = cursor.fetchone()

    cursor.close()
    conn.close()

    return request

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)