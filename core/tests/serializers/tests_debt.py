from django.test import TestCase
from core.serializers.debt import DebtCategorySerializer, DebtSerializer, DebtGainSerializer
from core.models.master.debt import MDebtCategoryMain, MDebtCategorySub
from core.models.user.debt import UDebt
from django.contrib.auth.models import User
from datetime import datetime


class DebtCategorySerializerTests(TestCase):
    """
    Debt Category Serializer TestClass
    """

    def setUp(self):
        self.debt_category = {
            "name": "ローン",
            "m_debt_category_subs": [
                {"name": "奨学金"},
                {"name": "銀行学資ローン"}
            ]
        }

    def test_debt_category_created_Correctly(self):
        serializer = DebtCategorySerializer(data=self.debt_category)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            self.assertEqual(set(data.keys()), {'id', 'name', 'm_debt_category_subs'})


class DebtSerializerTests(TestCase):

    def setUp(self):
        self.m_debt_category_main = MDebtCategoryMain.objects.create(name="ローン")
        self.m_debt_category_sub = MDebtCategorySub.objects.create(
            m_debt_category_main=self.m_debt_category_main, name="奨学金")
        self.owner = User.objects.create_user('TestUser', 'test@test.com', 'password')
        self.debt = {
            "name": "日本育英会第２種修士課程分",
            "current_principal_amount": 100000,
            "current_gained_amount": 100010,
            "m_debt_category_sub": self.m_debt_category_sub.id
        }

    def test_debt_created_Correctly(self):
        serializer = DebtSerializer(data=self.debt)
        if serializer.is_valid():
            serializer.save(owner=self.owner)
            data = serializer.data
            self.assertEqual(set(data.keys()),
                             {'id', 'name',
                              'current_principal_amount',
                              'current_gained_amount',
                              'm_debt_category_sub'})


class DebtGainSerializerTests(TestCase):
    """
    Debt Gain Serializer Test Cases
    """

    def setUp(self):
        self.m_debt_category_main = MDebtCategoryMain.objects.create(name="ローン")
        self.m_debt_category_sub = MDebtCategorySub.objects.create(
            m_debt_category_main=self.m_debt_category_main, name="奨学金")
        self.owner = User.objects.create_user('TestUser', 'test@test.com', 'password')
        self.u_debt = UDebt.objects.create(name='日本育英会第２種修士課程分',
                                           current_principal_amount=100000,
                                           current_gained_amount=100010,
                                           m_debt_category_sub=self.m_debt_category_sub,
                                           owner=self.owner)

    def test_debt_gain_correctly(self):
        gained_amount = 100020
        debt_gain = {
            'gained_date': datetime.date(datetime.now()),
            'gained_amount': gained_amount,
            'note': 'Test',
            'u_debt': self.u_debt.id
        }
        serializer = DebtGainSerializer(data=debt_gain)
        if serializer.is_valid():
            serializer.save(owner=self.owner)
            data = serializer.data
            self.assertEqual(set(data.keys()),
                             {'id', 'gained_date', 'gained_amount', 'note', 'u_debt'})
            self.assertEqual(data.pop('gained_amount'), gained_amount)
