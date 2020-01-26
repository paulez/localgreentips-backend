import logging
import urllib.parse

from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.test import APITestCase



from cities.models import Country, Region, City

logger = logging.getLogger(__name__)

register_url = "/auth/users/"
login_url = "/auth/token/login/"
logout_url = "/auth/token/logout/"
tips_url = "/tips/"
cities_url = "/cities/"

def get_tip_put_url(tip_id):
    return urllib.parse.urljoin(tips_url, str(tip_id), "/") + "/"

class TestUser:
    """Defines auth information for a user.
    """

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def register(self, client):
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        return client.post(register_url, data, format="json")

    def login(self, client):
        data = {
            "username": self.username,
            "password": self.password
        }
        response = client.post(login_url, data, format="json")
        logger.debug("Login response: %s", response)
        token = response.data["auth_token"]
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return response

    def logout(self, client):
        response = client.post(logout_url)
        client.credentials()
        return response

class AuthTests(APITestCase):

    def test_register_and_login(self):
        user = TestUser("titi",
                        "titi@test.com",
                        "pouetpouet")
        response = user.register(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = user.login(self.client)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        user = TestUser("toto",
                        "toto@test.fr",
                        "weshwesh")
        user.register(self.client)
        user.login(self.client)
        response = user.logout(self.client)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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
        response = self.client.post(tips_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TipAuthenticatedTests(APITestCase):
    def setUp(self):
        country = Country(name="Empire anarchique du Bachibouzouc",
                          population=12000)
        country.save()
        region = Region(name="Province dépendante du Bazar",
                        country=country)
        region.save()
        city1 = City(name="Trifouillis les Oies", region=region,
                     country=country,
                     location=Point(42, 127), population=42)
        city1.save()
        city2 = City(name="Montcuq", region=region,
                     country=country,
                     location=Point(42, 127), population=127)
        city2.save()
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

    def test_create_tip_no_location(self):
        tip_data = {
            "title": "test no location",
            "text": "testing with no location"
        }
        response = self.client.post(tips_url, tip_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
                    "id": test_city["country"]["id"],
                    "name": test_city["country"]["name"],
                }],
            }
        response = self.client.post(tips_url, tip_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
                "latitude": pos.y,
                "longitude": pos.x
        }
        response = self.client.get(tips_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["results"])
        test_tip = response.data["results"][0]
        logger.debug("Tip: %s", test_tip)
        self.assertEqual(test_tip["title"], "test local")

    def test_create_tip_with_only_city(self):
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
            "regions": [],
            "countries": [],
            }
        response = self.client.post(tips_url, tip_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
                "latitude": pos.y,
                "longitude": pos.x
        }
        response = self.client.get(tips_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["results"])
        test_tip = response.data["results"][0]
        logger.debug("Tip: %s", test_tip)
        self.assertEqual(test_tip["title"], "test local")

    def test_create_tip_for_nearby_city(self):
        pos = Point(42, 127)
        data = {
                "latitude": pos.y,
                "longitude": pos.x
        }
        response = self.client.get(cities_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cities = response.data["results"]
        test_city = cities[1]

        tip_data = {
            "title": "test local",
            "text": "testing local",
            "cities": [
                {
                    "id": test_city["id"],
                    "name": test_city["name"],
                }],
            "regions": [],
            "countries": [],
            }
        response = self.client.post(tips_url, tip_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
                "latitude": pos.y,
                "longitude": pos.x
        }
        response = self.client.get(tips_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["results"])
        test_tip = response.data["results"][0]
        logger.debug("Tip: %s", test_tip)
        self.assertEqual(test_tip["title"], "test local")


    def test_update_tip(self):
        pos = Point(42, 127)
        data = {
            "latitude": pos.y,
            "longitude": pos.x
        }
        tip_data = {
            "title": "test update",
            "text": "text before update",
        }
        response = self.client.post(tips_url, tip_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tip_id = response.data["id"]

        response = self.client.get(tips_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["results"])

        tip = response.data["results"][0]

        updated_text = "Updated text"
        tip["text"] = updated_text

        tip_url = get_tip_put_url(tip_id)
        logger.debug("put tip url: %s", tip_url)
        response = self.client.put(tip_url, tip, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_tip_id = response.data["id"]
        self.assertEqual(tip_id, updated_tip_id)
        self.assertEqual(response.data["text"], updated_text)

        response = self.client.get(tip_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], updated_text)


class PermissionTests(APITestCase):
    """Validate permissions.
    """

    def setUp(self):
        self.user1 = TestUser("toto", "toto@test.com", "weshwesh")
        self.user2 = TestUser("titi", "titi@test.com", "pouetpouet")
        self.user1.register(self.client)
        self.user2.register(self.client)

    def test_tip_update(self):
        self.user1.login(self.client)
        tip_data = {
            "title": "test auth",
            "text": "testing auth"
        }
        response = self.client.post(tips_url, tip_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tip_id = response.data["id"]

        self.user1.logout(self.client)
        self.user2.login(self.client)
        tip_data = {
            "title": "test update with other user",
            "text": "this should fail"
        }
        tip_url = get_tip_put_url(tip_id)
        response = self.client.put(tip_url, tip_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.user2.logout(self.client)
        self.user1.login(self.client)
        tip_data = {
            "title": "test update with correct user",
            "text": "this should succeed"
        }
        tip_url = get_tip_put_url(tip_id)
        response = self.client.put(tip_url, tip_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
