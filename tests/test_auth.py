import unittest
import json

from app.app import create_app, db


class AuthTestCases(unittest.TestCase):
    """
    Tests for  authentication
    """
    def setUp(self):
        self.app = create_app(config_name="testing")
        # Set up the test client
        self.client = self.app.test_client
        self.user_data = json.dumps(dict({
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "test_password"
        }))

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_registration(self):
        """
        Test new user registration
        """
        result = self.client().post("/api/bucketlists/auth/register/", data=self.user_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)


    def test_registration_without_user_email(self):
        """
        Test that empty user email  cannot register
        """
        unregistered = json.dumps(dict({
            "username": "testuser",
            "email": "",
            "password": "testpassword"
        }))

        result = self.client().post("/api/bucketlists/auth/register/", data=unregistered,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 400)

    def test_registration_without_username(self):
        """
        Test that empty user name  cannot register
        """
        unregistered = json.dumps(dict({
            "username": "",
            "email": "testuser@gmail.com",
            "password": "testpassword"
        }))
        result = self.client().post("/api/bucketlists/auth/register/", data=unregistered,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 400)

    def test_registration_without_user_password(self):
        """
        Test that empty user password  cannot register
        """
        unregistered = json.dumps(dict({
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": ""
        }))
        result = self.client().post("/api/bucketlists/auth/register/", data=unregistered,
                                    content_type="application/json")

        self.assertEqual(result.status_code, 400)

    def test_registration_with_special_characters(self):
        """
        test username registration with special characters

        """
        result = self.client().post("/api/bucketlists/auth/register/", data=json.dumps(dict({
            "username" : "collins*&",
            "email" : "collins@gmail.com",
            "password" : "mashcollo"
        })), content_type="application/json")
        self.assertEqual(result.status_code, 403)

    def test_registration_with_invalid_email(self):
        """
        test username registration with special characters

        """
        result = self.client().post("/api/bucketlists/auth/register/", data=json.dumps(dict({
            "username" : "collins",
            "email" : "collins@gmailcom",
            "password" : "mashcollo"
        })), content_type="application/json")
        self.assertEqual(result.status_code, 403)

    def test_registration_with_short_password(self):
        """
        test username registration with special characters

        """
        result = self.client().post("/api/bucketlists/auth/register/", data=json.dumps(dict({
            "username" : "collins",
            "email" : "collins@gmail.com",
            "password" : "mash"
        })), content_type="application/json")
        self.assertEqual(result.status_code, 403)

    def test_double_registration(self):
        """
        Test that double registration
        """
        result = self.client().post("/api/bucketlists/auth/register/", data=self.user_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)

        # Test double registration
        second_result = self.client().post("/api/bucketlists/auth/register/",
                                           data=self.user_data,
                                           content_type="application/json")
        self.assertEqual(second_result.status_code, 409)

    def test_register_with_a_nonexistent_url(self):
        """
        Test registration with an invalid url
        """
        response = self.client().post('/bucketlist/api/auth/regist/', data=self.user_data)
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        """
        Test that a user can login successfully
        """
        result = self.client().post("/api/bucketlists/auth/register/", data=self.user_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)

        login_result = self.client().post("/api/bucketlists/auth/login/", data=self.user_data,
                                          content_type="application/json")
        results = json.loads(login_result.data.decode())

        # Confirm the success message
        self.assertEqual(results["message"], "You logged in successfully.")
        # Confirm the status code and access token
        self.assertEqual(login_result.status_code, 200)
        self.assertTrue(results["access_token"])

    def test_login_non_registered_user(self):
        """
        Test that non registered users cannot log in
        """
        unregistered = json.dumps(dict({
            "username": "tiaroot",
            "email": "tiaroot@email.com",
            "password": "invalidpassword"
        }))

        result = self.client().post("/api/bucketlists/auth/login/", data=unregistered,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 401)

    def test_login_with_a_nonexistent_url(self):
        """
        Test login with invalid url
        """
        response = self.client().post('/bucketlist/api/auth/logon/', data=self.user_data)
        self.assertEqual(response.status_code, 404)
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
