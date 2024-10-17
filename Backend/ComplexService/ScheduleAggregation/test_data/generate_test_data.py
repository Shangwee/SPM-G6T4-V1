import requests
import json
import os
import time

# API endpoints to query for complex schedule
API_ENDPOINTS = {
    "accounts": "http://localhost:5001/user/",
    "schedules": "http://localhost:5002/schedule/personal/"
}

# Sample staff IDs to extract responses for. #TODO: Can remove a few don't need so many
STAFF_IDS = [151547, 151602, 140025, 140004, 140015, 140880]

# Function to send API request and save response as JSON
def extract_and_save_response(endpoint, staff_id):
    url = f"{endpoint}{staff_id}"
    try:
        response = requests.get(url, timeout=10)  # Adjust timeout as needed
        response.raise_for_status()  # Raise exception for bad responses

        # Parse and save JSON response
        data = response.json()

        # Construct file path in the current directory
        filename = f"{endpoint.split('/')[-2]}_{staff_id}.json"

        # Save to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Saved response for {staff_id} from {endpoint} to {filename}")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data for {staff_id} from {endpoint}: {e}")

# Function to iterate over staff IDs and endpoints
def fetch_and_save_all_responses():
    for endpoint_name, endpoint_url in API_ENDPOINTS.items():
        for staff_id in STAFF_IDS:
            extract_and_save_response(endpoint_url, staff_id)
            time.sleep(1)  # Sleep to avoid overwhelming the API (adjust as necessary)

# Main execution
if __name__ == '__main__':
    fetch_and_save_all_responses()
