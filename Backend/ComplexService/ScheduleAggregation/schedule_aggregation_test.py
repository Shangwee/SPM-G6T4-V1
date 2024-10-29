import unittest
import requests
from schedule_aggregation import app

class TestScheduleAggregation(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def get_actual_response(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def test_aggregate_schedules_single(self):
        expected_response = [
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Engineering",
                "Email": "Koh.Loo@allinone.com.sg",
                "Position": "Junior Engineers",
                "Reporting_Manager": 151408,
                "Request_ID": 1,
                "Role": 2,
                "Schedule_ID": 1,
                "Staff_FName": "Koh",
                "Staff_ID": 151547,
                "Staff_LName": "Loo"
            },
            {
                "Country": "Singapore",
                "Date": "Thu, 26 Sep 2024 00:00:00 GMT",
                "Dept": "Engineering",
                "Email": "Koh.Loo@allinone.com.sg",
                "Position": "Junior Engineers",
                "Reporting_Manager": 151408,
                "Request_ID": 3,
                "Role": 2,
                "Schedule_ID": 3,
                "Staff_FName": "Koh",
                "Staff_ID": 151547,
                "Staff_LName": "Loo"
            }
        ]

        actual_response = self.get_actual_response('http://host.docker.internal:6003/aggregateSchedule?type=Single&staff_id=151547&start_date=2024-09-24&end_date=2026-09-30')
        self.assertEqual(actual_response, expected_response)

    def test_aggregate_schedules_team(self):
        expected_response = [
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Engineering",
                "Email": "Koh.Loo@allinone.com.sg",
                "Position": "Junior Engineers",
                "Reporting_Manager": 151408,
                "Request_ID": 1,
                "Role": 2,
                "Schedule_ID": 1,
                "Staff_FName": "Koh",
                "Staff_ID": 151547,
                "Staff_LName": "Loo"
            },
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Engineering",
                "Email": "Vannah.Seng@allinone.com.sg",
                "Position": "Operation Planning Team",
                "Reporting_Manager": 151408,
                "Request_ID": 2,
                "Role": 2,
                "Schedule_ID": 2,
                "Staff_FName": "Vannah",
                "Staff_ID": 151602,
                "Staff_LName": "Seng"
            }
        ]

        actual_response = self.get_actual_response('http://host.docker.internal:6003/aggregateSchedule?type=Team&staff_id=151547&reporting_manager=151408&start_date=2024-09-01&end_date=2024-09-25')
        self.assertEqual(actual_response, expected_response)

    def test_aggregate_schedules_dept(self):
        expected_response = [
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Engineering",
                "Email": "Koh.Loo@allinone.com.sg",
                "Position": "Junior Engineers",
                "Reporting_Manager": 151408,
                "Request_ID": 1,
                "Role": 2,
                "Schedule_ID": 1,
                "Staff_FName": "Koh",
                "Staff_ID": 151547,
                "Staff_LName": "Loo"
            },
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Engineering",
                "Email": "Vannah.Seng@allinone.com.sg",
                "Position": "Operation Planning Team",
                "Reporting_Manager": 151408,
                "Request_ID": 2,
                "Role": 2,
                "Schedule_ID": 2,
                "Staff_FName": "Vannah",
                "Staff_ID": 151602,
                "Staff_LName": "Seng"
            }
        ]

        actual_response = self.get_actual_response('http://host.docker.internal:6003/aggregateSchedule?type=Dept&staff_id=151547&dept=Engineering&start_date=2024-09-01&end_date=2024-09-24')
        self.assertEqual(actual_response, expected_response)

    def test_aggregate_schedules_all(self):
        expected_response = [
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Engineering",
                "Email": "Koh.Loo@allinone.com.sg",
                "Position": "Junior Engineers",
                "Reporting_Manager": 151408,
                "Request_ID": 1,
                "Role": 2,
                "Schedule_ID": 1,
                "Staff_FName": "Koh",
                "Staff_ID": 151547,
                "Staff_LName": "Loo"
            },
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Engineering",
                "Email": "Vannah.Seng@allinone.com.sg",
                "Position": "Operation Planning Team",
                "Reporting_Manager": 151408,
                "Request_ID": 2,
                "Role": 2,
                "Schedule_ID": 2,
                "Staff_FName": "Vannah",
                "Staff_ID": 151602,
                "Staff_LName": "Seng"
            },
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Sales",
                "Email": "Emma.Heng@allinone.com.sg",
                "Position": "Account Manager",
                "Reporting_Manager": 140894,
                "Request_ID": 8,
                "Role": 2,
                "Schedule_ID": 8,
                "Staff_FName": "Emma",
                "Staff_ID": 140025,
                "Staff_LName": "Heng"
            },
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Sales",
                "Email": "Mary.Teo@allinone.com.sg",
                "Position": "Account Manager",
                "Reporting_Manager": 140894,
                "Request_ID": 9,
                "Role": 2,
                "Schedule_ID": 9,
                "Staff_FName": "Mary",
                "Staff_ID": 140004,
                "Staff_LName": "Teo"
            },
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Sales",
                "Email": "Oliva.Lim@allinone.com.sg",
                "Position": "Account Manager",
                "Reporting_Manager": 140894,
                "Request_ID": 10,
                "Role": 2,
                "Schedule_ID": 10,
                "Staff_FName": "Oliva",
                "Staff_ID": 140015,
                "Staff_LName": "Lim"
            },
            {
                "Country": "Singapore",
                "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
                "Dept": "Sales",
                "Email": "Heng.Chan@allinone.com.sg",
                "Position": "Account Manager",
                "Reporting_Manager": 140008,
                "Request_ID": 11,
                "Role": 2,
                "Schedule_ID": 11,
                "Staff_FName": "Heng",
                "Staff_ID": 140880,
                "Staff_LName": "Chan"
            }
        ]

        actual_response = self.get_actual_response('http://host.docker.internal:6003/aggregateSchedule?type=All&staff_id=140001&start_date=2024-09-24&end_date=2024-09-24')
        self.assertEqual(actual_response, expected_response)
    def test_aggregate_schedules_single_error(self):
        # Simulate an error response from the API
        with self.assertRaises(requests.exceptions.HTTPError):
            self.get_actual_response('http://host.docker.internal:6003/aggregateSchedule?type=Single&staff_id=invalid_id&start_date=2024-09-24&end_date=2026-09-30')

    def test_aggregate_schedules_team_error(self):
        # Simulate an error response from the API
        with self.assertRaises(requests.exceptions.HTTPError):
            self.get_actual_response('http://host.docker.internal:6003/aggregateSchedule?type=Team&staff_id=151547&reporting_manager=invalid&start_date=2024-09-01&end_date=2024-09-25')

    def test_aggregate_schedules_dept_error(self):
        # Simulate an error response from the API
        with self.assertRaises(requests.exceptions.HTTPError):
            self.get_actual_response('http://host.docker.internal:6003/aggregateSchedule?type=Dept&staff_id=151547&dept=wasd&start_date=2024-09-01&end_date=2024-09-24')

    def test_aggregate_schedules_all_error(self):
        # Simulate an error response from the API
        with self.assertRaises(requests.exceptions.HTTPError):
            self.get_actual_response('http://host.docker.internal:6003/aggregateSchedule?type=All&staff_id=invalid_id&start_date=2024-09-24&end_date=2024-09-24')


    def test_invalid_date_format(self):
        response = self.app.get('/aggregateSchedule?type=Single&staff_id=151547&start_date=invalid_date&end_date=2024-09-30')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_start_date_after_end_date(self):
        response = self.app.get('/aggregateSchedule?type=Single&staff_id=151547&start_date=2024-10-01&end_date=2024-09-30')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_unauthorized_access(self):
        response = self.app.get('/aggregateSchedule?type=All&staff_id=151547&start_date=2024-09-24&end_date=2024-09-24')
        self.assertEqual(response.status_code, 403)
        self.assertIn('error', response.get_json())

    def test_no_schedules_found(self):
        response = self.app.get('/aggregateSchedule?type=Single&staff_id=151547&start_date=2024-01-01&end_date=2024-01-02')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())


if __name__ == '__main__':
    unittest.main()