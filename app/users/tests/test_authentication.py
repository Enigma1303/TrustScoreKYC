from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(APITestCase):

    def setUp(self):
        self.signup_url = "/api/auth/signup/"
        self.login_url = "/api/auth/login/"

    def create_user(self, email="test@test.com", password="pass123"):
        return User.objects.create_user(email=email, password=password)

    def login_user(self, email, password):
        return self.client.post(self.login_url,{"email": email, "password": password},)


    def test_user_can_signup(self):
        response = self.client.post(
            self.signup_url,
            {
                "email": "newuser@test.com",
                "password": "StrongPass123"
            },
            
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, "newuser@test.com")

    def test_signup_fails_with_existing_email(self):
        self.create_user(email="duplicate@test.com", password="pass123")

        response = self.client.post(
            self.signup_url,
            {
                "email": "duplicate@test.com",
                "password": "pass123"
            },
            
        )

        self.assertEqual(response.status_code, 400)

    def test_signup_fails_with_missing_password(self):
        response = self.client.post(
            self.signup_url,
            {
                "email": "invalid@test.com"
            },
            
        )

        self.assertEqual(response.status_code, 400)


    def test_user_can_obtain_jwt_token(self):
        self.create_user(email="login@test.com", password="pass123")

        response = self.login_user("login@test.com", "pass123")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIsInstance(response.data["access"], str)
        self.assertIsInstance(response.data["refresh"], str)

    def test_login_fails_with_wrong_password(self):
        self.create_user(email="wrongpass@test.com", password="correctpass")

        response = self.login_user("wrongpass@test.com", "wrongpass")

        self.assertEqual(response.status_code, 401)
