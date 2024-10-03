from flask import Flask, request,jsonify
import requests
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Microservice URL configurations
ACCOUNTS_SERVICE_URL = "http://host.docker.internal:5001"
SCHEDULE_SERVICE_URL = "http://host.docker.internal:5002"
REQUEST_SERVICE_URL = "http://host.docker.internal:5003"

@app.route('/manageRequest/reject', methods=['POST'])
def reject():
    # get the staff_id and request_id from the request body
    data = request.get_json()
    staff_id = data['staff_id']
    request_id = data['request_id']

    # check if the user is allowed to reject the request
    role = check_staff_role(staff_id)
    if role == 1 or role == 3:
        # retrieve the request from the request service
        retrieve_request = requests.get(f"{REQUEST_SERVICE_URL}/request/{request_id}")
        if retrieve_request.status_code == 200:
            retrieve_request = retrieve_request.json()
            approver_id = retrieve_request['Approver_ID']

            # check if the user is allowed to reject the request
            if approver_id != staff_id:
                return jsonify({'error': 'You are not allowed to reject this request'}), 401
            
            # reject the request
            update_status = requests.put(f"{REQUEST_SERVICE_URL}/request/update/{request_id}?Status=2")
            if update_status.status_code == 200:
                return jsonify({'message': 'Request rejected successfully'}), 200
            else:
                return jsonify({'error': 'Failed to reject the request'}), 500
        
        # if the request does not exist
        else:
            return jsonify({'error': 'Failed to retrieve the request'}), 500
    
    # if the user is not allowed to reject the request
    return jsonify({'error': 'You are not allowed to reject this request'}), 401

@app.route('/manageRequest/accept', methods=['POST'])
def accept():
    # get the staff_id and request_id from the request
    data = request.get_json()
    staff_id = data['staff_id']
    request_id = data['request_id']

    # check if the user is allowed to accept the request
    role = check_staff_role(staff_id)
    if role == 1 or role == 3:
        # retrieve the request from the request service
        retrieve_request = requests.get(f"{REQUEST_SERVICE_URL}/request/{request_id}")
        if retrieve_request.status_code == 200:
            retrieve_request = retrieve_request.json()
            approver_id = retrieve_request['Approver_ID']

            # check if the user is allowed to accept the request
            if approver_id != staff_id:
                return jsonify({'error': 'You are not allowed to accept this request'}), 401
            
            # accept the request
            update_status = requests.put(f"{REQUEST_SERVICE_URL}/request/update/{request_id}?Status=1")

            if update_status.status_code == 200:
                # add the request to the schedule
                add_schedule = add_to_schedule(request_id)
                if add_schedule.status_code == 201:
                    return jsonify({'message': 'Request accepted and added to schedule'}), 201
                else:
                    return jsonify({'error': 'Failed to add the request to the schedule'}), 500
            else:
                return jsonify({'error': 'Failed to accept the request'}), 500
        else:
            return jsonify({'error': 'Failed to retrieve the request'}), 500
    
    # if the user is not allowed to accept the request
    return jsonify({'error': 'You are not allowed to reject this request'}), 401


def check_staff_role(staff_id):
    Employee = requests.get(f"{ACCOUNTS_SERVICE_URL}/user/{staff_id}")
    if Employee.status_code == 200:
        Employee = Employee.json()
        return Employee['Role']
    return None


def add_to_schedule(request_id):
    # retrieve the request from the request service
    retrieve_request = requests.get(f"{REQUEST_SERVICE_URL}/request/{request_id}")
    if retrieve_request.status_code == 200:
        retrieve_request = retrieve_request.json()
        date = retrieve_request['Date']
        employee_id = retrieve_request['Employee_ID']

        ## format the date as yyyy-mm-dd
        date_object = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
        formatted_date = date_object.strftime('%Y-%m-%d')

        # add the request to the schedule
        add_to_schedule = requests.post(f"{SCHEDULE_SERVICE_URL}/schedule", json={'staff_id': employee_id, 'date': formatted_date, 'request_id': request_id})

        return add_to_schedule
    # if the request does not exist
    return jsonify({'error': 'Failed to retrieve the request'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6002, debug=True)