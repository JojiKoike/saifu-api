from rest_framework import serializers
from ..models.master.asset import MAssetCategoryMain, MAssetCategorySub
from ..models.user.asset import UAsset
from ..models.transaction.asset import TAssetEvaluate


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


class AssetEvaluateSerializer(serializers.ModelSerializer):
    """
    Asset Evaluate Serializer
    """
    u_asset = serializers.UUIDField(required=True)

    class Meta:
        model = TAssetEvaluate
        fields = ('id', 'evaluate_date', 'evaluated_amount', 'note', 'u_asset')

    def create(self, validated_data):
        """
        Create Asset Evaluate Record
        :param validated_data:
        :return: TAssetEvaluate
        """
        evaluated_amount = validated_data.pop('evaluated_amount')
        owner = validated_data.pop('owner')

        """
        Update Current Evaluated Amount
        """
        u_asset_query_set = UAsset.objects.filter(owner=owner)
        u_asset = u_asset_query_set.get(pk=validated_data.pop('u_asset'))
        u_asset.current_evaluated_amount = evaluated_amount
        u_asset.save()

        """
        Create Asset Evaluate Record
        """
        t_asset_evaluate = TAssetEvaluate.objects.create(
            evaluated_amount=evaluated_amount,
            u_asset=u_asset, owner=owner, **validated_data)

        return t_asset_evaluate
