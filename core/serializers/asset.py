from rest_framework import serializers
from ..models.master.asset import MAssetCategoryMain, MAssetCategorySub
from ..models.user.asset import UAsset


class AssetCategorySubSerializer(serializers.ModelSerializer):
    """
    Asset Category Sub Serializer
    """
    m_asset_category_main = serializers.UUIDField(read_only=True)

    class Meta:
        model = MAssetCategorySub
        fields = ('id', 'name', 'm_asset_category_main')


class AssetCategorySerializer(serializers.ModelSerializer):
    """
    Asset Category Serializer
    """
    m_asset_category_subs = AssetCategorySubSerializer(many=True)

    class Meta:
        model = MAssetCategoryMain
        fields = ('id', 'name', 'm_asset_category_subs')

    def create(self, validated_data):
        m_asset_category_subs_data = validated_data.pop('m_asset_category_subs')
        m_asset_category_main = MAssetCategoryMain.objects.create(**validated_data)
        for m_asset_category_sub_data in m_asset_category_subs_data:
            MAssetCategorySub.objects.create(
                m_asset_category_main=m_asset_category_main, **m_asset_category_sub_data)
        return m_asset_category_main


class AssetSerializer(serializers.ModelSerializer):
    """
    Asset Serializer
    """
    class Meta:
        model = UAsset
        fields = ('id', 'name', 'current_capital_amount', 'current_evaluated_amount', 'm_asset_category_sub')
