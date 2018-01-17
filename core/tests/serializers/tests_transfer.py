from django.test import TestCase
from core.serializers.transfer import *
from core.models.master.asset import MAssetCategoryMain, MAssetCategorySub
from core.models.master.saifu import MSaifuCategoryMain, MSaifuCategorySub
from core.models.master.debt import MDebtCategoryMain, MDebtCategorySub
from core.models.user.saifu import USaifu
from core.models.user.asset import UAsset
from core.models.user.debt import UDebt
from django.contrib.auth.models import User


class TransferBetWeenSaifuAndAssetSerializerTests(TestCase):

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

    def test_transfer_from_saifu_to_asset_correctly(self):
        amount = 10000
        input_data = {
            'transfer_date': '2017-01-10',
            'amount': amount,
            'note': 'Test',
            'u_saifu': self.u_saifu.id,
            'u_asset': self.u_asset.id
        }
        serializer = TransferBetweenSaifuAndAssetSerializer(data=input_data)
        if serializer.is_valid():
            serializer.save(owner=self.owner)
            data = serializer.data
            self.assertEqual(set(data.keys()), {'id', 'transfer_date', 'amount', 'note', 'u_saifu', 'u_asset'})
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
        serializer = TransferBetweenSaifuAndAssetSerializer(data=input_data)
        if serializer.is_valid():
            serializer.save(owner=self.owner)
            data = serializer.data
            self.assertEqual(set(data.keys()), {'id', 'transfer_date', 'amount', 'note', 'u_saifu', 'u_asset'})
            updated_u_saifu = USaifu.objects.get(pk=self.u_saifu.id)
            self.assertEqual(updated_u_saifu.current_balance, 20000)
            updated_u_asset = UAsset.objects.get(pk=self.u_asset.id)
            self.assertEqual(updated_u_asset.current_capital_amount, 10000)
            self.assertEqual(updated_u_asset.current_evaluated_amount, 10000)


class TransferBetweenSaifuAndDebtSerializerTestCases(TestCase):
    """
    Transfer Between Saifu And Debt Serializer TestCases
    """

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
        self.m_debt_category_main = \
            MDebtCategoryMain.objects.create(name='ローン')
        self.m_debt_category_sub = \
            MDebtCategorySub.objects.create(name='奨学金',
                                            m_debt_category_main=self.m_debt_category_main)
        self.u_debt = UDebt.objects.create(name='日本育英会第２種修士課程分',
                                           current_principal_amount=100000,
                                           current_gained_amount=100010,
                                           m_debt_category_sub=self.m_debt_category_sub,
                                           owner=self.owner)

    def test_transfer_from_saifu_to_debt_correctly(self):
        amount = 10000
        input_data = {
            'transfer_date': '2017-01-10',
            'amount': amount,
            'note': 'Test',
            'u_saifu': self.u_saifu.id,
            'u_debt': self.u_debt.id
        }
        serializer = TransferBetweenSaifuAndDebtSerializer(data=input_data)
        if serializer.is_valid():
            serializer.save(owner=self.owner)
            data = serializer.data
            self.assertEqual(set(data.keys()), {'id', 'transfer_date', 'amount', 'note', 'u_saifu', 'u_debt'})
            updated_u_saifu = USaifu.objects.get(pk=self.u_saifu.id)
            self.assertEqual(updated_u_saifu.current_balance, 0)
            updated_u_debt = UDebt.objects.get(pk=self.u_debt.id)
            self.assertEqual(updated_u_debt.current_principal_amount, 100000)
            self.assertEqual(updated_u_debt.current_gained_amount, 90010)

    def test_transfer_from_debt_to_saifu_Correctly(self):
        amount = -10000
        input_data = {
            'transfer_date': '2017-01-10',
            'amount': amount,
            'note': 'Test',
            'u_saifu': self.u_saifu.id,
            'u_debt': self.u_debt.id
        }
        serializer = TransferBetweenSaifuAndDebtSerializer(data=input_data)
        if serializer.is_valid():
            serializer.save(owner=self.owner)
            data = serializer.data
            self.assertEqual(set(data.keys()), {'id', 'transfer_date', 'amount', 'note', 'u_saifu', 'u_debt'})
            updated_u_saifu = USaifu.objects.get(pk=self.u_saifu.id)
            self.assertEqual(updated_u_saifu.current_balance, 20000)
            updated_u_debt = UDebt.objects.get(pk=self.u_debt.id)
            self.assertEqual(updated_u_debt.current_principal_amount, 110000)
            self.assertEqual(updated_u_debt.current_gained_amount, 110010)

