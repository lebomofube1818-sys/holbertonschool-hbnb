#!/usr/bin/python3
"""
Unit tests for Users endpoints
"""

import unittest
from app import create_app
import json

class TestUserEndpoints(unittest.TestCase):
    """Test case for User API endpoints"""

    @classmethod
    def setUpClass(cls):
        """Set up test client once for all tests"""
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.base_url = "/api/v1/users/"

    def test_create_user_success(self):
        """Test creating a user successfully"""
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        }
        response = self.client.post(self.base_url,
                                    data=json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["first_name"], "Jane")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["email"], "jane.doe@example.com")
        self.assertIn("id", data)

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data"""
        payload = {
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        }
        response = self.client.post(self.base_url,
                                    data=json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_get_all_users(self):
        """Test retrieving all users"""
        response = self.client.get(self.base_url + "all")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_user_by_id_not_found(self):
        """Test retrieving a non-existent user"""
        response = self.client.get(self.base_url + "non-existent-id")
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_update_user_success(self):
        """Test updating an existing user"""
        # First, create a user
        payload = {
            "first_name": "Mark",
            "last_name": "Smith",
            "email": "mark.smith@example.com"
        }
        create_resp = self.client.post(self.base_url,
                                       data=json.dumps(payload),
                                       content_type="application/json")
        user_id = json.loads(create_resp.data)["id"]

        # Update the user
        update_payload = {
            "first_name": "Marcus",
            "last_name": "Smith",
            "email": "marcus.smith@example.com"
        }
        update_resp = self.client.put(self.base_url + user_id,
                                      data=json.dumps(update_payload),
                                      content_type="application/json")
        self.assertEqual(update_resp.status_code, 200)
        data = json.loads(update_resp.data)
        self.assertEqual(data["first_name"], "Marcus")
        self.assertEqual(data["email"], "marcus.smith@example.com")

    def test_update_user_invalid_data(self):
        """Test updating user with invalid data"""
        payload = {"first_name": "", "last_name": "", "email": "bademail"}
        response = self.client.put(self.base_url + "non-existent-id",
                                   data=json.dumps(payload),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
