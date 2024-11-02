import unittest
import requests

class TestMeetingAPI(unittest.TestCase): 
    def setUp(self):
        self.API_URL = "http://10.128.0.2:5004"  



    # test create meeting
    def test_create_meeting(self):
        obj = {
            "Created_By": 140894,
            "Date": "2024-12-01",
            "Title": "Test Case Meeting"
        }
        
        response = requests.post(self.API_URL + "/meeting", json = obj)
        if (response.status_code == 201):
            meetings_response = requests.get(f"{self.API_URL}/meeting")
            meetings = meetings_response.json()
            
            id = meetings[-1]['Meeting_ID']

            expected_response = {
                'data': {
                    "Meeting_ID": id,
                    "Created_By": 140894,
                    "Date": "Sun, 01 Dec 2024 00:00:00 GMT",
                    "Title": "Test Case Meeting"
                },
                'message': 'Meeting created successfully!'
            }
        elif (response.status_code == 409):
            expected_response = {
                'error': 'A meeting already exists for this user on the specified date.'
            }
        else:
            self.fail(f"Unexpected status code: {response.status_code}")

        self.assertEqual(response.json(), expected_response)
    
    # test create meeting staffs
    def test_create_meetingstaff(self):
        meetings_response = requests.get(f"{self.API_URL}/meeting")
        meetings = meetings_response.json()
        
        if not meetings:
            self.fail("No meetings found to associate with staff.")
        
        id = meetings[-1]['Meeting_ID']

        obj = {
            "Meeting_ID": id,
            "Staff_ID": 140002
        }

        response = requests.post(self.API_URL + "/meetingstaffs", json = obj)
        if (response.status_code == 201):
            expected_response = {
                'message': 'MeetingStaff created successfully!'
            }
        else:
            self.fail(f"Unexpected status code: {response.status_code}")

        self.assertEqual(response.json(), expected_response)

    # test retrieve meeting
    def test_get_meetings(self):
        response = requests.get(self.API_URL + "/meeting")
        self.assertEqual(response.status_code, 200)

    # test retrieve meeting staffs
    def test_get_meetingstaffs(self):
        meetings_response = requests.get(f"{self.API_URL}/meeting")
        meetings = meetings_response.json()
        Meeting_ID = meetings[-1]['Meeting_ID']

        response = requests.get(self.API_URL + "/meetingstaffs/" + str(Meeting_ID))
        self.assertEqual(response.status_code, 200)

    # test delete meeting
    def test_delete_meeting(self):
        meetings_response = requests.get(f"{self.API_URL}/meeting")
        meetings = meetings_response.json()
        Meeting_ID = meetings[-1]['Meeting_ID']

        response = requests.delete(self.API_URL + "/meeting/{}".format(Meeting_ID))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
