from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models.user.debt import UDebt
from core.models.master.debt import MDebtCategoryMain, MDebtCategorySub


class DebtCategoryViewSetTests(APITestCase):

    def setUp(self):
        self.data = {
            "name": "ローン",
            "m_debt_category_subs": [
                {"name": "奨学金"},
                {"name": "住宅ローン"}
            ]
        }

        self.userdata = {
            "username": "admin",
            'email': "admin@admin.com",
            "password": "testpassword"
        }
        self.user = User.objects.create_superuser(**self.userdata)

    def test_asset_category_create_unauthorized(self):
        response = self.client.post('/debt_category/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_asset_category_create_correctly(self):
        response = self.client.post('/auth/jwt/create/',
                                    {'username': 'admin', 'password': 'testpassword'}, format='json')
        token = response.data.pop('token')
        post_response = self.client.post('/debt_category/', self.data, format='json',
                                         HTTP_AUTHORIZATION='JWT {}'.format(token))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(post_response.data.keys()),
                         {'id', 'name', 'm_debt_category_subs'})

    def test_asset_category_get_unauthorized(self):
        response = self.client.get('/debt_category/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_asset_category_get_correctly(self):
        response = self.client.post('/auth/jwt/create/',
                                    {'username': 'admin', 'password': 'testpassword'}, format='json')
        token = response.data.pop('token')
        get_response = self.client.get('/debt_category/', self.data, format='json',
                                         HTTP_AUTHORIZATION='JWT {}'.format(token))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)


class DebtViewSetTests(APITestCase):

    def setUp(self):
        self.m_debt_category_main = MDebtCategoryMain.objects.create(name="ローン")
        self.m_debt_category_sub = MDebtCategorySub.objects.create(
            name="奨学金", m_debt_category_main=self.m_debt_category_main)
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.debt = {
            "name": "日本育英会第２種修士課程分",
            "current_principal_amount": 100000,
            "current_gained_amount": 100010,
            "m_debt_category_sub": self.m_debt_category_sub.id
        }

    def test_debt_created_Correctly(self):
        response = self.client.post('/auth/jwt/create/',
                                    {'username': 'TestUser', 'password': 'password'}, format='json')
        token = response.data.pop('token')
        post_response = self.client.post('/debt/', self.debt, format='json',
                                         HTTP_AUTHORIZATION='JWT {}'.format(token))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(post_response.data.keys()), {'id', 'name',
                                                          'current_principal_amount',
                                                          'current_gained_amount', 'm_debt_category_sub'})


class DebtGainViewSetTests(APITestCase):

    def setUp(self):
        self.gained_amount = 100020
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.m_debt_category_main = MDebtCategoryMain.objects.create(name="ローン")
        self.m_debt_category_sub = MDebtCategorySub.objects.create(
            name="奨学金", m_debt_category_main=self.m_debt_category_main)
        self.u_debt = UDebt.objects.create(name='日本育英会第２種修士課程分',
                                           current_principal_amount=10000000,
                                           current_gained_amount=20000000,
                                           m_debt_category_sub=self.m_debt_category_sub,
                                           owner=self.owner)
        self.asset_evaluate = {
            'gained_date': '2017-01-10',
            'gained_amount': self.gained_amount,
            'note': 'Test',
            'u_debt': self.u_debt.id
        }

    def test_debt_gain_Correctly(self):
        response = self.client.post('/auth/jwt/create/',
                                    {'username': 'TestUser', 'password': 'password'}, format='json')
        token = response.data.pop('token')
        post_response = self.client.post('/debt_gain/', self.asset_evaluate, format='json',
                                         HTTP_AUTHORIZATION='JWT {}'.format(token))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(post_response.data.keys()), {'id', 'gained_date',
                                                          'gained_amount', 'note', 'u_debt'})
        updated_u_debt = UDebt.objects.get(pk=self.u_debt.id)
        self.assertEqual(updated_u_debt.current_gained_amount, self.gained_amount)
