import unittest
import requests

class TestScheduleAPI(unittest.TestCase): 
    def setUp(self):
        self.API_URL = "http://host.docker.internal:5002"  

    # Test for getting a personal schedule
    def test_get_personal_schedule(self):
        response = requests.get(self.API_URL + "/schedule/personal/151547")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    # Test for getting a group schedule with staff IDs
    def test_get_group_schedule(self):
        staff_ids = "151547,151602"
        start_date = "2024-09-01"
        end_date = "2024-09-30"
        response = requests.get(self.API_URL + f"/schedule/group?staff_ids={staff_ids}&start_date={start_date}&end_date={end_date}")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    # Test for empty schedule response when no data is found
    def test_empty_schedule_response(self):
        response = requests.get(self.API_URL + "/schedule/personal/999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    # Test for single schedule filtered by date range
    def test_schedule_by_date_range(self):
        start_date = "2024-09-25"
        end_date = "2024-09-26"
        response = requests.get(self.API_URL + f"/schedule/personal/151547?start_date={start_date}&end_date={end_date}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['Date'], 'Thu, 26 Sep 2024 00:00:00 GMT')

    # Test for missing staff IDs in group schedule
    def test_group_schedule_no_staff_ids(self):
        response = requests.get(self.API_URL + "/schedule/group?start_date=2024-10-01&end_date=2024-10-15")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'No staff IDs provided')

    # Test for invalid date range (end date earlier than start date)
    def test_invalid_date_range(self):
        response = requests.get(self.API_URL + "/schedule/personal/151547?start_date=2024-10-15&end_date=2024-10-01")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid date range: start date is after end date')

    # Test for schedule with multiple staff IDs
    def test_schedule_with_multiple_staff_ids(self):
        staff_ids = "151547,151602"
        start_date = "2024-09-01"
        end_date = "2024-09-30"
        response = requests.get(self.API_URL + f"/schedule/group?staff_ids={staff_ids}&start_date={start_date}&end_date={end_date}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3) 

    # Test for retrieving schedule without date filters
    def test_schedule_no_date_filter(self):
        response = requests.get(self.API_URL + "/schedule/personal/151547")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


if __name__ == '__main__':
    unittest.main()
