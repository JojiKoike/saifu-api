from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models.user.saifu import USaifu
from core.models.user.asset import UAsset
from core.models.master.saifu import MSaifuCategoryMain, MSaifuCategorySub
from core.models.master.asset import MAssetCategoryMain, MAssetCategorySub


class TransferBetweenSaifuAndAssetViewSetTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.m_saifu_category_main = \
            MSaifuCategoryMain.objects.create(name="銀行口座")
        self.m_saifu_category_sub = \
            MSaifuCategorySub.objects.create(name='普通口座',
                                             m_saifu_category_main=self.m_saifu_category_main)
        self.u_saifu = USaifu.objects.create(name='スイス銀行', current_balance=10000,
                                             m_saifu_category_sub=self.m_saifu_category_sub,
                                             owner=self.owner)
        self.m_asset_category_main = \
            MAssetCategoryMain.objects.create(name='年金資産')
        self.m_asset_category_sub = \
            MAssetCategorySub.objects.create(name='個人年金',
                                             m_asset_category_main=self.m_asset_category_main)
        self.u_asset = UAsset.objects.create(name='iDeCo',
                                             current_capital_amount=10000,
                                             current_evaluated_amount=20000,
                                             m_asset_category_sub=self.m_asset_category_sub,
                                             owner=self.owner)

        self.jwt_response = self.client.post('/auth/jwt/create/',
                                    {'username': 'TestUser', 'password': 'password'}, format='json')
        self.jwt_token = self.jwt_response.data.pop('token')

    def test_transfer_from_saifu_to_asset_Correctly(self):
        amount = 10000
        input_data = {
            'transfer_date': '2017-01-10',
            'amount': amount,
            'note': 'Test',
            'u_saifu': self.u_saifu.id,
            'u_asset': self.u_asset.id
        }
        post_response = self.client.post('/transfer_between_saifu_and_asset/', input_data, format='json',
                                         HTTP_AUTHORIZATION='JWT {}'.format(self.jwt_token))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(post_response.data.keys()), {'id', 'transfer_date', 'amount', 'note', 'u_saifu', 'u_asset'})
        updated_u_saifu = USaifu.objects.get(pk=self.u_saifu.id)
        self.assertEqual(updated_u_saifu.current_balance, 0)
        updated_u_asset = UAsset.objects.get(pk=self.u_asset.id)
        self.assertEqual(updated_u_asset.current_capital_amount, 20000)
        self.assertEqual(updated_u_asset.current_evaluated_amount, 30000)

    def test_transfer_from_asset_to_saifu_Correctly(self):
        amount = -10000
        input_data = {
            'transfer_date': '2017-01-10',
            'amount': amount,
            'note': 'Test',
            'u_saifu': self.u_saifu.id,
            'u_asset': self.u_asset.id
        }
        post_response = self.client.post('/transfer_between_saifu_and_asset/', input_data, format='json',
                                         HTTP_AUTHORIZATION='JWT {}'.format(self.jwt_token))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        updated_u_saifu = USaifu.objects.get(pk=self.u_saifu.id)
        self.assertEqual(updated_u_saifu.current_balance, 20000)
        updated_u_asset = UAsset.objects.get(pk=self.u_asset.id)
        self.assertEqual(updated_u_asset.current_capital_amount, 10000)
        self.assertEqual(updated_u_asset.current_evaluated_amount, 10000)
