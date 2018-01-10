from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models.user.asset import UAsset
from core.models.master.asset import MAssetCategoryMain, MAssetCategorySub


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
                         {'id', 'name', 'm_asset_category_subs'})

    def test_asset_category_get_unauthorized(self):
        response = self.client.get('/asset_category/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AssetViewSetTests(APITestCase):

    def setUp(self):
        self.m_asset_category_main = MAssetCategoryMain.objects.create(name="年金資産")
        self.m_asset_category_sub = MAssetCategorySub.objects.create(
            name="個人年金", m_asset_category_main=self.m_asset_category_main)
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.asset = {
            "name": "iDeCo",
            "current_capital_amount": 10000000,
            "current_evaluated_amount": 20000000,
            "m_asset_category_sub": self.m_asset_category_sub.id
        }

    def test_asset_created_Correctly(self):
        response = self.client.post('/auth/jwt/create/',
                                    {'username': 'TestUser', 'password': 'password'}, format='json')
        token = response.data.pop('token')
        post_response = self.client.post('/asset/', self.asset, format='json',
                                         HTTP_AUTHORIZATION='JWT {}'.format(token))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(post_response.data.keys()), {'id', 'name',
                                                          'current_capital_amount',
                                                          'current_evaluated_amount', 'm_asset_category_sub'})


class AssetEvaluateViewSetTests(APITestCase):

    def setUp(self):
        self.evaluated_amount = 30000000
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.m_asset_category_main = MAssetCategoryMain.objects.create(name="年金資産")
        self.m_asset_category_sub = MAssetCategorySub.objects.create(
            name="個人型確定拠出年金", m_asset_category_main=self.m_asset_category_main)
        self.u_asset = UAsset.objects.create(name='iDeCo',
                                             current_capital_amount=10000000,
                                             current_evaluated_amount=20000000,
                                             m_asset_category_sub=self.m_asset_category_sub,
                                             owner=self.owner)
        self.asset_evaluate = {
            'evaluate_date': '2017-01-10',
            'evaluated_amount': self.evaluated_amount,
            'note': 'Test',
            'u_asset': self.u_asset.id
        }

    def test_asset_evaluate_Correctly(self):
        response = self.client.post('/auth/jwt/create/',
                                    {'username': 'TestUser', 'password': 'password'}, format='json')
        token = response.data.pop('token')
        post_response = self.client.post('/asset_evaluate/', self.asset_evaluate, format='json',
                                         HTTP_AUTHORIZATION='JWT {}'.format(token))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(post_response.data.keys()), {'id', 'evaluate_date',
                                                          'evaluated_amount', 'note', 'u_asset'})
        updated_u_asset = UAsset.objects.get(pk=self.u_asset.id)
        self.assertEqual(updated_u_asset.current_evaluated_amount, self.evaluated_amount)



