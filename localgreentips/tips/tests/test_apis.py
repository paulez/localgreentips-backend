from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

register_url = "/auth/users/"
login_url = "/auth/token/login/"
tips_url = "/tips/"

class AuthTests(APITestCase):

    def test_register_and_login(self):
        data = {
            "username": "titi",
            "email": "titi@test.com",
            "password": "pouetpouet"
        }
        response = self.client.post(register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "username": "titi",
            "password": "pouetpouet"
        }
        response = self.client.post(login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TipAuthenticatedTests(APITestCase):
    def setUp(self):
        data = {
            "username": "toto",
            "email": "toto@test.com",
            "password": "pouetpouet"
        }
        response = self.client.post(register_url, data, format="json")
        
        data = {
            "username": "toto",
            "password": "pouetpouet"
        }
        response = self.client.post(login_url, data, format="json")
        token = response.data["auth_token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_get_default_empty(self):
        response = self.client.get(tips_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
        
