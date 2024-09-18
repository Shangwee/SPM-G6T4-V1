import requests
import mysql.connector  
from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#TODO:What other functions to put here? Validation for users like managers and HR? 

#TODO:DB Config?? Add if needed later on.


# Function to aggregate schedules, restricted to managers and directors
@app.route('/aggregated_schedules', methods=['GET'])
def get_aggregated_schedules():
    user_id = request.args.get('user_id')  # Assume user_id is passed in the request
    
    # Fetch the role of the user trying to access this route
    user_role = get_user_role(user_id)
    
    # User validation. Only allow access for Managers and Directors
    if user_role not in ['Manager', 'Director']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Proceed to aggregate schedules if authorized
    data = aggregate_schedules()  
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



# Helper Function to retrieve user's role (can be called in the complex microservice)
def get_user_role(user_id):
    conn = mysql.connector.connect(
        host='localhost',  # #TODO: CHANGE THIS LATER ON. Need to test if this shit works. 
        user='root',
        password='',
        database='your_db_name'
    )
    cursor = conn.cursor(dictionary=True)
    
    # Fetch the user's role from the Employee table
    query = "SELECT Role FROM Employee WHERE Staff_ID = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if result:
        return result['Role']
    return None




def get_schedules_by_department(department): #For filtering by department
    response = requests.get(f"http://schedule-service/schedules_by_department?department={department}")
    return response.json()


def aggregate_schedules(): #For viewing overall schedule

    # List of departments based on the org chart and employee dataset. Change the dept names if the dept name in the employee.csv changes for whatever reason

    departments = [
        'Sales', 'Consultancy', 'Solutioning', 'Engineering',
        'HR', 'Finance', 'IT'
    ]
    
    all_schedules = []
    
    for dept in departments: #Looping through dept array to retrieve overall schedule. For HR and senior managemnet
        schedules = get_schedules_by_department(dept)
        all_schedules.extend(schedules)
        
    return all_schedules


