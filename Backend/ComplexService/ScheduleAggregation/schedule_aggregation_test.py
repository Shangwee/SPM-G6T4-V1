import unittest
from unittest.mock import patch
from schedule_aggregation import app, validate_date_range, get_user_position

class TestScheduleAggregator(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    
    @patch('schedule_aggregation.requests.get')  # <-- Correct the path here
    def test_single_schedule(self, mock_get):
        mock_get.return_value.json.return_value = {
    "augmented_schedules": [
        {
            "Country": "Singapore",
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Dept": "Engineering",
            "Email": "Koh.Loo@allinone.com.sg",
            "Position": "Junior Engineers",
            "Reporting_Manager": 151408,
            "Request_ID": 10,
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
            "Request_ID": 12,
            "Role": 2,
            "Schedule_ID": 3,
            "Staff_FName": "Koh",
            "Staff_ID": 151547,
            "Staff_LName": "Loo"
        }
    ],
    "original_schedules": [
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 10,
            "Schedule_ID": 1,
            "Staff_ID": 151547
        },
        {
            "Date": "Thu, 26 Sep 2024 00:00:00 GMT",
            "Request_ID": 12,
            "Schedule_ID": 3,
            "Staff_ID": 151547
        }
    ]
}
        mock_get.return_value.status_code = 200

        response = self.client.get('/aggregateSchedule?type=Single&staff_id=151547&start_date=2024-09-24&end_date=2026-09-30')
        self.assertEqual(response.status_code, 200)
        self.assertIn('augmented_schedules', response.json)

    # Test for "Team" type aggregation
    @patch('schedule_aggregation.requests.get')  # <-- Correct the path here
    def test_team_schedule(self, mock_get):
        mock_get.return_value.json.return_value = {
    "augmented_schedules": [
        {
            "Country": "Singapore",
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Dept": "Engineering",
            "Email": "Koh.Loo@allinone.com.sg",
            "Position": "Junior Engineers",
            "Reporting_Manager": 151408,
            "Request_ID": 10,
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
            "Request_ID": 11,
            "Role": 2,
            "Schedule_ID": 2,
            "Staff_FName": "Vannah",
            "Staff_ID": 151602,
            "Staff_LName": "Seng"
        },
        {
            "Country": "Singapore",
            "Date": "Thu, 26 Sep 2024 00:00:00 GMT",
            "Dept": "Engineering",
            "Email": "Koh.Loo@allinone.com.sg",
            "Position": "Junior Engineers",
            "Reporting_Manager": 151408,
            "Request_ID": 12,
            "Role": 2,
            "Schedule_ID": 3,
            "Staff_FName": "Koh",
            "Staff_ID": 151547,
            "Staff_LName": "Loo"
        },
        {
            "Country": "Vietnam",
            "Date": "Thu, 26 Sep 2024 00:00:00 GMT",
            "Dept": "Engineering",
            "Email": "Phalla.Yong@allinone.com.vn",
            "Position": "Junior Engineers",
            "Reporting_Manager": 151408,
            "Request_ID": 13,
            "Role": 2,
            "Schedule_ID": 4,
            "Staff_FName": "Phalla",
            "Staff_ID": 151459,
            "Staff_LName": "Yong"
        }
    ],
    "original_schedules": [
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 10,
            "Schedule_ID": 1,
            "Staff_ID": 151547
        },
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 11,
            "Schedule_ID": 2,
            "Staff_ID": 151602
        },
        {
            "Date": "Thu, 26 Sep 2024 00:00:00 GMT",
            "Request_ID": 12,
            "Schedule_ID": 3,
            "Staff_ID": 151547
        },
        {
            "Date": "Thu, 26 Sep 2024 00:00:00 GMT",
            "Request_ID": 13,
            "Schedule_ID": 4,
            "Staff_ID": 151459
        }
    ]
}
        mock_get.return_value.status_code = 200

        response = self.client.get('/aggregateSchedule?type=Team&staff_id=151547&reporting_manager=151408&start_date=2024-09-01&end_date=2024-09-30')
            # Add this to see what the mock is returning
        print(f"Mock returned: {mock_get.return_value.json.return_value}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('augmented_schedules', response.json)

    # Test for "Department" type aggregation
    @patch('schedule_aggregation.requests.get')  # <-- Correct the path here
    def test_department_schedule(self, mock_get):
        mock_get.return_value.json.return_value = {
    "augmented_schedules": [
        {
            "Country": "Singapore",
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Dept": "Engineering",
            "Email": "Koh.Loo@allinone.com.sg",
            "Position": "Junior Engineers",
            "Reporting_Manager": 151408,
            "Request_ID": 10,
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
            "Request_ID": 11,
            "Role": 2,
            "Schedule_ID": 2,
            "Staff_FName": "Vannah",
            "Staff_ID": 151602,
            "Staff_LName": "Seng"
        }
    ],
    "original_schedules": [
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 10,
            "Schedule_ID": 1,
            "Staff_ID": 151547
        },
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 11,
            "Schedule_ID": 2,
            "Staff_ID": 151602
        }
    ]
}
        mock_get.return_value.status_code = 200

        response = self.client.get('/aggregateSchedule?type=Dept&staff_id=151547&dept=Engineering&start_date=2024-09-01&end_date=2024-09-24')
        self.assertEqual(response.status_code, 200)
        self.assertIn('augmented_schedules', response.json)

    # Test for "All" type aggregation (only HR or Director should access)
    @patch('schedule_aggregation.get_user_position')
    @patch('schedule_aggregation.requests.get')  # <-- Correct the path here
    def test_authorized_all_schedule(self, mock_get_user_position, mock_get):
        mock_get_user_position.return_value = 'Director'
        mock_get.return_value.json.return_value = {
    "augmented_schedules": [
        {
            "Country": "Singapore",
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Dept": "Engineering",
            "Email": "Koh.Loo@allinone.com.sg",
            "Position": "Junior Engineers",
            "Reporting_Manager": 151408,
            "Request_ID": 10,
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
            "Request_ID": 11,
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
            "Request_ID": 17,
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
            "Request_ID": 18,
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
            "Request_ID": 19,
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
            "Request_ID": 20,
            "Role": 2,
            "Schedule_ID": 11,
            "Staff_FName": "Heng",
            "Staff_ID": 140880,
            "Staff_LName": "Chan"
        }
    ],
    "original_schedules": [
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 10,
            "Schedule_ID": 1,
            "Staff_ID": 151547
        },
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 11,
            "Schedule_ID": 2,
            "Staff_ID": 151602
        },
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 17,
            "Schedule_ID": 8,
            "Staff_ID": 140025
        },
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 18,
            "Schedule_ID": 9,
            "Staff_ID": 140004
        },
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 19,
            "Schedule_ID": 10,
            "Staff_ID": 140015
        },
        {
            "Date": "Tue, 24 Sep 2024 00:00:00 GMT",
            "Request_ID": 20,
            "Schedule_ID": 11,
            "Staff_ID": 140880
        }
    ]
}
        mock_get.return_value.status_code = 200

        response = self.client.get('/aggregateSchedule?type=All&staff_id=140001&start_date=2024-09-24&end_date=2026-09-30')
        print(f"Mocked user position: {mock_get_user_position.return_value}")
        print(f"Response: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('augmented_schedules', response.json)

if __name__ == '__main__':
    unittest.main()
