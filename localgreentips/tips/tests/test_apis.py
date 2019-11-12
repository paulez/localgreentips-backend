from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cities.models import Country, Region, City

register_url = "/auth/users/"
login_url = "/auth/token/login/"
tips_url = "/tips/"
cities_url = "/cities/"

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

class TipTests(APITestCase):

    def test_get_default_empty(self):
        response = self.client.get(tips_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_post_noauth(self):
        data = {
            "title": "test",
            "text": "this is a test",
        }
        response = self.client.post(tips_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class TipAuthenticatedTests(APITestCase):
    def setUp(self):
        country = Country(name="Empire anarchique du Bachibouzouc",
                          population=12000)
        country.save()
        region = Region(name="Province dépendante du Bazar",
                        country=country)
        region.save()
        city = City(name="Trifouillis les Oies", region=region,
                    country=country,
                    location=Point(42,127), population=42)
        city.save()
        data = {
            "username": "toto",
            "email": "toto@test.com",
            "password": "pouetpouet"
        }
        response = self.client.post(register_url, data, format="json")
        
        data = {
            "username": "toto",
            "password": "pouetpouet",
        }
        response = self.client.post(login_url, data, format="json")
        token = response.data["auth_token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_get_default_empty(self):
        response = self.client.get(tips_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
        

    def test_create_local_tip(self):
        pos = Point(42, 127)
        data = {
                "latitude": pos.y,
                "longitude": pos.x
        }
        response = self.client.get(cities_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cities = response.data["results"]
        test_city = cities[0]

        tip_data = {
            "title": "test local",
            "text": "testing local",
            "cities": [
                {
                    "id": test_city["id"],
                    "name": test_city["name"],
                }],
            "regions": [
                {
                    "id": test_city["region"]["id"],
                    "name": test_city["region"]["name"],
                }],
            "countries": [
                {
                    "id": test_city["region"]["country"]["id"],
                    "name": test_city["region"]["country"]["name"],
                }],
            }
        response = self.client.post(tips_url, tip_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
