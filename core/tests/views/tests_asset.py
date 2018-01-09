from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AssetCategoryViewSetTests(APITestCase):

    def setUp(self):
        self.data = {
            "name": "個人年金",
            "m_asset_category_subs": [
                {"name": "個人型確定拠出年金"},
                {"name": "年金財形貯蓄"}
            ]
        }

        self.userdata = {
            "username": "admin",
            'email': "admin@admin.com",
            "password": "testpassword"
        }
        self.user = User.objects.create_superuser(**self.userdata)

    def test_asset_category_create_unauthorized(self):
        response = self.client.post('/asset_category/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_asset_category_create_correctly(self):
        response = self.client.post('/auth/jwt/create/',
                                    {'username': 'admin', 'password': 'testpassword'}, format='json')
        token = response.data.pop('token')
        post_response = self.client.post('/asset_category/', self.data, format='json',
                                         HTTP_AUTHORIZATION='JWT {}'.format(token))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(post_response.data.keys()),
                         set(['id', 'name', 'm_asset_category_subs']))

    def test_asset_category_get_unauthorized(self):
        response = self.client.get('/asset_category/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
