from django.test import TestCase
from core.serializers.asset import *
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

    def test_asset_category_saved_Correctly(self):
        serializer = AssetCategorySerializer(data=self.asset_category)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            self.assertEqual(set(data.keys()), set(['id', 'name', 'm_asset_category_subs']))
