from django.test import TestCase
from django.contrib.auth.models import User
from core.models.user.saifu import USaifu
from core.models.user.asset import UAsset
from core.models.user.debt import UDebt
from core.models.master.saifu import MSaifuCategoryMain, MSaifuCategorySub
from core.models.master.asset import MAssetCategoryMain, MAssetCategorySub
from core.models.master.debt import MDebtCategoryMain, MDebtCategorySub


class USaifuTests(TestCase):
    """
    Saifu UserModel Tests
    """

    owner = None
    m_saifu_category_main = None
    m_saifu_category_sub = None

    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.m_saifu_category_main = MSaifuCategoryMain.objects.create(name='銀行口座')
        self.m_saifu_category_sub = MSaifuCategorySub.objects.create(name='普通預金',
                                                                     m_saifu_category_main=self.m_saifu_category_main)

    def test_USaifu_Created_Correctly(self):
        u_saifu = USaifu.objects.create(name="Suica", current_balance=5000,
                                        m_saifu_category_sub=self.m_saifu_category_sub, owner=self.owner)
        self.assertEqual(u_saifu.name, "Suica")
        self.assertEqual(u_saifu.current_balance, 5000)
        self.assertEqual(u_saifu.m_saifu_category_sub.name, "普通預金")


class UAssetTests(TestCase):
    """
    Asset UserModel Tests
    """

    owner = None
    m_asset_category_main = None
    m_asset_category_sub = None

    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.m_asset_category_main = MAssetCategoryMain.objects.create(name='年金資産')
        self.m_asset_category_sub = MAssetCategorySub.objects.create(name='個人年金',
                                                                     m_asset_category_main=self.m_asset_category_main)

    def test_UAsset_Created_Correctly(self):
        u_asset = UAsset.objects.create(name='iDeCo',
                                        current_capital_amount=10000000,
                                        current_evaluated_amount=20000000,
                                        m_asset_category_sub=self.m_asset_category_sub,
                                        owner=self.owner)
        self.assertEqual(u_asset.name, 'iDeCo')
        self.assertEqual(u_asset.current_capital_amount, 10000000)
        self.assertEqual(u_asset.current_evaluated_amount, 20000000)


class UDebtTests(TestCase):
    """
    Debt UserModel Tests
    """

    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.m_debt_category_main = MDebtCategoryMain.objects.create(name="ローン")
        self.m_debt_category_sub = MDebtCategorySub.objects.create(name="奨学金",
                                                                   m_debt_category_main=self.m_debt_category_main)

    def test_UDebt_Created_Correctly(self):
        u_debt = UDebt.objects.create(name='日本育英会第２種修士課程分',
                                      current_principal_amount=100000,
                                      current_gained_amount=100010,
                                      m_debt_category_sub=self.m_debt_category_sub,
                                      owner=self.owner)
        self.assertEqual(u_debt.name, '日本育英会第２種修士課程分')
        self.assertEqual(u_debt.current_principal_amount, 100000)
        self.assertEqual(u_debt.current_gained_amount, 100010)
        self.assertEqual(u_debt.m_debt_category_sub.name, self.m_debt_category_sub.name)
