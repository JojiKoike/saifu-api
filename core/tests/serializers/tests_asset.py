from django.test import TestCase
from core.serializers.asset import *
from core.models.master.asset import MAssetCategoryMain, MAssetCategorySub
from django.contrib.auth.models import User


class AssetCategorySerializerTests(TestCase):

    def setUp(self):
        self.asset_category = {
            "name": "個人年金",
            "m_asset_category_subs": [
                {"name": "個人型確定拠出年金"},
                {"name": "年金財形貯蓄"}
            ]
        }

    def test_asset_category_created_Correctly(self):
        serializer = AssetCategorySerializer(data=self.asset_category)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            self.assertEqual(set(data.keys()), set(['id', 'name', 'm_asset_category_subs']))


class AssetSerializerTests(TestCase):

    def setUp(self):
        self.m_asset_category_main = MAssetCategoryMain.objects.create(name="年金資産")
        self.m_asset_category_sub = MAssetCategorySub.objects.create(
            name="個人年金", m_asset_category_main=self.m_asset_category_main)
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.asset = {
            "name": "ideco",
            "current_capital_amount": 10000000,
            "current_evaluated_amount": 20000000,
            "m_asset_category_sub": self.m_asset_category_sub.id
        }

    def test_asset_created_Correctly(self):
        serializer = AssetSerializer(data=self.asset)
        if serializer.is_valid():
            serializer.save(owner=self.owner)
            data = serializer.data
            self.assertEqual(set(data.keys()),
                             set(['id', 'name', 'current_capital_amount',
                                  'current_evaluated_amount', 'm_asset_category_sub']))
